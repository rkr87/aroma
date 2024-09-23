# pylint: disable=too-many-arguments
"""Module for handling string translations."""

from dataclasses import dataclass, field

from classes.base.json_dataclass import JsonDataClass


@dataclass
class Strings(JsonDataClass):  # pylint: disable=too-many-instance-attributes
    """Singleton class for managing various string translations."""

    stock: str = ""
    custom: str = ""
    collections: str = ""
    rom_naming: str = ""
    refresh_roms: str = ""
    refresh_roms_desc: list[str] = field(default_factory=list)
    naming_method: str = ""
    naming_method_desc: list[str] = field(default_factory=list)
    console_naming: str = ""
    console_naming_desc: list[str] = field(default_factory=list)
    arcade_naming: str = ""
    arcade_naming_desc: list[str] = field(default_factory=list)
    naming_title_desc: str = ""
    naming_name_desc: str = ""
    naming_region_desc: str = ""
    naming_disc_desc: str = ""
    naming_format_desc: str = ""
    naming_hack_desc: str = ""
    naming_version_desc: str = ""
    naming_year_desc: str = ""
    naming_additional_desc: str = ""
    name_format: str = ""
    name_format_desc: list[str] = field(default_factory=list)
    options: str = ""
    logging_level: str = ""
    logging_desc: list[str] = field(default_factory=list)
    logging_debug: str = ""
    logging_info: str = ""
    logging_warning: str = ""
    logging_error: str = ""
    language: str = ""
    language_desc: list[str] = field(default_factory=list)
