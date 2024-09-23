"""TODO."""

from classes.base.class_singleton import ClassSingleton
from data.rom_db import RomDB
from manager.cache_manager import CacheManager


class RomManager(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._rom_db = RomDB()
        self._cache = CacheManager()

    def refresh_roms(self) -> None:
        """Refresh ROMs in app database and update TSP cache dbs."""
        self._rom_db.update()
        self._cache.update_cache_db(self._rom_db.data)
