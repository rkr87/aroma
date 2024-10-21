"""Defines the Navigator class, which manages menu navigation."""

from typing import TYPE_CHECKING

from app.input.controller import Controller
from app.menu.menu_base import MenuBase
from app.model.current_menu import CurrentMenu
from app.navigation.menu_main import MenuMain
from app.navigation.menu_stack import MenuStack
from sdl2 import (
    SDL_CONTROLLER_BUTTON_A,
    SDL_CONTROLLER_BUTTON_B,
    SDL_CONTROLLER_BUTTON_DPAD_DOWN,
    SDL_CONTROLLER_BUTTON_DPAD_LEFT,
    SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
    SDL_CONTROLLER_BUTTON_DPAD_UP,
    SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
    SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
    SDL_Event,
)
from shared.classes.class_singleton import ClassSingleton

if TYPE_CHECKING:
    from collections.abc import Callable


class NavController(ClassSingleton):
    """Manages the navigation between different menus in the application."""

    def __init__(self) -> None:
        super().__init__()
        self.menu_stack: MenuStack = MenuStack()
        self._logger.debug("NavController initialized with main menu")

    def current_menu(
        self, *, force_update: bool = False, start_menu: MenuBase | None = None
    ) -> CurrentMenu:
        """Return the current menu from the top of the stack."""
        if current := self.menu_stack.get_current(
            update_required=force_update,
        ):
            return current
        self._logger.info("Menu stack is empty, pushing start menu")
        if not start_menu:
            start_menu = MenuMain()
        return self.menu_stack.push(start_menu)

    def handle_events(
        self,
        event: SDL_Event,
    ) -> CurrentMenu:
        """Handle controller input events to navigate through menus."""
        if Controller.button_press(event, SDL_CONTROLLER_BUTTON_A):
            self._logger.debug("A button pressed, popping menu")
            self.menu_stack.pop()
            return self.current_menu(force_update=True)

        current: CurrentMenu = self.current_menu()
        button_actions: dict[int, Callable[..., None]] = {
            SDL_CONTROLLER_BUTTON_DPAD_DOWN: current.menu.select.next_item,
            SDL_CONTROLLER_BUTTON_DPAD_UP: current.menu.select.prev_item,
            SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: current.menu.select.next_page,
            SDL_CONTROLLER_BUTTON_LEFTSHOULDER: current.menu.select.prev_page,
            SDL_CONTROLLER_BUTTON_DPAD_RIGHT: current.menu.action.run_next,
            SDL_CONTROLLER_BUTTON_DPAD_LEFT: current.menu.action.run_prev,
            SDL_CONTROLLER_BUTTON_B: current.menu.action.run_selected,
        }

        for button, action in button_actions.items():
            if Controller.button_press(event, button):
                self._logger.debug(
                    "Button %s pressed, executing action",
                    button,
                )
                action()
                return self.current_menu(force_update=True)
        return current
