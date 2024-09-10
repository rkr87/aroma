"""
Defines a menu for configuring options, including various settings and choices.
"""

from model.menu_action import MenuAction
from model.menu_item_base import MenuItemBase
from model.menu_item_multi import MenuItemMulti
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
        super().__init__(
            "OPTIONS",
            self._build_menu()
        )

    def _build_menu(self) -> list[MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the options menu with predefined settings choices.
        """
        return [
            MenuItemMulti(
                "Option",
                [
                    MenuAction("One", None),
                    MenuAction("Two", None),
                    MenuAction("Three", None),
                    MenuAction("Four", None),
                ]
            )
        ]
