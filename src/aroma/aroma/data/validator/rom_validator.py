"""Validates ROM files based on system and naming conventions."""
from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import (EMU_EXT_KEY, EMU_PATH, ROM_DB_IGNORE_EXT,
                       ROM_DB_IGNORE_WORDS, ROM_PATH)
from tools import util


class RomValidator(ClassSingleton):
    """Validates ROM files based on various criteria."""

    def __init__(self) -> None:
        super().__init__()
        self._system_exts: dict[str, list[str]] = {}

    @staticmethod
    def _get_valid_emu_ext(system: str) -> list[str]:
        """Returns valid emulator extensions for the given system."""
        emu_config = EMU_PATH / system / "config.json"
        data = util.load_simple_json(emu_config)
        if EMU_EXT_KEY not in data or not data[EMU_EXT_KEY]:
            return []
        return [ext.lower() for ext in data[EMU_EXT_KEY].split("|")]

    @staticmethod
    def _is_not_hidden(path: Path) -> bool:
        """Checks if the file path is not hidden."""
        return not any(part.startswith(".") for part in path.parts)

    @staticmethod
    def _is_not_ignored_ext(path: Path) -> bool:
        """Checks if the file extension is not ignored."""
        ext = path.suffix.lstrip(".").lower()
        return ext not in ROM_DB_IGNORE_EXT

    @staticmethod
    def _is_not_ignored_word(path: Path) -> bool:
        """Checks if the file name does not contain ignored words."""
        return not any(word in path.stem for word in ROM_DB_IGNORE_WORDS)

    @staticmethod
    def _has_valid_relative_path(path: Path) -> bool:
        """Checks if the path has a valid relative structure."""
        relative_path = path.relative_to(ROM_PATH)
        return len(relative_path.parts) > 1

    @staticmethod
    def _has_valid_system_directory(path: Path) -> bool:
        """Checks if the emu directory exists for the ROM."""
        relative_path = path.relative_to(ROM_PATH)
        system = relative_path.parts[0]
        return (EMU_PATH / system).is_dir()

    def has_valid_ext(self, path: Path) -> bool:
        """Validates the file extension against the allowed extensions."""
        relative_path = path.relative_to(ROM_PATH)
        if (system := relative_path.parts[0]) not in self._system_exts:
            self._system_exts[system] = self._get_valid_emu_ext(system)
        ext = path.suffix.lstrip(".").lower()
        return not (exts := self._system_exts[system]) or ext in exts

    def check_path(self, path: Path) -> bool:
        """Validates the entire path based on multiple criteria."""
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
