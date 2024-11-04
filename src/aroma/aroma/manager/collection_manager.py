"""TODO."""

from pathlib import Path

from data.model.collection_config import CollectionConfig
from data.model.rom_detail import RomDetail
from data.source.collection_config_handler import CollectionConfigHandler
from manager.cache_manager import CacheManager
from manager.collection_bulk_ops_manager import CollectionBulkOpsManager
from manager.collection_ops_manager import CollectionOpsManager
from manager.collection_shortcut_manager import CollectionShortcutManager
from shared.classes.class_singleton import ClassSingleton
from shared.constants import COLLECTION_PATH


class CollectionManager(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self.operations = CollectionOpsManager()
        self.bulk = CollectionBulkOpsManager()
        self.config = CollectionConfigHandler()
        self.shortcuts = CollectionShortcutManager()
        self.cache = CacheManager()

    def refresh_collection(
        self, collection: CollectionConfig | Path, rom_db: dict[str, RomDetail]
    ) -> None:
        """TODO."""
        if isinstance(collection, Path):
            collection = self.config.get_collection(collection)
        if not collection.is_aroma_collection:
            return
        self.operations.clear_aroma_data(collection)
        shortcuts = self.shortcuts.get_non_aroma_shortcuts(collection, rom_db)
        aroma = self.shortcuts.create_aroma_shortcuts(collection, rom_db)
        shortcuts.update(aroma)
        self.cache.update_cache_db(shortcuts, COLLECTION_PATH)

    def refresh_collections(self, rom_db: dict[str, RomDetail]) -> None:
        """TODO."""
        for collection in self.config.get_collections(aroma_only=True):
            self.refresh_collection(collection, rom_db)
