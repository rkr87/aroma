"""
Defines a menu for managing collections, including adding new collections
and displaying existing ones.
"""

from model.menu_action import MenuAction
from model.menu_item import MenuItem
from model.menu_stack import MenuStack
from navigation.base_menu import BaseMenu
from navigation.menu_new_collection import MenuNewCollection


class MenuCollections(BaseMenu):
    """
    Manages a menu for collections, allowing users to add new collections
    or select from existing ones.
    """

    def __init__(
        self,
        menu_stack: MenuStack,
        new_collection_menu: MenuNewCollection
    ) -> None:
        """
        Initializes the MenuCollections with a menu stack for navigation and
        a menu for creating new collections.
        """
        self.menu_stack: MenuStack = menu_stack
        self.new_collection_menu: MenuNewCollection = new_collection_menu
        super().__init__("Collections", self._build_menu())

    def _build_menu(self) -> list[MenuItem]:
        """
        Builds the initial menu with options for adding a new collection
        and selecting existing ones.
        """
        return [
            MenuItem([MenuAction("< Add New >", self._new_collection_menu)]),
            MenuItem([MenuAction("Existing Collection One", None)]),
            MenuItem([MenuAction("Existing Collection Two", None)]),
        ]

    def _new_collection_menu(self) -> None:
        """
        Pushes the new collection menu onto the menu stack to allow users
        to create a new collection.
        """
        self.menu_stack.push(self.new_collection_menu)
