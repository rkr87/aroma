"""TODO."""

from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import TextGenerator
from sdl2 import (
    SDL_Surface,
)
from sdl2.ext import Renderer
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    SECONDARY_COLOR,
)
from shared.tools.util import tuple_to_sdl_color


class MenuRenderer(ClassSingleton):
    """TODO."""

    def __init__(self, renderer: Renderer, padding: int, spacing: int) -> None:
        super().__init__()
        self.renderer = renderer
        self.padding = padding
        self.spacing = spacing

    def _draw_menu_separator(self, y: int, width: int) -> None:
        """TODO."""
        # pylint: disable=duplicate-code
        SDLHelpers.draw_line(
            self.renderer,
            tuple_to_sdl_color(SECONDARY_COLOR),
            (0, width),
            (y, y),
        )
        # pylint: enable=duplicate-code

    def render(self, menu: MenuBase, y_start: int, max_width: int) -> None:
        """Render the current menu's items."""
        for i, item in enumerate(menu.update()):
            surfaces = self._get_menu_surfaces(item, max_width)
            if surfaces[0]:
                y: int = i * (surfaces[0].h + self.spacing) + y_start
                if item.bottom_separator:
                    self._draw_menu_separator(
                        y + surfaces[0].h + self.spacing // 2, max_width
                    )
                self._render_item(
                    surfaces[0], surfaces[1], surfaces[2], y, max_width
                )

        self._logger.debug("Rendered menu items")

    def _get_menu_surfaces(
        self, item: MenuItemBase, max_width: int
    ) -> tuple[SDL_Surface | None, SDL_Surface | None, SDL_Surface | None]:
        """Generate the text surfaces for the given menu item."""
        if isinstance(item, MenuItemSingle):
            select_surface = TextGenerator().get_selectable(
                item.get_text(),
                selected=item.selected,
                deactivated=item.deactivated,
                max_width=max_width - self.padding - self.spacing,
            )
            return select_surface, None, None
        if isinstance(item, MenuItemMulti):
            w_adj = 0
            pfx_surface = TextGenerator().get_text(item.get_prefix_text())
            if pfx_surface:
                w_adj += pfx_surface.w + self.spacing + self.padding
            chevron_surface = TextGenerator().get_selectable(
                "›",  # noqa: RUF001
                selected=item.selected,
            )
            if chevron_surface:
                w_adj += chevron_surface.w + self.spacing
            select_surface = TextGenerator().get_selectable(
                item.get_text(),
                selected=item.selected,
                deactivated=item.deactivated,
                max_width=max_width - w_adj,
            )
            return pfx_surface, select_surface, chevron_surface
        return None, None, None

    def _render_item(  # pylint: disable=too-many-positional-arguments
        self,
        text_surface: SDL_Surface,
        multi_val: SDL_Surface | None,
        chevron: SDL_Surface | None,
        y: int,
        width: int,
    ) -> None:
        """Render the item and its associated surfaces."""
        txt_width = text_surface.w
        SDLHelpers.render_surface(
            self.renderer,
            text_surface,
            self.padding,
            y,
        )
        if multi_val:
            SDLHelpers.render_surface(
                self.renderer,
                multi_val,
                self.padding + txt_width + self.spacing,
                y,
            )
        if chevron:
            SDLHelpers.render_surface(
                self.renderer,
                chevron,
                width - chevron.w - self.spacing,
                y,
            )
        self._logger.debug("Rendered item at y-offset %d", y)
