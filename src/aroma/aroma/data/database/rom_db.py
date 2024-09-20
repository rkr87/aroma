"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""
import json
from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import (APP_ROM_DB_PATH, ARCADE_ID_METHOD, ARCADE_NAMES_DB,
                       ARCADE_NAMING_SYSTEMS, CONSOLE_NAMES_DB,
                       NAMING_EXCLUDE_SYSTEMS, ROM_PATH)
from data.database.name_db import NameDB
from data.encoder.dataclass_encoder import DataclassEncoder
from data.parser.filename_parser import FilenameParser
from data.validator.rom_validator import RomValidator
from model.app_config import AppConfig
from model.rom_detail import RomDetail
from model.strings import Strings
from tools import util


class RomDB(ClassSingleton):
    """
    A singleton class to manage ROM details and naming preferences.
    It handles loading, updating, and saving ROM data, as well as processing
    arcade and console ROMs based on naming conventions.
    """

    def __init__(self) -> None:
        super().__init__()
        self._validator = RomValidator()
        self._db: dict[str, RomDetail] = {}
        self._parser = FilenameParser()

    @property
    def data(self) -> dict[str, RomDetail]:
        """Load and return the current ROM database."""
        self._load_db()
        return self._db

    def update_db(self, reset: bool = False) -> None:
        """
        Update the ROM database by scanning ROM_PATH for valid ROM files.
        If reset is True or a rebuild is required, the database is cleared.
        """
        if reset or AppConfig().db_rebuild_req:
            self._db = {}
        else:
            self._load_db()
        valid_files: list[tuple[Path, RomDetail | None]] = []
        for path in sorted(ROM_PATH.rglob("*")):
            if not self._validator.check_path(path):
                continue
            rel_path = path.relative_to(ROM_PATH)
            current = self._db.get("/".join(rel_path.parts))
            valid_files.append((rel_path, current))
        self._process_files(valid_files)
        self.save_db()
        AppConfig().update_value("db_rebuild_req", "")

    def _process_files(
        self,
        files: list[tuple[Path, RomDetail | None]]
    ) -> None:
        """Process the provided list of files and update the ROM database."""
        self._db = {}
        arcade_roms: dict[str, list[str]] = {}
        console_roms: dict[str, list[str]] = {}
        for path, current in files:
            system = path.parts[0]
            if system in NAMING_EXCLUDE_SYSTEMS:
                continue
            if system in ARCADE_NAMING_SYSTEMS:
                self._process_arcade_rom(path, current, arcade_roms)
            else:
                self._process_console_rom(path, current, console_roms)
        self._db.update(NameDB.query_vals(CONSOLE_NAMES_DB, console_roms))
        self._db.update(NameDB.query_vals(ARCADE_NAMES_DB, arcade_roms))
        self._process_remaining_files(files, {**arcade_roms, **console_roms})

    def _process_arcade_rom(
        self,
        path: Path,
        current: RomDetail | None,
        arcade_roms: dict[str, list[str]]
    ) -> None:
        """Process an arcade ROM file and update the database accordingly."""
        key = "/".join(path.parts)
        if current and current.id_method == ARCADE_ID_METHOD:
            self._db[key] = current
            return
        arcade_roms[key] = [path.stem]

    def _process_console_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]]
    ) -> None:
        """
        Process a console ROM file based on its type (compressed or regular).
        """
        if AppConfig().console_naming == Strings().stock:
            return
        key = "/".join(path.parts)
        if path.suffix in {".zip", ".7z"}:
            self._process_compressed_rom(path, current, console_roms, key)
            return
        self._process_regular_rom(path, current, console_roms, key)

    def _process_compressed_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]],
        key: str
    ) -> None:
        """Process ROMs that are contained in compressed archives."""
        file_crc = util.check_crc(ROM_PATH / path)
        if current and file_crc == current.id:
            self._db[key] = current
            return
        valid = [
            zf.crc for zf in util.get_archive_info(ROM_PATH / path)
            if self._validator.has_valid_ext(ROM_PATH / path / zf.filename)
        ]
        if current and len(valid) == 1 and current.id == valid[0]:
            self._db[key] = current
            return
        console_roms[key] = valid

    def _process_regular_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]],
        key: str
    ) -> None:
        """Process regular non-compressed ROM files and update the database."""
        file_crc = util.check_crc(ROM_PATH / path)
        if current and file_crc == current.id:
            self._db[key] = current
            return
        console_roms[key] = [file_crc]

    def _process_remaining_files(
        self,
        files: list[tuple[Path, RomDetail | None]],
        all_roms: dict[str, list[str]]
    ) -> None:
        """Handle remaining files not present in the name databases."""
        for path, current in files:
            if (key := "/".join(path.parts)) in self._db:
                continue
            if current and path.parts[0] in NAMING_EXCLUDE_SYSTEMS:
                self._db[key] = current
                continue
            if (ids := all_roms.get(key)) and current and current.id in ids:
                self._db[key] = current
                continue
            self._db[key] = self._parser.parse(path, ids[0] if ids else None)

    def _load_db(self) -> None:
        """
        Load the ROM database from a JSON file and validate the paths.
        Only valid entries will be included in the database.
        """
        if not self._db:
            self._db = {
                k: RomDetail(**v)
                for k, v in util.load_simple_json(APP_ROM_DB_PATH).items()
                if self._validator.check_path(ROM_PATH / k)
            }

    def save_db(self) -> None:
        """Save the current ROM database to a JSON file."""
        with open(APP_ROM_DB_PATH, "w", encoding="utf8") as file:
            json.dump(self._db, file, indent=4, cls=DataclassEncoder)
