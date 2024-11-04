"""Represents detailed information about a Shortcut file."""

from dataclasses import dataclass, field
from pathlib import Path

from data.model.launchable_detail import LaunchableDetail, LaunchableType
from data.model.rom_detail import RomDetail
from shared.constants import APP_NAME, IMG_PATH


@dataclass
class ShortcutDetail(LaunchableDetail):  # pylint: disable=too-many-instance-attributes
    """Data class for storing information about a Shortcut."""

    roms: list[RomDetail] = field(default_factory=list)

    def __post_init__(self) -> None:
        """TODO."""
        self.item_type = LaunchableType.SHORTCUT
        super().__post_init__()

    def format_name(self) -> str:
        """TODO."""
        rom_count = f" ({len(self.roms)})" if len(self.roms) > 1 else ""
        return self.name.replace(f"{APP_NAME}~", "") + rom_count

    def get_image_path(self) -> Path:
        """TODO."""
        image_override = (
            self.parent_path.parent / IMG_PATH / f"{self.name}.png"
        )
        if image_override.is_file() or not self.roms:
            return image_override

        return self.roms[0].get_image_path()
