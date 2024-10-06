"""Defines a menu for creating a new collection."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_single import MenuItemSingle


class MenuNewCollection(MenuBase):
    """Manages the menu for creating a new collection."""

    def __init__(self) -> None:
        super().__init__("NEW COLLECTION", self._build_menu())

    @staticmethod
    def _build_menu() -> OrderedDict[str, MenuItemBase]:
        """Build the menu."""
        logger = MenuNewCollection.get_static_logger()
        logger.debug("Building New Collection menu options.")
        return OrderedDict(
            [
                ("CUSTOM", MenuItemSingle("< Custom >", None)),
                ("ADD_ALL", MenuItemSingle("Add All Templates", None)),
            ],
        )

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        pass
