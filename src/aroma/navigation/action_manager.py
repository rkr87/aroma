"""
Module for managing actions related to menu items in a navigation system.
"""
from base.class_base import ClassBase
from model.menu_item_base import MenuItemBase
from model.menu_item_multi import MenuItemMulti
from model.menu_item_single import MenuItemSingle
from navigation.content_manager import ContentManager
from navigation.selection_manager import SelectionManager


class ActionManager(ClassBase):
    """
    Manages actions for selected menu items, including navigating through
    multi-actions.
    """

    def __init__(
        self,
        selection_manager: SelectionManager,
        content_manager: ContentManager
    ) -> None:
        """Initialize with selection and content managers."""
        super().__init__()
        self.select: SelectionManager = selection_manager
        self.content: ContentManager = content_manager

    def run_next(self) -> None:
        """Run the next action for a multi-action menu item."""
        if isinstance(item := self._get_current_item(), MenuItemMulti):
            item.next_action()

    def run_prev(self) -> None:
        """Run the previous action for a multi-action menu item."""
        if isinstance(item := self._get_current_item(), MenuItemMulti):
            item.prev_action()

    def run_selected(self) -> None:
        """Run the selected action for a single-action menu item."""
        if isinstance(item := self._get_current_item(), MenuItemSingle):
            item.run_action()

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        return self.content.items[self.select.state.selected]
