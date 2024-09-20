"""Represents detailed information about a ROM file."""

from dataclasses import dataclass, field


@dataclass
class RomDetail:  # pylint: disable=too-many-instance-attributes
    """Data class for storing information about a ROM."""

    title: str
    name: str
    source: str
    id_method: str = ""
    id: str = ""
    region: list[str] = field(default_factory=list)
    disc: list[str] = field(default_factory=list)
    format: list[str] = field(default_factory=list)
