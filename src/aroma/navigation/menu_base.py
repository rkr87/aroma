"""
Defines a Menu class for managing menu items, cycling through options, and
handling user input using a game controller.
"""

from abc import ABC
from collections.abc import Callable
from functools import partial
from typing import Any

from base.class_singleton import ClassSingleton
from model.menu_item_base import MenuItemBase
from model.menu_item_single import MenuItemSingle
from model.side_pane import SidePane
from navigation.action_manager import ActionManager
from navigation.content_manager import ContentManager
from navigation.selection_manager import SelectionManager


class MenuBase(ClassSingleton, ABC):
    """
    Base class for managing menu items, navigation, and user actions.
    """

    def __init__(
        self,
        breadcrumb: str,
        items: list[MenuItemBase],
        side_pane: SidePane | None = None
    ) -> None:
        """
        Initialize the menu with breadcrumb, items, and optional side pane.
        """
        super().__init__()
        self.breadcrumb = breadcrumb
        self.select = SelectionManager(len(items))
        self.content = ContentManager(items, self.select, side_pane)
        self.action = ActionManager(self.select, self.content)

    def update(self) -> list[MenuItemBase]:
        """
        Update the menu's selection state and return visible items.
        """
        for i, item in enumerate(self.content.items):
            item.selected = i == self.select.state.selected

        return self.content.get_slice()

    @staticmethod  # type: ignore
    def sub_menu(
        menu: "MenuBase",
        stack_push: Callable[["MenuBase"], Any],
        side_pane: SidePane | None = None
    ) -> MenuItemSingle:
        """
        Create a single menu item that pushes a submenu onto the menu stack.
        """
        return MenuItemSingle(
            menu.breadcrumb,
            partial(stack_push, menu),
            side_pane=side_pane
        )
