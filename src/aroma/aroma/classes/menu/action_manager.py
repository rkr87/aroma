"""
Module for managing actions related to menu items in a navigation system.
"""
from classes.base.class_base import ClassBase
from classes.menu.content_manager import ContentManager
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_multi import MenuItemMulti
from classes.menu.menu_item_single import MenuItemSingle
from classes.menu.selection_manager import SelectionManager


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
        item = self._get_current_item()
        if isinstance(item, MenuItemMulti):
            self._logger.debug(
                "Running next action for item %s", item
            )
            item.next_action()

    def run_prev(self) -> None:
        """Run the previous action for a multi-action menu item."""
        item = self._get_current_item()
        if isinstance(item, MenuItemMulti):
            self._logger.debug(
                "Running previous action for item %s", item
            )
            item.prev_action()

    def run_selected(self) -> None:
        """Run the selected action for a single-action menu item."""
        item = self._get_current_item()
        if isinstance(item, MenuItemSingle):
            self._logger.debug(
                "Running selected action for item %s", item
            )
            item.run_action()

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        selected_index = self.select.state.selected
        item_list = list(self.content.items.values())
        item = item_list[selected_index]
        self._logger.debug(
            "Retrieved current item %s at index %d", item, selected_index
        )
        return item
