"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""

import util
from base.class_singleton import ClassSingleton
from constants import (ARCADE_LIBRARY_APP_RESOURCE, ARCADE_LIBRARY_NAME,
                       ARCADE_NAMES_TARGET_FILE, CUSTOM_ARCADE_LIBRARY_CRC,
                       CUSTOM_STR, RUNNING_ON_TSP, STOCK_STR,
                       TSP_USER_LIBRARY_PATH)


class LibraryManager(ClassSingleton):
    """
    TODO
    """

    @staticmethod
    def get_arcade_library_status(menu_options: dict[str, str]) -> int:
        """
        TODO
        """
        logger = LibraryManager.get_static_logger()
        installed: str = "n/a"
        current: str = STOCK_STR
        if RUNNING_ON_TSP:
            installed = \
                util.check_crc(TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME)
            if installed == CUSTOM_ARCADE_LIBRARY_CRC:
                current = CUSTOM_STR
        logger.debug("Current library installed: %s (%s)", current, installed)
        if current not in menu_options:
            return 0
        return list(menu_options.keys()).index(current)

    @classmethod
    def install_arcade_library(cls, value: str) -> None:
        """
        TODO
        """
        if value == STOCK_STR:
            cls._install_stock_arcade_library()
            return
        cls._install_custom_arcade_library()
        return

    @staticmethod
    def _install_stock_arcade_library() -> None:
        """
        Install the stock arcade ROM naming library by replacing any custom
        library and removing custom arcade name lists.
        """
        logger = LibraryManager.get_static_logger()
        logger.info("Installing stock arcade naming library.")
        target_lib = TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME
        util.delete_file(ARCADE_NAMES_TARGET_FILE)
        util.delete_file(target_lib)

        if (backup := target_lib.with_suffix("stock")).is_file():
            util.rename_file(backup, target_lib)
        else:
            util.extract_from_zip(
                ARCADE_LIBRARY_APP_RESOURCE,
                f"{ARCADE_LIBRARY_NAME}.stock",
                target_lib
            )

    @staticmethod
    def _install_custom_arcade_library() -> None:
        """
        Install the custom arcade ROM naming library by backing up the stock
        library and adding a configurable list of arcade ROM names.
        """
        logger = LibraryManager.get_static_logger()
        logger.info("Installing custom arcade naming library.")
        target_lib = TSP_USER_LIBRARY_PATH / ARCADE_LIBRARY_NAME
        util.delete_file(backup := target_lib.with_suffix(".stock"))
        util.rename_file(target_lib, backup)

        util.extract_from_zip(
            ARCADE_LIBRARY_APP_RESOURCE,
            f"{ARCADE_LIBRARY_NAME}.custom",
            target_lib
        )
        util.extract_from_zip(
            ARCADE_LIBRARY_APP_RESOURCE,
            ARCADE_NAMES_TARGET_FILE.name,
            ARCADE_NAMES_TARGET_FILE
        )
