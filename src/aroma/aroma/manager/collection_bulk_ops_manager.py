"""TODO."""

from data.source.collection_config_handler import CollectionConfigHandler
from manager.collection_ops_manager import CollectionOpsManager
from shared.classes.class_singleton import ClassSingleton


class CollectionBulkOpsManager(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._operations = CollectionOpsManager()
        self._config = CollectionConfigHandler()

    def create_template_collections(self) -> None:
        """TODO."""
        templates = self._config.get_templates(missing_only=True)
        for item in templates:
            self._operations.create_template_collection(item)

    def delete_all_collections(self) -> None:
        """TODO."""
        for item in self._config.get_collections(aroma_only=True):
            self._operations.delete_collection(item)

    def set_systems_separated_all_collections(
        self, *, separated: bool
    ) -> None:
        """TODO."""
        for item in self._config.get_collections(aroma_only=True):
            self._operations.set_systems_separated(item, separated=separated)
