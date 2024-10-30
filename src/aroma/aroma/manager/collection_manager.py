"""TODO."""

from data.source.collection_config_handler import CollectionConfigHandler
from manager.collection_bulk_ops_manager import CollectionBulkOpsManager
from manager.collection_ops_manager import CollectionOpsManager
from shared.classes.class_singleton import ClassSingleton


class CollectionManager(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self.operations = CollectionOpsManager()
        self.bulk = CollectionBulkOpsManager()
        self.config = CollectionConfigHandler()
