"""Module for managing actions related to menu items."""

from app.menu.content_manager import ContentManager
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.menu.selection_manager import SelectionManager
from shared.classes.class_base import ClassBase


class ActionManager(ClassBase):
    """Manages actions for selected menu items."""

    def __init__(
        self,
        selection_manager: SelectionManager,
        content_manager: ContentManager,
    ) -> None:
        super().__init__()
        self.select: SelectionManager = selection_manager
        self.content: ContentManager = content_manager

    def run_next(self) -> None:
        """Run the next action for a multi-action menu item."""
        item = self._get_current_item()
        if isinstance(item, MenuItemMulti):
            self._logger.debug(
                "Running next action for item %s",
                item.prefix,
            )
            item.next_action()

    def run_prev(self) -> None:
        """Run the previous action for a multi-action menu item."""
        item = self._get_current_item()
        if isinstance(item, MenuItemMulti):
            self._logger.debug(
                "Running previous action for item %s",
                item.prefix,
            )
            item.prev_action()

    def run_selected(self) -> None:
        """Run the selected action for a single-action menu item."""
        item = self._get_current_item()
        if isinstance(item, MenuItemSingle):
            self._logger.debug(
                "Running selected action for item %s",
                item.get_text(),
            )
            item.run_action()

    def _get_current_item(self) -> MenuItemBase:
        """Retrieve the currently selected menu item."""
        selected_index = self.select.state.selected
        item_list = list(self.content.items.values())
        item = item_list[selected_index]
        self._logger.debug(
            "Retrieved current item %s at index %d",
            item,
            selected_index,
        )
        return item
