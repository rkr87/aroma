"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""

import os

import util
from base.class_singleton import ClassSingleton
from constants import CUSTOM_STR, RESOURCES, RUNNING_ON_TSP, STOCK_STR

CUSTOM_LIBRARY_CRC = "0x8a1cae0"
LIBRARY_PATH = "/usr/trimui/lib"
LIBRARY_NAME = "libgamename.so"
LIBRARY_ZIP = f"{RESOURCES}/naming/{LIBRARY_NAME}.zip"
ARCADE_NAMES_PATH = "/mnt/SDCARD/BIOS/arcade_lists"
ARCADE_NAMES_FILE = "arcade-rom-names.txt"
NAMES_ZIP = f"{RESOURCES}/naming/names.zip"


class ActionRomNaming(ClassSingleton):
    """
    A menu for managing ROM naming preferences.
    """

    @staticmethod
    def install_arcade_library(value: str) -> None:
        """
        TODO
        """
        if value == STOCK_STR:
            ActionRomNaming._install_stock_arcade_library()
            return
        ActionRomNaming._install_custom_arcade_library()
        return

    @staticmethod
    def get_arcade_library_status(menu_options: dict[str, str]) -> int:
        """
        TODO
        """
        logger = ActionRomNaming.get_static_logger()
        installed: str = "n/a"
        current: str = STOCK_STR
        if RUNNING_ON_TSP:
            installed = util.check_crc(f"{LIBRARY_PATH}/{LIBRARY_NAME}")
            if installed == CUSTOM_LIBRARY_CRC:
                current = CUSTOM_STR
        logger.debug("Current library installed: %s (%s)", current, installed)
        if current not in menu_options:
            return 0
        return list(menu_options.keys()).index(current)

    @staticmethod
    def _install_stock_arcade_library() -> None:
        """
        Install the stock arcade ROM naming library by replacing any custom
        library and removing custom arcade name lists.
        """
        logger = ActionRomNaming.get_static_logger()
        logger.info("Installing stock arcade naming library.")
        target_lib = f"{LIBRARY_PATH}/{LIBRARY_NAME}"
        arcade_names = f"{ARCADE_NAMES_PATH}/{ARCADE_NAMES_FILE}"
        util.delete_file(arcade_names)
        util.delete_file(target_lib)

        if os.path.exists(f"{target_lib}.stock"):
            util.rename_file(f"{target_lib}.stock", target_lib)
        else:
            util.extract_from_zip(
                LIBRARY_ZIP,
                f"{LIBRARY_NAME}.stock",
                target_lib
            )

    @staticmethod
    def _install_custom_arcade_library() -> None:
        """
        Install the custom arcade ROM naming library by backing up the stock
        library and adding a configurable list of arcade ROM names.
        """
        logger = ActionRomNaming.get_static_logger()
        logger.info("Installing custom arcade naming library.")
        target_lib = f"{LIBRARY_PATH}/{LIBRARY_NAME}"
        util.delete_file(f"{target_lib}.stock")
        util.rename_file(target_lib, f"{target_lib}.stock")

        util.extract_from_zip(
            LIBRARY_ZIP,
            f"{LIBRARY_NAME}.custom",
            target_lib
        )
        util.extract_from_zip(
            NAMES_ZIP,
            ARCADE_NAMES_FILE,
            f"{ARCADE_NAMES_PATH}/{ARCADE_NAMES_FILE}"
        )
