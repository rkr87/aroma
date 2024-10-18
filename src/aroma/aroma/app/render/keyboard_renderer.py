"""TODO."""

from app.input.keyboard import Keyboard
from app.model.keyboard_button import KeyboardButton
from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_BLENDMODE_BLEND,
    SDL_Rect,
    SDL_RenderFillRect,
    SDL_SetRenderDrawBlendMode,
    SDL_SetRenderDrawColor,
)
from sdl2.ext import Renderer, load_image
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    BG_COLOR,
    PRIMARY_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SECONDARY_COLOR,
)
from shared.tools import util

_BUTTON_SIZE: int = 80
_BUTTON_SPACING: int = 5
_INPUT_BOX_PADDING: int = 10


class KeyboardRenderer(ClassSingleton):
    """Handles rendering of the virtual keyboard."""

    @staticmethod
    def _calculate_keyboard_size() -> tuple[int, int]:
        """Calculate the total width and height of the keyboard."""
        rows = Keyboard().available_keys()
        total_height = (
            len(rows) * (_BUTTON_SIZE + _BUTTON_SPACING) - _BUTTON_SPACING
        )
        total_width = max(
            sum(key.weight * _BUTTON_SIZE + _BUTTON_SPACING for key in row)
            - _BUTTON_SPACING
            for row in rows
        )

        return total_width, total_height

    @staticmethod
    def _draw_button(
        renderer: Renderer,
        xy_pos: tuple[int, int],
        button: KeyboardButton,
        *,
        highlight: bool,
    ) -> int:
        """Draw a button with text centered and an optional highlight."""
        width = _BUTTON_SIZE * button.weight + _BUTTON_SPACING * (
            button.weight - 1
        )
        bg_color = (
            util.tuple_to_sdl_color(BG_COLOR)
            if not highlight and not button.toggled
            else util.tuple_to_sdl_color(SECONDARY_COLOR)
        )
        renderer.fill((xy_pos[0], xy_pos[1], width, _BUTTON_SIZE), bg_color)

        renderer.draw_rect(
            (xy_pos[0], xy_pos[1], width, _BUTTON_SIZE),
            util.tuple_to_sdl_color(PRIMARY_COLOR),
        )
        if not (surface := TextGenerator().get_text(button.key)):
            return 0
        text_pos: tuple[int, int] = (
            xy_pos[0] + (width - surface.w) // 2,
            xy_pos[1] + (_BUTTON_SIZE - surface.h) // 2,
        )
        if button.hint_img and (img := load_image(button.hint_img)):
            x_offset = img.w // 2 + _BUTTON_SPACING
            SDLHelpers.render_surface(
                renderer,
                img,
                text_pos[0] - x_offset,
                text_pos[1] - (img.h - surface.h) // 2,
            )
            text_pos = text_pos[0] + x_offset, text_pos[1]

        SDLHelpers.render_surface(renderer, surface, text_pos[0], text_pos[1])
        return width

    @staticmethod
    def _render_input_box(
        renderer: Renderer,
        text: str,
        prompt: str,
        width: int,
        y_end: int,
    ) -> None:
        """TODO."""
        if not (
            input_surface := TextGenerator().get_text(
                text, Style.SIDEPANE_HEADING
            )
        ):
            return
        box_height = input_surface.h + 2 * _INPUT_BOX_PADDING
        box_x = (SCREEN_WIDTH - width) // 2
        box_y = y_end - box_height - _BUTTON_SPACING

        SDL_SetRenderDrawColor(
            renderer.sdlrenderer, *util.tuple_to_sdl_color(BG_COLOR)
        )
        SDL_RenderFillRect(
            renderer.sdlrenderer,
            SDL_Rect(box_x, box_y, width, box_height),
        )
        SDL_SetRenderDrawColor(
            renderer.sdlrenderer, *util.tuple_to_sdl_color(SECONDARY_COLOR)
        )
        renderer.draw_rect((box_x, box_y, width, box_height))
        SDLHelpers.render_surface(
            renderer,
            input_surface,
            box_x + (width - input_surface.w) // 2,
            box_y + _INPUT_BOX_PADDING,
        )
        if prompt_surface := TextGenerator().get_text(prompt):
            SDLHelpers.render_surface(
                renderer,
                prompt_surface,
                (SCREEN_WIDTH - prompt_surface.w) // 2,
                box_y - prompt_surface.h - _BUTTON_SPACING,
            )

    @staticmethod
    def render(
        renderer: Renderer,
        selected_button: KeyboardButton | None,
        y_offset: int,
    ) -> None:
        """Render the keyboard and its current input."""
        keyboard = Keyboard()
        if not (keyboard := Keyboard()).is_open:
            return
        SDL_SetRenderDrawBlendMode(renderer.sdlrenderer, SDL_BLENDMODE_BLEND)
        SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 0, 225)
        SDL_RenderFillRect(
            renderer.sdlrenderer, SDL_Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        total_width, total_height = KeyboardRenderer._calculate_keyboard_size()

        y_offset = SCREEN_HEIGHT - total_height - y_offset
        KeyboardRenderer._render_input_box(
            renderer,
            keyboard.current_input or " ",
            keyboard.prompt or "INPUT",
            total_width,
            y_offset,
        )
        for row in keyboard.available_keys():
            x_offset = (SCREEN_WIDTH - total_width) // 2
            for button in row:
                button_width = KeyboardRenderer._draw_button(
                    renderer,
                    (x_offset, y_offset),
                    button,
                    highlight=button == selected_button,
                )
                x_offset += button_width + _BUTTON_SPACING
            y_offset += _BUTTON_SIZE + _BUTTON_SPACING