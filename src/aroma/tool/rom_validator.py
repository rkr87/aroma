"""TODO"""


from pathlib import Path

import util
from base.class_singleton import ClassSingleton
from constants import (EMU_EXT_KEY, EMU_PATH, ROM_DB_IGNORE_EXT,
                       ROM_DB_IGNORE_WORDS, ROM_PATH)


class RomValidator(ClassSingleton):
    """TODO"""

    def __init__(self) -> None:
        super().__init__()
        self._system_exts: dict[str, list[str]] = {}

    @staticmethod
    def _get_valid_emu_ext(system: str) -> list[str]:
        """TODO"""
        emu_config = EMU_PATH / system / "config.json"
        data = util.load_simple_json(emu_config)
        if EMU_EXT_KEY not in data or not data[EMU_EXT_KEY]:
            return []
        return [ext.lower() for ext in data[EMU_EXT_KEY].split("|")]

    @staticmethod
    def _is_not_hidden(path: Path) -> bool:
        """TODO"""
        return not any(part.startswith(".") for part in path.parts)

    @staticmethod
    def _is_not_ignored_ext(path: Path) -> bool:
        """TODO"""
        ext = path.suffix.lstrip(".").lower()
        return ext not in ROM_DB_IGNORE_EXT

    @staticmethod
    def _is_not_ignored_word(path: Path) -> bool:
        """TODO"""
        return not any(word in path.stem for word in ROM_DB_IGNORE_WORDS)

    @staticmethod
    def _has_valid_relative_path(path: Path) -> bool:
        """TODO"""
        relative_path = path.relative_to(ROM_PATH)
        return len(relative_path.parts) > 1

    @staticmethod
    def _has_valid_system_directory(path: Path) -> bool:
        """TODO"""
        relative_path = path.relative_to(ROM_PATH)
        system = relative_path.parts[0]
        return (EMU_PATH / system).is_dir()

    def has_valid_ext(self, path: Path) -> bool:
        """TODO"""
        relative_path = path.relative_to(ROM_PATH)
        if (system := relative_path.parts[0]) not in self._system_exts:
            self._system_exts[system] = self._get_valid_emu_ext(system)
        ext = path.suffix.lstrip(".").lower()
        return not (exts := self._system_exts[system]) or ext in exts

    def check_path(self, path: Path) -> bool:
        """TODO"""
        if not path.is_file():
            return False
        checks = [
            self._is_not_hidden,
            self._is_not_ignored_ext,
            self._is_not_ignored_word,
            self._has_valid_relative_path,
            self._has_valid_system_directory,
            self.has_valid_ext,
        ]
        return all(check(path) for check in checks)
