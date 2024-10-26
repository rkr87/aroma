"""Defines the ROM naming preferences menu."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.model.side_pane import SidePane
from app.strings import Strings
from shared.app_config import AppConfig
from shared.constants import (
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
from shared.tools import util


class MenuRomNaming(MenuBase):
    """A menu for managing ROM naming preferences."""

    def __init__(self) -> None:
        """Initialise the ROM naming menu with arcade ROM naming options."""
        super().__init__(Strings().rom_naming, OrderedDict())
        self._build_menu()

    def _build_menu(self) -> None:
        """Build the menu."""
        logger = MenuRomNaming.get_static_logger()
        logger.debug("Building Rom Naming menu options.")
        self.content.add_item("CONSOLE_NAMING", self._console_naming())
        self.content.add_item("NAME_FORMAT", self._name_format())

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

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        pass

    def _dynamic_menu_default_items(self) -> None:
        pass
