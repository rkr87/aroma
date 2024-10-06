"""Defines a menu for configuring options."""

import logging.config
from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
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
        super().__init__(Strings().options, self._build_menu())

    def _build_menu(self) -> OrderedDict[str, MenuItemBase]:  # pylint: disable=no-self-use
        """Build the options menu with predefined settings choices."""
        logger = MenuOptions.get_static_logger()
        logger.debug("Building Options menu options.")
        return OrderedDict(
            [
                ("LANGUAGE", self._language()),
                ("LOGGING", self._logging_level()),
            ],
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
            self._set_logging_level,
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
    def _set_logging_level(level: str) -> None:
        """Set the logging level and update configuration."""
        logging.getLogger().setLevel(level)

    @staticmethod
    def _set_language(language: str) -> None:
        """Set the application language and update configuration."""
        Strings.load(
            APP_TRANSLATION_PATH / f"{language}.json",
            APP_TRANSLATION_PATH / "english.json",
        )
        for menu in reversed(MenuBase.get_children()):
            menu.reset_menu()

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        pass
