"""
Defines a menu for configuring options, including various settings and choices.
"""

import logging.config
from collections import OrderedDict
from enum import Enum, auto
from pathlib import Path

from app_config import AppConfig, update_config
from constants import PATH_PREFIX
from menu.menu_base import MenuBase
from menu.menu_item_base import MenuItemBase
from menu.menu_item_multi import MenuItemMulti
from model.side_pane import SidePane
from strings import Strings


class MenuOptions(MenuBase):
    """
    Manages the menu for configuring options, providing various settings and
    choices.
    """

    LANG_FILE_SUFFIX = '.json'
    DEFAULT_LANG = 'english'

    class _Options(Enum):
        """
        Defines the options available in this menu.
        """
        LANGUAGE = auto()
        LOGGING = auto()

    @property
    def Option(self) -> type[_Options]:
        """
        Provides the enum class for this menu's options.
        """
        return self._Options

    def __init__(self) -> None:
        """
        Initializes the MenuOptions with a title and menu options for
        configuring settings.
        """
        self._config = AppConfig()
        super().__init__(Strings().options, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:  # pylint: disable=no-self-use
        """
        Builds the options menu with predefined settings choices.
        """
        logger = MenuOptions.get_static_logger()
        logger.debug("Building Options menu options.")
        return OrderedDict([
            (self.Option.LANGUAGE, self._language()),
            (self.Option.LOGGING, self._logging_level())
        ])

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
    def _set_logging_level(config_attr: str, level: str) -> None:
        """
        Sets the logging level and updates the configuration.
        """
        update_config(config_attr, level)
        logging.getLogger().setLevel(level)

    @staticmethod
    def _set_language(config_attr: str, language: str) -> None:
        """
        Sets the application language and updates the configuration. Reloads
        the strings and rebuilds menus.
        """
        update_config(config_attr, language)
        Strings.load(f"{PATH_PREFIX}/translations/{language}.json")
        for menu in reversed(MenuBase.get_children()):
            menu.rebuild()
