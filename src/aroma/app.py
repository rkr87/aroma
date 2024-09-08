"""
Main application class that manages SDL initialization, event handling, and the
application lifecycle.
"""

import logging
import sys

from sdl2 import (SDL_CONTROLLER_BUTTON_GUIDE, SDL_INIT_GAMECONTROLLER,
                  SDL_INIT_VIDEO, SDL_QUIT, SDL_Event, SDL_Init, SDL_PollEvent,
                  SDL_Quit)
from sdl2.ext import quit as ext_quit

from constants import RESOURCES
from input.controller import Controller
from model.current_menu import CurrentMenu
from navigation.navigator import Navigator
from render.screen import Screen
from render.text_generator import TextGenerator


class App:
    """
    Main application class for initializing and running the system.
    Manages the controller, rendering, and navigation between menus.
    """

    def __init__(self) -> None:
        """
        Initializes the SDL system, game controller, screen, and menu
        navigator.
        """
        super().__init__()
        if SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER) != 0:
            sys.exit(1)
        self.controller = Controller()
        text_generator = TextGenerator(f"{RESOURCES}/ui/DejaVuSans.ttf")
        self.screen = Screen(text_generator)
        self.navigator = Navigator()
        self.running = True

    def stop(self) -> None:
        """
        Cleans up resources and exits the application.
        Stops the event loop and closes SDL subsystems.
        """
        self.running = False
        self.controller.cleanup()
        ext_quit()
        SDL_Quit()
        sys.exit()

    def handle_event(self, event: SDL_Event) -> None:
        """
        Handles individual SDL events, including quitting and rendering
        updates.
        """
        logging.info("Event type: %s", event.type)
        if event.type == SDL_QUIT:
            self.stop()
            return
        if self.controller.button_press(event, SDL_CONTROLLER_BUTTON_GUIDE):
            self.stop()
            return

        menu: CurrentMenu = self.navigator.handle_events(event)
        self.screen.render_screen(menu)

    def poll_event(self) -> None:
        """
        Polls and processes SDL events continuously until the application is
        stopped.
        """
        while self.running:  # pylint: disable=while-used
            event = SDL_Event()
            if SDL_PollEvent(event):
                self.handle_event(event)

    def start(self) -> None:
        """
        Starts the application, rendering the initial screen and entering the
        event polling loop.
        """
        menu: CurrentMenu = self.navigator.handle_events()
        self.screen.render_screen(menu)
        self.poll_event()
