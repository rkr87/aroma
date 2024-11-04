"""TODO."""

from dataclasses import asdict
from pathlib import Path

from data.model.collection_config import CollectionConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    COLLAGEN_PATHS,
    COLLECTION_PATH,
    COLLECTION_TEMPLATES,
)
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
    def collection_exists(directory: str, *, aroma_only: bool = False) -> bool:
        """TODO."""
        return directory in CollectionConfigHandler._get_existing_coll_names(
            aroma_only=aroma_only
        )

    @staticmethod
    def _get_existing_coll_names(*, aroma_only: bool = False) -> set[str]:
        """TODO."""
        return {
            item.directory
            for item in CollectionConfigHandler.get_collections(
                aroma_only=aroma_only
            )
        }

    @staticmethod
    def get_templates(*, missing_only: bool = False) -> list[CollectionConfig]:
        """TODO."""
        existing_colls: set[str] = (
            CollectionConfigHandler._get_existing_coll_names()
            if missing_only
            else set()
        )
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

    @staticmethod
    def _validate_collagen_path(
        path: Path, existing_colls: set[str], *, non_aroma_only: bool
    ) -> bool:
        """TODO."""
        return (
            (path / "include.txt").is_file()
            and (COLLECTION_PATH / path.name).is_dir()
            and (not non_aroma_only or path.name not in existing_colls)
        )

    @staticmethod
    def _set_collagen_keywords(config: CollectionConfig, path: Path) -> None:
        """TODO."""
        include = util.read_text_file(
            path / "include.txt", remove_line_breaks=True
        )
        config.include = list({*include, *config.include})
        exclude = util.read_text_file(
            path / "exclude.txt", remove_line_breaks=True
        )
        config.exclude = list({*exclude, *config.exclude})

    @staticmethod
    def get_collagen_collections(
        *, non_aroma_only: bool = False
    ) -> list[CollectionConfig]:
        """TODO."""
        existing_colls: set[str] = (
            CollectionConfigHandler._get_existing_coll_names(aroma_only=True)
            if non_aroma_only
            else set()
        )
        collagen: dict[str, CollectionConfig] = {}
        for app_dir in COLLAGEN_PATHS:
            if not app_dir.is_dir():
                continue
            for path in app_dir.iterdir():
                if not CollectionConfigHandler._validate_collagen_path(
                    path, existing_colls, non_aroma_only=non_aroma_only
                ):
                    continue
                config = CollectionConfigHandler.get_collection(
                    COLLECTION_PATH / path.name, force_aroma=True
                )
                collagen.setdefault(path.name, config)
                CollectionConfigHandler._set_collagen_keywords(
                    collagen[path.name], path
                )
        return list(collagen.values())
