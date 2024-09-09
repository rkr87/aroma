"""
Defines a menu for configuring options, including various settings and choices.
"""

from model.menu_action import MenuAction
from model.menu_item import MenuItem
from model.side_pane import SidePane
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
            "Options",
            self._build_menu(),
            side_pane=SidePane("MenuLevelPane")
        )

    def _build_menu(self) -> list[MenuItem]:  # pylint: disable=no-self-use
        """
        Builds the options menu with predefined settings choices.
        """
        return [
            MenuItem([
                MenuAction("Option One", None, SidePane("ActionLevelPane1")),
                MenuAction("Option Two", None),
                MenuAction("Option Three", None, SidePane("ActionLevelPane2")),
                MenuAction("Option Four", None),
            ],
                side_pane=SidePane("ItemLevelPane")
            ),
            MenuItem([
                MenuAction("Option One", None),
                MenuAction("Option Two", None, SidePane("ActionLevelPane3")),
                MenuAction("Option Three", None),
                MenuAction("Option Four", None, SidePane("ActionLevelPane4")),
            ])
        ]
