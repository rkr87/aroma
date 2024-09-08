"""
Defines data structures for handling menu actions.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class MenuAction:  # type: ignore
    """
    Represents a menu action with associated text and an optional action to be
    executed.
    """
    text: str
    action: Callable[..., Any] | None
