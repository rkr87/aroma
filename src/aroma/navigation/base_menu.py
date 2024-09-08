"""
Defines a Menu class for managing menu items, cycling through options, and
handling user input using a game controller.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto

from sdl2 import (SDL_CONTROLLER_BUTTON_B, SDL_CONTROLLER_BUTTON_DPAD_DOWN,
                  SDL_CONTROLLER_BUTTON_DPAD_LEFT,
                  SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
                  SDL_CONTROLLER_BUTTON_DPAD_UP,
                  SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
                  SDL_CONTROLLER_BUTTON_RIGHTSHOULDER, SDL_Event)

from input.controller import Controller
from model.menu_action import MenuAction
from model.menu_item import MenuItem
from util import clamp

MAX_ITEMS_PER_PAGE = 12


class _MenuPos(Enum):
    """
    Enum to represent the position of the menu (bottom or top) relative to
    the visible page.
    """
    BOTTOM = auto()
    TOP = auto()


class BaseMenu:
    """
    Manages menu items, their selection, and input navigation.
    """
    @dataclass
    class _MenuState:  # pylint: disable=too-many-instance-attributes
        """
        Holds metadata about the menu state including pagination and selection.
        """
        total: int = 0
        max: int = 0
        selected: int = 0
        pos: _MenuPos = _MenuPos.BOTTOM
        start: int = 0

        @property
        def end(self) -> int:
            """
            Computes the end of the visible slice based on the start and max
            values.
            """
            return self.start + self.max

        @property
        def clamp(self) -> int:
            """
            Computes the maximum valid start index for pagination.
            """
            return self.total - self.max

        @property
        def slice_eq_max_clamp(self) -> bool:
            """
            Checks if the start of the slice is equal to the maximum clamp
            value.
            """
            return self.start == self.clamp

        @property
        def selected_in_slice(self) -> bool:
            """
            Checks if the currently selected index is within the visible slice.
            """
            return self.start <= self.selected < self.end

        @property
        def selected_gt_slice_start(self) -> bool:
            """
            Checks if the selected index is greater than the start of the
            slice.
            """
            return self.selected > self.start

        @property
        def selected_gte_slice_end(self) -> bool:
            """
            Checks if the selected index is greater than or equal to the end of
            the slice.
            """
            return self.selected >= self.end

        @property
        def pagination_required(self) -> bool:
            """
            Checks if pagination is needed based on the total number of items.
            """
            return self.total > self.max

        def update_items(self, item_count: int) -> None:
            """
            Updates the metadata based on the total number of items.
            """
            self.total = item_count
            self.max = min(item_count, MAX_ITEMS_PER_PAGE)

    def __init__(
        self,
        breadcrumb: str,
        items: list[MenuItem] | None = None
    ) -> None:
        """
        Initializes the menu with a breadcrumb title and optional menu items.
        """
        super().__init__()
        self.breadcrumb: str = breadcrumb
        self.items: list[MenuItem] = items or []
        self.meta = self._MenuState(len(self.items))

    def get_breadcrumb(self) -> str:
        """
        Returns the breadcrumb (title) of the menu.
        """
        return self.breadcrumb

    def add_item(
        self,
        actions: list[MenuAction]
    ) -> None:
        """Add a new menu item."""
        menu_item = MenuItem(actions)
        self.items.append(menu_item)
        self.meta.update_items(len(self.items))

    def remove_item(self, index: int) -> None:
        """Remove a menu item by index."""
        if 0 <= index < len(self.items):
            del self.items[index]
            self.meta.selected = min(
                self.meta.selected,
                len(self.items) - 1
            )
        self.meta.update_items(len(self.items))

    def update_item(
        self,
        index: int,
        actions: list[MenuAction]
    ) -> None:
        """Update an existing menu item."""
        if 0 <= index < len(self.items):
            self.items[index] = MenuItem(actions)

    def clear_items(self) -> None:
        """Clear all menu items."""
        self.items.clear()
        self.meta.selected = 0
        self.meta.update_items(len(self.items))

    def _cycle_items(self, records: int, recycle: bool = True) -> None:
        """Cycles through menu options, changing the selected option."""
        total_items: int = len(self.items)
        new_index: int = self.meta.selected + records

        if recycle:
            self.meta.selected = new_index % total_items
            return

        if self.meta.selected_gt_slice_start and records < 0:
            self.meta.selected = self.meta.start
            return

        if self.meta.slice_eq_max_clamp and records > 0:
            self.meta.selected = total_items - 1
            return

        self.meta.start = clamp(new_index, 0, self.meta.clamp)
        if (not self.meta.selected_in_slice or records < 0):
            self.meta.selected = self.meta.start

    def _cycle_actions(self, records: int) -> None:
        """Cycles through actions for the selected menu item."""
        item: MenuItem = self.items[self.meta.selected]
        item.action_index = (item.action_index + records) % len(item.actions)
        if len(item.actions) > 1:
            self._perform_action()

    def _next_page(self) -> None:
        """Cycles to the next menu page."""
        self._cycle_items(self.meta.max, False)
        self.meta.pos = _MenuPos.TOP

    def _prev_page(self) -> None:
        """Cycles to the previous menu page."""
        self._cycle_items(-self.meta.max, False)
        self.meta.pos = _MenuPos.TOP

    def _next_item(self) -> None:
        """Cycles to the next menu item."""
        self._cycle_items(1)
        self.meta.pos = _MenuPos.BOTTOM

    def _prev_item(self) -> None:
        """Cycles to the previous menu item."""
        self._cycle_items(-1)
        self.meta.pos = _MenuPos.TOP

    def _next_item_action(self) -> None:
        """Cycles to the next action for the selected menu item."""
        self._cycle_actions(1)

    def _prev_item_action(self) -> None:
        """Cycles to the previous action for the selected menu item."""
        self._cycle_actions(-1)

    def _perform_action(self) -> None:
        """Executes the currently selected action."""
        item: MenuItem = self.items[self.meta.selected]
        if action := item.actions[item.action_index].action:
            action()

    def handle_input(self, event: SDL_Event) -> None:
        """Handle input events for this menu."""
        button_actions: dict[int, Callable[..., None]] = {
            SDL_CONTROLLER_BUTTON_DPAD_DOWN: self._next_item,
            SDL_CONTROLLER_BUTTON_DPAD_UP: self._prev_item,
            SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: self._next_page,
            SDL_CONTROLLER_BUTTON_LEFTSHOULDER: self._prev_page,
            SDL_CONTROLLER_BUTTON_DPAD_RIGHT: self._next_item_action,
            SDL_CONTROLLER_BUTTON_DPAD_LEFT: self._prev_item_action,
            SDL_CONTROLLER_BUTTON_B: self._perform_action
        }
        for button, action in button_actions.items():
            if Controller.button_press(event, button):
                action()
                return

    def _get_slice(self) -> list[MenuItem]:
        """
        Returns the current slice of menu items for rendering.
        """
        if not self.meta.pagination_required:
            return self.items

        if (
            self.meta.pos == _MenuPos.BOTTOM and
            self.meta.selected >= self.meta.end
        ):
            self.meta.start = self.meta.selected - self.meta.max + 1

        elif (
            self.meta.selected < self.meta.start or
            self.meta.selected >= self.meta.end
        ):
            self.meta.start = self.meta.selected

        self.meta.start = min(self.meta.start, self.meta.total - self.meta.max)
        return self.items[self.meta.start:self.meta.end]

    def update(self) -> list[MenuItem]:
        """
        Update the selection state of menu items and return renderable items.
        """
        for i, option in enumerate(self.items):
            option.selected = i == self.meta.selected
        return self._get_slice()
