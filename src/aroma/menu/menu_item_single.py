"""
Module for handling single-action menu items.
"""
from collections.abc import Callable
from typing import Any

from menu.menu_action import MenuAction
from menu.menu_item_base import MenuItemBase
from model.side_pane import SidePane


class MenuItemSingle(MenuItemBase):
    """
    A menu item that handles a single action, executing it when selected.
    """

    def __init__(
        self,
        text: str,
        action: Callable[..., Any] | None,
        side_pane: SidePane | None = None,
        non_tsp_skip: bool = False
    ):
        super().__init__(side_pane=side_pane)
        self.action = MenuAction(text, action, non_tsp_skip=non_tsp_skip)

    def get_actions(self) -> list[MenuAction]:
        return [self.action]

    def get_action(self) -> MenuAction:
        return self.action

    def run_action(self) -> None:
        if self.selected:
            self._logger.debug("Running action: %s", self.action.text)
            self.action.run()

    def get_text(self) -> str:
        return self.action.text

    def get_prefix_text(self) -> None:
        return None

    def _get_action_side_pane(self) -> SidePane | None:
        return self.action.side_pane
