"""
Defines color constants, styles for text rendering, and a class for generating
styled text surfaces.
"""

import logging
from enum import StrEnum

from sdl2 import SDL_Surface, ext

# Predefined colors for text rendering
COLOR = ext.Color(217, 217, 217)
COLOR_SEL = ext.Color(23, 147, 209)


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
        self.font = ext.FontTTF(font_path, 30, COLOR)
        self.font.add_style(Style.SELECTED.value, 30, COLOR_SEL)
        self.font.add_style(Style.BOTTOM.value, 20, COLOR_SEL)
        self.font.add_style(Style.BREADCRUMB.value, 20, COLOR_SEL)
        self.font.add_style(Style.BREADCRUMB_TRAIL.value, 20, COLOR)
        self.font.add_style(Style.BUTTON_HELP_TEXT.value, 20, COLOR)

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
