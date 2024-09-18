"""TODO"""

import pickle
from pathlib import Path
from typing import cast

import util
from base.class_singleton import ClassSingleton
from constants import (ARCADE_ID_METHOD, ARCADE_NAMING_SYSTEMS,
                       NAMES_APP_RESOURCE, NAMING_EXCLUDE_SYSTEMS, ROM_PATH)
from model.rom_detail import RomDetail
from tool.filename_parser import FilenameParser
from tool.rom_validator import RomValidator


class RomNamer(ClassSingleton):
    """TODO"""

    def __init__(self) -> None:
        super().__init__()
        self._validator: RomValidator = RomValidator()
        self._arcade_names: dict[str, RomDetail] | None = None
        self._console_names: dict[str, RomDetail] | None = None
        self._parser: FilenameParser = FilenameParser()

    @staticmethod
    def _get_names(file_name: str) -> dict[str, RomDetail]:
        """TODO"""
        if get_zip := util.bytes_from_zip(NAMES_APP_RESOURCE, file_name):
            return cast(
                dict[str, RomDetail],
                pickle.loads(get_zip)
            )
        return {}

    def _get_arcade_names(self) -> dict[str, RomDetail]:
        """TODO"""
        if self._arcade_names is None:
            self._arcade_names = self._get_names("arcade")
        return self._arcade_names

    def _get_console_names(self) -> dict[str, RomDetail]:
        """TODO"""
        if self._console_names is None:
            self._console_names = self._get_names("console")
        return self._console_names

    def _check_arcade_roms(
        self,
        path: Path,
        current: RomDetail | None
    ) -> RomDetail | None:
        """TODO"""
        if path.parts[0] not in ARCADE_NAMING_SYSTEMS:
            return None
        if current and current.id_method == ARCADE_ID_METHOD:
            return current
        return self._get_arcade_names().get(path.stem)

    def _check_archived_roms(
        self,
        path: Path,
        current: RomDetail | None
    ) -> RomDetail | None:
        """TODO"""
        valid: list[str] = [
            zf.crc for zf in util.get_archive_info(ROM_PATH / path)
            if self._validator.has_valid_ext(ROM_PATH / path / zf.filename)
        ]
        if current and len(valid) == 1 and current.id == valid[0]:
            return current
        results: list[RomDetail] = [
            y for item in valid
            if (y := self._get_console_names().get(item))
        ]
        if len(results) != 1:
            return None
        return results[0]

    def _check_console_roms(
        self,
        path: Path,
        current: RomDetail | None
    ) -> RomDetail | None:
        """TODO"""
        if path.parts[0] in NAMING_EXCLUDE_SYSTEMS + ARCADE_NAMING_SYSTEMS:
            return None
        if archived := self._check_archived_roms(path, current):
            return archived
        file_crc = util.check_crc(ROM_PATH / path)
        if current and file_crc == current.id:
            detail: RomDetail | None = current
        else:
            detail = self._get_console_names().get(file_crc)
        return detail

    def get_rom_details(
        self,
        path: Path,
        current: RomDetail | None = None
    ) -> RomDetail:
        """TODO"""
        if (arcade := self._check_arcade_roms(path, current)):
            return arcade
        if (console := self._check_console_roms(path, current)):
            return console
        if current:
            return current
        return self._parser.parse(path)
