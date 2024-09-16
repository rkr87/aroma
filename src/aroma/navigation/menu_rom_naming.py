"""
Defines the ROM naming preferences menu, allowing users to manage
arcade ROM naming libraries.
"""


from collections import OrderedDict
from enum import Enum, auto

from action.action_rom_naming import ActionRomNaming
from app_config import AppConfig
from constants import CUSTOM_STR, STOCK_STR
from menu.menu_action import MenuAction
from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_multi import MenuItemMulti
from model.side_pane import SidePane
from strings import Strings


class MenuRomNaming(MenuBase):
    """
    A menu for managing ROM naming preferences.
    """

    class _Options(Enum):
        """
        Defines the options available in this menu.
        """
        ARCADE_NAMING = auto()
        NAMING_METHOD = auto()
        CONSOLE_NAMING = auto()
        NAME_FORMAT = auto()

    @property
    def Option(self) -> type[_Options]:
        """
        Provides the enum class for this menu's options.
        """
        return self._Options

    def __init__(self) -> None:
        """
        Initialize the ROM naming menu with arcade ROM naming options.
        """
        super().__init__(Strings().rom_naming, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """
        Build the menu for selecting between stock and custom arcade ROM
        naming libraries.
        """
        logger = MenuRomNaming.get_static_logger()
        logger.debug("Building Rom Naming menu options.")

        options: OrderedDict[Enum, MenuItemBase] = OrderedDict([
            (self.Option.NAMING_METHOD, self._naming_method())
        ])

        if AppConfig().naming_method == STOCK_STR:
            options[self.Option.ARCADE_NAMING] = self._arcade_rom_naming()
            return options

        options[self.Option.CONSOLE_NAMING] = self._console_naming()
        options[self.Option.NAME_FORMAT] = self._name_format()
        return options

    @staticmethod
    def _naming_method() -> MenuItemMulti:
        """
        TODO
        """
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom
        }
        actions, current = MenuBase._generate_config_actions(
            data,
            "naming_method",
            MenuRomNaming._rebuild_menu
        )
        return MenuItemMulti(
            Strings().naming_method,
            actions,
            current,
            SidePane(Strings().naming_method, Strings().naming_method_desc)
        )

    @staticmethod
    def _console_naming() -> MenuItemMulti:
        """
        TODO
        """
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom
        }
        actions, current = MenuBase._generate_config_actions(
            data,
            "console_naming"
        )
        return MenuItemMulti(
            Strings().console_naming,
            actions,
            current,
            SidePane(Strings().console_naming, Strings().console_naming_desc)
        )

    @staticmethod
    def _name_format() -> MenuItemMulti:
        """
        TODO
        """
        data: dict[str, str] = {
            "NONE": Strings().name_format_none,
            "NAME": Strings().name_format_name_only,
            "NAME_R": Strings().name_format_name_region,
            "NAME_D": Strings().name_format_name_disc,
            "NAME_R_D": Strings().name_format_name_region_disc
        }
        actions, current = MenuBase._generate_config_actions(
            data,
            "name_format"
        )
        return MenuItemMulti(
            Strings().name_format,
            actions,
            current,
            SidePane(Strings().name_format, Strings().name_format_desc)
        )

    @staticmethod
    def _arcade_rom_naming() -> MenuItemMulti:
        """
        Create a menu item for selecting between stock and custom ROM naming
        libraries, showing their current installation state.
        """
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom
        }
        actions: list[MenuAction] = MenuBase._generate_actions(
            data,
            ActionRomNaming.install_arcade_library,
            True
        )
        return MenuItemMulti(
            Strings().arcade_naming,
            actions,
            ActionRomNaming.get_arcade_library_status(data),
            SidePane(Strings().arcade_naming, Strings().arcade_naming_desc)
        )

    @staticmethod
    def _rebuild_menu(method: str) -> None:
        """TODO"""
        logger = MenuRomNaming.get_static_logger()
        logger.info("Rebuilding menu for %s naming method.", method)
        MenuRomNaming().rebuild()
