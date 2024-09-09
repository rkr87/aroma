"""
Defines color constants, styles for text rendering, and a class for generating
styled text surfaces.
"""

import logging
from enum import StrEnum

from sdl2 import (SDL_BlitSurface, SDL_CreateRGBSurface, SDL_Rect, SDL_Surface,
                  ext)

from constants import PRIMARY_COLOR, SECONDARY_COLOR
from util import tuple_to_sdl_color


class Style(StrEnum):
    """
    Enum representing various text styles for rendering.
    """
    DEFAULT = "default"
    SELECTED = "selected"
    BOTTOM = "bottom"
    BREADCRUMB = "breadcrumb"
    BREADCRUMB_TRAIL = "breadcrumb_trail"
    BUTTON_HELP_TEXT = "button_help_text"
    SIDEPANE_HEADING = "sidepane_heading"
    SIDEPANE_CONTENT = "sidepane_content"


class TextGenerator:
    """
    A class to handle text rendering with different styles based on user
    selection.
    """

    def __init__(self, font_path: str) -> None:
        """
        Initializes the TextGenerator with a font and adds different styles.
        """
        super().__init__()
        color = tuple_to_sdl_color(PRIMARY_COLOR)
        selected = tuple_to_sdl_color(SECONDARY_COLOR)
        self.font = ext.FontTTF(font_path, 30, color)
        self.font.add_style(Style.SELECTED.value, 30, selected)
        self.font.add_style(Style.BOTTOM.value, 20, selected)
        self.font.add_style(Style.BREADCRUMB.value, 20, selected)
        self.font.add_style(Style.BREADCRUMB_TRAIL.value, 20, color)
        self.font.add_style(Style.BUTTON_HELP_TEXT.value, 20, color)
        self.font.add_style(Style.SIDEPANE_HEADING.value, 30, selected)
        self.font.add_style(Style.SIDEPANE_CONTENT.value, 25, color)

    def get_selectable(
        self,
        text: str,
        selected: bool
    ) -> SDL_Surface | None:
        """
        Returns a text surface styled based on whether the text is selected.
        """
        style: Style = Style.SELECTED if selected else Style.DEFAULT
        return self.get_text(text, style)

    def get_text(
        self,
        text: str,
        style: Style
    ) -> SDL_Surface | None:
        """
        Renders the text using the specified style and returns the resulting
        SDL_Surface.
        """
        text_surface: SDL_Surface | None = \
            self.font.render_text(text, style.value)
        if text_surface is None:
            logging.error("Failed to render text to surface.")
        return text_surface

    @staticmethod
    def _create_fixed_surface(width: int, height: int) -> SDL_Surface:
        """
        Creates a fixed-size SDL_Surface with a specified width and height.
        """
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
            amask
        )

    def _get_wrapped_lines(
        self,
        text: str,
        max_width: int,
        style: Style
    ) -> list[SDL_Surface]:
        """
        Breaks the text into lines that fit within the specified width and
        returns a list of SDL_Surfaces for each line.
        """
        lines: list[str] = []
        line: str = ''
        for word in text.split(' '):
            test_line: str = f"{line} {word}".strip()
            text_surface: SDL_Surface | None = self.get_text(test_line, style)
            if text_surface and text_surface.w > max_width:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test_line
        if line:
            lines.append(line)
        return [s for l in lines if (s := self.get_text(l, style))]

    def get_wrapped_text(
        self,
        text: str,
        max_width: int,
        style: Style
    ) -> SDL_Surface | None:
        """
        Wraps the text within the given width and returns an SDL_Surface
        containing the wrapped text.
        """
        if not (lines := self._get_wrapped_lines(text, max_width, style)):
            return None

        total_height = sum(surface.h for surface in lines)
        final_surface = self._create_fixed_surface(max_width, total_height)

        y_offset = 0
        for surface in lines:
            SDL_BlitSurface(
                surface,
                None,
                final_surface,
                SDL_Rect(0, y_offset, surface.w, surface.h)
            )
            y_offset += surface.h

        return final_surface
