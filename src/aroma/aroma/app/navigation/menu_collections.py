"""Defines a menu for managing collections."""

from collections import OrderedDict
from enum import Enum, auto

from app.navigation.menu_new_collection import MenuNewCollection
from app.navigation.menu_stack import MenuStack
from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from tools.strings import Strings


class MenuCollections(MenuBase):
    """Manages a menu for collections."""

    class _Options(Enum):
        """Defines the options available in this menu."""

        NEW = auto()

    @property
    def option(self) -> type[_Options]:
        """Provides the enum class for this menu's options."""
        return self._Options

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.new_collection_menu: MenuNewCollection = MenuNewCollection()
        super().__init__(Strings().collections, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """Build the initial menu."""
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building Collections menu options.")
        return OrderedDict(
            [
                (
                    self.option.NEW,
                    self.sub_menu(
                        self.new_collection_menu,
                        self.menu_stack.push,
                    ),
                ),
            ],
        )
