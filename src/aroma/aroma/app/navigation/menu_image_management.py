"""Defines the Image Management preferences menu."""

from collections import OrderedDict
from pathlib import Path

from app.background_worker import BackgroundWorker
from app.menu.menu_action import MenuAction
from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.strings import Strings
from manager.rom_manager import RomManager
from shared.app_config import AppConfig
from shared.constants import (
    RESOURCES,
    SCRAPER_MEDIA_TYPES,
    SCRAPER_REGION_TREE,
)


class MenuImageManagement(MenuBase):
    """A menu for managing Image Management preferences."""

    def __init__(self) -> None:
        super().__init__(Strings().image_management, self._build_menu())

    def _build_menu(self) -> OrderedDict[str, MenuItemBase]:
        """Build and return the menu items."""
        logger = MenuImageManagement.get_static_logger()
        logger.debug("Building Image Management menu options.")

        options: OrderedDict[str, MenuItemBase] = OrderedDict(
            [
                ("SCRAPE_MISSING", self._scrape_missing()),
                ("SCRAPE_USER", self._scrape_user()),
                ("SCRAPE_PASSWORD", self._scrape_password()),
                ("SCRAPE_CPU_THREADS", self._scrape_cpu_threads()),
                ("SCRAPE_MEDIA_TYPE", self._scrape_media_type()),
                ("SCRAPE_REGION", self._scrape_region()),
                ("DAYS_TO_RESCRAPE", self._days_to_rescrape()),
                ("SCRAPE_ON_REFRESH", self._scrape_on_refresh()),
                ("REMOVE_BROKEN", self._remove_broken_images()),
                ("REMOVE_BROKEN_REFRESH", self._remove_on_refresh()),
            ],
        )
        return options

    @staticmethod
    def _scrape_missing() -> MenuItemSingle:
        """Create option to scrape missing images."""

        def scrape() -> None:
            """TODO."""
            BackgroundWorker().do_work(
                RomManager().scrape_missing_images, Strings().scraping_imgs
            )

        return MenuItemSingle(
            Strings().scrape_missing,
            scrape,
            SidePane(Strings().scrape_missing, Strings().scrape_missing_desc),
        )

    @staticmethod
    def _scrape_media_type() -> MenuItemMulti:
        """Create option to select media types for scraping."""
        data: dict[str, tuple[str, SidePane]] = {
            i: (
                i.upper(),
                SidePane(
                    header=f"{Strings().scrape_media_type}: {i.upper()}",
                    img=f"{RESOURCES}/scraping/{i}.png",
                ),
            )
            for i in SCRAPER_MEDIA_TYPES
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "scrape_media_type"
        )
        return MenuItemMulti(
            Strings().scrape_media_type,
            actions,
            current,
            SidePane(content=Strings().scrape_media_type_desc),
        )

    @staticmethod
    def _scrape_region() -> MenuItemMulti:
        """Create option to select scraping region."""
        data: dict[str, str] = {
            i: str(Strings().get_value(f"scrape_region_{i}")).upper()
            for i in SCRAPER_REGION_TREE
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "scrape_preferred_region"
        )
        return MenuItemMulti(
            Strings().scrape_preferred_region,
            actions,
            current,
            SidePane(
                Strings().scrape_preferred_region,
                Strings().scrape_preferred_region_desc,
            ),
        )

    @staticmethod
    def _scrape_cpu_threads() -> MenuItemMulti:
        """Create option to select number of CPU threads."""
        data: dict[int, str] = {i: str(i) for i in range(0, 33, 4)}
        actions, current = MenuImageManagement._generate_config_actions(
            data, "_scrape_cpu_threads"
        )
        return MenuItemMulti(
            Strings().scrape_max_cpu_threads,
            actions,
            current,
            SidePane(
                Strings().scrape_max_cpu_threads,
                Strings().scrape_max_cpu_threads_desc,
            ),
        )

    @staticmethod
    def _scrape_user() -> MenuItemMulti:
        """Create option to input scraping user credentials."""
        return MenuItemMulti(
            Strings().scrape_user,
            [MenuAction(AppConfig().screenscraper_userid.upper(), None)],
            0,
            SidePane(
                Strings().scrape_user,
                Strings().scrape_user_desc,
            ),
        )

    @staticmethod
    def _scrape_password() -> MenuItemMulti:
        """Create option to input scraping password."""
        return MenuItemMulti(
            Strings().scrape_password,
            [MenuAction(AppConfig().screenscraper_password, None)],
            0,
            SidePane(
                Strings().scrape_password,
                Strings().scrape_password_desc,
            ),
        )

    @staticmethod
    def _days_to_rescrape() -> MenuItemMulti:
        """Create option to select interval days for rescraping."""
        data: dict[int, str] = {
            -1: Strings().scrape_days_to_retry_never,
            0: Strings().scrape_days_to_retry_always,
            7: f"7 {Strings().scrape_days_to_retry_days}",
            14: f"14 {Strings().scrape_days_to_retry_days}",
            30: f"30 {Strings().scrape_days_to_retry_days}",
            90: f"90 {Strings().scrape_days_to_retry_days}",
            180: f"180 {Strings().scrape_days_to_retry_days}",
            365: f"365 {Strings().scrape_days_to_retry_days}",
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "days_until_scrape_attempt"
        )
        return MenuItemMulti(
            Strings().scrape_days_to_retry,
            actions,
            current,
            SidePane(
                Strings().scrape_days_to_retry,
                Strings().scrape_days_to_retry_desc,
            ),
        )

    @staticmethod
    def _scrape_on_refresh() -> MenuItemMulti:
        """Create option to toggle scraping on refresh."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "scrape_on_refresh"
        )
        return MenuItemMulti(
            Strings().scrape_missing_refresh,
            actions,
            current,
            SidePane(
                Strings().scrape_missing_refresh,
                Strings().scrape_missing_refresh_desc,
            ),
        )

    @staticmethod
    def _remove_broken_images() -> MenuItemSingle:
        """Create option to remove broken images."""

        def remove() -> None:
            """TODO."""
            BackgroundWorker().do_work(
                RomManager().remove_broken_images,
                Strings().removing_broken_imgs,
            )

        return MenuItemSingle(
            Strings().remove_broken,
            remove,
            SidePane(Strings().remove_broken, Strings().remove_broken_desc),
        )

    @staticmethod
    def _remove_on_refresh() -> MenuItemMulti:
        """Create option to toggle removal of broken images on refresh."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "remove_broken_images_on_refresh"
        )
        return MenuItemMulti(
            Strings().remove_broken_refresh,
            actions,
            current,
            SidePane(
                Strings().remove_broken_refresh,
                Strings().remove_broken_refresh_desc,
            ),
        )

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        pass
