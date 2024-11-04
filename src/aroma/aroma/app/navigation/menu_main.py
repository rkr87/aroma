"""Defines the main menu of the application."""

from collections import OrderedDict
from pathlib import Path

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collection_management import MenuCollectionManagement
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
        super().__init__(APP_NAME, OrderedDict())
        self._build_menu()

    def _build_menu(self) -> None:
        """Build the initial main menu."""
        logger = self.get_static_logger()
        logger.debug("Building Main menu options.")
        self.content.add_item("COLLECTIONS", self._collections_menu())
        self.content.add_item("ROM_NAMING", self._rom_naming_menu())
        self.content.add_item("IMG_MNGT", self._image_management_menu())
        self.content.add_item("EMU_MNGT", self._emu_management_menu())
        self.content.add_item("DOWNLOADER", self._downloader_menu())
        self.content.add_item("OPTIONS", self._options_menu())
        self.content.add_item("REFRESH", self._refresh_roms())

    def _collections_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.dynamic_sub_menu(
            Strings().collection_management,
            None,
            None,
            MenuCollectionManagement(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().collection_management,
                Strings().collection_management_desc,
            ),
        )

    def _rom_naming_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.sub_menu(
            MenuRomNaming(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().rom_naming,
                Strings().rom_naming_desc,
            ),
        )

    def _image_management_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.sub_menu(
            MenuImageManagement(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().image_management,
                Strings().image_management_desc,
            ),
        )

    def _emu_management_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.dynamic_sub_menu(
            Strings().emu_management,
            None,
            None,
            MenuEmuManagement(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().emu_management,
                Strings().emu_management_desc,
            ),
        )

    def _downloader_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.dynamic_sub_menu(
            Strings().downloader,
            None,
            None,
            MenuDownloader(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().downloader,
                Strings().downloader_desc,
            ),
        )

    def _options_menu(self) -> MenuItemSingle:
        """TODO."""
        return self.sub_menu(
            MenuOptions(),
            MenuStack().push,
            side_pane=SidePane(
                Strings().options,
                Strings().options_desc,
            ),
        )

    @staticmethod
    def _refresh_roms() -> MenuItemSingle:
        """Create a menu item that refreshes the ROM database."""

        def refresh_roms() -> None:
            BackgroundWorker().do_work(
                RomManager().refresh_roms, Strings().refreshing_roms
            )

        return MenuItemSingle(
            Strings().refresh_roms,
            refresh_roms,
            SidePane(Strings().refresh_roms, Strings().refresh_roms_desc),
        )

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        pass

    def _dynamic_menu_default_items(self) -> None:
        pass
