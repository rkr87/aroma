"""TODO."""

from collections import OrderedDict
from pathlib import Path

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_main import MenuMain
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from shared import constants
from shared.app_config import AppConfig
from updater import Updater


class MenuAppUpdate(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        super().__init__(Strings().update_available, OrderedDict())
        self._build_menu()

    def _build_menu(self) -> None:  # pylint: disable=no-self-use
        """TODO."""
        self.content.add_item("UPDATE", self._update())
        self.content.add_item("START_APP", self._start_app())

    @staticmethod
    def _update() -> MenuItemSingle:
        """TODO."""

        def update() -> None:
            Updater.download_and_extract_release()
            AppConfig().update_user_config(constants.APP_CONFIG_PATH)
            print("AROMA UPDATED|RESTART REQUIRED", flush=True)  # noqa: T201

        def work() -> None:
            BackgroundWorker().do_work(
                update, Strings().applying_update, exit_on_complete=True
            )

        return MenuItemSingle(
            Strings().update,
            work,
            SidePane(Strings().update, Strings().update_desc),
            non_tsp_skip=True,
        )

    @staticmethod
    def _start_app() -> MenuItemSingle:
        """TODO."""

        def start() -> None:
            MenuStack().push(MenuMain(), reset=True)

        return MenuItemSingle(
            Strings().launch_app,
            start,
            SidePane(Strings().launch_app, Strings().launch_app_desc),
        )

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        pass

    def _dynamic_menu_default_items(self) -> None:
        pass
