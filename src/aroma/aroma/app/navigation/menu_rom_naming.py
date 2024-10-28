"""Defines the ROM naming preferences menu."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.strings import Strings
from shared.app_config import AppConfig
from shared.constants import (
    CUSTOM_STR,
    STOCK_STR,
)


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

    def _name_format(self) -> MenuItemSingle:
        """Create a menu item for selecting the naming format for ROMs."""
        return self._generate_keyboard_config_item(
            "name_format",
            Strings().name_format,
            [
                Strings().get_mapped_name_format(
                    AppConfig().name_format, include_prefix=True
                ),
                "",
                *Strings().name_format_desc,
                "",
                *Strings().get_format_mapping(": "),
            ],
            Strings().name_format_prompt,
            help_info=[", ".join(Strings().get_format_mapping())],
        )

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        pass

    def _dynamic_menu_default_items(self) -> None:
        pass
