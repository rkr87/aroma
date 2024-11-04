"""Defines a menu for configuring options."""

import logging.config
from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.model.side_pane import SidePane
from app.strings import Strings
from shared.app_config import AppConfig
from shared.constants import APP_TRANSLATION_PATH


class MenuOptions(MenuBase):
    """Manages the menu for configuring options choices."""

    LANG_FILE_SUFFIX = ".json"
    DEFAULT_LANG = "english"

    def __init__(self) -> None:
        self._config = AppConfig()
        super().__init__(Strings().options, OrderedDict())
        self._build_menu()

    def _build_menu(self) -> None:  # pylint: disable=no-self-use
        """Build the options menu with predefined settings choices."""
        logger = MenuOptions.get_static_logger()
        logger.debug("Building Options menu options.")
        self.content.add_item("LANGUAGE", self._language())
        self.content.add_item("UPDATES", self._check_for_updates())
        self.content.add_item("LOGGING", self._logging_level())

    def _check_for_updates(self) -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = self._generate_config_actions(
            data, "check_for_updates"
        )
        return MenuItemMulti(
            Strings().check_for_updates,
            actions,
            current,
            SidePane(
                Strings().check_for_updates,
                Strings().check_for_updates_desc,
            ),
        )

    def _language(self) -> MenuItemMulti:
        """Create menu item for selecting the language."""
        data: dict[str, str] = {}
        default: int = 0
        for i, f in enumerate(APP_TRANSLATION_PATH.iterdir()):
            if f.is_file() and f.suffix == self.LANG_FILE_SUFFIX:
                data[f.stem] = f.stem.upper()
            if f.stem.lower() == self.DEFAULT_LANG:
                default = i

        actions, current = self._generate_config_actions(
            data,
            "language",
            self._set_language,
            default=default,
        )
        return MenuItemMulti(
            Strings().language,
            actions,
            current,
            SidePane(
                Strings().language,
                Strings().language_desc,
            ),
        )

    def _logging_level(self) -> MenuItemMulti:
        """Create menu item for selecting the logging level."""
        data: dict[str, str] = {
            "DEBUG": Strings().logging_debug,
            "INFO": Strings().logging_info,
            "WARNING": Strings().logging_warning,
            "ERROR": Strings().logging_error,
        }
        actions, current = self._generate_config_actions(
            data,
            "logging_level",
            logging.getLogger().setLevel,
            1,
        )
        return MenuItemMulti(
            Strings().logging_level,
            actions,
            current,
            SidePane(
                Strings().logging_level,
                Strings().logging_desc,
            ),
        )

    @staticmethod
    def _set_language(language: str) -> None:
        """Set the application language and update configuration."""
        Strings.load(
            APP_TRANSLATION_PATH / f"{language}.json",
            APP_TRANSLATION_PATH / "english.json",
        )
        for menu in reversed(MenuBase.get_children()):
            menu.reset_menu()

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        pass

    def _dynamic_menu_default_items(self) -> None:
        pass
