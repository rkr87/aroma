from sdl2 import SDL_Surface
from sdl2.ext import Color

class FontTTF:
    def __init__(self, font: str, size: int, color: Color, index: int = 0, height_chars: str | None = None) -> None: ...
    def add_style(self, name: str, size: int, color: Color, bg_color: Color | None = None) -> None: ...
    def render_text(self, text: str, style: str = 'default', line_h: int | str | None = None, width: int | None = None, align: str = 'left') -> SDL_Surface | None: ...