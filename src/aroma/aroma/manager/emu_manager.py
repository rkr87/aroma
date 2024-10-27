"""TODO."""

from pathlib import Path

from data.model.emu_config import EmuConfig
from data.model.rom_detail import RomDetail
from data.source.emu_config_handler import EmuConfigHandler
from shared.classes.class_singleton import ClassSingleton
from shared.constants import EMU_PATH
from shared.tools import util

_MODIFIED_FLAG = "## MODIFIED BY AROMA ##"

_LAUNCH_MENU_SCRIPT = (
    'aroma="/mnt/SDCARD/Apps/aroma/scripts/rom_launcher.sh"'
    ' && [ -f "$aroma" ]'
    ' && "$aroma" "$1" "$0"'
    " && exit 0\n"
)

_REMOVE_LAUNCH_MENU_LIST = [
    '/mnt/SDCARD/Apps/aroma/scripts/rom_launcher.sh "$1" "$0" && exit 0\n',
    _LAUNCH_MENU_SCRIPT,
]


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
    def _is_visible_system(system: str) -> bool:
        """TODO."""
        label = EmuConfigHandler().get(system).label
        for entry in EmuManager._load_visibility_file():
            if entry["label"] == label:
                return bool(entry["show"])
        return False

    @staticmethod
    def get_configurable_systems() -> list[EmuConfig]:
        """TODO."""
        return [
            config
            for path in EMU_PATH.iterdir()
            if EmuConfigHandler.is_configurable_system(path.name)
            and EmuManager._is_visible_system(path.name)
            and (config := EmuConfigHandler().get(path.name))
            and (config.has_cpu_freq_file or config.launchlist)
        ]

    @staticmethod
    def _get_valid_systems() -> list[EmuConfig]:
        """TODO."""
        return [
            config
            for path in EMU_PATH.iterdir()
            if EmuConfigHandler.is_valid_system(path.name)
            and (config := EmuConfigHandler().get(path.name))
        ]

    @staticmethod
    def set_default_emu(system_path: Path, launch_file: str) -> None:
        """TODO."""
        config = util.load_simple_json(system_path / "config.json")
        config["launch"] = launch_file
        EmuConfigHandler().get(system_path.name).launch = launch_file
        util.save_simple_json(config, system_path / "config.json")

    @staticmethod
    def _get_lines(path: Path) -> list[str]:
        """TODO."""
        lines = util.read_text_file(path)
        if _MODIFIED_FLAG not in lines:
            util.create_backup_file(path)
            lines.insert(1, _MODIFIED_FLAG)
            lines.append(_MODIFIED_FLAG)
        return lines

    def _add_launch_menu(self, path: Path) -> None:
        """TODO."""
        lines = self._remove_launch_menu(path, save_changes=False)
        lines.insert(1, _LAUNCH_MENU_SCRIPT)
        with path.open("w", encoding="utf-8", newline="\n") as file:
            file.writelines(lines)

    @staticmethod
    def _remove_launch_menu(
        path: Path, *, save_changes: bool = True
    ) -> list[str]:
        """TODO."""
        lines = EmuManager._get_lines(path)
        for remove_item in _REMOVE_LAUNCH_MENU_LIST:
            if remove_item in lines:
                lines.remove(remove_item)
        if save_changes:
            with path.open("w", encoding="utf-8", newline="\n") as file:
                file.writelines(lines)
        return lines

    def add_emu_launch_menus(self) -> None:
        """TODO."""
        for config in self._get_valid_systems():
            self._add_launch_menu(config.system / config.launch)
            for item in config.launchlist:
                if item.launch == config.launch or not item.launch:
                    continue
                self._add_launch_menu(config.system / item.launch)

    def remove_emu_launch_menus(self) -> None:
        """TODO."""
        for config in self._get_valid_systems():
            self._remove_launch_menu(config.system / config.launch)
            for item in config.launchlist:
                if item.launch == config.launch or not item.launch:
                    continue
                self._remove_launch_menu(config.system / item.launch)

    def restore_backup_launch_scripts(self) -> None:
        """TODO."""
        for config in self._get_valid_systems():
            util.restore_backup_file(config.system / config.launch)
            for item in config.launchlist:
                if item.launch == config.launch or not item.launch:
                    continue
                util.restore_backup_file(config.system / config.launch)
