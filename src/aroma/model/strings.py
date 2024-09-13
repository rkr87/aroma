# pylint: disable=too-many-arguments
"""
Module for handling string translations.
"""
import json
from dataclasses import dataclass

from base.class_singleton import ClassSingleton


@dataclass
class Strings(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """
    Singleton class for managing various string translations.
    """
    stock: str = ""
    custom: str = ""
    collections: str = ""
    rom_naming: str = ""
    arcade_rom_naming: str = ""
    _arcade_rom_naming_stock: str = ""
    _arcade_rom_naming_custom: str = ""
    options: str = ""

    @classmethod
    def from_file(cls, file_path: str) -> "Strings":
        """
        Load translations from a JSON file and set class attributes.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data: dict[str, str | list[str]] = json.load(f)
        new_dict: dict[str, str] = {
            k: '\n'.join(v) if isinstance(v, list) else v
            for k, v in data.items()
        }
        return cls(**new_dict)

    def arcade_rom_naming_stock(self, installed: str) -> str:
        """
        Format arcade ROM naming stock string with provided installation info.
        """
        return self._arcade_rom_naming_stock.format(installed=installed)

    def arcade_rom_naming_custom(
        self,
        installed: str,
        library_path: str,
        library_name: str,
        arcade_names_path: str,
        arcade_names_file: str
    ) -> str:
        """
        Format arcade ROM naming custom string with provided details.
        """
        return self._arcade_rom_naming_custom.format(
            installed=installed,
            library_path=library_path,
            library_name=library_name,
            arcade_names_path=arcade_names_path,
            arcade_names_file=arcade_names_file
        )
