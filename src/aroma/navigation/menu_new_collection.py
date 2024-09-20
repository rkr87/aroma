"""
Defines a menu for creating a new collection, including options to add
templates and customize the collection.
"""

from collections import OrderedDict
from enum import Enum, auto

from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_single import MenuItemSingle


class MenuNewCollection(MenuBase):
    """
    Manages the menu for creating a new collection, offering options to
    customise and add templates to the collection.
    """

    class _Options(Enum):
        """
        Defines the options available in this menu.
        """
        CUSTOM = auto()
        ADD_ALL = auto()

    @property
    def Option(self) -> type[_Options]:
        """
        Provides the enum class for this menu's options.
        """
        return self._Options

    def __init__(self) -> None:
        """
        Initializes the MenuNewCollection with a title and menu options for
        creating a new collection.
        """
        super().__init__("NEW COLLECTION", self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the menu with options for creating a new collection, including
        custom and template-based options.
        """
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building New Collection menu options.")
        return OrderedDict([
            (self.Option.CUSTOM, MenuItemSingle("< Custom >", None)),
            (self.Option.ADD_ALL, MenuItemSingle("Add All Templates", None))
        ])
