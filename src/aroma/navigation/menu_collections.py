"""
Defines a menu for managing collections, including adding new collections
and displaying existing ones.
"""

from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from model.strings import Strings
from navigation.menu_new_collection import MenuNewCollection
from navigation.menu_stack import MenuStack


class MenuCollections(MenuBase):
    """
    Manages a menu for collections, allowing users to add new collections
    or select from existing ones.
    """

    def __init__(self) -> None:
        """
        Initializes the MenuCollections with a menu stack for navigation and
        a menu for creating new collections.
        """
        self.menu_stack: MenuStack = MenuStack()
        self.new_collection_menu: MenuNewCollection = MenuNewCollection()
        super().__init__(Strings().collections, self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:
        """
        Builds the initial menu with options for adding a new collection
        and selecting existing ones.
        """
        return [
            self.sub_menu(
                self.new_collection_menu,
                self.menu_stack.push
            )
        ]
