"""TODO."""

from pathlib import Path

from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_Surface,
)
from sdl2.ext import Renderer, load_image
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    RESOURCES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

_BUTTONS = [
    (f"{RESOURCES}/ui/button-LEFT.png", None),
    (f"{RESOURCES}/ui/button-RIGHT.png", "LEFT/RIGHT"),
    (f"{RESOURCES}/ui/button-L.png", None),
    (f"{RESOURCES}/ui/button-UP.png", None),
    (f"{RESOURCES}/ui/button-DOWN.png", None),
    (f"{RESOURCES}/ui/button-R.png", "UP/DOWN"),
    (f"{RESOURCES}/ui/button-A.png", "SELECT"),
    (f"{RESOURCES}/ui/button-B.png", "BACK"),
    (f"{RESOURCES}/ui/button-MENU.png", "EXIT"),
]


class ButtonHintRenderer(ClassSingleton):
    """TODO."""

    @staticmethod
    def _get_button_info() -> (
        tuple[list[tuple[SDL_Surface, SDL_Surface | None]], int]
    ):
        """TODO."""
        max_height: int = 0
        button_info: list[tuple[SDL_Surface, SDL_Surface | None]] = []
        for img, text in reversed(_BUTTONS):
            if not Path(img).is_file() or not (surface := load_image(img)):
                continue
            max_height = max(surface.h, max_height)
            if not text:
                button_info.append((surface, None))
                continue
            if text_surface := TextGenerator().get_text(
                text,
                Style.BUTTON_HELP_TEXT,
            ):
                max_height = max(text_surface.h, max_height)
            button_info.append((surface, text_surface))
        return button_info, max_height

    @staticmethod
    def render(renderer: Renderer, spacing: int) -> int:
        """Render button icons and associated help text."""
        button_info, max_height = ButtonHintRenderer._get_button_info()
        center_y: int = SCREEN_HEIGHT - spacing - (max_height // 2)
        x: int = SCREEN_WIDTH
        for surface, text_surface in button_info:
            if text_surface:
                x -= text_surface.w + spacing * 2
                SDLHelpers.render_surface(
                    renderer,
                    text_surface,
                    x,
                    center_y - text_surface.h // 2,
                )
            x -= surface.w + spacing
            SDLHelpers.render_surface(
                renderer, surface, x, center_y - surface.h // 2
            )

        ButtonHintRenderer.get_static_logger().debug(
            "Rendered background with button icons"
        )
        return SCREEN_HEIGHT - spacing - max_height
