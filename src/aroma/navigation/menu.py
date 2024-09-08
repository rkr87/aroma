"""
Defines a Menu class for managing menu items, cycling through options, and
handling user input using a game controller.
"""

from collections.abc import Callable

from sdl2 import (SDL_CONTROLLER_BUTTON_B, SDL_CONTROLLER_BUTTON_DPAD_DOWN,
                  SDL_CONTROLLER_BUTTON_DPAD_LEFT,
                  SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
                  SDL_CONTROLLER_BUTTON_DPAD_UP, SDL_Event)

from input.controller import Controller
from navigation.menu_item import MenuAction, MenuItem


class Menu:
    """
    Manages menu items, their selection, and input navigation.
    """

    def __init__(
        self,
        breadcrumb: str,
        options: list[MenuItem] | None = None
    ) -> None:
        """
        Initializes the menu with a breadcrumb title and optional menu items.
        """
        super().__init__()
        self.breadcrumb: str = breadcrumb
        self.options: list[MenuItem] = options or []
        self.selected_index = 0

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
        self.options.append(menu_item)

    def remove_item(self, index: int) -> None:
        """Remove a menu item by index."""
        if 0 <= index < len(self.options):
            del self.options[index]
            self.selected_index = min(
                self.selected_index,
                len(self.options) - 1
            )

    def update_item(
        self,
        index: int,
        actions: list[MenuAction]
    ) -> None:
        """Update an existing menu item."""
        if 0 <= index < len(self.options):
            self.options[index] = MenuItem(actions)

    def clear_items(self) -> None:
        """Clear all menu items."""
        self.options.clear()
        self.selected_index = 0

    def _cycle_items(self, negative: bool = False) -> None:
        """Cycles through menu options, changing the selected option."""
        val: int = -1 if negative else 1
        self.selected_index = (self.selected_index + val) % len(self.options)

    def _cycle_actions(self, negative: bool = False) -> None:
        """Cycles through actions for the selected menu item."""
        item = self.options[self.selected_index]
        val: int = -1 if negative else 1
        item.action_index = (item.action_index + val) % len(item.actions)
        if len(item.actions) > 1:
            self._perform_action()

    def _cycle_items_down(self) -> None:
        """Cycles to the previous menu option."""
        self._cycle_items(True)

    def _cycle_action_down(self) -> None:
        """Cycles to the previous action for the selected menu item."""
        self._cycle_actions(True)

    def _perform_action(self) -> None:
        """Executes the currently selected action."""
        item: MenuItem = self.options[self.selected_index]
        if action := item.actions[item.action_index].action:
            action()

    def handle_input(self, event: SDL_Event) -> None:
        """Handle input events for this menu."""
        button_actions: dict[int, Callable[..., None]] = {
            SDL_CONTROLLER_BUTTON_DPAD_DOWN: self._cycle_items,
            SDL_CONTROLLER_BUTTON_DPAD_UP: self._cycle_items_down,
            SDL_CONTROLLER_BUTTON_DPAD_RIGHT: self._cycle_actions,
            SDL_CONTROLLER_BUTTON_DPAD_LEFT: self._cycle_action_down,
            SDL_CONTROLLER_BUTTON_B: self._perform_action
        }
        for button, action in button_actions.items():
            if Controller.button_press(event, button):
                action()
                return

    def update(self) -> list[MenuItem]:
        """Update the selection state of menu items."""
        for i, option in enumerate(self.options):
            option.selected = i == self.selected_index
        return self.options
