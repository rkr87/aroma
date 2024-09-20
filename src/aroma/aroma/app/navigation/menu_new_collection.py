"""Defines a menu for creating a new collection."""

from collections import OrderedDict
from enum import Enum, auto

from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_single import MenuItemSingle


class MenuNewCollection(MenuBase):
    """Manages the menu for creating a new collection."""

    class _Options(Enum):
        """Defines the options available in this menu."""

        CUSTOM = auto()
        ADD_ALL = auto()

    @property
    def option(self) -> type[_Options]:
        """Provides the enum class for this menu's options."""
        return self._Options

    def __init__(self) -> None:
        super().__init__("NEW COLLECTION", self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """Build the menu."""
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building New Collection menu options.")
        return OrderedDict(
            [
                (self.option.CUSTOM, MenuItemSingle("< Custom >", None)),
                (
                    self.option.ADD_ALL,
                    MenuItemSingle("Add All Templates", None),
                ),
            ],
        )
