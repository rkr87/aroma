"""Represents detailed information about a ROM file."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from data.model.launchable_detail import LaunchableDetail, LaunchableType
from shared.app_config import AppConfig
from shared.constants import (
    IMG_PATH,
    NAMING_ADDITIONAL_ID,
    NAMING_DISC_ID,
    NAMING_FORMAT_ID,
    NAMING_HACK_ID,
    NAMING_NAME_ID,
    NAMING_REGION_ID,
    NAMING_TITLE_ID,
    NAMING_VERSION_ID,
    NAMING_YEAR_ID,
)


@dataclass
class RomDetail(LaunchableDetail):  # pylint: disable=too-many-instance-attributes
    """Data class for storing information about a ROM."""

    title: str
    source: str
    id_method: str = ""
    id: str = ""
    region: list[str] = field(default_factory=list)
    disc: list[str] = field(default_factory=list)
    format: list[str] = field(default_factory=list)
    hack: str | None = None
    version: str | None = None
    year: str | None = None
    additional: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """TODO."""
        self.item_type = LaunchableType.ROM
        super().__post_init__()

    @property
    def name_clean(self) -> str:
        """Return the ROM's name with special characters removed."""
        name_clean = re.sub(r"[^a-zA-Z0-9\s]", " ", self.name)
        return re.sub(r"\s+", " ", name_clean)

    def format_name(self, format_string: str | None = None) -> str:
        """Generate a formatted string representation of the ROM name."""
        formats = {
            NAMING_TITLE_ID: self.title,
            NAMING_NAME_ID: self.name,
            NAMING_REGION_ID: self._format_region,
            NAMING_DISC_ID: self._format_disc,
            NAMING_FORMAT_ID: self._format_vformat,
            NAMING_HACK_ID: self.hack if self.hack else "",
            NAMING_VERSION_ID: self.version if self.version else "",
            NAMING_YEAR_ID: self.year if self.year else "",
            NAMING_ADDITIONAL_ID: self._format_additional,
        }
        result = format_string if format_string else AppConfig().name_format
        for k, v in formats.items():
            result = result.replace(k, v)
        empty_parens = ["[]", "()", r"{}"]
        for s in empty_parens:
            result = result.replace(s, "")
        result = re.sub(r"\s+", " ", result)
        return result.strip()

    @property
    def _format_disc(self) -> str:
        """Format the disc information for display."""
        if not self.disc:
            return ""
        return " ".join(reversed(self.disc))

    @property
    def _format_region(self) -> str:
        """Format the region information for display."""
        if not self.region:
            return ""
        return ",".join(reversed(self.region))

    @property
    def _format_vformat(self) -> str:
        """Format the format information for display."""
        if not self.format:
            return ""
        return ",".join(self.format)

    @property
    def _format_additional(self) -> str:
        """Format additional information for display."""
        if not self.additional:
            return ""
        return "|".join(self.additional)

    def get_image_path(self) -> Path:
        """TODO."""
        return (
            IMG_PATH
            / self.parent
            / Path(self.item_path).with_suffix(".png").name
        )
