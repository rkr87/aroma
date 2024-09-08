"""
Handles screen rendering for the application, including menus, breadcrumbs, and
background elements.
"""
from sdl2 import (SDL_CreateTextureFromSurface, SDL_DestroyTexture, SDL_Rect,
                  SDL_RenderCopy, SDL_Surface, SDL_Texture)
from sdl2.ext import Color, Renderer, Window, load_image

from constants import RESOURCES, SCREEN_HEIGHT, SCREEN_WIDTH
from model.current_menu import CurrentMenu
from model.menu_item import MenuItem
from navigation.menu import Menu
from render.text_generator import Style, TextGenerator

BG_COLOR = Color(16, 16, 16)


class Screen:
    """
    Manages the screen rendering process, including menus, backgrounds, and
    breadcrumbs.
    """

    def __init__(self, text_generator: TextGenerator) -> None:
        """
        Initializes the screen with a window, renderer, and text generator.
        """
        super().__init__()
        self.window = Window("aROMa", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.window.show()
        self.renderer = Renderer(self.window)
        self.text_gen: TextGenerator = text_generator

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
        dstrect = SDL_Rect(x, y, surface.w, surface.h)
        SDL_RenderCopy(self.renderer.sdlrenderer, texture, None, dstrect)
        SDL_DestroyTexture(texture)

    def _render_background(self) -> None:
        """
        Renders the background with button icons and associated help text.
        """
        self.renderer.clear(BG_COLOR)
        buttons: list[tuple[str, str]] = [
            (f"{RESOURCES}/ui/button-A.png", "SELECT"),
            (f"{RESOURCES}/ui/button-B.png", "BACK"),
            (f"{RESOURCES}/ui/button-MENU.png", "EXIT")
        ]

        y: int = SCREEN_HEIGHT - 10
        x: int = SCREEN_WIDTH - 10
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
                    x -= surface.w + 10
                self._render_surface(surface, x, y - surface.h)
                x -= 25

    def _render_breadcrumbs(self, breadcrumbs: list[str]) -> None:
        """
        Renders the breadcrumb trail for the current menu.
        """
        crumb_offset = 0
        if len(breadcrumbs) > 1:
            crumb_trail = f"{' > '.join(breadcrumbs[:-1])} > "
            trail_text: SDL_Surface | None = \
                self.text_gen.get_text(crumb_trail, Style.BREADCRUMB_TRAIL)
            if trail_text:
                self._render_surface(trail_text, 10, 10)
                crumb_offset = trail_text.w
        breadcrumb_text: SDL_Surface | None = \
            self.text_gen.get_text(breadcrumbs[-1], Style.BREADCRUMB)
        self._render_surface(breadcrumb_text, 10 + crumb_offset, 10)

    def _render_menu(self, menu: Menu) -> None:
        """Renders the current menu's items."""
        items: list[MenuItem] = menu.update()
        for i, item in enumerate(items):
            text: str = item.actions[item.action_index].text
            text_surface: SDL_Surface | None = \
                self.text_gen.get_selectable(text, item.selected)
            if text_surface:
                y_adj: int = i * (text_surface.h + 15)
                self._render_surface(text_surface, 50, 65 + y_adj)

    def render_screen(
        self,
        menu: CurrentMenu
    ) -> None:
        """
        Renders the full screen, including background, breadcrumbs, and menu
        items.
        """
        self._render_background()
        self._render_breadcrumbs(menu.breadcrumbs)
        self._render_menu(menu.menu)
        self.renderer.present()
