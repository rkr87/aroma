"""Defines the RomManager class for managing ROMs and associated resources."""

from data.model.rom_detail import RomDetail
from data.source.name_db import NameDB
from data.source.rom_db import RomDB
from manager.cache_manager import CacheManager
from manager.emu_manager import EmuManager
from manager.image_manager import ImageManager
from shared.app_config import AppConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import ROM_PATH


class RomManager(ClassSingleton):
    """Handles ROM database operations and related image management."""

    def __init__(self) -> None:
        super().__init__()
        self._rom_db = RomDB()

    @property
    def data(self) -> dict[str, RomDetail]:
        """TODO."""
        return self._rom_db.data

    def refresh_roms(self) -> None:
        """Refresh ROMs in the app database and update the TSP cache."""
        self._rom_db.update()
        CacheManager().update_cache_db(self._rom_db.data, ROM_PATH)
        if AppConfig().remove_broken_images_on_refresh:
            ImageManager().remove_broken_images(self._rom_db.valid_paths)
        if AppConfig().scrape_on_refresh:
            ImageManager().scrape_images(self._rom_db.data)
        if AppConfig().clean_emu_on_refresh:
            EmuManager().clean_emus(self._rom_db.data)

    def remove_broken_images(self) -> None:
        """Remove images not associated with valid ROM paths."""
        self._rom_db.update()
        ImageManager().remove_broken_images(self._rom_db.valid_paths)

    def scrape_missing_images(self) -> None:
        """Scrape and download missing images for valid ROMs."""
        self._rom_db.update()
        ImageManager().scrape_images(self._rom_db.data)

    def clean_emus(self) -> None:
        """Scrape and download missing images for valid ROMs."""
        self._rom_db.update()
        EmuManager().clean_emus(self._rom_db.data)

    @staticmethod
    def cleanup() -> None:
        """TODO."""
        NameDB().remove_db()
