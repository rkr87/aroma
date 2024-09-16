"""
Main application class that manages SDL initialization, event handling, and the
application lifecycle.
"""
import logging
import logging.config
import sys

from sdl2 import (SDL_CONTROLLER_BUTTON_GUIDE, SDL_INIT_GAMECONTROLLER,
                  SDL_INIT_VIDEO, SDL_QUIT, SDL_Event, SDL_Init, SDL_PollEvent,
                  SDL_Quit)
from sdl2.ext import quit as ext_quit

from app_config import AppConfig
from base.class_singleton import ClassSingleton
from constants import APP_NAME, APP_PATH
from input.controller import Controller
from model.current_menu import CurrentMenu
from navigation.nav_controller import NavController
from render.screen import Screen
from strings import Strings


class App(ClassSingleton):
    """
    Main application class for initializing and running the system.
    Manages the controller, rendering, and navigation between menus.
    """

    def __init__(self) -> None:
        """
        Initializes the SDL system, game controller, screen, and menu
        navigator.
        """
        config = AppConfig.load(f"{APP_PATH}/config.json")
        logging.config.fileConfig(
            f"{APP_PATH}/aroma/resources/config/logging.conf"
        )
        logging.getLogger().setLevel(config.logging_level)
        Strings.load(f"{APP_PATH}/translations/{config.language}.json")

        super().__init__()
        self._logger.info("Initialising %s", APP_NAME)
        if SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER) != 0:
            self._logger.error("Failed to initialize SDL")
            sys.exit(1)
        self.controller = Controller()
        self.screen = Screen()
        self.navigator = NavController()
        self.running = True
        self._logger.info("SDL and game controller initialised successfully.")

    def stop(self) -> None:
        """
        Cleans up resources and exits the application.
        Stops the event loop and closes SDL subsystems.
        """
        self._logger.info("Stopping application.")
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
        if event.type == SDL_QUIT:
            self._logger.info("SDL_QUIT event received.")
            self.stop()
            return
        if self.controller.button_press(event, SDL_CONTROLLER_BUTTON_GUIDE):
            self._logger.info("Controller guide button pressed.")
            self.stop()
            return

        menu: CurrentMenu = self.navigator.handle_events(event)
        self.screen.render_screen(menu)

    def poll_event(self) -> None:
        """
        Polls and processes SDL events continuously until the application is
        stopped.
        """
        self._logger.info("Event polling started.")
        while self.running:  # pylint: disable=while-used
            event = SDL_Event()
            if SDL_PollEvent(event):
                self.handle_event(event)
        self._logger.info("Event polling stopped.")

    def start(self) -> None:
        """
        Starts the application, rendering the initial screen and entering the
        event polling loop.
        """
        self._logger.info("Application starting.")
        menu: CurrentMenu = self.navigator.handle_events()
        self.screen.render_screen(menu)
        self.poll_event()
