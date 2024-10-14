"""TODO."""

from dataclasses import dataclass

from data.enums.cpu_governor import CPUGovernor


@dataclass
class CPUProfile:  # pylint: disable=too-many-instance-attributes
    """TODO."""

    name: str
    governor: CPUGovernor | None
    min_freq: int | None
    max_freq: int | None
    cores: int | None
    # Profile only # pylint: disable=duplicate-code
    down_threshold: int | None = None
    up_threshold: int | None = None
    freq_step: int | None = None
    sampling_down_factor: int | None = None
    sampling_rate: int | None = None
    sampling_rate_min: int | None = None
