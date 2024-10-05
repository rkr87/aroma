"""TODO."""

from collections import OrderedDict
from pathlib import Path

from app.navigation.menu_downloader_category import MenuDownloaderCategory
from app.navigation.menu_stack import MenuStack
from classes.menu.menu_base import MenuBase
from model.side_pane import SidePane
from tools import util
from tools.app_config import AppConfig


class MenuDownloaderList(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        """TODO."""
        self.menu_stack: MenuStack = MenuStack()
        self.category_menu: MenuDownloaderCategory = MenuDownloaderCategory()
        super().__init__("DOWNLOADER LIST", OrderedDict())

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self,
        breadcrumb: str,
        path: Path | None,
        identifier: str | None = None,  # noqa: ARG002
    ) -> None:
        if not path:
            raise FileNotFoundError
        logger = MenuDownloaderList.get_static_logger()
        logger.debug("Building System Downloader menu options.")
        self.breadcrumb = breadcrumb
        file_type: str = ".json"
        self.content.clear_items()
        for list_file in path.iterdir():
            if not list_file.is_file() or list_file.suffix != file_type:
                continue
            data = util.load_simple_json(list_file)
            if data["auth_req"] and (
                not AppConfig().archive_password
                or not AppConfig().archive_userid
            ):
                continue
            self.content.add_item(
                list_file.stem.upper(),
                self.dynamic_sub_menu(
                    list_file.stem.upper(),
                    list_file,
                    None,
                    self.category_menu,
                    self.menu_stack.push,
                    side_pane=SidePane(
                        list_file.stem.upper(),
                        data["desc"],
                    ),
                ),
            )