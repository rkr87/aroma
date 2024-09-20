"""
Defines a Menu class for managing menu items.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import Callable
from enum import Enum
from functools import partial
from typing import Any

from classes.base.class_singleton import ClassSingleton
from classes.menu.action_manager import ActionManager
from classes.menu.content_manager import ContentManager
from classes.menu.menu_action import MenuAction
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_single import MenuItemSingle
from classes.menu.selection_manager import SelectionManager
from model.app_config import AppConfig
from model.side_pane import SidePane
from tools import util


class MenuBase(ClassSingleton, ABC):
    """
    Base class for managing menu items, navigation, and user actions.
    """

    def __init__(
        self,
        breadcrumb: str,
        items: OrderedDict[Enum, MenuItemBase],
        side_pane: SidePane | None = None
    ) -> None:
        """
        Initialize the menu with breadcrumb, items, and optional side pane.
        """
        super().__init__()
        self.breadcrumb: str = breadcrumb
        self.select: SelectionManager = SelectionManager(len(items))
        self.content: ContentManager = ContentManager(
            items, self.select, side_pane
        )
        self.action: ActionManager = ActionManager(self.select, self.content)
        self._logger.info("Initialised %s menu", breadcrumb)

    @property
    @abstractmethod
    def Option(self) -> type[Enum]:  # pylint: disable=invalid-name
        """
        Abstract property that must return the enum class for menu options.
        Each subclass must define its own menu options.
        """

    def rebuild(self, *args: Any, **kwargs: Any) -> None:
        """
        Rebuild the menu with new arguments and restore the previously selected
        item.
        """
        selected = self.select.state.selected
        self.reset_instance(*args, **kwargs)
        self.select.state.selected = selected

    def update(self) -> list[MenuItemBase]:
        """
        Update the menu's selection state and return visible items.
        """
        for i, item in enumerate(self.content.items.values()):
            item.selected = i == self.select.state.selected
        self._logger.debug(
            "Updated menu with selected index: %d", self.select.state.selected
        )
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

    @staticmethod
    def _generate_config_actions(
        data: dict[str, str],
        config_attr: str,
        function: Callable[[str], None] | None = None,
        default: int = 0,
        non_tsp_skip: bool = False
    ) -> tuple[list[MenuAction], int]:
        """
        Generates a list of menu actions for configuring a specific option and
        determines the current selection.
        """

        def config_func(val: str) -> None:
            AppConfig().update_value(config_attr, val)
            if function:
                logger = MenuBase.get_static_logger()
                logger.info(
                    "Executing action %s(%s)",
                    util.get_callable_name(function),
                    val
                )
                function(val)

        if (config := AppConfig().get_value(config_attr)) in data:
            default = list(data).index(config)

        actions: list[MenuAction] = MenuBase._generate_actions(
            data,
            config_func,
            non_tsp_skip
        )
        return actions, default

    @staticmethod
    def _generate_actions(
        data: dict[str, str],
        function: Callable[[str], None] | None = None,
        non_tsp_skip: bool = False
    ) -> list[MenuAction]:
        """
        Creates menu actions from the provided data mapping.
        """
        actions: list[MenuAction] = []
        for k, v in data.items():
            actions.append(
                MenuAction(
                    v,
                    None if not function else partial(function, k),
                    non_tsp_skip=non_tsp_skip
                )
            )
        return actions

    def _rebuild_menu(self, reason: str) -> None:
        """Rebuilds the menu."""
        logger = MenuBase.get_static_logger()
        logger.info("Rebuilding %s menu, reason: %s", type(self), reason)
        self.rebuild()