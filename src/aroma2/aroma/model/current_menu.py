"""Defines data structures for handling the currently active menu."""

from dataclasses import dataclass

from classes.menu.menu_base import MenuBase


@dataclass
class CurrentMenu:
    """Represents the currently active menu and its navigation breadcrumbs."""

    menu: MenuBase
    breadcrumbs: list[str]
    update_required: bool
