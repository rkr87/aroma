"""
Defines the Navigator class, which manages navigation through multiple menus
using a stack-based approach.
"""

import sdl2

from input.controller import Controller
from model.current_menu import CurrentMenu
from model.menu_stack import MenuStack
from navigation.menu_collections import MenuCollections
from navigation.menu_main import MenuMain
from navigation.menu_new_collection import MenuNewCollection
from navigation.menu_options import MenuOptions


class Navigator:
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
        self.main: MenuMain = self._init_menus()

    def _init_menus(self) -> MenuMain:
        """
        Initializes the main menu and its submenus, returning the main menu
        instance.
        """
        return MenuMain(
            self.menu_stack,
            MenuCollections(
                self.menu_stack,
                MenuNewCollection()
            ),
            MenuOptions()
        )

    def _current_menu(self, force_update: bool = False) -> CurrentMenu:
        """
        Returns the current menu from the top of the stack. If the stack is
        empty, it pushes the main menu onto the stack and returns it.
        """
        if current := self.menu_stack.get_current(force_update):
            return current
        return self.menu_stack.push(self.main)

    def handle_events(
        self,
        event: sdl2.SDL_Event | None = None
    ) -> CurrentMenu:
        """
        Handles controller input events to navigate through menus. If the event
        is None, it returns the current menu. If the A button is pressed, it
        pops the top menu from the stack. Otherwise, it processes the input for
        the current menu and returns it.
        """
        if event is None:
            return self._current_menu(True)
        if Controller.button_press(event, sdl2.SDL_CONTROLLER_BUTTON_A):
            self.menu_stack.pop()
            return self._current_menu(True)
        current: CurrentMenu = self._current_menu()
        if not (input_received := current.menu.handle_input(event)):
            return current
        new: CurrentMenu = self._current_menu()
        new.update_required = input_received
        return new
