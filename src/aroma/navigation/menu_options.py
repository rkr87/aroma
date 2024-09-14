"""
Defines a menu for configuring options, including various settings and choices.
"""

from menu.menu_action import MenuAction
from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_multi import MenuItemMulti
from strings import Strings


class MenuOptions(MenuBase):
    """
    Manages the menu for configuring options, providing various settings and
    choices.
    """

    def __init__(self) -> None:
        """
        Initializes the MenuOptions with a title and menu options for
        configuring settings.
        """
        super().__init__(Strings().options, self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the options menu with predefined settings choices.
        """
        logger = MenuOptions.get_static_logger()
        logger.debug("Building Options menu options.")
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
