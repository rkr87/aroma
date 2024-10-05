"""TODO."""

from collections import OrderedDict
from functools import partial
from pathlib import Path

from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_single import MenuItemSingle
from constants import ROM_PATH
from data.archive_api import download_file
from data.rom_db import RomDB
from tools import util


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
        existing_files = RomDB().data
        for item in data[identifier]:
            menu_item = MenuItemSingle(
                item["name"].upper(),
                partial(
                    download_file,
                    data["id"],
                    item["path"],
                    ROM_PATH / path.parent.name / item["name"],
                    auth_req=data["auth_req"],
                ),
            )
            menu_item.deactivated = (
                f"{path.parent.name}/{item["name"]}" in existing_files
            )
            self.content.add_item(item["name"].upper(), menu_item)