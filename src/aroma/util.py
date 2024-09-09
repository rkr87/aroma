"""
Utility functions.
"""
from typing import overload

from sdl2.ext import Color


@overload
def clamp(value: int, min_value: int, max_value: int) -> int: ...
@overload
def clamp(value: float, min_value: float, max_value: float) -> float: ...


def clamp(
    value: int | float,
    min_value: int | float,
    max_value: int | float
) -> int | float:
    """
    Clamps a value between a minimum and maximum range.
    """
    return max(min_value, min(value, max_value))


def tuple_to_sdl_color(rgb: tuple[int, int, int]) -> Color:
    """
    Converts a tuple of RGB values to an SDL2 Color object.
    """
    return Color(rgb[0], rgb[1], rgb[2])
