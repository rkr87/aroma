"""TODO."""

from collections import OrderedDict
from collections.abc import Callable
from functools import partial
from pathlib import Path

from app.menu.menu_action import MenuAction
from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.model.side_pane import SidePane
from app.strings import Strings
from data.enums.cpu_governor import CPUGovernor
from data.model.cpu_profile import CPUProfile
from data.model.emu_config import EmuConfig
from manager.emu_manager import EmuManager
from shared.constants import (
    CPU_FREQ_STEP,
    MAX_CPU_FREQ,
    MIN_CPU_FREQ,
)


class MenuEmuConfig(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        super().__init__("EMU CONFIG", OrderedDict())

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self,
        breadcrumb: str,
        path: Path | None,
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        if not path:
            raise FileNotFoundError
        logger = MenuEmuConfig.get_static_logger()
        logger.debug("Building Emu Config menu options.")
        self.breadcrumb = breadcrumb
        self.content.clear_items()
        config = EmuManager().get_system_config(path.name)
        if config.launchlist:
            self.content.add_item("DEFAULT_EMU", self._default_emu(config))

        if config.has_cpu_freq_file:
            self.content.add_item("CPU_PROFILE", self._cpu_profile(config))
            self.content.add_item("CPU_GOVERNOR", self._cpu_governor(config))
            self.content.add_item("CPU_MIN_FREQ", self._cpu_min_freq(config))
            self.content.add_item("CPU_MAX_FREQ", self._cpu_max_freq(config))

    @staticmethod
    def _default_emu(config: EmuConfig) -> MenuItemMulti:
        """TODO."""
        actions: list[MenuAction] = []
        current = 0
        for index, item in enumerate(config.launchlist):
            if item.launch == config.launch:
                current = index
            actions.append(
                MenuAction(
                    item.name.upper(),
                    partial(
                        EmuManager.set_default_emu,
                        config.system,
                        item.launch,
                    ),
                ),
            )
        return MenuItemMulti(
            Strings().default_emu,
            actions,
            current,
            SidePane(Strings().default_emu, Strings().default_emu_desc),
        )

    def _cpu_profile(self, config: EmuConfig) -> MenuItemMulti:
        """TODO."""

        def set_profile(profile: CPUProfile) -> None:
            """TODO."""
            EmuManager.set_cpu_profile(config.system, profile)
            self.build_dynamic_menu(self.breadcrumb, config.system, None)

        profiles = [
            CPUProfile("CUSTOM"),
            CPUProfile(
                "BALANCED",
                CPUGovernor.ON_DEMAND,
                402000,
                1608000,
            ),
            CPUProfile(
                "POWERSAVE",
                CPUGovernor.CONSERVATIVE,
                402000,
                1608000,
            ),
            CPUProfile(
                "PERFOMANCE",
                CPUGovernor.ON_DEMAND,
                603000,
                1809000,
            ),
        ]

        current = 0
        actions: list[MenuAction] = []
        for index, item in enumerate(profiles):
            if item.name == config.aroma_cpu_profile:
                current = index
            actions.append(
                MenuAction(
                    str(item.name).upper(),
                    partial(set_profile, item),
                ),
            )
        return MenuItemMulti(
            Strings().cpu_profile,
            actions,
            current,
            SidePane(Strings().cpu_profile, Strings().cpu_profile_desc),
        )

    @staticmethod
    def _format_freq(freq: int) -> str:
        """TODO."""
        return f"{freq / 1000:,.0f} MHz"

    @staticmethod
    def _get_freq_range(
        lower: int, upper: int, additional: int | None = None
    ) -> OrderedDict[int | None, str]:
        """TODO."""
        data: OrderedDict[int | None, str] = OrderedDict(
            (i, MenuEmuConfig._format_freq(i))
            for i in range(lower, upper, CPU_FREQ_STEP)
        )
        if additional and additional not in data:
            data[additional] = MenuEmuConfig._format_freq(additional)
            data = OrderedDict(sorted(data.items()))
        return data

    def _cpu_min_freq(self, config: EmuConfig) -> MenuItemMulti:
        """TODO."""
        max_freq = (
            ((config.max_freq // CPU_FREQ_STEP) + 1) * CPU_FREQ_STEP
            if config.max_freq
            else MAX_CPU_FREQ
        )
        data: OrderedDict[int | None, str] = self._get_freq_range(
            MIN_CPU_FREQ, max_freq, config.min_freq
        )
        data[None] = Strings().none_set
        actions, current = self._update_frequency_actions(
            data,
            config.min_freq,
            config.system,
            EmuManager.set_cpu_min_freq,
        )
        return MenuItemMulti(
            Strings().cpu_min_frequency,
            actions,
            current,
            SidePane(
                Strings().cpu_min_frequency, Strings().cpu_min_frequency_desc
            ),
        )

    def _cpu_max_freq(self, config: EmuConfig) -> MenuItemMulti:
        """TODO."""
        min_freq = max(config.min_freq or MIN_CPU_FREQ, MIN_CPU_FREQ)
        data: OrderedDict[int | None, str] = self._get_freq_range(
            min_freq, MAX_CPU_FREQ, config.max_freq
        )
        data[None] = Strings().none_set
        actions, current = self._update_frequency_actions(
            data,
            config.max_freq,
            config.system,
            EmuManager.set_cpu_max_freq,
        )
        return MenuItemMulti(
            Strings().cpu_max_frequency,
            actions,
            current,
            SidePane(
                Strings().cpu_max_frequency, Strings().cpu_max_frequency_desc
            ),
        )

    def _cpu_governor(self, config: EmuConfig) -> MenuItemMulti:
        """TODO."""

        def set_governor(governor: CPUGovernor | None) -> None:
            """TODO."""
            EmuManager.set_cpu_governor(config.system, governor)
            self.build_dynamic_menu(self.breadcrumb, config.system, None)

        data = {
            None: Strings().none_set,
            CPUGovernor.ON_DEMAND: Strings().cpu_governor_on_demand,
            CPUGovernor.CONSERVATIVE: Strings().cpu_governor_conservative,
            CPUGovernor.PERFORMANCE: Strings().cpu_governor_performance,
            CPUGovernor.POWERSAVE: Strings().cpu_governor_powersave,
            CPUGovernor.USERSPACE: Strings().cpu_governor_userspace,
            CPUGovernor.SCHEDUTIL: Strings().cpu_governor_schedutil,
            CPUGovernor.INTERACTIVE: Strings().cpu_governor_interactive,
        }
        actions: list[MenuAction] = []
        current = 0
        for index, item in enumerate(data):
            if item and item.value == config.governor:
                current = index
            actions.append(
                MenuAction(
                    str(data.get(item)).upper(),
                    partial(set_governor, item),
                ),
            )
        return MenuItemMulti(
            Strings().cpu_governor,
            actions,
            current,
            SidePane(Strings().cpu_governor, Strings().cpu_governor_desc),
        )

    def _update_frequency_actions(
        self,
        data: OrderedDict[int | None, str],
        current_val: int | None,
        system_path: Path,
        function: Callable[[Path, int | None], None],
    ) -> tuple[list[MenuAction], int]:
        """TODO."""

        def update_freq(freq: int | None) -> None:
            function(system_path, freq)
            self.build_dynamic_menu(self.breadcrumb, system_path, None)

        actions: list[MenuAction] = []
        current: int = -1
        for index, item in enumerate(data):
            if item and item == current_val:
                current = index
            actions.append(
                MenuAction(str(data.get(item)), partial(update_freq, item))
            )
        return actions, current
