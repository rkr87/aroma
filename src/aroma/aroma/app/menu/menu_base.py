"""Defines a Menu class for managing menu items."""

from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any, TypeVar, cast

from app.input.keyboard import Keyboard
from app.menu.action_manager import ActionManager
from app.menu.content_manager import ContentManager
from app.menu.menu_action import MenuAction
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_single import MenuItemSingle
from app.menu.selection_manager import SelectionManager
from app.model.side_pane import SidePane
from shared.app_config import AppConfig
from shared.classes.class_singleton import ClassSingleton
from shared.tools import util

_T = TypeVar("_T", str, int, bool)


class MenuBase(ClassSingleton, ABC):
    """Base class for managing menu items, navigation, and user actions."""

    def __init__(
        self,
        breadcrumb: str,
        items: OrderedDict[str, MenuItemBase],
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

    def reset_menu(self) -> None:
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
        *,
        side_pane: SidePane | None = None,
    ) -> MenuItemSingle:
        """Create a menu item that pushes a submenu onto the menu stack."""
        return MenuItemSingle(
            menu.breadcrumb,
            partial(stack_push, menu),
            side_pane=side_pane,
        )

    @staticmethod  # type: ignore[misc]
    def dynamic_sub_menu(  # pylint: disable=too-many-arguments  # noqa: PLR0913
        text: str,
        path: Path | None,
        identifier: str | None,
        menu: "MenuBase",
        stack_push: Callable[["MenuBase"], Any],
        *,
        side_pane: SidePane | None = None,
    ) -> MenuItemSingle:
        """Create a menu item that pushes a submenu onto the menu stack."""

        def rebuild_and_push() -> None:
            """TODO."""
            menu.build_dynamic_menu(text, path, identifier)
            stack_push(menu)

        return MenuItemSingle(
            text,
            rebuild_and_push,
            side_pane=side_pane,
        )

    def _generate_keyboard_config_item(
        self,
        config_attr: str,
        label: str,
        desc: list[str],
        prompt: str,
    ) -> MenuItemSingle:
        """TODO."""
        current_val = str(AppConfig().get_value(config_attr))

        def update_config(value: str) -> None:
            AppConfig().update_value(config_attr, value)
            self.reset_menu()

        def get_user_input() -> None:
            Keyboard().open(
                prompt.upper(),
                update_config,
                current_val,
            )

        return MenuItemSingle(
            label.upper(),
            get_user_input,
            SidePane(
                label.upper(),
                [f"CURRENT: {current_val or 'NOT SET'}", *desc],
            ),
        )

    @staticmethod
    def _generate_config_actions(
        data: dict[_T, str] | dict[_T, tuple[str, SidePane]],
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
        data: dict[_T, str] | dict[_T, tuple[str, SidePane]],
        function: Callable[[_T], None] | None = None,
        *,
        non_tsp_skip: bool = False,
    ) -> list[MenuAction]:
        """Create menu actions from the provided data mapping."""
        actions: list[MenuAction] = []
        for k, v in data.items():
            if isinstance(v, tuple):
                text = v[0]
                sidepane = v[1]
            else:
                text = v
                sidepane = None
            actions.append(
                MenuAction(
                    text,
                    None if not function else partial(function, k),
                    non_tsp_skip=non_tsp_skip,
                    side_pane=sidepane,
                ),
            )
        return actions

    def _reset_menu_action(self, reason: str) -> None:
        """Rebuilds the menu."""
        logger = MenuBase.get_static_logger()
        logger.info("Rebuilding %s menu, reason: %s", type(self), reason)
        self.reset_menu()

    @abstractmethod
    def build_dynamic_menu(
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        """TODO."""
