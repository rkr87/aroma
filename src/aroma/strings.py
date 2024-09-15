# pylint: disable=too-many-arguments
"""
Module for handling string translations.
"""
from dataclasses import dataclass

from base.json_dataclass import JsonDataClass


@dataclass
class Strings(JsonDataClass):  # pylint: disable=too-many-instance-attributes
    """
    Singleton class for managing various string translations.
    """
    stock: str = ""
    custom: str = ""
    collections: str = ""
    rom_naming: str = ""
    naming_method: str = ""
    naming_method_desc: str = ""
    console_naming: str = ""
    console_naming_desc: str = ""
    arcade_rom_naming: str = ""
    _arcade_rom_naming_stock: str = ""
    _arcade_rom_naming_custom: str = ""
    name_format: str = ""
    name_format_desc: str = ""
    name_format_none: str = ""
    name_format_name_only: str = ""
    name_format_name_region: str = ""
    name_format_name_region_disc: str = ""
    name_format_name_disc: str = ""
    no_cleaning: str = ""
    options: str = ""
    logging_level: str = ""
    logging_desc: str = ""
    logging_debug: str = ""
    logging_info: str = ""
    logging_warning: str = ""
    logging_error: str = ""
    language: str = ""
    language_desc: str = ""

    def arcade_rom_naming_stock(self, installed: str) -> str:
        """
        Format arcade ROM naming stock string with provided installation info.
        """
        self._logger.debug(
            "Formatting stock arcade ROM naming with: %s", installed
        )
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
        self._logger.debug((
            "Formatting custom arcade ROM naming with installed: %s, "
            "library_path: %s, library_name: %s, arcade_names_path: %s, "
            "arcade_names_file: %s"
        ),
            installed, library_path, library_name, arcade_names_path,
            arcade_names_file
        )
        return self._arcade_rom_naming_custom.format(
            installed=installed,
            library_path=library_path,
            library_name=library_name,
            arcade_names_path=arcade_names_path,
            arcade_names_file=arcade_names_file
        )
