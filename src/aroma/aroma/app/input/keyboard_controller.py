"""TODO."""

from typing import TYPE_CHECKING

from app.input.controller import Controller
from app.input.keyboard import Keyboard
from app.model.keyboard_button import KeyboardButton
from sdl2 import (
    SDL_CONTROLLER_BUTTON_A,
    SDL_CONTROLLER_BUTTON_B,
    SDL_CONTROLLER_BUTTON_DPAD_DOWN,
    SDL_CONTROLLER_BUTTON_DPAD_LEFT,
    SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
    SDL_CONTROLLER_BUTTON_DPAD_UP,
    SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
    SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
    SDL_CONTROLLER_BUTTON_START,
    SDL_CONTROLLER_BUTTON_X,
    SDL_CONTROLLER_BUTTON_Y,
    SDL_CONTROLLERBUTTONDOWN,
    SDL_Event,
)
from shared.classes.class_singleton import ClassSingleton

if TYPE_CHECKING:
    from collections.abc import Callable


class KeyboardController(ClassSingleton):
    """Handles input from the controller for the virtual keyboard."""

    def __init__(self) -> None:
        super().__init__()
        self.keyboard = Keyboard()
        self.selected_row = 0
        self.selected_col = 0

    @property
    def is_open(self) -> bool:
        """TODO."""
        return self.keyboard.is_open

    def handle_events(self, event: SDL_Event | None = None) -> bool:
        """Handle SDL events and map them to keyboard actions."""
        if not event:
            return False
        if event.type == SDL_CONTROLLERBUTTONDOWN:
            self._handle_button_down(event)
            return True

        if self.keyboard.update_req:
            self.keyboard.update_req = False
            return True
        return False

    def _nav_horizontal(self, offset: int) -> None:
        """TODO."""
        keys = self.keyboard.available_keys()[self.selected_row]
        max_col = sum(x.weight for x in keys)
        current = self.get_current_button()
        self.selected_col = (
            current[1] + current[0].weight if offset > 0 else current[1] - 1
        ) % max_col

    def _nav_left(self) -> None:
        """TODO."""
        self._nav_horizontal(-1)

    def _nav_right(self) -> None:
        """TODO."""
        self._nav_horizontal(1)

    def _nav_vertical(self, offset: int) -> None:
        """TODO."""
        self.selected_row = (self.selected_row + offset) % len(
            self.keyboard.available_keys()
        )

    def _nav_down(self) -> None:
        """TODO."""
        self._nav_vertical(1)

    def _nav_up(self) -> None:
        """TODO."""
        self._nav_vertical(-1)

    def _handle_button_down(self, button_event: SDL_Event) -> None:
        """Handle button presses."""
        button_actions: dict[int, Callable[..., None]] = {
            SDL_CONTROLLER_BUTTON_DPAD_DOWN: self._nav_down,
            SDL_CONTROLLER_BUTTON_DPAD_UP: self._nav_up,
            SDL_CONTROLLER_BUTTON_DPAD_RIGHT: self._nav_right,
            SDL_CONTROLLER_BUTTON_DPAD_LEFT: self._nav_left,
            SDL_CONTROLLER_BUTTON_LEFTSHOULDER: self.keyboard.toggle_shift,
            SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: self.keyboard.toggle_capslock,
            SDL_CONTROLLER_BUTTON_A: self.keyboard.close,
            SDL_CONTROLLER_BUTTON_B: self._select_key,
            SDL_CONTROLLER_BUTTON_X: self.keyboard.backspace,
            SDL_CONTROLLER_BUTTON_Y: self.keyboard.space,
            SDL_CONTROLLER_BUTTON_START: self.keyboard.submit,
        }
        for button, action in button_actions.items():
            if Controller.button_press(button_event, button):
                action()

    def _select_key(self) -> None:
        """Select the currently highlighted key."""
        self.keyboard.handle_key(self.get_current_button()[0])

    def get_current_button(self) -> tuple[KeyboardButton, int]:
        """TODO."""
        buttons = self.keyboard.available_keys()[self.selected_row]
        col = 0
        default = buttons[0]
        for button in buttons:
            if col <= self.selected_col < col + button.weight:
                default = button
                break
            col += button.weight
        return default, col
