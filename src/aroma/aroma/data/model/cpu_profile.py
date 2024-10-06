"""TODO."""

from dataclasses import dataclass

from data.enums.cpu_governor import CPUGovernor


@dataclass
class CPUProfile:
    """TODO."""

    name: str
    governor: CPUGovernor | None = None
    min_freq: int | None = None
    max_freq: int | None = None
