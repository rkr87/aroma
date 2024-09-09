"""
Defines a menu for creating a new collection, including options to add
templates and customize the collection.
"""

from model.menu_action import MenuAction
from model.menu_item import MenuItem
from navigation.base_menu import BaseMenu


class MenuNewCollection(BaseMenu):
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

    def _build_menu(self) -> list[MenuItem]:  # pylint: disable=no-self-use
        """
        Builds the menu with options for creating a new collection, including
        custom and template-based options.
        """
        return [
            MenuItem([MenuAction("< Custom >", None)]),
            MenuItem([MenuAction("Add All Templates", None)]),
            MenuItem([MenuAction("TEMPLATE: Collection One", None)]),
            MenuItem([MenuAction("TEMPLATE: Collection Two", None)]),
        ]
