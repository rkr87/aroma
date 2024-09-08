"""
Defines a menu for configuring options, including various settings and choices.
"""

from model.menu_action import MenuAction
from model.menu_item import MenuItem
from navigation.base_menu import BaseMenu


class MenuOptions(BaseMenu):
    """
    Manages the menu for configuring options, providing various settings and
    choices.
    """

    def __init__(self) -> None:
        """
        Initializes the MenuOptions with a title and menu options for
        configuring settings.
        """
        super().__init__("Options", self._build_menu())

    def _build_menu(self) -> list[MenuItem]:
        """
        Builds the options menu with predefined settings choices.
        """
        example = MenuItem([
            MenuAction("Option One", None),
            MenuAction("Option Two", None),
            MenuAction("Option Three", None),
            MenuAction("Option Four", None),
        ])
        return [example]
