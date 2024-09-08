"""
Defines data structures for handling menu actions and menu items.
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


@dataclass
class MenuItem:
    """
    Represents a menu item containing a list of actions, with an index for the
    selected action and a flag for selection state.
    """
    actions: list[MenuAction]
    action_index: int = 0
    selected: bool = False
