# pylint: disable=too-many-arguments
"""
Module for defining application configuration settings.
"""

from dataclasses import dataclass

from classes.base.json_dataclass import JsonDataClass


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
    db_rebuild_req: str = ""

    @staticmethod
    def set_db_rebuild_required(reason: str) -> None:
        """
        Set a flag indicating that a rebuild of the ROM database is
        required.
        """
        AppConfig.get_static_logger().info(
            "Force full rebuild of RomDB: %s", reason
        )
        AppConfig().update_value("db_rebuild_req", reason)
