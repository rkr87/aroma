"""TODO."""

import re
from dataclasses import dataclass
from pathlib import Path

from shared.constants import CUSTOM_STR


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
    background: str
    icon: str
    valid_ext: list[str]
    launchlist: list[Launchlist]
    aroma_cpu_profile: str | None = None
    has_cpu_freq_file: bool = False
    governor: str | None = None
    min_freq: int | None = None
    max_freq: int | None = None
    cores: int | None = None
    # Profile only # pylint: disable=duplicate-code
    down_threshold: int | None = None
    up_threshold: int | None = None
    freq_step: int | None = None
    sampling_down_factor: int | None = None
    sampling_rate: int | None = None
    sampling_rate_min: int | None = None

    @property
    def format_label(self) -> str:
        """TODO."""
        if not (label := re.sub(r"\s+", " ", self.label).strip()):
            return self.system.name
        return f"{label} ({self.system.name})"

    def apply_custom_cpu_profile(self) -> None:
        """TODO."""
        self.aroma_cpu_profile = CUSTOM_STR
        self.down_threshold = None
        self.up_threshold = None
        self.freq_step = None
        self.sampling_down_factor = None
        self.sampling_rate = None
        self.sampling_rate_min = None
