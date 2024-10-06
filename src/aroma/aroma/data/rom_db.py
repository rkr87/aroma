"""Defines the ROM naming preferences menu."""

import ast
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import (
    APP_ROM_DB_PATH,
    ARCADE_ID_METHOD,
    ARCADE_NAMES_DB,
    ARCADE_NAMING_SYSTEMS,
    CONSOLE_ID_METHOD,
    CONSOLE_NAMES_DB,
    FILE_ID_METHOD,
    NAMING_EXCLUDE_SYSTEMS,
    ROM_PATH,
    RUNNING_ON_TSP,
    STOCK_STR,
)
from data.name_db import NameDB
from data.parser.filename_parser import FilenameParser
from data.validator.rom_validator import RomValidator
from model.rom_detail import RomDetail
from tools import util
from tools.app_config import AppConfig
from tools.enhanced_json_encoder import EnhancedJSONEncoder


class RomDB(ClassSingleton):
    """A singleton class to manage ROM details and naming preferences."""

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

    @property
    def valid_paths(self) -> list[Path]:
        """Load and return valid ROM paths."""
        self._load_db()
        return [Path(p) for p in self._db]

    def update(self, *, reset: bool = False) -> None:
        """Refresh ROMs in app database."""
        self._update_db(reset=reset)
        if not RUNNING_ON_TSP:
            self._get_unmatched()

    def _update_db(self, *, reset: bool) -> None:
        """Update the ROM database by scanning ROM_PATH for valid ROM files."""
        if reset or AppConfig().db_rebuild_req:
            self._db = {}
            self._logger.info(
                "Database reset requested, clearing current database."
            )
            AppConfig().db_rebuild_req = False
            AppConfig().save()
        else:
            self._load_db()
        valid_files: list[tuple[Path, RomDetail | None]] = []
        for path in ROM_PATH.rglob("*"):
            if not self._validator.check_path(path):
                continue
            rel_path = path.relative_to(ROM_PATH)
            current = self._db.get("/".join(rel_path.parts))
            valid_files.append((rel_path, current))
        self._logger.debug("Processing %d valid files.", len(valid_files))
        self._process_files_in_batches(valid_files)
        self.save_db()

    def _get_unmatched(self) -> None:
        """Output unmatched crcs to file."""
        unmatched: dict[str, RomDetail] = {
            ast.literal_eval(v.id)[0]: v
            for _, v in self._db.items()
            if v.id_method == FILE_ID_METHOD
        }
        for k, v in unmatched.items():
            v.id_method = "crc"
            v.source = "aroma_overrides"
            v.hack = "SET MANUALLY"
            v.id = k
        path = APP_ROM_DB_PATH.parent / "unmatched_items.json"
        with path.open("w", encoding="utf8") as file:
            json.dump(unmatched, file, indent=4, cls=EnhancedJSONEncoder)

    def _process_files_in_batches(
        self,
        files: list[tuple[Path, RomDetail | None]],
        batch_size: int = 500,
    ) -> None:
        """Process files in batches to reduce memory pressure."""
        self._db = {}
        arcade_roms: dict[str, list[str]] = {}
        console_roms: dict[str, list[str]] = {}
        self._logger.debug(
            "Starting to process files in batches of %d.", batch_size
        )
        with ThreadPoolExecutor() as executor:
            future_to_batch = {
                executor.submit(
                    self._collect_rom_data,
                    files[i : i + batch_size],
                    arcade_roms,
                    console_roms,
                ): i
                for i in range(0, len(files), batch_size)
            }
            for future in as_completed(future_to_batch):
                future.result()
        self._logger.info("Fetched arcade and console ROM data.")
        if console_roms:
            self._db.update(NameDB.query(CONSOLE_NAMES_DB, console_roms))
        if arcade_roms:
            self._db.update(NameDB.query(ARCADE_NAMES_DB, arcade_roms))
        self._process_remaining_files(files, {**arcade_roms, **console_roms})

    def _collect_rom_data(
        self,
        files: list[tuple[Path, RomDetail | None]],
        arcade_roms: dict[str, list[str]],
        console_roms: dict[str, list[str]],
    ) -> None:
        """Collect ROM data for querying."""
        for path, current in files:
            system = path.parts[0]
            if system in NAMING_EXCLUDE_SYSTEMS:
                self._logger.debug(
                    "Excluding system %s from processing.", system
                )
                continue
            if system in ARCADE_NAMING_SYSTEMS:
                self._process_arcade_rom(path, current, arcade_roms)
            else:
                self._process_console_rom(path, current, console_roms)

    def _process_arcade_rom(
        self,
        path: Path,
        current: RomDetail | None,
        arcade_roms: dict[str, list[str]],
    ) -> None:
        """Process an arcade ROM file and update the database accordingly."""
        key = "/".join(path.parts)
        if current and current.id_method == ARCADE_ID_METHOD:
            self._db[key] = current
            self._logger.debug(
                "Arcade ROM %s already exists in database.", key
            )
            return
        arcade_roms[key] = [path.stem]
        self._logger.debug("Added arcade ROM %s for processing.", key)

    def _process_console_rom(
        self,
        path: Path,
        current: RomDetail | None,
        console_roms: dict[str, list[str]],
    ) -> None:
        """Process a console ROM file based on its type."""
        if AppConfig().console_naming == STOCK_STR:
            self._logger.debug(
                "Console naming is set to stock; skipping %s.", path
            )
            return
        key = "/".join(path.parts)
        if current and current.id_method == CONSOLE_ID_METHOD:
            self._db[key] = current
            self._logger.debug(
                "Console ROM %s already exists in database.", key
            )
            return
        with ThreadPoolExecutor() as executor:
            func = (
                self._process_compressed_rom
                if path.suffix in {".zip", ".7z"}
                else self._process_regular_rom
            )
            future = executor.submit(func, path)
            if result := future.result():
                if (
                    current
                    and current.id_method == FILE_ID_METHOD
                    and current.id == str(result)
                ):
                    self._db[key] = current
                    self._logger.debug(
                        "Processed console ROM %s with result %s.", key, result
                    )
                    return
                console_roms[key] = result
                self._logger.debug(
                    "Processed console ROM %s with result %s.", key, result
                )

    def _process_compressed_rom(self, path: Path) -> list[str]:
        """Process ROMs that are contained in compressed archives."""
        archive_info = util.get_archive_info(ROM_PATH / path)
        valid_crcs = [
            zf.crc
            for zf in archive_info
            if self._validator.has_valid_ext(ROM_PATH / path / zf.filename)
        ]
        self._logger.debug(
            "Found %d valid CRCs in compressed ROM %s.", len(valid_crcs), path
        )
        return valid_crcs

    @staticmethod
    def _process_regular_rom(path: Path) -> list[str]:
        """Process regular non-compressed ROM files and update the database."""
        file_crc = util.check_crc(ROM_PATH / path)
        RomDB.get_static_logger().debug(
            "Computed CRC for regular ROM %s: %s", path, file_crc
        )
        return [file_crc]

    def _process_remaining_files(
        self,
        files: list[tuple[Path, RomDetail | None]],
        all_roms: dict[str, list[str]],
    ) -> None:
        """Handle remaining files not present in the name databases."""
        for path, current in files:
            if (key := "/".join(path.parts)) in self._db:
                self._logger.debug("ROM %s already processed; skipping.", key)
                continue
            if current and path.parts[0] in NAMING_EXCLUDE_SYSTEMS:
                self._db[key] = current
                self._logger.debug(
                    "Added excluded system ROM %s directly to database.", key
                )
                continue
            if (
                (ids := all_roms.get(key))
                and current
                and current.id == str(ids)
            ):
                self._db[key] = current
                self._logger.debug(
                    "Added unchanged ROM %s directly to database.", key
                )
                continue
            self._db[key] = self._parser.parse(path, ids)
            self._logger.debug("Parsed ROM %s and added to database.", key)

    def _load_db(self) -> None:
        """Load the ROM database from a JSON file and validate the paths."""
        if not self._db:
            RomDB.get_static_logger().info(
                "Loading ROM database from %s.", APP_ROM_DB_PATH
            )
            self._db = {
                k: RomDetail(**v)
                for k, v in util.load_simple_json(APP_ROM_DB_PATH).items()
                if self._validator.check_path(ROM_PATH / k)
            }
            RomDB.get_static_logger().info(
                "Loaded %d ROM details.", len(self._db)
            )

    def save_db(self) -> None:
        """Save the current ROM database to a JSON file."""
        RomDB.get_static_logger().info(
            "Saving ROM database to %s.", APP_ROM_DB_PATH
        )
        with APP_ROM_DB_PATH.open("w", encoding="utf8") as file:
            json.dump(self._db, file, indent=4, cls=EnhancedJSONEncoder)
