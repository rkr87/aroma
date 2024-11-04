"""TODO."""

import shutil
from pathlib import Path

from data.model.collection_config import CollectionConfig
from data.source.collection_config_handler import CollectionConfigHandler
from shared.app_config import AppConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    APP_NAME,
    COLLECTION_DEFAULTS,
    COLLECTION_PATH,
    COLLECTION_TEMPLATES,
)
from shared.tools import util


class CollectionOpsManager(ClassSingleton):  # pylint: disable=too-many-public-methods
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._config = CollectionConfigHandler()

    @staticmethod
    def get_default_file(
        file_name: str, directory: str, *, from_template: bool = False
    ) -> Path:
        """TODO."""
        default = COLLECTION_DEFAULTS / file_name
        if not from_template:
            return default
        template_path = COLLECTION_TEMPLATES / directory / file_name
        if not template_path.is_file():
            return default
        return template_path

    def _create_collection(
        self, config: CollectionConfig, *, from_template: bool = False
    ) -> None:
        """TODO."""
        config.systems_separated = (
            AppConfig().separate_collections_by_system_default
        )
        config.is_aroma_collection = True
        self._config.save_collection(config)
        files = [
            config.background,
            config.icon,
            config.iconsel,
        ]
        dest_path = COLLECTION_PATH / config.directory
        for file_name in files:
            if (dest_path / file_name).is_file():
                continue
            source = self.get_default_file(
                file_name, config.directory, from_template=from_template
            )
            if source.is_file():
                shutil.copy2(source, dest_path / file_name)
        launch = self.get_default_file(
            config.launch, config.directory, from_template=from_template
        )
        if launch.is_file():
            shutil.copy2(launch, dest_path / config.launch)
        (dest_path / config.rompath).mkdir(parents=True, exist_ok=True)
        (dest_path / config.imgpath).mkdir(parents=True, exist_ok=True)

    def create_collagen_collection(self, collagen: CollectionConfig) -> None:
        """TODO."""
        self._create_collection(collagen)
        self.clear_data(collagen, aroma_data_only=False)

    def create_template_collection(self, template: CollectionConfig) -> None:
        """TODO."""
        self._create_collection(template, from_template=True)

    def create_custom_collection(self, name: str) -> bool:
        """TODO."""
        if not name:
            return False
        path = COLLECTION_PATH / name

        if (path / "config.json").is_file():
            config = self._config.get_collection(path)
            is_new = not config.is_aroma_collection
        else:
            is_new = True
            config = CollectionConfig(name, name, is_aroma_collection=True)
        self._create_collection(config)
        return is_new

    @staticmethod
    def delete_collection(path: CollectionConfig | Path) -> None:
        """TODO."""
        if isinstance(path, CollectionConfig):
            path = COLLECTION_PATH / path.directory
        if path.is_dir():
            shutil.rmtree(path)

    def rename_collection(
        self, path: CollectionConfig | Path, new_name: str
    ) -> CollectionConfig | None:
        """TODO."""
        if isinstance(path, CollectionConfig):
            path = COLLECTION_PATH / path.directory
        new_path = path.parent / new_name
        if new_path.is_dir():
            return None
        path.rename(new_path)
        config = self._config.get_collection(new_path)
        config.directory = new_name
        config.label = new_name
        self._config.save_collection(config)
        return config

    def set_systems_separated(
        self, config: CollectionConfig | Path, *, separated: bool
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        if config.systems_separated == separated:
            return
        config.systems_separated = separated
        self._config.save_collection(config)
        self.clear_data(config)

    def clear_data(
        self, config: CollectionConfig | Path, *, aroma_data_only: bool = True
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        paths = [
            COLLECTION_PATH / config.directory / config.rompath,
            COLLECTION_PATH / config.directory / config.imgpath,
        ]
        for path in paths:
            if not path.is_dir():
                continue
            self._clear_path(path, aroma_data_only=aroma_data_only)

    @staticmethod
    def _clear_path(path: Path, *, aroma_data_only: bool) -> None:
        """TODO."""
        if not aroma_data_only:
            shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)
            return
        for shortcut in path.rglob(f"*{APP_NAME}~*.txt"):
            shortcut.unlink()
        util.delete_empty_dirs(path)

    def set_group_method_override(
        self, config: CollectionConfig | Path, *, override: bool
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        if config.override_group_method == override:
            return
        config.override_group_method = override
        self._config.save_collection(config)

    def set_group_method(
        self, config: CollectionConfig | Path, name_format: str
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        config.custom_group_method = name_format
        self._config.save_collection(config)

    def add_comma_separated_keywords(
        self,
        config: CollectionConfig | Path,
        keywords: str,
        *,
        exclude_words: bool = False,
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        config.is_aroma_collection = True
        words = {w.strip() for w in keywords.split(",") if w.strip()}
        if exclude_words:
            config.exclude = list(set(config.exclude) | words)
        else:
            config.include = list(set(config.include) | words)
        self._config.save_collection(config)

    def clear_keywords(
        self, config: CollectionConfig | Path, *, exclude_words: bool = False
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        if exclude_words:
            config.exclude = []
        else:
            config.include = []
            config.is_aroma_collection = False
        self._config.save_collection(config)

    def delete_keyword(
        self,
        config: CollectionConfig | Path,
        keyword: str,
        *,
        exclude_words: bool = False,
    ) -> None:
        """TODO."""
        if isinstance(config, Path):
            config = self._config.get_collection(config)
        if exclude_words:
            config.exclude.remove(keyword)
        else:
            config.include.remove(keyword)
            config.is_aroma_collection = bool(config.include)
        self._config.save_collection(config)
