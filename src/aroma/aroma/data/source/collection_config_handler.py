"""TODO."""

from dataclasses import asdict
from pathlib import Path

from data.model.collection_config import CollectionConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import COLLECTION_PATH, COLLECTION_TEMPLATES
from shared.tools import util


class CollectionConfigHandler(ClassSingleton):
    """TODO."""

    @staticmethod
    def get_collection(
        collection_path: Path, *, force_aroma: bool = False
    ) -> CollectionConfig:
        """TODO."""
        config_dict = util.load_simple_json(collection_path / "config.json")
        config = CollectionConfig.from_dict(config_dict, collection_path.name)
        if force_aroma:
            config.is_aroma_collection = True
        return config

    @staticmethod
    def get_collections(*, aroma_only: bool = False) -> list[CollectionConfig]:
        """TODO."""
        return [
            config
            for path in COLLECTION_PATH.iterdir()
            if (path / "config.json").is_file()
            and (config := CollectionConfigHandler.get_collection(path))
            and (not aroma_only or config.is_aroma_collection)
        ]

    @staticmethod
    def has_collections() -> bool:
        """TODO."""
        return any(Path(COLLECTION_PATH).iterdir())

    @staticmethod
    def save_collection(config: CollectionConfig) -> None:
        """TODO."""
        util.save_simple_json(
            asdict(config), COLLECTION_PATH / config.directory / "config.json"
        )

    @staticmethod
    def template_exists(directory: str) -> bool:
        """TODO."""
        existing_collections: list[str] = [
            item.directory
            for item in CollectionConfigHandler.get_collections()
        ]
        return directory in existing_collections

    @staticmethod
    def get_templates(*, missing_only: bool = False) -> list[CollectionConfig]:
        """TODO."""
        existing_colls: list[str] = []
        if missing_only:
            existing_colls = [
                item.directory
                for item in CollectionConfigHandler.get_collections()
            ]
        return [
            config
            for path in COLLECTION_TEMPLATES.iterdir()
            if (path / "config.json").is_file()
            and (
                config := CollectionConfigHandler.get_collection(
                    path, force_aroma=True
                )
            )
            and (not missing_only or config.directory not in existing_colls)
        ]
