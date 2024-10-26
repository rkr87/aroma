"""TODO."""

import re

from data.model.emu_config import EmuConfig, Launchlist
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    EMU_EXT_KEY,
    EMU_PATH,
    INVALID_SYSTEM_PREFIX,
    NON_CONFIGURABLE_SYSTEMS,
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
    def _get_cpufreq_val(item: str, content: str) -> str | None:
        """TODO."""
        if results := re.search(
            r"echo (.+) > [\w\d/]+cpufreq/" + item, content
        ):
            return str(results.group(1))
        return None

    @staticmethod
    def _get_cpufreq_vals(emu_config: EmuConfig, content: str) -> EmuConfig:
        """TODO."""
        if m := EmuConfigHandler._get_cpufreq_val("scaling_governor", content):
            emu_config.governor = m
        if (
            m := EmuConfigHandler._get_cpufreq_val("scaling_min_freq", content)
        ) and m.isnumeric():
            emu_config.min_freq = int(m)
        if (
            m := EmuConfigHandler._get_cpufreq_val("scaling_max_freq", content)
        ) and m.isnumeric():
            emu_config.max_freq = int(m)
        return emu_config

    @staticmethod
    def _get_cpucore_vals(emu_config: EmuConfig, content: str) -> EmuConfig:
        """TODO."""
        emu_config.cores = 4
        if cores := re.findall(
            r"echo\s+(1|0)\s+>\s+/sys/devices/system/cpu/cpu\d+/online",
            content,
        ):
            emu_config.cores = sum(int(match) for match in cores)
        return emu_config

    @staticmethod
    def _get_cpufreq(emu_config: EmuConfig, system: str) -> EmuConfig:
        """TODO."""
        if not (cpu := EMU_PATH / system / "cpufreq.sh").is_file():
            return emu_config
        emu_config.has_cpu_freq_file = True
        with cpu.open() as f:
            content = f.read()
        EmuConfigHandler._get_cpufreq_vals(emu_config, content)
        EmuConfigHandler._get_cpucore_vals(emu_config, content)
        return emu_config

    @staticmethod
    def _get_system(system: str) -> "EmuConfig":
        """TODO."""
        config = util.load_simple_json(EMU_PATH / system / "config.json")
        emu_config = EmuConfig(
            EMU_PATH / system,
            config.get("label", ""),
            config.get("launch", ""),
            util.tsp_path(str(config.get("background", ""))),
            util.tsp_path(str(config.get("icon", ""))),
            [
                ext.lower()
                for ext in config.get(EMU_EXT_KEY, "").split("|")
                if ext
            ],
            [Launchlist.from_dict(y) for y in config.get("launchlist", [])],
            config.get("aroma_cpu_profile", None),
        )
        return EmuConfigHandler._get_cpufreq(emu_config, system)

    @staticmethod
    def is_valid_system(system: str) -> bool:
        """TODO."""
        return (
            not system.startswith(INVALID_SYSTEM_PREFIX)
            and (EMU_PATH / system / "config.json").is_file()
        )

    @staticmethod
    def is_configurable_system(system: str) -> bool:
        """TODO."""
        return (
            EmuConfigHandler.is_valid_system(system)
            and system in NON_CONFIGURABLE_SYSTEMS
        )
