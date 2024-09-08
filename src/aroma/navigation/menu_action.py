"""
Defines data structures for handling menu actions.
"""
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class MenuAction:  # type: ignore
    """
    Represents a menu action with associated text and an optional action to be
    executed.
    """
    text: str
    action: Callable[..., None] | None
