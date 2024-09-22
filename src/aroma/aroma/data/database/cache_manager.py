"""CacheManager module for managing ROM caching operations."""

from dataclasses import dataclass
from pathlib import Path

from apsw import Connection, Cursor
from classes.base.class_singleton import ClassSingleton
from constants import (
    APP_NAME,
    ARCADE_NAMING_SYSTEMS,
    EMU_PATH,
    ROM_PATH,
    TSP_CACHE_DB_SUFFIX,
)
from model.rom_detail import RomDetail

RESET_TABLE = """
    DROP TABLE IF EXISTS %s;
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disp TEXT NOT NULL,
        path TEXT NOT NULL,
        imgpath TEXT NOT NULL,
        type INTEGER DEFAULT 0,
        ppath TEXT NOT NULL,
        pinyin TEXT NOT NULL,
        cpinyin TEXT NOT NULL,
        opinyin TEXT NOT NULL
    )
"""

INSERT_STATEMENT = """
    INSERT INTO %s_roms
        (disp, path, imgpath, type, ppath, pinyin, cpinyin, opinyin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

IGNORE_ANCESTORS: int = 2


class CacheManager(ClassSingleton):
    """Manage caching operations for ROM data."""

    @dataclass
    class _RowEntry:
        """Represents a single entry for ROM or directory details."""

        raw_path: Path
        _name: str
        _is_dir: bool = False

        @property
        def display_name(self) -> str:
            """Return the display name of the ROM or directory."""
            if self._is_dir:
                return ">".join(self.raw_path.parts[1:])
            if self._system in ARCADE_NAMING_SYSTEMS:
                return f"{self._name} "
            return self._name

        @property
        def rom_path(self) -> str:
            """Return the ROM file path."""
            return f"{self._emu_path}/Roms/{'/'.join(self.raw_path.parts)}"

        @property
        def img_path(self) -> str:
            """Return the image path for the ROM or directory."""
            if not self._is_dir:
                filename = self.raw_path.with_suffix(".png").name
                return f"{self._emu_path}/Imgs/{self._system}/{filename}"
            filename = f"{'/'.join(self.raw_path.parts)}/_root.png"
            return f"{self._emu_path}/Roms/{filename}"

        @property
        def type(self) -> int:
            """Return the type, 1 for directory, 0 for ROM."""
            return 1 if self._is_dir else 0

        @property
        def parent_path(self) -> str:
            """Return the parent directory path."""
            if len(self.raw_path.parts) == IGNORE_ANCESTORS:
                return "."
            return ">".join(self.raw_path.parts[1:-1])

        @property
        def _emu_path(self) -> str:
            """Return the emulation base path."""
            return f"{EMU_PATH}/{self._system}/../.."

        @property
        def _system(self) -> str:
            """Return the system name derived from the path."""
            return self.raw_path.parts[0]

        def _get_dir_path(self, name: str) -> str:
            """Return the formatted directory path for a given name."""
            parts = self.raw_path.parts[1:]
            return f"{'_'*(parts.count(name)-1)}{name}"

        def to_db_tuple(self) -> tuple[str, str, str, int, str, str, str, str]:
            """Generate a tuple for database insertion."""
            return (
                self.display_name,
                self.rom_path,
                self.img_path,
                self.type,
                self.parent_path,
                "" if self._is_dir else self.display_name,
                "" if self._is_dir else self.display_name,
                "" if self._is_dir else self.opinyin,
            )

        @property
        def opinyin(self) -> str:
            """Return the pinyin value for the ROM or directory."""
            if self._system in ARCADE_NAMING_SYSTEMS:
                return f"{APP_NAME}_{self.raw_path.stem}"
            return self.display_name

    @staticmethod
    def _replace_table(cursor: Cursor, system: str) -> None:
        """Drop and recreate the cache table for a system."""
        table_name = f"{system}_roms"
        statement = RESET_TABLE % (table_name, table_name)
        cursor.execute(statement)

    @staticmethod
    def _generate_rows(
        roms: dict[str, RomDetail],
    ) -> dict[str, list["CacheManager._RowEntry"]]:
        """Generate row entries for ROMs and directories."""
        system_dict: dict[str, list[CacheManager._RowEntry]] = {}
        for path_str, rom in roms.items():
            CacheManager._add_rom_entry(system_dict, path_str, rom)
        for system, rows in system_dict.items():
            CacheManager._add_directory_entries(system_dict, system, rows)
        return system_dict

    @staticmethod
    def _add_rom_entry(
        system_dict: dict[str, list["CacheManager._RowEntry"]],
        path_str: str,
        rom: RomDetail,
    ) -> None:
        """Add a ROM entry to the system dictionary."""
        path = Path(path_str)
        system = path.parts[0]
        rom_entry = CacheManager._RowEntry(path, rom.format_name)
        system_dict.setdefault(system, []).append(rom_entry)

    @staticmethod
    def _add_directory_entries(
        system_dict: dict[str, list["CacheManager._RowEntry"]],
        system: str,
        rows: list["CacheManager._RowEntry"],
    ) -> None:
        """Add directory entries to the system dictionary."""
        dirs = {
            ancestor
            for r in rows
            for ancestor in r.raw_path.parents
            if len(ancestor.parts) > 1
        }
        for i in sorted(dirs):
            dir_entry = CacheManager._RowEntry(i, i.name, _is_dir=True)
            system_dict.setdefault(system, []).append(dir_entry)

    @staticmethod
    def update_cache_db(roms: dict[str, RomDetail]) -> None:
        """Update the cache database with ROM and directory entries."""
        systems = CacheManager._generate_rows(roms)
        for system, rows in systems.items():
            cache_db = ROM_PATH / system / f"{system}{TSP_CACHE_DB_SUFFIX}"
            with Connection(str(cache_db)) as conn:
                cursor = conn.cursor()
                CacheManager._replace_table(cursor, system)
                data_to_insert = [entry.to_db_tuple() for entry in rows]
                statement = INSERT_STATEMENT % (system)
                cursor.executemany(statement, data_to_insert)
