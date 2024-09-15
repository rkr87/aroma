# pylint: disable=too-many-arguments
"""
Module for defining application configuration settings.
"""

from dataclasses import dataclass

from base.json_dataclass import JsonDataClass


def update_config(option: str, level: str) -> None:
    """
    Updates the configuration with the specified option and value.
    """
    AppConfig().update_value(option, level)


@dataclass
class AppConfig(JsonDataClass):   # pylint: disable=too-many-instance-attributes
    """
    Represents configuration settings for the application.
    """
    label: str = ""
    icon: str = ""
    iconsel: str = ""
    launch: str = ""
    description: str = ""
    language: str = ""
    logging_level: str = ""
    naming_method: str = ""
    console_naming: str = ""
    name_format: str = ""
