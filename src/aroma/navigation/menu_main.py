"""
Defines the main menu of the application, providing navigation options
to access collections and settings.
"""

from model.menu_action import MenuAction
from model.menu_item import MenuItem
from model.menu_stack import MenuStack
from navigation.base_menu import BaseMenu
from navigation.menu_collections import MenuCollections
from navigation.menu_options import MenuOptions


class MenuMain(BaseMenu):
    """
    Manages the main menu, allowing users to navigate to collections and
    options menus.
    """

    def __init__(
        self,
        menu_stack: MenuStack,
        collections_menu: MenuCollections,
        options_menu: MenuOptions
    ) -> None:
        """
        Initializes the MenuMain with navigation to collections and options
        menus.
        """
        self.menu_stack: MenuStack = menu_stack
        self.collections_menu: MenuCollections = collections_menu
        self.options_menu: MenuOptions = options_menu
        super().__init__("aROMa", self._build_menu())

    def _build_menu(self) -> list[MenuItem]:
        """
        Builds the main menu with options to navigate to collections and options.
        """
        return [
            MenuItem([MenuAction("Collections", self._collections_menu)]),
            MenuItem([MenuAction("Options", self._options_menu)]),
        ]

    def _collections_menu(self) -> None:
        """
        Pushes the collections menu onto the menu stack to allow users to
        navigate to the collections menu.
        """
        self.menu_stack.push(self.collections_menu)

    def _options_menu(self) -> None:
        """
        Pushes the options menu onto the menu stack to allow users to
        navigate to the options menu.
        """
        self.menu_stack.push(self.options_menu)
