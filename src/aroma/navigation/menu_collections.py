"""
Defines a menu for managing collections, including adding new collections
and displaying existing ones.
"""

from model.menu_item_base import MenuItemBase
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
        super().__init__("COLLECTIONS", self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:
        """
        Builds the initial menu with options for adding a new collection
        and selecting existing ones.
        """
        return [
            self.create_sub_menu(
                self.new_collection_menu,
                self.menu_stack.push
            )
        ]
