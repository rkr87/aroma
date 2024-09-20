"""
Defines a menu for managing collections, including adding new collections
and displaying existing ones.
"""

from collections import OrderedDict
from enum import Enum, auto

from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from navigation.menu_new_collection import MenuNewCollection
from navigation.menu_stack import MenuStack
from strings import Strings


class MenuCollections(MenuBase):
    """
    Manages a menu for collections, allowing users to add new collections
    or select from existing ones.
    """
    class _Options(Enum):
        """
        Defines the options available in this menu.
        """
        NEW = auto()

    @property
    def Option(self) -> type[_Options]:
        """
        Provides the enum class for this menu's options.
        """
        return self._Options

    def __init__(self) -> None:
        """
        Initializes the MenuCollections with a menu stack for navigation and
        a menu for creating new collections.
        """
        self.menu_stack: MenuStack = MenuStack()
        self.new_collection_menu: MenuNewCollection = MenuNewCollection()
        super().__init__(Strings().collections, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """
        Builds the initial menu with options for adding a new collection
        and selecting existing ones.
        """
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building Collections menu options.")
        return OrderedDict([
            (
                self.Option.NEW,
                self.sub_menu(self.new_collection_menu, self.menu_stack.push)
            )
        ])
