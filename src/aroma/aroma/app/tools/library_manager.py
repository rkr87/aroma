"""Manages installation and status of arcade ROM naming libraries."""

from shared.classes.base.class_singleton import ClassSingleton
from shared.constants import (
    ARCADE_LIBRARY_APP_RESOURCE,
    ARCADE_LIBRARY_NAME,
    ARCADE_NAMES_TARGET_FILE,
    CUSTOM_ARCADE_LIBRARY_CRC,
    CUSTOM_STR,
    RUNNING_ON_TSP,
    STOCK_STR,
    TSP_USER_LIBRARY_PATH,
)
from shared.tools import util


class LibraryManager(ClassSingleton):
    """Manages installation and status of arcade ROM naming libraries."""

    @staticmethod
    def get_arcade_library_status(menu_options: dict[str, str]) -> int:
        """Retrieve the status of the installed arcade library."""
        logger = LibraryManager.get_static_logger()
        installed: str = "n/a"
        current: str = STOCK_STR
        if RUNNING_ON_TSP:
            installed = util.check_crc(
                TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME,
            )
            if installed == CUSTOM_ARCADE_LIBRARY_CRC:
                current = CUSTOM_STR
        logger.debug("Current library installed: %s (%s)", current, installed)
        if current not in menu_options:
            return 0
        return list(menu_options.keys()).index(current)

    @classmethod
    def install_arcade_library(cls, value: str) -> None:
        """Install the specified arcade ROM naming library."""
        if value == STOCK_STR:
            cls._install_stock_arcade_library()
            return
        cls._install_custom_arcade_library()

    @staticmethod
    def _install_stock_arcade_library() -> None:
        """Install the stock arcade ROM naming library."""
        logger = LibraryManager.get_static_logger()
        logger.info("Installing stock arcade naming library.")
        target_lib = TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME
        util.delete_file(ARCADE_NAMES_TARGET_FILE)
        util.delete_file(target_lib)

        if (backup := target_lib.with_suffix(".stock")).is_file():
            util.rename_file(backup, target_lib)
        else:
            util.extract_from_zip(
                ARCADE_LIBRARY_APP_RESOURCE,
                f"{ARCADE_LIBRARY_NAME}.stock",
                target_lib,
            )

    @staticmethod
    def _install_custom_arcade_library() -> None:
        """Install the custom arcade ROM naming library."""
        logger = LibraryManager.get_static_logger()
        logger.info("Installing custom arcade naming library.")
        target_lib = TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME
        util.delete_file(backup := target_lib.with_suffix(".stock"))
        util.rename_file(target_lib, backup)

        util.extract_from_zip(
            ARCADE_LIBRARY_APP_RESOURCE,
            f"{ARCADE_LIBRARY_NAME}.custom",
            target_lib,
        )
        util.extract_from_zip(
            ARCADE_LIBRARY_APP_RESOURCE,
            ARCADE_NAMES_TARGET_FILE.name,
            ARCADE_NAMES_TARGET_FILE,
        )
