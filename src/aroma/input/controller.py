"""
Handles game controller input and initialization using SDL2 functions.
"""
from sdl2 import (SDL_CONTROLLERBUTTONDOWN, SDL_Event, SDL_GameController,
                  SDL_GameControllerClose, SDL_GameControllerOpen,
                  SDL_IsGameController, SDL_NumJoysticks)


class Controller:
    """
    Manages game controller input and initialization.
    """

    def __init__(self) -> None:
        """
        Initializes the Controller class and attempts to connect to a game
        controller.
        """
        super().__init__()
        self.controller: SDL_GameController | None = None
        self._init_controller()

    def _init_controller(self) -> None:
        """
        Initializes the controller if one is connected.
        """
        if SDL_NumJoysticks() > 0 and SDL_IsGameController(0):
            self.controller = SDL_GameControllerOpen(0)

    @staticmethod
    def button_press(event: SDL_Event, button: int) -> bool:
        """
        Checks if a specific controller button is pressed.
        """
        return event.type == SDL_CONTROLLERBUTTONDOWN and \
            event.cbutton.button == button

    def cleanup(self) -> None:
        """
        Cleans up and closes the controller when finished.
        """
        if self.controller:
            SDL_GameControllerClose(self.controller)
