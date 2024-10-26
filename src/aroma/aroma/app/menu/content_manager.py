"""Manages the content of menu items and side panes in the navigation system.

This module defines the `ContentManager` class, which is responsible for
managing the menu items, handling updates, and retrieving the currently
visible slice of items for rendering. It also manages the side pane content
based on the current selection.
"""

from collections import OrderedDict

from app.menu.menu_item_base import MenuItemBase
from app.menu.selection_manager import SelectionManager
from app.model.side_pane import SidePane
from shared.classes.class_base import ClassBase


class ContentManager(ClassBase):
    """Handles content management for menu items and side panes."""

    def __init__(
        self,
        items: OrderedDict[str, MenuItemBase],
        selection_manager: SelectionManager,
        side_pane: SidePane | None = None,
    ) -> None:
        super().__init__()
        self._items: OrderedDict[str, MenuItemBase] = items
        self.select: SelectionManager = selection_manager
        self._side_pane: SidePane | None = side_pane

    def deactivate_item(self, key: str) -> None:
        """TODO."""
        self._items[key].deactivated = True

    def add_item(self, key: str, item: MenuItemBase) -> None:
        """Add a menu item to the list."""
        self._items[key] = item
        self.select.state.total += 1
        self._logger.debug("Added item %s to list", item)

    def add_section(self, *items: tuple[str, MenuItemBase]) -> None:
        """Add a menu item section."""
        for index, (key, item) in enumerate(items):
            if index == len(items) - 1:
                item.bottom_separator = True
            self.add_item(key, item)

    def update_item(self, key: str, item: MenuItemBase) -> None:
        """Add a menu item to the list."""
        if key not in self._items:
            self.add_item(key, item)
            return
        self._items[key] = item

    def remove_item(self, key: str) -> None:
        """Remove a menu item by index."""
        if key in self._items:
            removed_item = self._items.pop(key)
            self.select.state.total -= 1
            self._logger.debug("Removed item %s from list", removed_item)

    def clear_items(self) -> None:
        """Clear all menu items."""
        self._items.clear()
        self.select.state.total = 0
        self._logger.debug("Cleared all menu items")

    @property
    def items(self) -> OrderedDict[str, MenuItemBase]:
        """TODO."""
        return self._items

    @items.setter
    def items(self, items: OrderedDict[str, MenuItemBase]) -> None:
        """TODO."""
        self._items = items
        self.select.state.total = len(items)

    def get_slice(self) -> list[MenuItemBase]:
        """Retrieve the current slice of visible menu items."""
        item_list = list(self._items.values())
        if not self.select.state.total > self.select.state.max:
            return item_list
        return item_list[self.select.state.start : self.select.state.end]

    @property
    def side_pane(self) -> SidePane | None:
        """Retrieve the merged side pane for the current selection."""
        merged_pane = SidePane.merge(
            self._get_current_item().side_pane,
            self._side_pane,
        )
        self._logger.debug("Merged side pane: %s", merged_pane)
        return merged_pane

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        item_list = list(self._items.values())
        selected_item = item_list[self.select.state.selected]
        self._logger.debug("Retrieved current item: %s", selected_item)
        return selected_item
