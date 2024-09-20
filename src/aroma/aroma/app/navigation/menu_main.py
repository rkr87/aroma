"""
Defines the main menu of the application, providing navigation options
to access collections and settings.
"""

from collections import OrderedDict
from enum import Enum, auto

from app.navigation.menu_collections import MenuCollections
from app.navigation.menu_options import MenuOptions
from app.navigation.menu_rom_naming import MenuRomNaming
from app.navigation.menu_stack import MenuStack
from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_single import MenuItemSingle
from constants import APP_NAME
from data.database.rom_db import RomDB
from model.side_pane import SidePane
from model.strings import Strings


class MenuMain(MenuBase):
    """
    Manages the main menu, allowing users to navigate to collections and
    options menus.
    """

    class _Options(Enum):
        """
        Defines the options available in this menu.
        """
        COLLECTIONS = auto()
        ROM_NAMING = auto()
        OPTIONS = auto()
        REFRESH = auto()

    @property
    def Option(self) -> type[_Options]:
        """
        Provides the enum class for this menu's options.
        """
        return self._Options

    def __init__(self) -> None:
        """
        Initializes the MenuMain with navigation to collections and options
        menus.
        """
        side_pane: SidePane = SidePane(
            "Header Test",
            (
                "some very long content to test word wrap while rendering the "
                "side pane also need to do some nested side pane testing by "
                "applying a different side pane to each menu item and actions"
                "\n\nthis side pane is generated at the menu level"
            )
        )
        super().__init__(APP_NAME, self._build_menu(), side_pane)

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """
        Builds the main menu with options to navigate to collections and
        options.
        """
        logger = self.get_static_logger()
        logger.debug("Building Main menu options.")
        return OrderedDict([
            (
                self.Option.COLLECTIONS,
                self.sub_menu(MenuCollections(), MenuStack().push)
            ),
            (
                self.Option.ROM_NAMING,
                self.sub_menu(MenuRomNaming(), MenuStack().push)
            ),
            (
                self.Option.OPTIONS,
                self.sub_menu(MenuOptions(), MenuStack().push)
            ),
            (self.Option.REFRESH, self._refresh_roms())
        ])

    @staticmethod
    def _refresh_roms() -> MenuItemSingle:
        """
        Creates a menu item that refreshes the ROM database.
        """
        return MenuItemSingle(
            Strings().refresh_roms,
            RomDB().update_db,
            SidePane(Strings().refresh_roms, Strings.refresh_roms_desc)
        )