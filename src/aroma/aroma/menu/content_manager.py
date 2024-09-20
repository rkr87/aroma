"""
Manages the content of menu items and side panes in the navigation system.

This module defines the `ContentManager` class, which is responsible for
managing the menu items, handling updates, and retrieving the currently
visible slice of items for rendering. It also manages the side pane content
based on the current selection.
"""

from collections import OrderedDict
from enum import Enum

from base.class_base import ClassBase
from menu.menu_item_base import MenuItemBase
from menu.selection_manager import SelectionManager
from model.side_pane import SidePane


class ContentManager(ClassBase):
    """Handles content management for menu items and side panes."""

    def __init__(
        self,
        items: OrderedDict[Enum, MenuItemBase],
        selection_manager: SelectionManager,
        side_pane: SidePane | None = None,
    ) -> None:
        """
        Initialize with menu items, a selection manager, and an optional side
        pane.
        """
        super().__init__()
        self.items: OrderedDict[Enum, MenuItemBase] = items
        self.select: SelectionManager = selection_manager
        self._side_pane: SidePane | None = side_pane

    def add_item(self, key: Enum, item: MenuItemBase) -> None:
        """Add a menu item to the list."""
        self.items[key] = item
        self._logger.debug("Added item %s to list", item)

    def remove_item(self, key: Enum) -> None:
        """Remove a menu item by index."""
        if key in self.items:
            removed_item = self.items.pop(key)
            self._logger.debug("Removed item %s from list", removed_item)

    def clear_items(self) -> None:
        """Clear all menu items."""
        self.items.clear()
        self._logger.debug("Cleared all menu items")

    def get_slice(self) -> list[MenuItemBase]:
        """Retrieve the current slice of visible menu items."""
        item_list = list(self.items.values())
        if not self.select.state.total > self.select.state.max:
            return item_list

        start = self.select.state.start
        end = self.select.state.end
        item_slice = item_list[start:end]
        self._logger.debug(
            "Retrieved slice from index %d to %d", start, end
        )
        return item_slice

    @property
    def side_pane(self) -> SidePane | None:
        """Retrieve the merged side pane for the current selection."""
        merged_pane = SidePane.merge(
            self._get_current_item().side_pane,
            self._side_pane
        )
        self._logger.debug("Merged side pane: %s", merged_pane)
        return merged_pane

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        item_list = list(self.items.values())
        selected_item = item_list[self.select.state.selected]
        self._logger.debug("Retrieved current item: %s", selected_item)
        return selected_item
