"""
Defines data structures for handling the currently active menu and its
navigation history.
"""
from dataclasses import dataclass

from navigation.base_menu import BaseMenu


@dataclass
class CurrentMenu:
    """
    Represents the currently active menu and its navigation breadcrumbs.
    """
    menu: BaseMenu
    breadcrumbs: list[str]
    update_required: bool
