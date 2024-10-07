"""Defines the main menu of the application."""

from collections import OrderedDict
from pathlib import Path

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collections import MenuCollections
from app.navigation.menu_downloader import MenuDownloader
from app.navigation.menu_emu_management import MenuEmuManagement
from app.navigation.menu_image_management import MenuImageManagement
from app.navigation.menu_options import MenuOptions
from app.navigation.menu_rom_naming import MenuRomNaming
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from manager.rom_manager import RomManager
from shared.constants import APP_NAME


class MenuMain(MenuBase):
    """Manages the main menu."""

    def __init__(self) -> None:
        super().__init__(APP_NAME, self._build_menu())

    def _build_menu(self) -> OrderedDict[str, MenuItemBase]:
        """Build the initial main menu."""
        logger = self.get_static_logger()
        logger.debug("Building Main menu options.")
        return OrderedDict(
            [
                (
                    "COLLECTIONS",
                    self.sub_menu(
                        MenuCollections(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().collections,
                            Strings().collections_desc,
                        ),
                    ),
                ),
                (
                    "ROM_NAMING",
                    self.sub_menu(
                        MenuRomNaming(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().rom_naming,
                            Strings().rom_naming_desc,
                        ),
                    ),
                ),
                (
                    "IMG_MNGT",
                    self.sub_menu(
                        MenuImageManagement(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().image_management,
                            Strings().image_management_desc,
                        ),
                    ),
                ),
                (
                    "EMU_MNGT",
                    self.dynamic_sub_menu(
                        Strings().emu_management,
                        None,
                        None,
                        MenuEmuManagement(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().emu_management,
                            Strings().emu_management_desc,
                        ),
                    ),
                ),
                (
                    "DOWNLOADER",
                    self.dynamic_sub_menu(
                        Strings().downloader,
                        None,
                        None,
                        MenuDownloader(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().downloader,
                            Strings().downloader_desc,
                        ),
                    ),
                ),
                (
                    "OPTIONS",
                    self.sub_menu(
                        MenuOptions(),
                        MenuStack().push,
                        side_pane=SidePane(
                            Strings().options,
                            Strings().options_desc,
                        ),
                    ),
                ),
                ("REFRESH", self._refresh_roms()),
            ],
        )

    @staticmethod
    def _refresh_roms() -> MenuItemSingle:
        """Create a menu item that refreshes the ROM database."""

        def refresh_roms() -> None:
            """TODO."""
            BackgroundWorker().do_work(
                RomManager().refresh_roms, Strings().refreshing_roms
            )

        return MenuItemSingle(
            Strings().refresh_roms,
            refresh_roms,
            SidePane(Strings().refresh_roms, Strings().refresh_roms_desc),
        )

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self, breadcrumb: str, path: Path | None, identifier: str | None
    ) -> None:
        pass
