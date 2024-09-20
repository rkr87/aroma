"""
Defines the Navigator class, which manages navigation through multiple menus
using a stack-based approach.
"""

from collections.abc import Callable

from sdl2 import (SDL_CONTROLLER_BUTTON_A, SDL_CONTROLLER_BUTTON_B,
                  SDL_CONTROLLER_BUTTON_DPAD_DOWN,
                  SDL_CONTROLLER_BUTTON_DPAD_LEFT,
                  SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
                  SDL_CONTROLLER_BUTTON_DPAD_UP,
                  SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
                  SDL_CONTROLLER_BUTTON_RIGHTSHOULDER, SDL_Event)

from app.input.controller import Controller
from app.navigation.menu_main import MenuMain
from app.navigation.menu_stack import MenuStack
from classes.base.class_singleton import ClassSingleton
from model.current_menu import CurrentMenu


class NavController(ClassSingleton):
    """
    Manages the navigation between different menus in the application using a
    stack-based approach.
    """

    def __init__(self) -> None:
        """
        Initializes the Navigator with an empty menu stack and sets up the main
        menu and its associated submenus.
        """
        super().__init__()
        self.menu_stack: MenuStack = MenuStack()
        self.main: MenuMain = MenuMain()
        self._logger.debug("NavController initialized with main menu")

    def _current_menu(self, force_update: bool = False) -> CurrentMenu:
        """
        Returns the current menu from the top of the stack. If the stack is
        empty, it pushes the main menu onto the stack and returns it.
        """
        if current := self.menu_stack.get_current(force_update):
            return current
        self._logger.info("Menu stack is empty, pushing main menu")
        return self.menu_stack.push(self.main)

    def handle_events(
        self,
        event: SDL_Event | None = None
    ) -> CurrentMenu:
        """
        Handles controller input events to navigate through menus. If the event
        is None, it returns the current menu. If the A button is pressed, it
        pops the top menu from the stack. Otherwise, it processes the input for
        the current menu and returns it.
        """
        if event is None:
            self._logger.debug("No event passed, updating current menu")
            return self._current_menu(True)

        if Controller.button_press(event, SDL_CONTROLLER_BUTTON_A):
            self._logger.debug("A button pressed, popping menu")
            self.menu_stack.pop()
            return self._current_menu(True)

        current: CurrentMenu = self._current_menu()
        button_actions: dict[int, Callable[..., None]] = {
            SDL_CONTROLLER_BUTTON_DPAD_DOWN: current.menu.select.next_item,
            SDL_CONTROLLER_BUTTON_DPAD_UP: current.menu.select.prev_item,
            SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: current.menu.select.next_page,
            SDL_CONTROLLER_BUTTON_LEFTSHOULDER: current.menu.select.prev_page,
            SDL_CONTROLLER_BUTTON_DPAD_RIGHT: current.menu.action.run_next,
            SDL_CONTROLLER_BUTTON_DPAD_LEFT: current.menu.action.run_prev,
            SDL_CONTROLLER_BUTTON_B: current.menu.action.run_selected
        }

        for button, action in button_actions.items():
            if Controller.button_press(event, button):
                self._logger.debug(
                    "Button %s pressed, executing action", button
                )
                action()
                return self._current_menu(True)
        return current
