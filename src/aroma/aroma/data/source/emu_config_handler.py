"""TODO."""

import re

from data.model.emu_config import EmuConfig, Launchlist
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    EMU_EXT_KEY,
    EMU_PATH,
    NON_CONFIGURABLE_SYSTEM_PREFIX,
)
from shared.tools import util


class EmuConfigHandler(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._config_cache: dict[str, EmuConfig] = {}

    def get(self, system: str) -> EmuConfig:
        """TODO."""
        self._check_cache(system)
        return self._config_cache[system]

    def _check_cache(self, system: str) -> None:
        """TODO."""
        if system in self._config_cache:
            return
        self._config_cache[system] = self._get_system(system)

    @staticmethod
    def _get_system(system: str) -> "EmuConfig":
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
            util.tsp_path(config.get("background", "")),
            util.tsp_path(config.get("icon", "")),
            [ext.lower() for ext in config.get(EMU_EXT_KEY, "").split("|")],
            [Launchlist.from_dict(y) for y in config.get("launchlist", [])],
            governor,
            min_freq,
            max_freq,
            cpu_freq_file,
            config.get("aroma_cpu_profile", None),
        )
