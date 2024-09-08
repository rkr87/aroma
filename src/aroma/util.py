"""
Utility functions.
"""
from typing import overload


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
