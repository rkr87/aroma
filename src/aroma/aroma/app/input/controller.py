"""Handles game controller input and initialization using SDL2 functions."""

from sdl2 import (
    SDL_CONTROLLERBUTTONDOWN,
    SDL_Event,
    SDL_GameController,
    SDL_GameControllerClose,
    SDL_GameControllerOpen,
    SDL_IsGameController,
    SDL_NumJoysticks,
)
from shared.classes.class_singleton import ClassSingleton


class Controller(ClassSingleton):
    """Manages game controller input and initialization."""

    def __init__(self) -> None:
        super().__init__()
        self.controller: SDL_GameController | None = None
        self._logger.debug("Initializing Controller...")
        self._init_controller()

    def _init_controller(self) -> None:
        """Initialise the controller if connected."""
        if SDL_NumJoysticks() > 0 and SDL_IsGameController(0):
            self.controller = SDL_GameControllerOpen(0)
            if self.controller:
                self._logger.info("Controller initialized successfully.")
            else:
                self._logger.warning("Failed to initialize controller.")
        else:
            self._logger.warning("No game controller detected.")

    @staticmethod
    def button_press(event: SDL_Event, button: int) -> bool:
        """Check if provided controller button is pressed."""
        is_pressed: bool = (
            event.type == SDL_CONTROLLERBUTTONDOWN
            and event.cbutton.button == button
        )
        if is_pressed:
            logger = Controller.get_static_logger()
            logger.debug("Button %d pressed.", button)
        return is_pressed

    def cleanup(self) -> None:
        """Clean up and close the controller."""
        if self.controller:
            SDL_GameControllerClose(self.controller)
            self._logger.info("Controller closed.")
        else:
            self._logger.debug("No controller to close.")
