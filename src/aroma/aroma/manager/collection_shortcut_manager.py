"""TODO."""

import re
from pathlib import Path
from re import Pattern

from data.model.collection_config import CollectionConfig
from data.model.rom_detail import RomDetail
from data.model.shortcut_detail import ShortcutDetail
from data.source.collection_config_handler import CollectionConfigHandler
from data.validator.rom_validator import RomValidator
from manager.collection_ops_manager import CollectionOpsManager
from shared.app_config import AppConfig
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    APP_NAME,
    COLLECTION_PATH,
    ROM_PATH,
)
from shared.tools import util


class CollectionShortcutManager(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self.app_config = AppConfig()
        self.config = CollectionConfigHandler()
        self.operations = CollectionOpsManager()
        self._validator = RomValidator()

    @staticmethod
    def _generate_pattern(collection: CollectionConfig) -> Pattern[str] | None:
        """TODO."""
        if not collection.is_aroma_collection or not collection.include:
            return None
        pattern = "(?=.*(?:" + "|".join(collection.include) + "))"
        if collection.exclude:
            exclude_pattern = "(?!.*(?:" + "|".join(collection.exclude) + "))"
            pattern = f"{pattern}{exclude_pattern}"
        return re.compile(pattern, re.IGNORECASE)

    def _get_group_method(self, collection: CollectionConfig) -> str:
        """TODO."""
        if collection.override_group_method:
            return collection.custom_group_method
        if self.app_config.override_collection_group_method:
            return self.app_config.custom_collection_group_method
        return self.app_config.name_format

    @staticmethod
    def _get_path(
        group_method: str,
        collection: CollectionConfig,
        rom: RomDetail,
    ) -> Path:
        """TODO."""
        base_path = COLLECTION_PATH / collection.directory / collection.rompath
        if collection.systems_separated:
            base_path = base_path / rom.parent
        file_name = f"{APP_NAME}~{rom.format_name(group_method)}.txt"
        return base_path / file_name

    def _get_matches(
        self, collection: CollectionConfig, rom_db: dict[str, RomDetail]
    ) -> dict[str, ShortcutDetail]:
        """TODO."""
        matches: dict[str, ShortcutDetail] = {}
        if not (pattern := self._generate_pattern(collection)):
            return matches
        group_method = self._get_group_method(collection)
        for rom in rom_db.items():
            if not pattern.match(rom[1].name):
                continue
            path = self._get_path(group_method, collection, rom[1])
            matches.setdefault(
                str(util.make_valid_path(path)),
                ShortcutDetail(
                    path.stem,
                    f"{collection.directory}/{collection.rompath}",
                    str(
                        util.make_valid_path(path.relative_to(COLLECTION_PATH))
                    ),
                ),
            ).roms.append(rom[1])
        return matches

    def create_aroma_shortcuts(
        self, collection: CollectionConfig, rom_db: dict[str, RomDetail]
    ) -> dict[str, ShortcutDetail]:
        """TODO."""
        matches = self._get_matches(collection, rom_db)
        for path_str, shortcut in matches.items():
            path = Path(path_str)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as file:
                file.writelines(
                    [f"{rom.full_path}\n" for rom in shortcut.roms]
                )
        return matches

    def get_non_aroma_shortcuts(
        self, collection: CollectionConfig, rom_db: dict[str, RomDetail]
    ) -> dict[str, ShortcutDetail]:
        """TODO."""
        result: dict[str, ShortcutDetail] = {}
        base_path = COLLECTION_PATH / collection.directory / collection.rompath
        for path in base_path.rglob("*"):
            if not self._validator.check_launchable_path(path):
                continue
            roms: list[RomDetail] = []
            if path.suffix in {".txt"}:
                roms = [
                    rom_db[rel]
                    for line in util.read_text_file(path, convert_paths=True)
                    if (rel := str(Path(line).relative_to(ROM_PATH)))
                    and rel in rom_db
                ]
            result[str(path)] = ShortcutDetail(
                path.stem,
                f"{collection.directory}/{collection.rompath}",
                str(path.relative_to(COLLECTION_PATH)),
                roms,
            )
        return result
