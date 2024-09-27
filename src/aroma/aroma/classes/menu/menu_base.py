"""Defines a Menu class for managing menu items."""

from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import Callable
from enum import Enum
from functools import partial
from typing import Any, TypeVar, cast

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

_T = TypeVar("_T", str, int, bool)


class MenuBase(ClassSingleton, ABC):
    """Base class for managing menu items, navigation, and user actions."""

    def __init__(
        self,
        breadcrumb: str,
        items: OrderedDict[Enum, MenuItemBase],
        side_pane: SidePane | None = None,
    ) -> None:
        super().__init__()
        self.breadcrumb: str = breadcrumb
        self.select: SelectionManager = SelectionManager(len(items))
        self.content: ContentManager = ContentManager(
            items,
            self.select,
            side_pane,
        )
        self.action: ActionManager = ActionManager(self.select, self.content)
        self._logger.info("Initialised %s menu", breadcrumb)

    @property
    @abstractmethod
    def option(self) -> type[Enum]:  # pylint: disable=invalid-name
        """Abstract property that returns the enum class for menu options."""

    def rebuild(self) -> None:
        """Rebuild the menu and restore the previously selected item."""
        selected = self.select.state.selected
        self.reset_instance()
        self.select.state.selected = selected

    def update(self) -> list[MenuItemBase]:
        """Update the menu's selection state and return visible items."""
        for i, item in enumerate(self.content.items.values()):
            item.selected = i == self.select.state.selected
        self._logger.debug(
            "Updated menu with selected index: %d",
            self.select.state.selected,
        )
        return self.content.get_slice()

    @staticmethod  # type: ignore[misc]
    def sub_menu(
        menu: "MenuBase",
        stack_push: Callable[["MenuBase"], Any],
        side_pane: SidePane | None = None,
    ) -> MenuItemSingle:
        """Create a menu item that pushes a submenu onto the menu stack."""
        return MenuItemSingle(
            menu.breadcrumb,
            partial(stack_push, menu),
            side_pane=side_pane,
        )

    @staticmethod
    def _generate_config_actions(
        data: dict[_T, str],
        config_attr: str,
        function: Callable[[_T], None] | None = None,
        default: int = 0,
        *,
        non_tsp_skip: bool = False,
    ) -> tuple[list[MenuAction], int]:
        """Generate a menu actions for configuring a specific option."""

        def config_func(val: _T) -> None:
            AppConfig().update_value(config_attr, val)
            if function:
                logger = MenuBase.get_static_logger()
                logger.info(
                    "Executing action %s(%s)",
                    util.get_callable_name(function),
                    val,
                )
                function(val)

        if (config := cast(_T, AppConfig().get_value(config_attr))) in data:
            options: list[_T] = list(data.keys())
            default = options.index(config)

        actions: list[MenuAction] = MenuBase._generate_actions(
            data,
            config_func,
            non_tsp_skip=non_tsp_skip,
        )
        return actions, default

    @staticmethod
    def _generate_actions(
        data: dict[_T, str],
        function: Callable[[_T], None] | None = None,
        *,
        non_tsp_skip: bool = False,
    ) -> list[MenuAction]:
        """Create menu actions from the provided data mapping."""
        actions: list[MenuAction] = []
        for k, v in data.items():
            actions.append(
                MenuAction(
                    v,
                    None if not function else partial(function, k),
                    non_tsp_skip=non_tsp_skip,
                ),
            )
        return actions

    def _rebuild_menu(self, reason: str) -> None:
        """Rebuilds the menu."""
        logger = MenuBase.get_static_logger()
        logger.info("Rebuilding %s menu, reason: %s", type(self), reason)
        self.rebuild()
