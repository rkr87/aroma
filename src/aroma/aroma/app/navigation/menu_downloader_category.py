"""TODO."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.model.side_pane import SidePane
from app.navigation.menu_downloader_item import MenuDownloaderItem
from app.navigation.menu_stack import MenuStack
from shared.tools import util


class MenuDownloaderCategory(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.item_menu: MenuDownloaderItem = MenuDownloaderItem()

        super().__init__("DOWNLOADER CATEGORY", OrderedDict())

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self,
        breadcrumb: str,
        path: Path | None,
        identifier: str | None = None,  # noqa: ARG002
    ) -> None:
        if not path:
            raise FileNotFoundError
        logger = MenuDownloaderCategory.get_static_logger()
        logger.debug("Building System Downloader menu options.")
        self.breadcrumb = breadcrumb
        self.content.clear_items()
        for category, items in util.load_simple_json(path).items():
            if category in {"id", "desc", "auth_req"}:
                continue
            self.content.add_item(
                category,
                self.dynamic_sub_menu(
                    category.upper(),
                    path,
                    category,
                    self.item_menu,
                    self.menu_stack.push,
                    side_pane=SidePane(
                        category.upper(),
                        [item["name"] for item in items],
                    ),
                ),
            )
