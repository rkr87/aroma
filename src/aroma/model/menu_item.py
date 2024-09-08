"""
Defines data structures for handling menu items.
"""
from dataclasses import dataclass

from model.menu_action import MenuAction


@dataclass
class MenuItem:
    """
    Represents a menu item containing a list of actions, with an index for the
    selected action and a flag for selection state.
    """
    actions: list[MenuAction]
    action_index: int = 0
    selected: bool = False
