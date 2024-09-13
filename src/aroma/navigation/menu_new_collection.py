"""
Defines a menu for creating a new collection, including options to add
templates and customize the collection.
"""

from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_single import MenuItemSingle


class MenuNewCollection(MenuBase):
    """
    Manages the menu for creating a new collection, offering options to
    customise and add templates to the collection.
    """

    def __init__(self) -> None:
        """
        Initializes the MenuNewCollection with a title and menu options for
        creating a new collection.
        """
        super().__init__("NEW COLLECTION", self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the menu with options for creating a new collection, including
        custom and template-based options.
        """
        return [
            MenuItemSingle("< Custom >", None),
            MenuItemSingle("Add All Templates", None),
            MenuItemSingle("TEMPLATE: Collection One", None),
            MenuItemSingle("TEMPLATE: Collection Two", None),
        ]
