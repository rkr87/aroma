"""Handles screen rendering for the application."""

import ctypes
from pathlib import Path

from sdl2 import (
    SDL_BLENDMODE_BLEND,
    SDL_PIXELFORMAT_RGBA32,
    SDL_BlitScaled,
    SDL_CreateRGBSurface,
    SDL_CreateRGBSurfaceWithFormat,
    SDL_CreateTextureFromSurface,
    SDL_DestroyTexture,
    SDL_FreeSurface,
    SDL_Rect,
    SDL_RenderCopy,
    SDL_RenderDrawLine,
    SDL_SetRenderDrawColor,
    SDL_SetSurfaceBlendMode,
    SDL_Surface,
    SDL_Texture,
)
from sdl2.ext import Color, Renderer, load_image
from shared.classes.class_singleton import ClassSingleton


class SDLHelpers(ClassSingleton):
    """TODO."""

    @staticmethod
    def create_fixed_surface(width: int, height: int) -> SDL_Surface:
        """Create a fixed-size SDL_Surface."""
        rmask = 0x000000FF
        gmask = 0x0000FF00
        bmask = 0x00FF0000
        amask = 0xFF000000

        return SDL_CreateRGBSurface(
            0,
            width,
            height,
            32,
            rmask,
            gmask,
            bmask,
            amask,
        )

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
        *,
        free_surface: bool = True,
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
            SDL_FreeSurface(surface)
            return

        if isinstance(surface, ctypes.POINTER(SDL_Surface)):
            surface_width = surface.contents.w
            surface_height = surface.contents.h
        else:
            surface_width = surface.w
            surface_height = surface.h

        if free_surface:
            SDL_FreeSurface(surface)
        dstrect = SDL_Rect(x, y, surface_width, surface_height)
        SDL_RenderCopy(renderer.sdlrenderer, texture, None, dstrect)
        SDL_DestroyTexture(texture)
        SDLHelpers.get_static_logger().debug(
            "Rendered surface at (%d, %d)", x, y
        )

    @staticmethod
    def _scale_image(
        image_path: str, max_width: int, max_height: int
    ) -> SDL_Surface | None:
        """TODO."""
        if not (surface := load_image(image_path)):
            return None
        scale_factor = min(max_width / surface.w, max_height / surface.h, 1)
        new_width = int(surface.w * scale_factor)
        new_height = int(surface.h * scale_factor)
        has_alpha = surface.format.contents.Amask != 0
        scaled_surface = SDL_CreateRGBSurfaceWithFormat(
            0,
            new_width,
            new_height,
            32,
            SDL_PIXELFORMAT_RGBA32,
        )
        if not scaled_surface:
            SDL_FreeSurface(surface)
            return None
        if has_alpha:
            SDL_SetSurfaceBlendMode(scaled_surface, SDL_BLENDMODE_BLEND)

        SDL_BlitScaled(surface, None, scaled_surface, None)
        SDL_FreeSurface(surface)
        return scaled_surface

    @staticmethod
    def load_scaled_image(
        image_path: str | None, max_width: int, max_height: int
    ) -> SDL_Surface | None:
        """TODO."""
        if not image_path or not Path(image_path).is_file():
            return None
        return SDLHelpers._scale_image(image_path, max_width, max_height)
