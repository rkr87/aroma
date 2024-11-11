"""Handles screen rendering for the application."""

from app.model.current_menu import CurrentMenu
from app.model.keyboard_button import KeyboardButton
from app.render.breadcrumb_renderer import BreadcrumbRenderer
from app.render.button_hint_renderer import ButtonHintRenderer
from app.render.keyboard_renderer import KeyboardRenderer
from app.render.menu_renderer import MenuRenderer
from app.render.sidepane_renderer import SidepaneRenderer
from app.render.work_overlay_renderer import WorkOverlayRenderer
from sdl2.ext import Renderer, Window
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    APP_NAME,
    BG_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from shared.tools.util import tuple_to_sdl_color

_SPACING = 13
_PADDING = 39
_SPLIT_PANE = int((SCREEN_WIDTH / 7 * 3) + _PADDING + _SPACING)


class ScreenManager(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """Manages the screen rendering process."""

    def __init__(self) -> None:
        super().__init__()
        window = Window(APP_NAME, size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        window.show()
        self.renderer = Renderer(window)
        self.button_hint = ButtonHintRenderer(self.renderer, _SPACING)
        self.breadcrumb = BreadcrumbRenderer(self.renderer, _SPACING)
        self.sidepane = SidepaneRenderer(
            self.renderer, _SPLIT_PANE, _PADDING, _SPACING
        )
        self.menu = MenuRenderer(self.renderer, _PADDING, _SPACING)
        self._logger.info("Screen initialised")

    def render(
        self,
        current: CurrentMenu,
        keyboard_button: KeyboardButton | None = None,
    ) -> None:
        """Render the screen background, breadcrumbs, menu, and side pane."""
        if current.update_required:
            self.renderer.clear(tuple_to_sdl_color(BG_COLOR))
            button_hint_start = self.button_hint.render()
            breadcrumb_height = self.breadcrumb.render(current.breadcrumbs)
            trim_x = self.sidepane.render(
                current.menu.content.side_pane,
                breadcrumb_height + _SPACING,
                button_hint_start - _SPACING,
            )
            self.menu.render(
                current.menu,
                breadcrumb_height + _SPACING,
                trim_x,
            )
            WorkOverlayRenderer.render(self.renderer)
            KeyboardRenderer.render(
                self.renderer,
                keyboard_button,
                SCREEN_HEIGHT - button_hint_start + _SPACING,
            )
            self.renderer.present()
            current.update_required = False
            self._logger.debug("Rendered screen for current menu")
