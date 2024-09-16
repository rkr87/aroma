"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""

import json

import util
from base.class_singleton import ClassSingleton
from constants import APP_ROM_DB_PATH, ROM_PATH
from validator.rom_validator import RomValidator


class RomManager(ClassSingleton):
    """
    TODO
    """

    def __init__(self) -> None:
        super().__init__()
        self._validator = RomValidator()

    def update(
        self,
        reset: bool = False
    ) -> dict[str, str]:
        """
        TODO
        """
        db = {}
        if not reset:
            db = {
                k: v for k, v in util.load_simple_json(APP_ROM_DB_PATH).items()
                if (ROM_PATH / k).is_file()
            }
        for path in sorted(ROM_PATH.rglob("*")):
            if not self._validator.check_path(path):
                continue
            rel_path = path.relative_to(ROM_PATH)
            if (rom := "/".join(rel_path.parts)) not in db:
                db[rom] = self._validator.get_rom_name(rel_path)
        return db


rom_db = RomManager()
res = rom_db.update()
with open(APP_ROM_DB_PATH, "w", encoding="utf8") as f:
    json.dump(res, f, indent=4)
