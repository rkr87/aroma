"""TODO."""

import re
from dataclasses import dataclass
from pathlib import Path

from constants import EMU_EXT_KEY, EMU_PATH, NON_CONFIGURABLE_SYSTEM_PREFIX
from tools import util


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

    @staticmethod
    def get_system(system: str) -> "EmuConfig":
        """TODO."""
        config = util.load_simple_json(EMU_PATH / system / "config.json")
        governor = None
        min_freq = None
        max_freq = None
        cpu_freq_file = False
        if (
            not system.startswith(tuple(NON_CONFIGURABLE_SYSTEM_PREFIX))
            and (cpu := EMU_PATH / system / "cpufreq.sh").is_file()
        ):
            cpu_freq_file = True
            with cpu.open() as f:
                content = f.read()
            if m := re.search(
                r"echo (.+) > [\w\d/]+cpufreq/scaling_governor", content
            ):
                governor = str(m.group(1))
            if m := re.search(
                r"echo (.+) > [\w\d/]+cpufreq/scaling_min_freq", content
            ):
                min_freq = int(m.group(1))
            if m := re.search(
                r"echo (.+) > [\w\d/]+cpufreq/scaling_max_freq", content
            ):
                max_freq = int(m.group(1))
        return EmuConfig(
            EMU_PATH / system,
            config.get("label", ""),
            config.get("launch", ""),
            [ext.lower() for ext in config.get(EMU_EXT_KEY, "").split("|")],
            [Launchlist.from_dict(y) for y in config.get("launchlist", [])],
            governor,
            min_freq,
            max_freq,
            cpu_freq_file,
            config.get("aroma_cpu_profile", None),
        )
