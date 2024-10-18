"""TODO."""

from typing import TYPE_CHECKING

from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2.ext import Renderer
from shared.classes.class_singleton import ClassSingleton

if TYPE_CHECKING:
    from sdl2 import SDL_Surface


class BreadcrumbRenderer(ClassSingleton):
    """TODO."""

    @staticmethod
    def render(
        renderer: Renderer, breadcrumbs: list[str], spacing: int
    ) -> int:
        """Render the breadcrumb trail for the current menu."""
        crumb_offset = 0
        max_y: int = 0
        if len(breadcrumbs) > 1:
            crumb_trail = f"{' › '.join(breadcrumbs[:-1])} › "  # noqa: RUF001
            trail_text: SDL_Surface | None = TextGenerator().get_text(
                crumb_trail,
                Style.BREADCRUMB_TRAIL,
            )
            if trail_text:
                crumb_offset = trail_text.w
                max_y = max(max_y, trail_text.h + spacing)
                SDLHelpers.render_surface(
                    renderer, trail_text, spacing, spacing
                )

        breadcrumb_text: SDL_Surface | None = TextGenerator().get_text(
            breadcrumbs[-1],
            Style.BREADCRUMB,
        )
        if breadcrumb_text:
            max_y = max(max_y, breadcrumb_text.h + spacing)
            SDLHelpers.render_surface(
                renderer,
                breadcrumb_text,
                spacing + crumb_offset,
                spacing,
            )
        BreadcrumbRenderer.get_static_logger().debug(
            "Rendered breadcrumbs: %s", breadcrumbs
        )
        return max_y
