"""TODO."""

from pathlib import Path

from data.enums.cpu_governor import CPUGovernor
from data.model.cpu_profile import CPUProfile
from data.model.emu_config import EmuConfig
from data.model.rom_detail import RomDetail
from data.source.emu_config_handler import EmuConfigHandler
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    EMU_PATH,
    NON_CONFIGURABLE_SYSTEM_PREFIX,
)
from shared.tools import util


class EmuManager(ClassSingleton):
    """TODO."""

    @staticmethod
    def get_system_config(system: str) -> EmuConfig:
        """TODO."""
        return EmuConfigHandler().get(system)

    @staticmethod
    def _create_visibility_file() -> list[dict[str, str | int]]:
        """TODO."""
        data: list[dict[str, str | int]] = [
            {"label": EmuConfigHandler().get(system.name).label, "show": 0}
            for system in EMU_PATH.iterdir()
        ]
        EmuManager._save_visibility_file(data)
        return data

    @staticmethod
    def _load_visibility_file() -> list[dict[str, str | int]]:
        """TODO."""
        if not (emu_file := EMU_PATH / "show.json").is_file():
            return EmuManager._create_visibility_file()
        return util.load_json_list(emu_file)

    @staticmethod
    def _save_visibility_file(entries: list[dict[str, str | int]]) -> None:
        """TODO."""
        return util.save_simple_json(entries, EMU_PATH / "show.json")

    @staticmethod
    def clean_emus(rom_db: dict[str, RomDetail]) -> None:
        """TODO."""
        valid: set[str] = set()
        checked: set[str] = set()
        for key in rom_db:
            if (system := Path(key).parts[0]) in checked:
                continue
            valid.add(EmuConfigHandler().get(system).label)
            checked.add(system)
        for entry in (entries := EmuManager._load_visibility_file()):
            entry["show"] = int(entry["label"] in valid)
        EmuManager._save_visibility_file(entries)

    @staticmethod
    def is_valid_system(system: str) -> bool:
        """TODO."""
        return (EMU_PATH / system).is_dir()

    @staticmethod
    def _is_visible_system(system: str) -> bool:
        """TODO."""
        label = EmuConfigHandler().get(system).label
        for entry in EmuManager._load_visibility_file():
            if entry["label"] == label:
                return bool(entry["show"])
        return False

    @staticmethod
    def _is_configurable_system(system: str) -> bool:
        """TODO."""
        return (
            EmuManager.is_valid_system(system)
            and not system.startswith(tuple(NON_CONFIGURABLE_SYSTEM_PREFIX))
            and EmuManager._is_visible_system(system)
        )

    @staticmethod
    def get_configurable_systems() -> list[EmuConfig]:
        """TODO."""
        return [
            config
            for path in EMU_PATH.iterdir()
            if EmuManager._is_configurable_system(path.name)
            and (config := EmuConfigHandler().get(path.name))
            and (config.has_cpu_freq_file or config.launchlist)
        ]

    @staticmethod
    def set_default_emu(system_path: Path, launch_file: str) -> None:
        """TODO."""
        config = util.load_simple_json(system_path / "config.json")
        config["launch"] = launch_file
        EmuConfigHandler().get(system_path.name).launch = launch_file
        util.save_simple_json(config, system_path / "config.json")

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
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_governor(
        system_path: Path, governor: CPUGovernor | None
    ) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.governor = governor.value if governor else None
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_min_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.min_freq = frequency
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_max_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.max_freq = frequency
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_cores(system_path: Path, cores: int) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.apply_custom_cpu_profile()
        config.cores = cores
        EmuManager._save_cpu_profile(system_path, config)

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
            for line in EmuManager._get_cpu_core_lines(config):
                f.write(line)
            for line in EmuManager._get_cpu_freq_lines(config):
                f.write(line)
            for line in EmuManager._get_cpu_gov_lines(config):
                f.write(line)

        config_file = util.load_simple_json(system_path / "config.json")
        config_file["aroma_cpu_profile"] = config.aroma_cpu_profile
        util.save_simple_json(config_file, system_path / "config.json")
