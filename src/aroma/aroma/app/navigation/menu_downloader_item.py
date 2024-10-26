"""TODO."""

from collections import OrderedDict
from functools import partial
from pathlib import Path
from typing import Any

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.strings import Strings
from manager.download_manager import download_archive_org_file
from shared.constants import ROM_PATH
from shared.tools import util


class MenuDownloaderItem(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        super().__init__("DOWNLOADER ITEM", OrderedDict())

    def _dynamic_menu_default_items(self) -> None:
        pass

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        if not identifier or not path:
            raise FileNotFoundError
        data = util.load_simple_json(path)
        for item in data[identifier]:
            self._create_menu_item(data, path, item)

    def _create_menu_item(
        self,
        list_data: dict[str, Any],
        path: Path,
        item: dict[str, Any],
    ) -> None:
        """TODO."""
        key = item["name"].upper()
        target_file = ROM_PATH / path.parent.name / str(item["name"])

        def download() -> None:
            """TODO."""
            result = download_archive_org_file(
                list_data["id"],
                item["path"],
                target_file,
                auth_req=list_data["auth_req"],
            )
            if result:
                self.content.deactivate_item(key)

        menu_item = MenuItemSingle(
            item["name"].upper(),
            partial(
                BackgroundWorker().do_work,
                download,
                Strings().downloading_file,
            ),
        )
        menu_item.deactivated = target_file.is_file()
        self.content.add_item(key, menu_item)
