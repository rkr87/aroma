"""
Module for handling multi-action menu items.
"""
from menu.menu_action import MenuAction
from menu.menu_item_base import MenuItemBase
from model.side_pane import SidePane


class MenuItemMulti(MenuItemBase):
    """
    A menu item with multiple actions, allowing cycling between them and
    executing the selected action.
    """

    def __init__(
        self,
        prefix: str,
        actions: list[MenuAction],
        action_index: int = 0,
        side_pane: SidePane | None = None
    ):
        """
        Initialize a multi-action menu item with a prefix, action list, and
        optional side pane.
        """
        super().__init__(side_pane=side_pane)
        self.prefix: str = prefix
        self.actions: list[MenuAction] = actions
        self.action_index: int = action_index

    def get_actions(self) -> list[MenuAction]:
        return self.actions

    def get_action(self) -> MenuAction:
        return self.actions[self.action_index]

    def run_action(self) -> None:
        if self.selected and self.actions:
            current_action = self.actions[self.action_index]
            self._logger.debug("Running action: %s", current_action.text)
            current_action.run()

    def get_text(self) -> str:
        current_action = self.actions[self.action_index]
        return current_action.text

    def get_prefix_text(self) -> str:
        return f"{self.prefix}:"

    def next_action(self) -> None:
        """Cycle to the next action in the list and execute it."""
        self.action_index = (self.action_index + 1) % len(self.actions)
        self._logger.debug("Cycling to next action: %d", self.action_index)
        self.run_action()

    def prev_action(self) -> None:
        """Cycle to the previous action in the list and execute it."""
        self.action_index = (self.action_index - 1) % len(self.actions)
        self._logger.debug("Cycling to previous action: %d", self.action_index)
        self.run_action()

    def _get_action_side_pane(self) -> SidePane | None:
        return self.get_action().side_pane
