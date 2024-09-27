"""Defines the ROM naming preferences menu."""

from collections import OrderedDict
from enum import Enum, auto
from typing import TYPE_CHECKING

from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_multi import MenuItemMulti
from constants import (
    CUSTOM_STR,
    NAMING_ADDITIONAL_ID,
    NAMING_DISC_ID,
    NAMING_FORMAT_ID,
    NAMING_FORMATS_RESOURCE,
    NAMING_HACK_ID,
    NAMING_NAME_ID,
    NAMING_REGION_ID,
    NAMING_TITLE_ID,
    NAMING_VERSION_ID,
    NAMING_YEAR_ID,
    STOCK_STR,
)
from model.app_config import AppConfig
from model.side_pane import SidePane
from model.strings import Strings
from tools import util
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
        formats: list[str] = util.load_simple_json(NAMING_FORMATS_RESOURCE)[
            "formats"
        ]

        def _replace_var(unformatted: str) -> str:
            s = Strings()
            mapping: dict[str, str] = {
                NAMING_TITLE_ID: s.naming_title_desc,
                NAMING_NAME_ID: s.naming_name_desc,
                NAMING_REGION_ID: s.naming_region_desc,
                NAMING_DISC_ID: s.naming_disc_desc,
                NAMING_FORMAT_ID: s.naming_format_desc,
                NAMING_HACK_ID: s.naming_hack_desc,
                NAMING_VERSION_ID: s.naming_version_desc,
                NAMING_YEAR_ID: s.naming_year_desc,
                NAMING_ADDITIONAL_ID: s.naming_additional_desc,
            }
            formatted = unformatted.lower()
            for k, v in mapping.items():
                formatted = formatted.replace(k, v)
            return formatted

        data: dict[str, str] = {k.lower(): _replace_var(k) for k in formats}
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
