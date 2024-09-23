"""TODO."""

from classes.base.class_singleton import ClassSingleton
from data.rom_db import RomDB
from manager.cache_manager import CacheManager
from manager.image_manager import ImageManager
from model.app_config import AppConfig


class RomManager(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._rom_db = RomDB()
        self._cache = CacheManager()
        self._images = ImageManager()

    def refresh_roms(self) -> None:
        """Refresh ROMs in app database and update TSP cache dbs."""
        self._rom_db.update()
        self._cache.update_cache_db(self._rom_db.data)
        if AppConfig().remove_broken_images_on_refresh:
            self._images.remove_broken_images(self._rom_db.valid_paths)

    def remove_broken_images(self) -> None:
        """Remove images not associated with valid ROM paths."""
        self._rom_db.update()
        self._images.remove_broken_images(self._rom_db.valid_paths)
