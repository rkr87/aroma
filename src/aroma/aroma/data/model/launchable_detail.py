"""TODO."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from shared.constants import COLLECTION_PATH, ROM_PATH
from shared.tools.enhanced_json_encoder import EXCLUDE_FROM_SERIALIZATION


class LaunchableType(Enum):
    """TODO."""

    ROM = 1
    SHORTCUT = 2


@dataclass
class LaunchableDetail(ABC):  # pylint: disable=too-many-instance-attributes
    """TODO."""

    name: str
    parent: str
    item_path: str
    base_path: Path = field(
        init=False, metadata={EXCLUDE_FROM_SERIALIZATION: True}
    )
    item_type: LaunchableType = field(
        init=False, metadata={EXCLUDE_FROM_SERIALIZATION: True}
    )

    def __post_init__(self) -> None:
        """TODO."""
        self.base_path = (
            COLLECTION_PATH
            if self.item_type == LaunchableType.SHORTCUT
            else ROM_PATH
        )

    @property
    def parent_path(self) -> Path:
        """TODO."""
        return self.base_path / self.parent

    @property
    def full_path(self) -> Path:
        """TODO."""
        return self.base_path / self.item_path

    @abstractmethod
    def get_image_path(self) -> Path:
        """TODO."""

    @abstractmethod
    def format_name(self) -> str:
        """Generate a formatted string representation of the name."""
