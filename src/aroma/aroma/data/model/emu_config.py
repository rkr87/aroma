"""TODO."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Launchlist:
    """TODO."""

    name: str
    launch: str

    @staticmethod
    def from_dict(obj: dict[str, str]) -> "Launchlist":
        """TODO."""
        _name = str(obj.get("name", ""))
        _launch = str(obj.get("launch", ""))
        return Launchlist(_name, _launch)


@dataclass
class EmuConfig:  # pylint: disable = too-many-instance-attributes
    """TODO."""

    system: Path
    label: str
    launch: str
    valid_ext: list[str]
    launchlist: list[Launchlist]
    governor: str | None
    min_freq: int | None
    max_freq: int | None
    has_cpu_freq_file: bool
    aroma_cpu_profile: str | None = None
