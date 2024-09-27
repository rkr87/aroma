"""Defines the Image Management preferences menu."""

from collections import OrderedDict
from enum import Enum, auto

from classes.menu.menu_action import MenuAction
from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_multi import MenuItemMulti
from classes.menu.menu_item_single import MenuItemSingle
from constants import SCRAPER_MEDIA_TYPES, SCRAPER_REGION_TREE
from manager.rom_manager import RomManager
from model.app_config import AppConfig
from model.side_pane import SidePane
from model.strings import Strings


class MenuImageManagement(MenuBase):
    """A menu for managing Image Management preferences."""

    class _Options(Enum):
        """Defines the options available in this menu."""

        SCRAPE_MISSING = auto()
        SCRAPE_USER = auto()
        SCRAPE_PASSWORD = auto()
        SCRAPE_REGION = auto()
        SCRAPE_MEDIA_TYPE = auto()
        DAYS_TO_RESCRAPE = auto()
        SCRAPE_CPU_THREADS = auto()
        SCRAPE_ON_REFRESH = auto()
        REMOVE_BROKEN = auto()
        REMOVE_BROKEN_REFRESH = auto()

    @property
    def option(self) -> type[_Options]:
        """Provides the enum class for this menu's options."""
        return self._Options

    def __init__(self) -> None:
        super().__init__(Strings().image_management, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """Build and return the menu items."""
        logger = MenuImageManagement.get_static_logger()
        logger.debug("Building Image Management menu options.")

        options: OrderedDict[Enum, MenuItemBase] = OrderedDict(
            [
                (self.option.SCRAPE_MISSING, self._scrape_missing()),
                (self.option.SCRAPE_USER, self._scrape_user()),
                (self.option.SCRAPE_PASSWORD, self._scrape_password()),
                (self.option.SCRAPE_CPU_THREADS, self._scrape_cpu_threads()),
                (self.option.SCRAPE_MEDIA_TYPE, self._scrape_media_type()),
                (self.option.SCRAPE_REGION, self._scrape__region()),
                (self.option.DAYS_TO_RESCRAPE, self._days_to_rescrape()),
                (self.option.SCRAPE_ON_REFRESH, self._scrape_on_refresh()),
                (self.option.REMOVE_BROKEN, self._remove_broken_images()),
                (self.option.REMOVE_BROKEN_REFRESH, self._remove_on_refresh()),
            ],
        )
        return options

    @staticmethod
    def _scrape_missing() -> MenuItemSingle:
        """Create option to scrape missing images."""
        return MenuItemSingle(
            Strings().scrape_missing,
            RomManager().scrape_missing_images,
            SidePane(Strings().scrape_missing, Strings().scrape_missing_desc),
        )

    @staticmethod
    def _scrape_media_type() -> MenuItemMulti:
        """Create option to select media types for scraping."""
        data: dict[str, str] = {i: i.upper() for i in SCRAPER_MEDIA_TYPES}
        actions, current = MenuImageManagement._generate_config_actions(
            data, "scrape_media_type"
        )
        return MenuItemMulti(
            Strings().scrape_media_type,
            actions,
            current,
            SidePane(
                Strings().scrape_media_type,
                Strings().scrape_media_type_desc,
            ),
        )

    @staticmethod
    def _scrape__region() -> MenuItemMulti:
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
        return MenuItemSingle(
            Strings().remove_broken,
            RomManager().remove_broken_images,
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
