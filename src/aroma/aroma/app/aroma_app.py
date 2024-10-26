"""Main application class."""

import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

from app.background_worker import BackgroundWorker
from app.input.controller import Controller
from app.input.keyboard_controller import KeyboardController
from app.navigation.menu_launch_options import MenuLaunchOptions
from app.navigation.nav_controller import NavController
from app.screen_manager import ScreenManager
from app.strings import Strings
from manager.rom_manager import RomManager
from sdl2 import (
    SDL_CONTROLLER_BUTTON_GUIDE,
    SDL_INIT_GAMECONTROLLER,
    SDL_INIT_VIDEO,
    SDL_QUIT,
    SDL_Event,
    SDL_Init,
    SDL_PollEvent,
    SDL_Quit,
)
from sdl2.ext import quit as ext_quit
from shared import constants
from shared.app_config import AppConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import APP_NAME

if TYPE_CHECKING:
    from app.model.current_menu import CurrentMenu


class AromaApp(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """Main application class for initialising and running the system."""

    def __init__(self) -> None:
        Strings().load(
            constants.APP_TRANSLATION_PATH / f"{AppConfig().language}.json",
            constants.APP_TRANSLATION_PATH / "english.json",
        )
        super().__init__()

        self._logger.info("Initialising %s", APP_NAME)
        if SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER) != 0:
            self._logger.error("Failed to initialize SDL")
            sys.exit(1)
        self.controller = Controller()
        self.screen = ScreenManager()
        self.navigator = NavController()
        self.keyboard = KeyboardController()
        self.running = True
        self._logger.info("SDL and game controller initialised successfully.")

    def stop(self) -> None:
        """Clean up resources and exits the application."""
        self._logger.info("Stopping application.")
        self.running = False
        RomManager().cleanup()
        self.controller.cleanup()
        ext_quit()
        SDL_Quit()
        sys.exit()

    def handle_event(self, event: SDL_Event) -> None:
        """Handle individual SDL events."""
        if event.type == SDL_QUIT:
            self._logger.info("SDL_QUIT event received.")
            self.stop()
            return
        if self.controller.button_press(event, SDL_CONTROLLER_BUTTON_GUIDE):
            self._logger.info("Controller guide button pressed.")
            self.stop()
            return

        if self.keyboard.is_open:
            req_update = self.keyboard.handle_events(event)
            menu: CurrentMenu = self.navigator.current_menu(
                force_update=req_update
            )
            self.screen.render(menu, self.keyboard.get_current_button()[0])
        else:
            menu = self.navigator.handle_events(event)
            self.screen.render(menu)

    def _check_worker(self) -> None:
        """TODO."""
        if not BackgroundWorker().busy:
            return
        while BackgroundWorker().busy:  # pylint: disable=while-used
            time.sleep(0.01)
        menu = self.navigator.current_menu(force_update=True)
        self.screen.render(menu)

    def poll_event(self) -> None:
        """Poll and process SDL events."""
        self._logger.info("Event polling started.")
        while self.running:  # pylint: disable=while-used
            self._check_worker()
            event = SDL_Event()
            if SDL_PollEvent(event):
                self.handle_event(event)
        self._logger.info("Event polling stopped.")

    def start_main(self) -> None:
        """Start the application."""
        self._logger.info("Application starting.")
        menu: CurrentMenu = self.navigator.current_menu()
        self.screen.render(menu)
        self.poll_event()

    def start_launch_menu(self, shortcut_path: Path) -> None:
        """TODO."""
        self._logger.info("Application starting.")
        shortcut_menu = MenuLaunchOptions()
        shortcut_menu.init_dynamic_menu(
            f"LAUNCHING {shortcut_path.stem.upper()}", shortcut_path, None
        )
        menu: CurrentMenu = self.navigator.current_menu(
            start_menu=shortcut_menu
        )
        self.screen.render(menu)
        self.poll_event()
