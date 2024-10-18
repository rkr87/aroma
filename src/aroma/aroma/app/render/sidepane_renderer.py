"""TODO."""

from app.model.side_pane import SidePane
from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_Surface,
)
from sdl2.ext import Renderer
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SECONDARY_COLOR,
)
from shared.tools.util import tuple_to_sdl_color


class SidepaneRenderer(ClassSingleton):
    """TODO."""

    def __init__(
        self, renderer: Renderer, x_start: int, padding: int, spacing: int
    ) -> None:
        super().__init__()
        self.renderer = renderer
        self.x_start = x_start
        self.padding = padding
        self.spacing = spacing

    def _draw_sidepane_separator(self, y: int, y_end: int) -> None:
        """TODO."""
        # pylint: disable=duplicate-code
        SDLHelpers.draw_line(
            self.renderer,
            tuple_to_sdl_color(SECONDARY_COLOR),
            (self.x_start, self.x_start),
            (y, y_end),
        )
        # pylint: enable=duplicate-code

    def _draw_sidepane_header(self, header_text: str | None, y: int) -> int:
        """TODO."""
        if not (header := self._get_header_surface(header_text)):
            return y
        y_adj = header.h + self.spacing // 2
        SDLHelpers.render_surface(
            self.renderer,
            header,
            self.x_start + self.spacing,
            y,
        )
        return y + y_adj

    def _draw_sidepane_icon(
        self,
        icon: str | None,
        y: int,
        h: int,
        w: int,
        *,
        v_centre: bool = True,
    ) -> int:
        """TODO."""
        if icon and (surface := SDLHelpers.load_scaled_image(icon, w, h)):
            ch = surface.contents.h
            SDLHelpers.render_surface(
                self.renderer,
                surface,
                SCREEN_WIDTH // 2
                + self.x_start // 2
                - surface.contents.w // 2,
                y + h // 2 - ch // 2 if v_centre else y,
            )
            return y + int(h if v_centre else ch) + self.spacing // 2
        return y

    def _draw_sidepane_images(
        self, background: str | None, icon: str | None, y: int
    ) -> int:
        """TODO."""
        if background and (
            bg_surface := SDLHelpers.load_scaled_image(
                background,
                SCREEN_WIDTH - self.x_start - self.padding,
                SCREEN_HEIGHT // 2,
            )
        ):
            bg_size = bg_surface.contents.w, bg_surface.contents.h
            SDLHelpers.render_surface(
                self.renderer,
                bg_surface,
                SCREEN_WIDTH // 2 - bg_size[0] // 2 + self.x_start // 2,
                y,
            )
            self._draw_sidepane_icon(icon, y, bg_size[1], bg_size[0])
            return int(y + bg_size[1] + self.spacing // 2)
        return self._draw_sidepane_icon(icon, y, 400, 400, v_centre=False)

    def render(self, side_pane: SidePane | None, y: int, y_end: int) -> int:
        """Render the side pane with header and content."""
        if not side_pane:
            return SCREEN_WIDTH
        self._draw_sidepane_separator(y, y_end)
        y = self._draw_sidepane_header(side_pane.header, y)
        y = self._draw_sidepane_images(side_pane.bg_img, side_pane.img, y)

        if content := self._get_content_surface(side_pane.content, y_end - y):
            SDLHelpers.render_surface(
                self.renderer, content, self.x_start + self.spacing, y
            )
        self._logger.debug("Rendered side pane")
        return self.x_start

    @staticmethod
    def _get_header_surface(header_text: str | None) -> SDL_Surface | None:
        """Get the surface for the header text."""
        if not header_text:
            return None
        return TextGenerator().get_text(header_text, Style.SIDEPANE_HEADING)

    def _get_content_surface(
        self,
        content_text: str | list[str] | None,
        max_height: int | None = None,
    ) -> SDL_Surface | None:
        """Get the surface for the content text."""
        if not content_text:
            return None
        if isinstance(content_text, list):
            content_text = "\n".join(content_text)
        return TextGenerator().get_wrapped_text(
            content_text,
            SCREEN_WIDTH - self.x_start - self.padding,
            Style.SIDEPANE_CONTENT,
            max_height=max_height,
        )
