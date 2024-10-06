"""Defines color constants, styles for text rendering."""

from enum import StrEnum

from sdl2 import (
    SDL_BlitSurface,
    SDL_CreateRGBSurface,
    SDL_Rect,
    SDL_Surface,
    ext,
)
from shared.classes.base.class_singleton import ClassSingleton
from shared.constants import (
    INACTIVE_COLOR,
    INACTIVE_SEL,
    PRIMARY_COLOR,
    RESOURCES,
    SECONDARY_COLOR,
)
from shared.tools.util import tuple_to_sdl_color


class Style(StrEnum):
    """Enum representing various text styles for rendering."""

    DEFAULT = "default"
    SELECTED = "selected"
    BOTTOM = "bottom"
    BREADCRUMB = "breadcrumb"
    BREADCRUMB_TRAIL = "breadcrumb_trail"
    BUTTON_HELP_TEXT = "button_help_text"
    SIDEPANE_HEADING = "sidepane_heading"
    SIDEPANE_CONTENT = "sidepane_content"
    INACTIVE = "deactivated"
    INACTIVE_SELECTED = "inactive_selected"


class TextGenerator(ClassSingleton):
    """A class to handle text rendering with different styles."""

    _DEFAULT_FONT = f"{RESOURCES}/ui/DejaVuSans.ttf"

    def __init__(self, font_path: str | None = None) -> None:
        super().__init__()
        color = tuple_to_sdl_color(PRIMARY_COLOR)
        selected = tuple_to_sdl_color(SECONDARY_COLOR)
        inactive = tuple_to_sdl_color(INACTIVE_COLOR)
        inactive_sel = tuple_to_sdl_color(INACTIVE_SEL)
        self.font = ext.FontTTF(font_path or self._DEFAULT_FONT, 26, color)
        self.font.add_style(Style.SELECTED.value, 26, selected)
        self.font.add_style(Style.INACTIVE.value, 26, inactive)
        self.font.add_style(Style.INACTIVE_SELECTED.value, 26, inactive_sel)
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
        *,
        selected: bool,
        deactivated: bool = False,
        max_width: int = 0,
    ) -> SDL_Surface | None:
        """Return a selectable text surface."""
        if not deactivated:
            style: Style = Style.SELECTED if selected else Style.DEFAULT
        else:
            style = Style.INACTIVE_SELECTED if selected else Style.INACTIVE
        return self.get_text(text, style, max_width)

    def get_text(
        self, text: str, style: Style = Style.DEFAULT, max_width: int = 0
    ) -> SDL_Surface | None:
        """Render the text using the provided style."""
        if not text:
            self._logger.debug("Empty text provided for style %s", style)
            return None

        if not (text_surface := self._render_surface(text, style)):
            self._logger.error("Failed to render text for style %s", style)
            return None

        if not max_width or text_surface.w < max_width:
            return text_surface

        return self._wrap_text_to_width(text, style, max_width)

    def _render_surface(self, text: str, style: Style) -> SDL_Surface | None:
        """Render text surface with the specified style."""
        return self.font.render_text(text, style.value)

    def _wrap_text_to_width(
        self, text: str, style: Style, max_width: int
    ) -> SDL_Surface | None:
        """Wrap text to fit within the specified width."""
        new_text = ""
        for word in text.split(" "):
            test_line = f"{new_text} {word}".strip()
            text_surface = self._render_surface(test_line, style)
            if text_surface and text_surface.w > max_width:
                return self._render_surface(f"{new_text}...", style)
            new_text = test_line
        return self._render_surface(new_text, style)

    @staticmethod
    def _create_fixed_surface(width: int, height: int) -> SDL_Surface:
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

    def _process_paragraph(
        self,
        paragraph: str,
        max_width: int,
        style: Style,
    ) -> list[str]:
        """Process paragraph, reducing line length to fit in provided width."""
        lines: list[str] = []
        current_line = ""
        words = paragraph.split(" ")
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
        style: Style,
    ) -> list[SDL_Surface]:
        """Break text into lines that fit within provided width."""
        lines: list[str] = []
        blocks = text.split("\n\n")
        for block in enumerate(blocks):
            for paragraph in block[1].split("\n"):
                lines.extend(
                    self._process_paragraph(paragraph, max_width, style),
                )
            if block[0] < len(blocks) - 1:
                lines.append(" ")
        wrapped_lines = [
            surface
            for line in lines
            if (surface := self.get_text(line, style))
        ]
        self._logger.debug(
            "Wrapped text into SDL_Surfaces: %d surfaces created",
            len(wrapped_lines),
        )
        return wrapped_lines

    @staticmethod
    def _blit_lines_to_surface(
        final_surface: SDL_Surface, lines: list[SDL_Surface]
    ) -> None:
        """Blit the lines onto the final surface."""
        y_offset = 0
        for surface in lines:
            SDL_BlitSurface(
                surface,
                None,
                final_surface,
                SDL_Rect(0, y_offset, surface.w, surface.h),
            )
            y_offset += surface.h

    @staticmethod
    def _truncate_lines(
        lines: list[SDL_Surface], max_height: int
    ) -> tuple[list[SDL_Surface], int]:
        """Truncate the lines to fit within the maximum height."""
        truncated_lines: list[SDL_Surface] = []
        truncated_height = 0
        for surface in lines:
            if truncated_height + surface.h > max_height:
                break
            truncated_lines.append(surface)
            truncated_height += surface.h
        return truncated_lines, truncated_height

    def get_wrapped_text(
        self,
        text: str,
        max_width: int,
        style: Style,
        max_height: int | None = None,
    ) -> SDL_Surface | None:
        """Wrap text within the given width and optional maximum height."""
        if not (lines := self._get_wrapped_lines(text, max_width, style)):
            self._logger.info(
                "No text surfaces created for the given width %d and style %s",
                max_width,
                style,
            )
            return None

        total_height = sum(surface.h for surface in lines)

        if max_height is not None and total_height > max_height:
            lines, total_height = self._truncate_lines(lines, max_height)

        final_surface = self._create_fixed_surface(max_width, total_height)

        self._blit_lines_to_surface(final_surface, lines)

        self._logger.debug(
            "Final wrapped text surface created with size %dx%d",
            max_width,
            total_height,
        )
        return final_surface
