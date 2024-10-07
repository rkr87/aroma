"""Handles screen rendering for the application."""

import ctypes

from sdl2 import (
    SDL_CreateTextureFromSurface,
    SDL_DestroyTexture,
    SDL_Rect,
    SDL_RenderCopy,
    SDL_RenderDrawLine,
    SDL_SetRenderDrawColor,
    SDL_Surface,
    SDL_Texture,
)
from sdl2.ext import Color, Renderer
from shared.classes.class_singleton import ClassSingleton


class SDLHelpers(ClassSingleton):
    """TODO."""

    @staticmethod
    def draw_line(
        renderer: Renderer,
        color: Color,
        x: tuple[int, int],
        y: tuple[int, int],
    ) -> None:
        """Draw a line on the screen using provided color and coordinates."""
        SDL_SetRenderDrawColor(
            renderer.sdlrenderer,
            color.r,
            color.g,
            color.b,
            color.a,
        )
        SDL_RenderDrawLine(
            renderer.sdlrenderer,
            x[0],
            y[0],
            x[1],
            y[1],
        )
        SDLHelpers.get_static_logger().debug(
            "Drawn line from %s to %s with color %s",
            x,
            y,
            color,
        )

    @staticmethod
    def render_surface(
        renderer: Renderer,
        surface: SDL_Surface | None,
        x: int,
        y: int,
    ) -> None:
        """Render a given surface at the specified screen coordinates."""
        if surface is None:
            return

        texture: SDL_Texture | None = SDL_CreateTextureFromSurface(
            renderer.sdlrenderer,
            surface,
        )
        if texture is None:
            SDLHelpers.get_static_logger().error(
                "Failed to create texture from surface"
            )
            return

        if isinstance(surface, ctypes.POINTER(SDL_Surface)):
            surface_width = surface.contents.w
            surface_height = surface.contents.h
        else:
            surface_width = surface.w
            surface_height = surface.h

        dstrect = SDL_Rect(x, y, surface_width, surface_height)
        SDL_RenderCopy(renderer.sdlrenderer, texture, None, dstrect)
        SDL_DestroyTexture(texture)
        SDLHelpers.get_static_logger().debug(
            "Rendered surface at (%d, %d)", x, y
        )
