"""Validates ROM files based on system and naming conventions."""

from pathlib import Path

from data.source.emu_config_handler import EmuConfigHandler
from manager.emu_manager import EmuManager
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    ROM_DB_IGNORE_EXT,
    ROM_DB_IGNORE_WORDS,
    ROM_PATH,
)


class RomValidator(ClassSingleton):
    """Validates ROM files based on various criteria."""

    @staticmethod
    def _is_not_hidden(path: Path) -> bool:
        """Check if the file path is not hidden."""
        return not any(part.startswith(".") for part in path.parts)

    @staticmethod
    def _is_not_ignored_ext(path: Path) -> bool:
        """Check if the file extension is not ignored."""
        ext = path.suffix.lstrip(".").lower()
        return ext not in ROM_DB_IGNORE_EXT

    @staticmethod
    def _is_not_ignored_word(path: Path) -> bool:
        """Check if the file name does not contain ignored words."""
        return not any(word in path.stem for word in ROM_DB_IGNORE_WORDS)

    @staticmethod
    def _has_valid_relative_path(path: Path) -> bool:
        """Check if the path has a valid relative structure."""
        relative_path = path.relative_to(ROM_PATH)
        return len(relative_path.parts) > 1

    @staticmethod
    def _has_valid_system_directory(path: Path) -> bool:
        """Check if the emu directory exists for the ROM."""
        system = path.relative_to(ROM_PATH).parts[0]
        return EmuConfigHandler.is_valid_system(system)

    @staticmethod
    def has_valid_ext(path: Path) -> bool:
        """Validate the file extension against the allowed extensions."""
        ext = path.suffix.lstrip(".").lower()
        system = path.relative_to(ROM_PATH).parts[0]
        return (
            not (exts := EmuManager().get_system_config(system).valid_ext)
            or ext in exts
        )

    @staticmethod
    def check_path(path: Path) -> bool:
        """Validate the entire path based on multiple criteria."""
        if not path.is_file():
            return False
        checks = [
            RomValidator._is_not_hidden,
            RomValidator._is_not_ignored_ext,
            RomValidator._is_not_ignored_word,
            RomValidator._has_valid_relative_path,
            RomValidator._has_valid_system_directory,
            RomValidator.has_valid_ext,
        ]
        return all(check(path) for check in checks)
