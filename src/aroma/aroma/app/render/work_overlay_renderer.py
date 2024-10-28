"""TODO."""

from app.background_worker import BackgroundWorker
from app.render.sdl_helpers import SDLHelpers
from app.render.text_generator import Style, TextGenerator
from sdl2 import (
    SDL_Rect,
    SDL_RenderFillRect,
    SDL_SetRenderDrawBlendMode,
    SDL_SetRenderDrawColor,
)
from sdl2.blendmode import SDL_BLENDMODE_BLEND
from sdl2.ext import Renderer
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    BG_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class WorkOverlayRenderer(ClassSingleton):
    """TODO."""

    @staticmethod
    def render(renderer: Renderer) -> None:
        """Render an overlay indicating that a job is in progress."""
        if not (worker := BackgroundWorker()).busy:
            return
        SDL_SetRenderDrawBlendMode(renderer.sdlrenderer, SDL_BLENDMODE_BLEND)
        SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 0, 240)
        overlay_rect = SDL_Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        SDL_RenderFillRect(renderer.sdlrenderer, overlay_rect)
        wh = (480, 270)
        xy = (
            (SCREEN_WIDTH - wh[0]) // 2,
            (SCREEN_HEIGHT - wh[1]) // 2,
        )

        SDL_SetRenderDrawColor(renderer.sdlrenderer, *BG_COLOR, 255)
        progress_rect = SDL_Rect(xy[0], xy[1], wh[0], wh[1])
        SDL_RenderFillRect(renderer.sdlrenderer, progress_rect)

        if msg := TextGenerator().get_text(worker.message, Style.DEFAULT):
            msg_x = xy[0] + (wh[0] - msg.w) // 2
            msg_y = xy[1] + (wh[1] - msg.h) // 2
            SDLHelpers.render_surface(renderer, msg, msg_x, msg_y)
