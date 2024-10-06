"""TODO."""

from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import CUSTOM_STR, EMU_PATH, NON_CONFIGURABLE_SYSTEM_PREFIX
from data.emu_config_handler import EmuConfigHandler
from enums.cpu_governor import CPUGovernor
from model.cpu_profile import CPUProfile
from model.emu_config import EmuConfig
from model.rom_detail import RomDetail
from tools import util


class EmuManager(ClassSingleton):
    """TODO."""

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
        if profile.min_freq:
            config.min_freq = profile.min_freq
        if profile.max_freq:
            config.max_freq = profile.max_freq
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_governor(
        system_path: Path, governor: CPUGovernor | None
    ) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.aroma_cpu_profile = CUSTOM_STR
        config.governor = governor.value if governor else None
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_min_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.aroma_cpu_profile = CUSTOM_STR
        config.min_freq = frequency
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def set_cpu_max_freq(system_path: Path, frequency: int | None) -> None:
        """TODO."""
        config = EmuConfigHandler().get(system_path.name)
        config.aroma_cpu_profile = CUSTOM_STR
        config.max_freq = frequency
        EmuManager._save_cpu_profile(system_path, config)

    @staticmethod
    def _save_cpu_profile(system_path: Path, config: EmuConfig) -> None:
        """TODO."""
        template: str = "echo %s > /sys/devices/system/cpu/cpu0/cpufreq/%s\n"
        with (system_path / "cpufreq.sh").open(mode="w") as f:
            f.write("#!/bin/sh\n")
            if config.governor:
                f.write(template % (config.governor, "scaling_governor"))
            if config.min_freq:
                f.write(template % (config.min_freq, "scaling_min_freq"))
            if config.max_freq:
                f.write(template % (config.max_freq, "scaling_max_freq"))

        config_file = util.load_simple_json(system_path / "config.json")
        config_file["aroma_cpu_profile"] = config.aroma_cpu_profile
        util.save_simple_json(config_file, system_path / "config.json")
