"""TODO."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_downloader_list import MenuDownloaderList
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from manager.emu_manager import EmuManager
from shared.constants import DOWNLOADER_PATH


class MenuDownloader(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        """TODO."""
        self.menu_stack: MenuStack = MenuStack()
        self.list_menu: MenuDownloaderList = MenuDownloaderList()
        super().__init__(Strings().downloader, self.default_items())

    def default_items(self) -> OrderedDict[str, MenuItemBase]:
        """TODO."""
        a_pw = self._archive_password()
        a_pw.bottom_separator = True
        return OrderedDict(
            [
                ("ARCHIVE_USER_ID", self._archive_user()),
                ("ARCHIVE_PASSWORD", a_pw),
            ]
        )

    def _archive_user(self) -> MenuItemSingle:
        """TODO."""
        return self._generate_keyboard_config_item(
            "archive_userid",
            Strings().archive_user,
            Strings().archive_user_desc,
            Strings().archive_user_prompt,
        )

    def _archive_password(self) -> MenuItemSingle:
        """TODO."""
        return self._generate_keyboard_config_item(
            "archive_password",
            Strings().archive_password,
            Strings().archive_password_desc,
            Strings().archive_password_prompt,
        )

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self,
        breadcrumb: str,
        path: Path | None = None,  # noqa: ARG002
        identifier: str | None = None,  # noqa: ARG002
    ) -> None:
        logger = MenuDownloader.get_static_logger()
        logger.debug("Building Downloader menu options.")

        self.breadcrumb = breadcrumb
        self.content.clear_items()
        self.content.items = self.default_items()
        for child_path in DOWNLOADER_PATH.iterdir():
            if not child_path.is_dir() or not EmuManager.is_valid_system(
                child_path.name
            ):
                continue
            self.content.add_item(
                child_path.name.upper(),
                self.dynamic_sub_menu(
                    child_path.name.upper(),
                    child_path,
                    None,
                    self.list_menu,
                    self.menu_stack.push,
                    side_pane=SidePane(
                        child_path.name.upper(),
                        [file.stem for file in child_path.glob("*.json")],
                    ),
                ),
            )
