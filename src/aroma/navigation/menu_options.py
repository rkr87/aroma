"""
Defines a menu for configuring options, including various settings and choices.
"""

import logging.config
from collections.abc import Callable
from functools import partial
from pathlib import Path

from app_config import AppConfig
from constants import PATH_PREFIX
from menu.menu_action import MenuAction
from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_multi import MenuItemMulti
from model.side_pane import SidePane
from strings import Strings


def _update_config(option: str, level: str) -> None:
    """
    Updates the configuration with the specified option and value.
    """
    AppConfig().update_value(option, level)


class MenuOptions(MenuBase):
    """
    Manages the menu for configuring options, providing various settings and
    choices.
    """

    LANG_FILE_SUFFIX = '.json'
    DEFAULT_LANG = 'english'

    def __init__(self) -> None:
        """
        Initializes the MenuOptions with a title and menu options for
        configuring settings.
        """
        self._config = AppConfig()
        super().__init__(Strings().options, self._build_menu())

    def _build_menu(self) -> list[MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the options menu with predefined settings choices.
        """
        logger = MenuOptions.get_static_logger()
        logger.debug("Building Options menu options.")
        return [
            self._language(),
            self._logging_level()
        ]

    def _language(self) -> MenuItemMulti:
        """
        Creates a menu item for selecting the language from available options.
        """
        directory = Path(f'{PATH_PREFIX}/translations')

        data: dict[str, str] = {}
        default: int = 0
        for i, f in enumerate(directory.iterdir()):
            if f.is_file() and f.suffix == self.LANG_FILE_SUFFIX:
                data[f.stem] = f.stem.upper()
            if f.stem.lower() == self.DEFAULT_LANG:
                default = i

        actions, current = self._generate_config_actions(
            data,
            "language",
            self._set_language,
            default=default
        )
        return MenuItemMulti(
            Strings().language,
            actions,
            current,
            SidePane(
                Strings().language,
                Strings().language_desc
            )
        )

    def _logging_level(self) -> MenuItemMulti:
        """
        Creates a menu item for selecting the logging level from predefined
        options.
        """
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
            1
        )
        return MenuItemMulti(
            Strings().logging_level,
            actions,
            current,
            SidePane(
                Strings().logging_level,
                Strings().logging_desc
            )
        )

    @staticmethod
    def _generate_config_actions(
        data: dict[str, str],
        config_attr: str,
        function: Callable[[str, str], None] = _update_config,
        default: int = 0
    ) -> tuple[list[MenuAction], int]:
        """
        Generates a list of menu actions for configuring a specific option and
        determines the current selection.
        """
        current = default
        if (val := AppConfig().get_value(config_attr)) in data:
            current = list(data).index(val)

        actions = [
            MenuAction(v, partial(function, config_attr, k))
            for k, v in data.items()
        ]
        return actions, current

    @staticmethod
    def _set_logging_level(config_attr: str, level: str) -> None:
        """
        Sets the logging level and updates the configuration.
        """
        _update_config(config_attr, level)
        logging.getLogger().setLevel(level)

    @staticmethod
    def _set_language(config_attr: str, language: str) -> None:
        """
        Sets the application language and updates the configuration. Reloads
        the strings and rebuilds menus.
        """
        _update_config(config_attr, language)
        Strings.load(f"{PATH_PREFIX}/translations/{language}.json")
        for menu in reversed(MenuBase.get_children()):
            menu.rebuild()
