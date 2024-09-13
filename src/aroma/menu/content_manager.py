"""
Manages the content of menu items and side panes in the navigation system.

This module defines the `ContentManager` class, which is responsible for
managing the menu items, handling updates, and retrieving the currently
visible slice of items for rendering. It also manages the side pane content
based on the current selection.
"""

from base.class_base import ClassBase
from menu.menu_item_base import MenuItemBase
from menu.selection_manager import SelectionManager
from model.side_pane import SidePane


class ContentManager(ClassBase):
    """Handles content management for menu items and side panes."""

    def __init__(
        self,
        items: list[MenuItemBase],
        selection_manager: SelectionManager,
        side_pane: SidePane | None = None,
    ) -> None:
        """
        Initialize with menu items, a selection manager, and an optional side
        pane.
        """
        super().__init__()
        self.items: list[MenuItemBase] = items
        self.select: SelectionManager = selection_manager
        self._side_pane: SidePane | None = side_pane

    def add_item(self, item: MenuItemBase) -> None:
        """Add a menu item to the list."""
        self.items.append(item)

    def remove_item(self, index: int) -> None:
        """Remove a menu item by index."""
        if 0 <= index < len(self.items):
            del self.items[index]

    def update_item(self, index: int, new_item: MenuItemBase) -> None:
        """Update a menu item at a given index."""
        if 0 <= index < len(self.items):
            self.items[index] = new_item

    def clear_items(self) -> None:
        """Clear all menu items."""
        self.items.clear()

    def get_slice(self) -> list[MenuItemBase]:
        """Retrieve the current slice of visible menu items."""
        if not self.select.state.total > self.select.state.max:
            return self.items

        start = self.select.state.start
        end = self.select.state.end
        return self.items[start:end]

    @property
    def side_pane(self) -> SidePane | None:
        """Retrieve the merged side pane for the current selection."""
        return SidePane.merge(
            self._get_current_item().side_pane,
            self._side_pane
        )

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        return self.items[self.select.state.selected]
