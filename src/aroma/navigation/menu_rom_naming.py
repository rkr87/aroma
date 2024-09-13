"""
TODO
"""

import os

from constants import RESOURCES, RUNNING_ON_TSP
from menu.menu_action import MenuAction
from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_multi import MenuItemMulti
from model.side_pane import SidePane
from model.strings import Strings
from util import check_crc, extract_from_zip


class MenuRomNaming(MenuBase):
    """
    A menu for managing ROM naming preferences.
    """
    CUSTOM_LIBRARY_CRC = "0x8a1cae0"
    LIBRARY_PATH = "/usr/trimui/lib"
    LIBRARY_NAME = "libgamename.so"
    LIBRARY_ZIP = f"{RESOURCES}/naming/{LIBRARY_NAME}.zip"
    ARCADE_NAMES_PATH = "/mnt/SDCARD/BIOS/arcade_lists"
    ARCADE_NAMES_FILE = "arcade-rom-names.txt"
    NAMES_ZIP = f"{RESOURCES}/naming/names.zip"

    def __init__(self) -> None:
        """
        Initialize the ROM naming menu with arcade ROM naming options.
        """
        super().__init__(Strings().rom_naming, self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:
        """
        Build the menu for selecting between stock and custom arcade ROM
        naming libraries.
        """
        return [
            self._arcade_rom_naming()
        ]

    def _arcade_rom_naming(self) -> MenuItemMulti:
        """
        Create a menu item for selecting between stock and custom ROM naming
        libraries, showing their current installation state.
        """
        installed: str = "n/a"
        if RUNNING_ON_TSP:
            installed = check_crc(f"{self.LIBRARY_PATH}/{self.LIBRARY_NAME}")
        current: int = 1 if installed == self.CUSTOM_LIBRARY_CRC else 0
        return MenuItemMulti(
            Strings().arcade_rom_naming,
            [
                MenuAction(
                    Strings().stock,
                    self._install_stock_arcade_library,
                    SidePane(
                        content=Strings().arcade_rom_naming_stock(installed)
                    ),
                    True
                ),
                MenuAction(
                    Strings().custom,
                    self._install_custom_arcade_library,
                    SidePane(
                        content=Strings().arcade_rom_naming_custom(
                            installed,
                            self.LIBRARY_PATH,
                            self.LIBRARY_NAME,
                            self.ARCADE_NAMES_PATH,
                            self.ARCADE_NAMES_FILE
                        )
                    ),
                    True
                )
            ],
            current,
            SidePane(header=Strings().arcade_rom_naming)
        )

    def _install_stock_arcade_library(self) -> None:
        """
        Install the stock arcade ROM naming library by replacing any custom
        library and removing custom arcade name lists.
        """
        target_lib = f"{self.LIBRARY_PATH}/{self.LIBRARY_NAME}"
        arcade_names = f"{self.ARCADE_NAMES_PATH}/{self.ARCADE_NAMES_FILE}"
        if os.path.exists(arcade_names):
            os.remove(arcade_names)
        if os.path.exists(target_lib):
            os.remove(target_lib)
        if os.path.exists(f"{target_lib}.stock"):
            os.rename(f"{target_lib}.stock", target_lib)
        else:
            extract_from_zip(
                self.LIBRARY_ZIP,
                f"{self.LIBRARY_NAME}.stock",
                target_lib
            )
        # TODO - uncomment this # pylint: disable=fixme
        # reboot()

    def _install_custom_arcade_library(self) -> None:
        """
        Install the custom arcade ROM naming library by backing up the stock
        library and adding a configurable list of arcade ROM names.
        """
        target_lib = f"{self.LIBRARY_PATH}/{self.LIBRARY_NAME}"
        if os.path.exists(f"{target_lib}.stock"):
            os.remove(f"{target_lib}.stock")
        os.rename(target_lib, f"{target_lib}.stock")
        extract_from_zip(
            self.LIBRARY_ZIP,
            f"{self.LIBRARY_NAME}.custom",
            target_lib
        )
        extract_from_zip(
            self.NAMES_ZIP,
            self.ARCADE_NAMES_FILE,
            f"{self.ARCADE_NAMES_PATH}/{self.ARCADE_NAMES_FILE}"
        )
        # TODO - uncomment this # pylint: disable=fixme
        # reboot()
