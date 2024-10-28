"""TODO."""

from pathlib import Path

from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_Surface,
)
from sdl2.ext import Renderer
from sdl2.ext.image import load_image
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


class ButtonHintRenderer(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """TODO."""

    def __init__(self, renderer: Renderer, spacing: int) -> None:
        super().__init__()
        self.renderer = renderer
        self.spacing = spacing
        self.button_info, self.max_height = self._get_button_info()
        self.centre = SCREEN_HEIGHT - spacing - (self.max_height // 2)

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

    def render(self) -> int:
        """Render button icons and associated help text."""
        x: int = SCREEN_WIDTH
        for surface, text_surface in self.button_info:
            if text_surface:
                x -= text_surface.w + self.spacing * 2
                SDLHelpers.render_surface(
                    self.renderer,
                    text_surface,
                    x,
                    self.centre - text_surface.h // 2,
                    free_surface=False,
                )
            x -= surface.w + self.spacing
            SDLHelpers.render_surface(
                self.renderer,
                surface,
                x,
                self.centre - surface.h // 2,
                free_surface=False,
            )

        ButtonHintRenderer.get_static_logger().debug(
            "Rendered background with button icons"
        )
        return SCREEN_HEIGHT - self.spacing - self.max_height
