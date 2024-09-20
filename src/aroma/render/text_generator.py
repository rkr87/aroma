"""
Defines color constants, styles for text rendering, and a class for generating
styled text surfaces.
"""

from enum import StrEnum

from sdl2 import (SDL_BlitSurface, SDL_CreateRGBSurface, SDL_Rect, SDL_Surface,
                  ext)

from base.class_singleton import ClassSingleton
from constants import PRIMARY_COLOR, RESOURCES, SECONDARY_COLOR
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


class TextGenerator(ClassSingleton):
    """
    A class to handle text rendering with different styles based on user
    selection.
    """

    _DEFAULT_FONT = f"{RESOURCES}/ui/DejaVuSans.ttf"

    def __init__(self, font_path: str | None = None) -> None:
        """
        Initializes the TextGenerator with a font and adds different styles.
        """
        super().__init__()
        color = tuple_to_sdl_color(PRIMARY_COLOR)
        selected = tuple_to_sdl_color(SECONDARY_COLOR)
        self.font = ext.FontTTF(font_path or self._DEFAULT_FONT, 26, color)
        self.font.add_style(Style.SELECTED.value, 26, selected)
        self.font.add_style(Style.BOTTOM.value, 20, selected)
        self.font.add_style(Style.BREADCRUMB.value, 20, selected)
        self.font.add_style(Style.BREADCRUMB_TRAIL.value, 20, color)
        self.font.add_style(Style.BUTTON_HELP_TEXT.value, 25, color)
        self.font.add_style(Style.SIDEPANE_HEADING.value, 26, selected)
        self.font.add_style(Style.SIDEPANE_CONTENT.value, 21, color)
        self._logger.info("TextGenerator initialized with font %s", font_path)

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
        style: Style = Style.DEFAULT
    ) -> SDL_Surface | None:
        """
        Renders the text using the specified style and returns the resulting
        SDL_Surface.
        """
        if not text:
            self._logger.warning("Empty text provided for style %s", style)
            return None
        if (text_surface := self.font.render_text(text, style.value)) is None:
            self._logger.error(
                "Failed to render text to surface for style %s", style
            )
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

    def _process_paragraph(
        self,
        paragraph: str,
        max_width: int,
        style: Style
    ) -> list[str]:
        """
        Processes a paragraph, breaking it into lines that fit within the
        specified width.
        """
        lines: list[str] = []
        current_line = ''
        words = paragraph.split(' ')
        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_surface = self.get_text(test_line, style)
            if text_surface and text_surface.w > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        self._logger.debug("Processed paragraph into lines: %s", lines)
        return lines

    def _get_wrapped_lines(
        self,
        text: str,
        max_width: int,
        style: Style
    ) -> list[SDL_Surface]:
        """
        Breaks the text into lines that fit within the specified width and
        returns a list of SDL_Surfaces for each line. Considers newline
        characters for line breaks, including multiple consecutive newlines.
        """
        lines: list[str] = []
        blocks = text.split('\n\n')
        for block in enumerate(blocks):
            for paragraph in block[1].split('\n'):
                lines.extend(
                    self._process_paragraph(paragraph, max_width, style)
                )
            if block[0] < len(blocks) - 1:
                lines.append(' ')
        wrapped_lines = [s for l in lines if (s := self.get_text(l, style))]
        self._logger.debug(
            "Wrapped text into SDL_Surfaces: %d surfaces created",
            len(wrapped_lines)
        )
        return wrapped_lines

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
            self._logger.warning(
                "No text surfaces created for the given width %d and style %s",
                max_width,
                style
            )
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

        self._logger.debug(
            "Final wrapped text surface created with size %dx%d",
            max_width,
            total_height
        )
        return final_surface
