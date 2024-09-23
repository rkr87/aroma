# pylint: disable=too-many-arguments
"""Module for defining application configuration settings."""

from dataclasses import dataclass

from classes.base.json_dataclass import JsonDataClass


@dataclass
class AppConfig(JsonDataClass):  # pylint: disable=too-many-instance-attributes
    """Represents configuration settings for the application."""

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
    db_rebuild_req: bool = False
    remove_broken_images_on_refresh: bool = False

    @staticmethod
    def set_db_rebuild_required(reason: str | None = None) -> None:
        """Set ROM DB rebuild required flag."""
        AppConfig().db_rebuild_req = (check := bool(reason))
        AppConfig().save()
        if check:
            AppConfig.get_static_logger().info(
                "Force full rebuild of RomDB: %s",
                reason,
            )
