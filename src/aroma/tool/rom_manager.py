"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""

from __future__ import annotations

import json

import util
from base.class_singleton import ClassSingleton
from constants import APP_ROM_DB_PATH, ROM_PATH
from encoder.dataclass_encoder import DataclassEncoder
from model.rom_detail import RomDetail
from tool.rom_namer import RomNamer
from tool.rom_validator import RomValidator


class RomManager(ClassSingleton):
    """
    TODO
    """

    def __init__(self) -> None:
        super().__init__()
        self._validator = RomValidator()
        self._namer = RomNamer()
        self._db: dict[str, RomDetail] = self._load_db()

    @property
    def data(self) -> dict[str, RomDetail]:
        """TODO"""
        return self._db

    def update_db(
        self,
        reset: bool = False
    ) -> None:
        """
        TODO
        """
        if reset:
            self._db = {}
        for path in sorted(ROM_PATH.rglob("*")):
            rel_path = path.relative_to(ROM_PATH)
            if current := self._db.get(key := "/".join(rel_path.parts)):
                self._db[key] = self._namer.get_rom_details(rel_path, current)
                continue
            if not self._validator.check_path(path):
                continue
            self._db[key] = self._namer.get_rom_details(rel_path)
        self.save_db()

    def _load_db(self) -> dict[str, RomDetail]:
        """
        TODO
        """
        return {
            k: RomDetail(**v)
            for k, v in util.load_simple_json(APP_ROM_DB_PATH).items()
            if self._validator.check_path(ROM_PATH / k)
        }

    def save_db(self) -> None:
        """TODO"""
        with open(APP_ROM_DB_PATH, "w", encoding="utf8") as file:
            json.dump(self._db, file, indent=4, cls=DataclassEncoder)


rom_db = RomManager()
rom_db.update_db()
