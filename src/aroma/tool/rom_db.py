"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""
import json
from pathlib import Path

import util
from app_config import AppConfig
from base.class_singleton import ClassSingleton
from constants import (APP_ROM_DB_PATH, ARCADE_ID_METHOD, ARCADE_NAMES_DB,
                       ARCADE_NAMING_SYSTEMS, CONSOLE_NAMES_DB,
                       NAMING_EXCLUDE_SYSTEMS, ROM_PATH)
from encoder.dataclass_encoder import DataclassEncoder
from model.rom_detail import RomDetail
from strings import Strings
from tool.filename_parser import FilenameParser
from tool.name_db import NameDB
from tool.rom_validator import RomValidator


class RomDB(ClassSingleton):
    """
    TODO
    """

    def __init__(self) -> None:
        super().__init__()
        self._validator = RomValidator()
        self._db: dict[str, RomDetail] = {}
        self._parser = FilenameParser()

    @property
    def data(self) -> dict[str, RomDetail]:
        """TODO"""
        self._load_db()
        return self._db

    def update_db(
        self,
        reset: bool = False
    ) -> None:
        """
        TODO
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
        """TODO"""
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
        self._process_remaining_files(files)

    def _process_arcade_rom(
        self,
        path: Path,
        current: RomDetail | None,
        arcade_roms: dict[str, list[str]]
    ) -> None:
        """Process arcade ROMs"""
        key = "/".join(path.parts)
        if current and current.id_method == ARCADE_ID_METHOD:
            self._db[key] = current
        else:
            arcade_roms[key] = [path.stem]

    def _process_console_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]]
    ) -> None:
        """Process console ROMs"""
        if AppConfig().console_naming == Strings().stock:
            return
        key = "/".join(path.parts)
        if path.suffix in {".zip", ".7z"}:
            self._process_compressed_rom(path, current, console_roms, key)
        else:
            self._process_regular_rom(path, current, console_roms, key)

    def _process_compressed_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]],
        key: str
    ) -> None:
        """Process ROMs in compressed archives"""
        valid = [
            zf.crc for zf in util.get_archive_info(ROM_PATH / path)
            if self._validator.has_valid_ext(ROM_PATH / path / zf.filename)
        ]
        if current and len(valid) == 1 and current.id == valid[0]:
            self._db[key] = current
        else:
            console_roms[key] = valid

    def _process_regular_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]],
        key: str
    ) -> None:
        """Process regular non-compressed ROM files"""
        file_crc = util.check_crc(ROM_PATH / path)
        if current and file_crc == current.id:
            self._db[key] = current
        else:
            console_roms[key] = [file_crc]

    def _process_remaining_files(
        self,
        files: list[tuple[Path, RomDetail | None]]
    ) -> None:
        """Handle remaining files not present in name dbs"""
        fn: dict[str, RomDetail] = {
            key: current or self._parser.parse(path)
            for path, current in files
            if (key := "/".join(path.parts)) not in self._db
        }
        self._db.update(fn)

    def _load_db(self) -> None:
        """
        TODO
        """
        if not self._db:
            self._db = {
                k: RomDetail(**v)
                for k, v in util.load_simple_json(APP_ROM_DB_PATH).items()
                if self._validator.check_path(ROM_PATH / k)
            }

    def save_db(self) -> None:
        """TODO"""
        with open(APP_ROM_DB_PATH, "w", encoding="utf8") as file:
            json.dump(self._db, file, indent=4, cls=DataclassEncoder)

    @staticmethod
    def set_rebuild_required(reason: str) -> None:
        """TODO"""
        RomDB.get_static_logger().info(
            "Force full rebuild of RomDB: %s", reason
        )
        AppConfig().update_value("db_rebuild_req", reason)


if __name__ == "__main__":
    rm = RomDB()
    rm.update_db(True)
