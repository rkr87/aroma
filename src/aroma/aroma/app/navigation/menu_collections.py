"""Defines a menu for managing collections."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.navigation.menu_new_collection import MenuNewCollection
from app.navigation.menu_stack import MenuStack
from app.strings import Strings


class MenuCollections(MenuBase):
    """Manages a menu for collections."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.new_collection_menu: MenuNewCollection = MenuNewCollection()
        super().__init__(Strings().collections, self._build_menu())

    def _build_menu(self) -> OrderedDict[str, MenuItemBase]:
        """Build the initial menu."""
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building Collections menu options.")
        new = (
            "NEW",
            self.sub_menu(self.new_collection_menu, self.menu_stack.push),
        )
        return OrderedDict([new])

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        pass
