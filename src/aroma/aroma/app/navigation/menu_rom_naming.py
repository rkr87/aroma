"""Defines the ROM naming preferences menu."""

from collections import OrderedDict
from enum import Enum, auto
from typing import TYPE_CHECKING

from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_multi import MenuItemMulti
from constants import CUSTOM_STR, STOCK_STR
from model.app_config import AppConfig
from model.side_pane import SidePane
from model.strings import Strings
from tools.library_manager import LibraryManager

if TYPE_CHECKING:
    from classes.menu.menu_action import MenuAction


class MenuRomNaming(MenuBase):
    """A menu for managing ROM naming preferences."""

    class _Options(Enum):
        """Defines the options available in this menu."""

        ARCADE_NAMING = auto()
        NAMING_METHOD = auto()
        CONSOLE_NAMING = auto()
        NAME_FORMAT = auto()

    @property
    def option(self) -> type[_Options]:
        """Provides the enum class for this menu's options."""
        return self._Options

    def __init__(self) -> None:
        """Initialize the ROM naming menu with arcade ROM naming options."""
        super().__init__(Strings().rom_naming, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """Build the menu."""
        logger = MenuRomNaming.get_static_logger()
        logger.debug("Building Rom Naming menu options.")

        options: OrderedDict[Enum, MenuItemBase] = OrderedDict(
            [
                (self.option.NAMING_METHOD, self._naming_method()),
            ],
        )

        if AppConfig().naming_method == STOCK_STR:
            options[self.option.ARCADE_NAMING] = self._arcade_rom_naming()
            return options

        options[self.option.CONSOLE_NAMING] = self._console_naming()
        options[self.option.NAME_FORMAT] = self._name_format()
        return options

    def _naming_method(self) -> MenuItemMulti:
        """Create a menu item for selecting the naming method."""
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom,
        }
        actions, current = self._generate_config_actions(
            data,
            "naming_method",
            self._rebuild_menu,
        )
        return MenuItemMulti(
            Strings().naming_method,
            actions,
            current,
            SidePane(Strings().naming_method, Strings().naming_method_desc),
        )

    @staticmethod
    def _console_naming() -> MenuItemMulti:
        """Create a menu item for managing console naming preferences."""
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom,
        }
        actions, current = MenuRomNaming._generate_config_actions(
            data,
            "console_naming",
            AppConfig().set_db_rebuild_required,
        )
        return MenuItemMulti(
            Strings().console_naming,
            actions,
            current,
            SidePane(Strings().console_naming, Strings().console_naming_desc),
        )

    @staticmethod
    def _name_format() -> MenuItemMulti:
        """Create a menu item for selecting the naming format for ROMs."""
        data: dict[str, str] = {
            "NONE": Strings().name_format_none,
            "NAME": Strings().name_format_name_only,
            "NAME_R": Strings().name_format_name_region,
            "NAME_D": Strings().name_format_name_disc,
            "NAME_R_D": Strings().name_format_name_region_disc,
        }
        actions, current = MenuRomNaming._generate_config_actions(
            data,
            "name_format",
        )
        return MenuItemMulti(
            Strings().name_format,
            actions,
            current,
            SidePane(Strings().name_format, Strings().name_format_desc),
        )

    @staticmethod
    def _arcade_rom_naming() -> MenuItemMulti:
        """Create menu item for selecting arcade ROM naming libraries."""
        data: dict[str, str] = {
            STOCK_STR: Strings().stock,
            CUSTOM_STR: Strings().custom,
        }
        actions: list[MenuAction] = MenuRomNaming._generate_actions(
            data,
            LibraryManager.install_arcade_library,
            non_tsp_skip=True,
        )
        return MenuItemMulti(
            Strings().arcade_naming,
            actions,
            LibraryManager.get_arcade_library_status(data),
            SidePane(Strings().arcade_naming, Strings().arcade_naming_desc),
        )
