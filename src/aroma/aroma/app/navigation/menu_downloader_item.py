"""TODO."""

from collections import OrderedDict
from functools import partial
from pathlib import Path
from typing import Any

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from data.model.rom_detail import RomDetail
from manager.download_manager import download_archive_org_file
from manager.rom_manager import RomManager
from shared.constants import ROM_PATH
from shared.tools import util


class MenuDownloaderItem(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        super().__init__("DOWNLOADER ITEM", OrderedDict())

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        if not identifier or not path:
            raise FileNotFoundError
        logger = MenuDownloaderItem.get_static_logger()
        logger.debug("Building Item Downloader menu options.")
        self.breadcrumb = breadcrumb
        self.content.clear_items()
        data = util.load_simple_json(path)
        existing_files = RomManager().data
        for item in data[identifier]:
            self._create_menu_item(data, path, item, existing_files)

    def _create_menu_item(
        self,
        list_data: dict[str, Any],
        path: Path,
        item: dict[str, Any],
        existing_files: dict[str, RomDetail],
    ) -> None:
        """TODO."""
        key = item["name"].upper()

        def download() -> None:
            """TODO."""
            result = download_archive_org_file(
                list_data["id"],
                item["path"],
                ROM_PATH / path.parent.name / item["name"],
                auth_req=list_data["auth_req"],
            )
            if result:
                self.content.deactivate_item(key)

        menu_item = MenuItemSingle(
            item["name"].upper(),
            partial(
                BackgroundWorker().do_work,
                download,
                "Downloading File...",
            ),
        )
        menu_item.deactivated = (
            f"{path.parent.name}/{item['name']}" in existing_files
        )
        self.content.add_item(key, menu_item)
