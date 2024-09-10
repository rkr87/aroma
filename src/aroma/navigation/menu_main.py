"""
Defines the main menu of the application, providing navigation options
to access collections and settings.
"""

from constants import APP_NAME
from model.menu_item_base import MenuItemBase
from model.menu_stack import MenuStack
from model.side_pane import SidePane
from navigation.menu_base import MenuBase
from navigation.menu_collections import MenuCollections
from navigation.menu_options import MenuOptions
from navigation.menu_rom_naming import MenuRomNaming


class MenuMain(MenuBase):
    """
    Manages the main menu, allowing users to navigate to collections and
    options menus.
    """

    def __init__(
        self,
        menu_stack: MenuStack,
        collections_menu: MenuCollections,
        rom_naming_menu: MenuRomNaming,
        options_menu: MenuOptions
    ) -> None:
        """
        Initializes the MenuMain with navigation to collections and options
        menus.
        """
        self.menu_stack = menu_stack
        self.collections_menu: MenuCollections = collections_menu
        self.options_menu: MenuOptions = options_menu
        self.rom_naming_menu: MenuRomNaming = rom_naming_menu
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

    def _build_menu(self) -> list[MenuItemBase]:
        """
        Builds the main menu with options to navigate to collections and
        options.
        """
        return [
            self.create_sub_menu(self.collections_menu, self.menu_stack.push),
            self.create_sub_menu(self.rom_naming_menu, self.menu_stack.push),
            self.create_sub_menu(self.options_menu, self.menu_stack.push)
        ]
