"""TODO."""

from pathlib import Path

from data.enums.cpu_governor import CPUGovernor
from data.model.cpu_profile import CPUProfile
from data.model.emu_config import EmuConfig
from data.source.emu_config_handler import EmuConfigHandler
from shared.classes.class_singleton import ClassSingleton
from shared.tools import util


class EmuCPUProfileManager(ClassSingleton):
    """TODO."""

    @staticmethod
    def set_cpu_profile(system_path: Path, profile: CPUProfile) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.aroma_cpu_profile = profile.name
        if profile.governor:
            config.governor = profile.governor.value
            config.down_threshold = profile.down_threshold
            config.up_threshold = profile.up_threshold
            config.freq_step = profile.freq_step
            config.sampling_down_factor = profile.sampling_down_factor
            config.sampling_rate = profile.sampling_rate
            config.sampling_rate_min = profile.sampling_rate_min
        if profile.min_freq:
            config.min_freq = profile.min_freq
        if profile.max_freq:
            config.max_freq = profile.max_freq
        if profile.cores:
            config.cores = profile.cores
        EmuCPUProfileManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_governor(
        system_path: Path, governor: CPUGovernor | None
    ) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.governor = governor.value if governor else None
        EmuCPUProfileManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_min_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.min_freq = frequency
        EmuCPUProfileManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_max_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.max_freq = frequency
        EmuCPUProfileManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_cores(system_path: Path, cores: int) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.cores = cores
        EmuCPUProfileManager._save_cpu_profile(system_path, config)

    @staticmethod
    def _get_cpu_gov_lines(config: EmuConfig) -> list[str]:
        """TODO."""
        if not config.governor:
            return []
        gov_str: str = "echo %s > /sys/devices/system/cpu/cpufreq/%s/%s\n"
        items: dict[int | None, str] = {
            config.down_threshold: "down_threshold",
            config.up_threshold: "up_threshold",
            config.freq_step: "freq_step",
            config.sampling_down_factor: "sampling_down_factor",
            config.sampling_rate: "sampling_rate",
            config.sampling_rate_min: "sampling_rate_min",
        }
        return [
            gov_str % (k, config.governor, v) for k, v in items.items() if k
        ]

    @staticmethod
    def _get_cpu_freq_lines(config: EmuConfig) -> list[str]:
        """TODO."""
        cpu_str: str = "echo %s > /sys/devices/system/cpu/cpu0/cpufreq/%s\n"
        items: dict[int | str | None, str] = {
            config.min_freq: "scaling_min_freq",
            config.max_freq: "scaling_max_freq",
            config.governor: "scaling_governor",
        }
        return [cpu_str % (k, v) for k, v in items.items() if k]

    @staticmethod
    def _get_cpu_core_lines(config: EmuConfig) -> list[str]:
        """TODO."""
        if not config.cores:
            return []
        core_str: str = "echo %s > /sys/devices/system/cpu/cpu%s/online\n"
        return [core_str % (int(i < config.cores), i) for i in range(4)]

    @staticmethod
    def _save_cpu_profile(system_path: Path, config: EmuConfig) -> None:
        """TODO."""
        with (system_path / "cpufreq.sh").open(mode="w") as f:
            f.write("#!/bin/sh\n")
            for line in EmuCPUProfileManager._get_cpu_core_lines(config):
                f.write(line)
            for line in EmuCPUProfileManager._get_cpu_freq_lines(config):
                f.write(line)
            for line in EmuCPUProfileManager._get_cpu_gov_lines(config):
                f.write(line)

        config_file = util.load_simple_json(system_path / "config.json")
        config_file["aroma_cpu_profile"] = config.aroma_cpu_profile
        util.save_simple_json(config_file, system_path / "config.json")
