"""
Defines the Navigator class, which manages navigation through multiple menus
using a stack-based approach.
"""
from functools import partial

import sdl2

from input.controller import Controller
from model.current_menu import CurrentMenu
from model.menu_action import MenuAction
from model.menu_stack import MenuStack
from navigation.menu import Menu


class Navigator:
    """
    Manages the navigation between different menus in the application.
    """

    def __init__(self) -> None:
        """
        Initializes the Navigator with menus and sets up the main menu.
        """
        super().__init__()
        self.menu_stack: MenuStack = MenuStack()
        self.menus: dict[str, Menu] = self._init_menus()

    def _init_menus(self) -> dict[str, Menu]:
        """
        Initializes and returns a dictionary of menus used in the application.
        """
        new_collection: Menu = self._build_menu_new_collection()
        collections: Menu = self._build_menu_collections(new_collection)
        options: Menu = self._build_menu_options()
        main: Menu = self._build_menu_main(collections, options)
        return {
            "new_collection": new_collection,
            "collections": collections,
            "options": options,
            "main": main
        }

    def _build_menu_new_collection(self) -> Menu:
        """
        Builds and returns the "New Collection" menu.
        """
        menu: Menu = Menu("New Collection")
        menu.add_item([MenuAction("< Custom >", None)])
        menu.add_item([MenuAction("Add All Templates", None)])
        menu.add_item([MenuAction("TEMPLATE: Collection One", None)])
        menu.add_item([MenuAction("TEMPLATE: Collection Two", None)])
        return menu

    def _build_menu_collections(self, new_collection_menu: Menu) -> Menu:
        """
        Builds and returns the "Collections" menu.
        """
        menu: Menu = Menu("Collections")
        menu.add_item([
            MenuAction(
                "< Add New >",
                partial(self.menu_stack.push, new_collection_menu)
            )
        ])
        menu.add_item([MenuAction("Existing Collection One", None)])
        menu.add_item([MenuAction("Existing Collection Two", None)])
        return menu

    def _build_menu_options(self) -> Menu:
        """
        Builds and returns the "Options" menu.
        """
        menu: Menu = Menu("Options")
        menu.add_item([
            MenuAction("Option One", None),
            MenuAction("Option Two", None),
            MenuAction("Option Three", None),
            MenuAction("Option Four", None),
        ])
        return menu

    def _build_menu_main(
        self,
        collections_menu: Menu,
        options_menu: Menu
    ) -> Menu:
        """
        Builds and returns the main menu.
        """
        menu: Menu = Menu("aROMa")
        menu.add_item([
            MenuAction("Collections",
                       partial(self.menu_stack.push, collections_menu))
        ])
        menu.add_item([MenuAction("UI Tweaks", None)])
        menu.add_item([
            MenuAction("Options", partial(self.menu_stack.push, options_menu))
        ])
        return menu

    def _current_menu(self) -> CurrentMenu:
        """
        Returns the current menu from the top of the stack, or navigates to the
        main menu if the stack is empty.
        """
        if current := self.menu_stack.get_current():
            return current
        return self.menu_stack.push(self.menus['main'])

    def handle_events(
        self,
        event: sdl2.SDL_Event | None = None
    ) -> CurrentMenu:
        """
        Handles controller input events, navigates through menus, and returns
        the current menu.
        """
        if event is None:
            return self._current_menu()
        if Controller.button_press(event, sdl2.SDL_CONTROLLER_BUTTON_A):
            self.menu_stack.pop()
            return self._current_menu()
        current: CurrentMenu = self._current_menu()
        current.menu.handle_input(event)
        return current
