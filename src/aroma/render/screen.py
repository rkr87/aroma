"""
Handles screen rendering for the application, including menus, breadcrumbs, and
background elements.
"""
import ctypes

from sdl2 import (SDL_CreateTextureFromSurface, SDL_DestroyTexture, SDL_Rect,
                  SDL_RenderCopy, SDL_RenderDrawLine, SDL_SetRenderDrawColor,
                  SDL_Surface, SDL_Texture)
from sdl2.ext import Color, Renderer, Window, load_image

from constants import (APP_NAME, BG_COLOR, RESOURCES, SCREEN_HEIGHT,
                       SCREEN_WIDTH, SECONDARY_COLOR)
from model.current_menu import CurrentMenu
from model.menu_item_base import MenuItemBase
from model.menu_item_multi import MenuItemMulti
from model.menu_item_single import MenuItemSingle
from model.side_pane import SidePane
from navigation.base_menu import BaseMenu
from render.text_generator import Style, TextGenerator
from util import tuple_to_sdl_color


class Screen:
    """
    Manages the screen rendering process, including menus, backgrounds, and
    breadcrumbs.
    """

    SPACING = 15
    PADDING = 40
    SPLIT_PANE = int((SCREEN_WIDTH / 7 * 3) + PADDING + SPACING)

    def __init__(self, text_generator: TextGenerator) -> None:
        """
        Initializes the screen with a window, renderer, and text generator.
        """
        super().__init__()
        self.window = Window(APP_NAME, size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.window.show()
        self.renderer = Renderer(self.window)
        self.text_gen: TextGenerator = text_generator

    @property
    def _side_pane_line_pos(self) -> int:
        """
        Calculates the x-position for the side pane separator line.
        """
        return self.SPLIT_PANE - int(self.PADDING / 2)

    def _draw_line(
        self,
        color: Color,
        x: tuple[int, int],
        y: tuple[int, int]
    ) -> None:
        """
        Draws a line on the screen using the specified color and coordinates.
        """
        SDL_SetRenderDrawColor(
            self.renderer.sdlrenderer,
            color.r,
            color.g,
            color.b,
            color.a
        )
        SDL_RenderDrawLine(
            self.renderer.sdlrenderer,
            x[0],
            y[0],
            x[0] + x[1],
            y[0] + y[1]
        )

    def _render_surface(
        self,
        surface: SDL_Surface | None,
        x: int,
        y: int
    ) -> None:
        """
        Renders a given surface at the specified (x, y) position on the screen.
        """
        if surface is None:
            return

        texture: SDL_Texture | None = \
            SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, surface)
        if texture is None:
            return

        if isinstance(surface, ctypes.POINTER(SDL_Surface)):
            surface_width = surface.contents.w
            surface_height = surface.contents.h
        else:
            surface_width = surface.w
            surface_height = surface.h

        dstrect = SDL_Rect(x, y, surface_width, surface_height)
        SDL_RenderCopy(self.renderer.sdlrenderer, texture, None, dstrect)
        SDL_DestroyTexture(texture)

    def _render_background(self) -> None:
        """
        Renders the background with button icons and associated help text.
        """
        self.renderer.clear(tuple_to_sdl_color(BG_COLOR))
        buttons: list[tuple[str, str]] = [
            (f"{RESOURCES}/ui/button-A.png", "SELECT"),
            (f"{RESOURCES}/ui/button-B.png", "BACK"),
            (f"{RESOURCES}/ui/button-MENU.png", "EXIT")
        ]

        y: int = SCREEN_HEIGHT - self.SPACING
        x: int = SCREEN_WIDTH - self.SPACING
        for button in reversed(buttons):
            image_path: str = button[0]
            text: str = button[1]
            y_adj: int = 0
            if surface := load_image(image_path):
                text_surface: SDL_Surface | None = \
                    self.text_gen.get_text(text, Style.BUTTON_HELP_TEXT)
                if text_surface:
                    x -= text_surface.w
                    y_adj = surface.h - (int((surface.h - text_surface.h) / 2))
                    self._render_surface(text_surface, x, y - y_adj)
                    x -= surface.w + self.SPACING
                self._render_surface(surface, x, y - surface.h)
                x -= 25

    def _render_breadcrumbs(self, breadcrumbs: list[str]) -> None:
        """
        Renders the breadcrumb trail for the current menu.
        """
        crumb_offset = 0
        if len(breadcrumbs) > 1:
            crumb_trail = f"{' › '.join(breadcrumbs[:-1])} › "
            trail_text: SDL_Surface | None = \
                self.text_gen.get_text(crumb_trail, Style.BREADCRUMB_TRAIL)
            if trail_text:
                self._render_surface(trail_text, self.SPACING, self.SPACING)
                crumb_offset = trail_text.w
        breadcrumb_text: SDL_Surface | None = \
            self.text_gen.get_text(breadcrumbs[-1], Style.BREADCRUMB)
        self._render_surface(
            breadcrumb_text,
            self.SPACING + crumb_offset,
            self.SPACING
        )

    def _render_menu(self, menu: BaseMenu) -> None:
        """Renders the current menu's items."""
        items: list[MenuItemBase] = menu.update()

        for i, item in enumerate(items):
            text_surface, multi_val, chevron = self._get_menu_surfaces(item)
            if text_surface:
                y_adj: int = i * (text_surface.h + self.SPACING)
                self._render_item(text_surface, multi_val, chevron, y_adj)

    def _get_menu_surfaces(
        self,
        item: MenuItemBase
    ) -> tuple[SDL_Surface | None, SDL_Surface | None, SDL_Surface | None]:
        """Generates the text surfaces for the given menu item."""
        select_surface = \
            self.text_gen.get_selectable(item.get_text(), item.selected)
        if isinstance(item, MenuItemSingle):
            return select_surface, None, None
        if isinstance(item, MenuItemMulti):
            pfx_surface = self.text_gen.get_text(item.get_prefix_text())
            chevron_surface = self.text_gen.get_text("›")
            return pfx_surface, select_surface, chevron_surface
        return None, None, None

    def _render_item(
        self,
        text_surface: SDL_Surface,
        multi_val: SDL_Surface | None,
        chevron: SDL_Surface | None,
        y_adj: int
    ) -> None:
        """Renders the item and its associated surfaces."""
        self._render_surface(
            text_surface,
            self.PADDING,
            self.PADDING + self.SPACING + y_adj
        )
        if multi_val:
            self._render_surface(
                multi_val,
                self.PADDING + text_surface.w + self.SPACING,
                self.PADDING + self.SPACING + y_adj
            )
        if chevron:
            self._render_surface(
                chevron,
                self.SPLIT_PANE - chevron.w - self.PADDING,
                self.PADDING + self.SPACING + y_adj
            )

    def _render_sidepane(self, side_pane: SidePane | None) -> None:
        """Render the side pane with header and content."""
        if not side_pane:
            return
        if header := self._get_header_surface(side_pane.header):
            self._render_surface(
                header,
                self.SPLIT_PANE,
                self.PADDING + self.SPACING
            )
        if content := self._get_content_surface(side_pane.content):
            y_adj = 0 if not header else header.h + self.SPACING
            self._render_surface(
                content,
                self.SPLIT_PANE,
                self.PADDING + self.SPACING + y_adj
            )

    def _get_header_surface(
        self,
        header_text: str | None
    ) -> SDL_Surface | None:
        """Get the surface for the header text."""
        if not header_text:
            return None
        return self.text_gen.get_text(header_text, Style.SIDEPANE_HEADING)

    def _get_content_surface(
        self,
        content_text: str | None
    ) -> SDL_Surface | None:
        """Get the surface for the content text."""
        if not content_text:
            return None
        return self.text_gen.get_wrapped_text(
            content_text,
            SCREEN_WIDTH - self.SPLIT_PANE - self.PADDING,
            Style.SIDEPANE_CONTENT
        )

    def render_screen(
        self,
        menu: CurrentMenu
    ) -> None:
        """
        Renders the entire screen including background, breadcrumbs, menu, and
        side pane.
        """
        if menu.update_required:
            self._render_background()
            self._render_breadcrumbs(menu.breadcrumbs)
            self._render_menu(menu.menu)
            line_y = self.SPACING + self.PADDING
            self._draw_line(
                tuple_to_sdl_color(SECONDARY_COLOR),
                (self._side_pane_line_pos, 0),
                (line_y, SCREEN_HEIGHT - line_y * 2)
            )
            self._render_sidepane(menu.menu.get_side_pane())
            self.renderer.present()
            menu.update_required = False
