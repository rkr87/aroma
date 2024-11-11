"""TODO."""

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_downloader_list import MenuDownloaderList
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from data.source.emu_config_handler import EmuConfigHandler
from shared.constants import ARCHIVE_AUTH_CONFIG, DOWNLOADER_PATH

if TYPE_CHECKING:
    from app.menu.menu_item_base import MenuItemBase


class MenuDownloader(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        """TODO."""
        self.menu_stack: MenuStack = MenuStack()
        self.list_menu: MenuDownloaderList = MenuDownloaderList()
        super().__init__(Strings().downloader, OrderedDict())

    def _dynamic_menu_default_items(self) -> None:
        items: list[tuple[str, MenuItemBase]] = [
            ("ARCHIVE_USER_ID", self._archive_user()),
            ("ARCHIVE_PASSWORD", self._archive_password()),
        ]
        if ARCHIVE_AUTH_CONFIG.is_file():
            items.append(("ARCHIVE_RESET", self._reset_auth()))
        self.content.add_section(*items)

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

    def _reset_auth(self) -> MenuItemSingle:
        """TODO."""

        def reset() -> None:
            ARCHIVE_AUTH_CONFIG.unlink()
            self.regenerate_dynamic_menu()

        return MenuItemSingle(
            Strings().archive_reset,
            reset,
            side_pane=SidePane(
                Strings().archive_reset,
                Strings().archive_reset_desc,
            ),
        )

    def _build_dynamic_menu(
        self,
        path: Path | None = None,  # noqa: ARG002
        identifier: str | None = None,  # noqa: ARG002
    ) -> None:
        for child_path in DOWNLOADER_PATH.iterdir():
            if not child_path.is_dir() or not EmuConfigHandler.is_valid_system(
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
