# pylint: disable=too-many-arguments
"""Module for defining application configuration settings."""

from dataclasses import dataclass

from shared.classes.json_dataclass import JsonDataClass


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
    console_naming: str = ""
    name_format: str = ""
    db_rebuild_req: bool = False
    remove_broken_images_on_refresh: bool = False
    days_until_scrape_attempt: int = 7
    scrape_on_refresh: bool = False
    scrape_media_type: str = ""
    scrape_preferred_region: str = ""
    screenscraper_userid: str = ""
    screenscraper_password: str = ""
    _scrape_cpu_threads: int = 0
    archive_userid: str = ""
    archive_password: str = ""
    clean_emu_on_refresh: bool = False
    version: str = ""

    @property
    def scrape_cpu_threads(self) -> int | None:
        """Return number of CPU threads for scraping, or None if not set."""
        return w if (w := self._scrape_cpu_threads) > 0 else None

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
