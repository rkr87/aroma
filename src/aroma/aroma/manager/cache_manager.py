"""CacheManager module for managing ROM caching operations."""

from collections.abc import Mapping
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from apsw import Connection, Cursor
from data.model.launchable_detail import LaunchableDetail, LaunchableType
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    APP_NAME,
    ARCADE_NAMING_SYSTEMS,
    EMU_PATH,
    ROM_PATH,
    TSP_CACHE_DB_SUFFIX,
)

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


class CacheManager(ClassSingleton):
    """Manage caching operations for ROM data."""

    @dataclass
    class _RowEntry:  # pylint: disable=too-many-instance-attributes
        """Represents a single entry for ROM or directory details."""

        raw_path: Path
        _name: str
        _is_dir: bool = False
        _launchable_item: LaunchableDetail | None = None
        is_valid_dir: bool = False
        _ignore_ancestors: int | None = None

        def __post_init__(self) -> None:
            with suppress(ValueError):
                self._ignore_ancestors = self.raw_path.parts.index("Roms") + 1
                if self.raw_path.is_relative_to(ROM_PATH):
                    self._ignore_ancestors += 1
            if (
                self._is_dir
                and self._ignore_ancestors
                and self.raw_path.parts[self._ignore_ancestors :]
            ):
                self.is_valid_dir = True

        def _is_arcade_rom(self) -> bool:
            """TODO."""
            return (
                self._launchable_item is not None
                and self._launchable_item.item_type == LaunchableType.ROM
                and self._launchable_item.parent in ARCADE_NAMING_SYSTEMS
            )

        @property
        def display_name(self) -> str:
            """Return the display name of the ROM or directory."""
            if self._is_dir:
                return self._get_dir_string()
            if self._is_arcade_rom():
                return f"{self._name} "
            return self._name

        def _get_dir_string(self, *, exclude_self: bool = False) -> str:
            """TODO."""
            if not self._ignore_ancestors:
                return "."
            if exclude_self:
                return (
                    ">".join(self.raw_path.parts[self._ignore_ancestors : -1])
                    or "."
                )
            return (
                ">".join(self.raw_path.parts[self._ignore_ancestors :]) or "."
            )

        @property
        def rom_path(self) -> str:
            """Return the ROM file path."""
            if (
                self._launchable_item is None
                or self._launchable_item.item_type == LaunchableType.SHORTCUT
            ):
                return str(self.raw_path)
            return str(
                EMU_PATH
                / self._launchable_item.parent
                / ".."
                / ".."
                / "Roms"
                / self._launchable_item.item_path
            )

        @property
        def img_path(self) -> str:
            """Return the image path for the ROM or directory."""
            if self._is_dir or not self._launchable_item:
                return str(self.raw_path / "_root.png")
            return str(self._launchable_item.get_image_path())

        @property
        def type(self) -> int:
            """Return the type, 1 for directory, 0 for ROM."""
            return 1 if self._is_dir else 0

        @property
        def parent_path(self) -> str:
            """Return the parent directory path."""
            return self._get_dir_string(exclude_self=True)

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
            if self._is_arcade_rom():
                return f"{APP_NAME}_{self.raw_path.stem}"
            return self.display_name

    @staticmethod
    def _replace_table(cursor: Cursor, parent: str) -> None:
        """Drop and recreate the cache table for a system."""
        table_name = f"{parent}_roms"
        statement = RESET_TABLE % (table_name, table_name)
        cursor.execute(statement)

    @staticmethod
    def _generate_rows(
        launchables: Mapping[str, LaunchableDetail],
    ) -> dict[str, list["CacheManager._RowEntry"]]:
        """Generate row entries for ROMs and directories."""
        parent_dict: dict[str, list[CacheManager._RowEntry]] = {}
        for launchable in launchables.values():
            CacheManager._add_launchable_entry(parent_dict, launchable)
        for parent, rows in parent_dict.items():
            CacheManager._add_directory_entries(parent_dict, parent, rows)
        return parent_dict

    @staticmethod
    def _add_launchable_entry(
        parent_dict: dict[str, list["CacheManager._RowEntry"]],
        launchable: LaunchableDetail,
    ) -> None:
        """Add a ROM entry to the system dictionary."""
        row_entry = CacheManager._RowEntry(
            launchable.full_path,
            launchable.format_name(),
            _launchable_item=launchable,
        )
        parent_dict.setdefault(launchable.parent, []).append(row_entry)

    @staticmethod
    def _add_directory_entries(
        parent_dict: dict[str, list["CacheManager._RowEntry"]],
        parent: str,
        rows: list["CacheManager._RowEntry"],
    ) -> None:
        """Add directory entries to the system dictionary."""
        dirs = {ancestor for r in rows for ancestor in r.raw_path.parents}
        for i in sorted(dirs):
            dir_entry = CacheManager._RowEntry(i, i.name, _is_dir=True)
            if dir_entry.is_valid_dir:
                parent_dict.setdefault(parent, []).append(dir_entry)

    @staticmethod
    def update_cache_db(
        launchables: Mapping[str, LaunchableDetail], base_path: Path
    ) -> None:
        """Update the cache database with ROM and directory entries."""
        for parent, rows in CacheManager._generate_rows(launchables).items():
            base_parent = Path(parent).name
            cache_db = (
                base_path / parent / f"{base_parent}{TSP_CACHE_DB_SUFFIX}"
            )
            with Connection(str(cache_db)) as conn:
                cursor = conn.cursor()
                CacheManager._replace_table(cursor, base_parent)
                data_to_insert = [entry.to_db_tuple() for entry in rows]
                statement = INSERT_STATEMENT % base_parent
                cursor.executemany(statement, data_to_insert)
