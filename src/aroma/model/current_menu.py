"""
Defines data structures for handling the currently active menu and its
navigation history.
"""
from dataclasses import dataclass

from navigation.menu import Menu


@dataclass
class CurrentMenu:
    """
    Represents the currently active menu and its navigation breadcrumbs.
    """
    menu: Menu
    breadcrumbs: list[str]
