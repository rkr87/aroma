"""TODO."""

from enum import Enum


class CPUGovernor(Enum):
    """TODO."""

    ON_DEMAND = "ondemand"
    PERFORMANCE = "performance"
    CONSERVATIVE = "conservative"
    POWERSAVE = "powersave"
    USERSPACE = "userspace"
    SCHEDUTIL = "schedutil"
    INTERACTIVE = "interactive"
