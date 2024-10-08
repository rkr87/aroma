"""Handles screen rendering for the application."""

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.current_menu import CurrentMenu
from app.model.side_pane import SidePane
from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_Rect,
    SDL_RenderFillRect,
    SDL_SetRenderDrawBlendMode,
    SDL_SetRenderDrawColor,
    SDL_Surface,
)
from sdl2.blendmode import SDL_BLENDMODE_BLEND
from sdl2.ext import Renderer, Window, load_image
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    APP_NAME,
    BG_COLOR,
    RESOURCES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SECONDARY_COLOR,
)
from shared.tools.util import tuple_to_sdl_color


class Screen(ClassSingleton):
    """Manages the screen rendering process."""

    SPACING = 13
    PADDING = 39
    SPLIT_PANE = int((SCREEN_WIDTH / 7 * 3) + PADDING + SPACING)

    def __init__(self) -> None:
        super().__init__()
        self.window = Window(APP_NAME, size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.window.show()
        self.renderer = Renderer(self.window)
        self.text_gen: TextGenerator = TextGenerator()
        self._logger.info("Screen initialised")

    @property
    def _side_pane_line_pos(self) -> int:
        """Calculates the x-position for the side pane separator line."""
        return self.SPLIT_PANE - int(self.PADDING / 2)

    def _get_button_info(
        self,
    ) -> tuple[list[tuple[SDL_Surface, SDL_Surface | None]], int]:
        """TODO."""
        buttons: list[tuple[str, str | None]] = [
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
        max_height: int = 0
        button_info: list[tuple[SDL_Surface, SDL_Surface | None]] = []
        for img, text in reversed(buttons):
            if surface := load_image(img):
                max_height = max(surface.h, max_height)
                if not text:
                    button_info.append((surface, None))
                    continue
                text_surface: SDL_Surface | None = self.text_gen.get_text(
                    text,
                    Style.BUTTON_HELP_TEXT,
                )
                if text_surface:
                    max_height = max(text_surface.h, max_height)
                button_info.append((surface, text_surface))
        return button_info, max_height

    def _render_background(self) -> int:
        """Render the background with button icons and associated help text."""
        self.renderer.clear(tuple_to_sdl_color(BG_COLOR))
        button_info, max_height = self._get_button_info()
        center_y: int = SCREEN_HEIGHT - self.SPACING - (max_height // 2)
        x: int = SCREEN_WIDTH
        for surface, text_surface in button_info:
            if text_surface:
                x -= text_surface.w + self.SPACING * 2
                SDLHelpers.render_surface(
                    self.renderer,
                    text_surface,
                    x,
                    center_y - text_surface.h // 2,
                )
            x -= surface.w + self.SPACING
            SDLHelpers.render_surface(
                self.renderer, surface, x, center_y - surface.h // 2
            )

        self._logger.debug("Rendered background with button icons")
        return center_y - self.SPACING - max_height // 2

    def _render_breadcrumbs(self, breadcrumbs: list[str]) -> int:
        """Render the breadcrumb trail for the current menu."""
        crumb_offset = 0
        max_y: int = 0
        if len(breadcrumbs) > 1:
            crumb_trail = f"{' › '.join(breadcrumbs[:-1])} › "  # noqa: RUF001
            trail_text: SDL_Surface | None = self.text_gen.get_text(
                crumb_trail,
                Style.BREADCRUMB_TRAIL,
            )
            if trail_text:
                SDLHelpers.render_surface(
                    self.renderer, trail_text, self.SPACING, self.SPACING
                )
                crumb_offset = trail_text.w
                max_y = max(max_y, trail_text.h + self.SPACING)
        breadcrumb_text: SDL_Surface | None = self.text_gen.get_text(
            breadcrumbs[-1],
            Style.BREADCRUMB,
        )
        if breadcrumb_text:
            SDLHelpers.render_surface(
                self.renderer,
                breadcrumb_text,
                self.SPACING + crumb_offset,
                self.SPACING,
            )
            max_y = max(max_y, breadcrumb_text.h + self.SPACING)
        self._logger.debug("Rendered breadcrumbs: %s", breadcrumbs)
        return max_y

    def _render_menu(
        self, menu: MenuBase, y_start: int, max_width: int
    ) -> None:
        """Render the current menu's items."""
        items: list[MenuItemBase] = menu.update()

        for i, item in enumerate(items):
            surfaces = self._get_menu_surfaces(item, max_width)
            if surfaces[0]:
                y: int = i * (surfaces[0].h + self.SPACING) + y_start
                self._render_item(surfaces[0], surfaces[1], surfaces[2], y)
        self._logger.debug("Rendered menu items")

    def _get_menu_surfaces(
        self, item: MenuItemBase, max_width: int
    ) -> tuple[SDL_Surface | None, SDL_Surface | None, SDL_Surface | None]:
        """Generate the text surfaces for the given menu item."""
        select_surface = self.text_gen.get_selectable(
            item.get_text(),
            selected=item.selected,
            deactivated=item.deactivated,
            max_width=max_width,
        )
        if isinstance(item, MenuItemSingle):
            return select_surface, None, None
        if isinstance(item, MenuItemMulti):
            pfx_surface = self.text_gen.get_text(item.get_prefix_text())
            chevron_surface = self.text_gen.get_selectable(
                "›",  # noqa: RUF001
                selected=item.selected,
            )
            return pfx_surface, select_surface, chevron_surface
        return None, None, None

    def _render_item(
        self,
        text_surface: SDL_Surface,
        multi_val: SDL_Surface | None,
        chevron: SDL_Surface | None,
        y: int,
    ) -> None:
        """Render the item and its associated surfaces."""
        SDLHelpers.render_surface(
            self.renderer,
            text_surface,
            self.PADDING,
            y,
        )
        if multi_val:
            SDLHelpers.render_surface(
                self.renderer,
                multi_val,
                self.PADDING + text_surface.w + self.SPACING,
                y,
            )
        if chevron:
            SDLHelpers.render_surface(
                self.renderer,
                chevron,
                self.SPLIT_PANE - chevron.w - self.PADDING,
                y,
            )
        self._logger.debug("Rendered item at y-offset %d", y)

    def _render_sidepane(
        self, side_pane: SidePane | None, y: int, y_end: int
    ) -> int:
        """Render the side pane with header and content."""
        if not side_pane:
            return SCREEN_WIDTH
        SDLHelpers.draw_line(
            self.renderer,
            tuple_to_sdl_color(SECONDARY_COLOR),
            (self._side_pane_line_pos, self._side_pane_line_pos),
            (y, y_end),
        )
        if header := self._get_header_surface(side_pane.header):
            SDLHelpers.render_surface(
                self.renderer,
                header,
                self.SPLIT_PANE,
                y,
            )
        content_height = y_end - y - (header.h if header else 0)
        if content := self._get_content_surface(
            side_pane.content, content_height
        ):
            y += 0 if not header else header.h + self.SPACING // 2
            SDLHelpers.render_surface(
                self.renderer, content, self.SPLIT_PANE, y
            )
        self._logger.debug("Rendered side pane")
        return self.SPLIT_PANE

    def _get_header_surface(
        self,
        header_text: str | None,
    ) -> SDL_Surface | None:
        """Get the surface for the header text."""
        if not header_text:
            return None
        return self.text_gen.get_text(header_text, Style.SIDEPANE_HEADING)

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
        return self.text_gen.get_wrapped_text(
            content_text,
            SCREEN_WIDTH - self.SPLIT_PANE - self.PADDING,
            Style.SIDEPANE_CONTENT,
            max_height=max_height,
        )

    def _render_worker_overlay(self) -> None:
        """Render an overlay indicating that a job is in progress."""
        if not (worker := BackgroundWorker()).busy:
            return
        SDL_SetRenderDrawBlendMode(
            self.renderer.sdlrenderer, SDL_BLENDMODE_BLEND
        )
        SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 225)
        overlay_rect = SDL_Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        SDL_RenderFillRect(self.renderer.sdlrenderer, overlay_rect)
        rect_wh = (480, 270)
        rect_xy = (
            (SCREEN_WIDTH - rect_wh[0]) // 2,
            (SCREEN_HEIGHT - rect_wh[1]) // 2,
        )

        SDL_SetRenderDrawColor(self.renderer.sdlrenderer, *BG_COLOR, 255)
        progress_rect = SDL_Rect(
            rect_xy[0], rect_xy[1], rect_wh[0], rect_wh[1]
        )
        SDL_RenderFillRect(self.renderer.sdlrenderer, progress_rect)

        msg_surface: SDL_Surface | None = self.text_gen.get_text(
            worker.message, Style.DEFAULT
        )
        if msg_surface:
            msg_x = rect_xy[0] + (rect_wh[0] - msg_surface.w) // 2
            msg_y = rect_xy[1] + (rect_wh[1] - msg_surface.h) // 2
            SDLHelpers.render_surface(self.renderer, msg_surface, msg_x, msg_y)

    def render_screen(
        self,
        current: CurrentMenu,
    ) -> None:
        """Render the screen background, breadcrumbs, menu, and side pane."""
        if current.update_required:
            help_h = self._render_background()
            crumb_h = self._render_breadcrumbs(current.breadcrumbs)
            side_pane_w = self._render_sidepane(
                current.menu.content.side_pane, crumb_h + self.SPACING, help_h
            )
            self._render_menu(
                current.menu,
                crumb_h + self.SPACING,
                side_pane_w - self.PADDING * 2,
            )
            self._render_worker_overlay()
            self.renderer.present()
            current.update_required = False
            self._logger.debug("Rendered screen for current menu")
