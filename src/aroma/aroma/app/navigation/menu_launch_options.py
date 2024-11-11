"""TODO."""

import json
import sys
from collections import OrderedDict
from functools import partial
from pathlib import Path

from app.menu.menu_action import MenuAction
from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.strings import Strings
from manager.emu_manager import EmuManager
from shared.constants import EMU_PATH, ROM_PATH
from shared.tools import util


class MenuLaunchOptions(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        super().__init__("LAUNCH_MENU", OrderedDict())
        self._selected_rom = 0
        self._roms: list[Path] = []
        self._selected_emu = ""

    def _build_dynamic_menu(
        self,
        path: Path | None,
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        if not path:
            raise FileNotFoundError
        self._build_rom_list(path)
        self._launch_option()
        self._rom_selector()
        self._emu_selector()

    def _build_rom_list(self, path: Path) -> None:
        """TODO."""
        if path.suffix in {".txt"}:
            self._roms = list(
                {
                    Path(util.tsp_path(rom))
                    for rom in util.read_text_file(path)
                    if rom.strip()
                }
            )
        else:
            path = Path(util.tsp_path(path)).resolve(strict=False)
            self._roms = [path]

    def _launch_rom(self) -> None:
        """TODO."""
        result = {
            "launch": self._selected_emu,
            "rom": str(self._roms[self._selected_rom]),
        }
        print(f"AROMA LAUNCH RESULT: {json.dumps(result)}", flush=True)  # noqa: T201
        sys.exit()

    def _launch_option(self) -> None:
        """TODO."""
        menu_item = MenuItemSingle(
            Strings().launch_rom,
            self._launch_rom,
            SidePane(Strings().launch_rom),
        )
        self.content.add_item("LAUNCH", menu_item)

    def _set_selected_rom(self, index: int) -> None:
        """TODO."""
        self._selected_rom = index
        self._emu_selector()

    def _set_selected_emu(self, emu: str) -> None:
        """TODO."""
        self._selected_emu = emu

    def _rom_selector(self) -> None:
        """TODO."""
        self._selected_rom = 0
        if len(self._roms) <= 1:
            return
        roms = {
            i: str(rom.relative_to(ROM_PATH).with_suffix("")).upper()
            for i, rom in enumerate(self._roms)
        }
        actions = self._generate_actions(roms, self._set_selected_rom)

        menu_item = MenuItemMulti(
            Strings().rom,
            actions,
            side_pane=SidePane(
                Strings().rom, list(roms.values()), trim_long_lines=True
            ),
        )
        self.content.add_item("ROM_SELECTOR", menu_item)

    def _emu_selector(self) -> None:
        """TODO."""
        rom = self._roms[self._selected_rom]
        system = rom.relative_to(ROM_PATH).parts[0]
        config = EmuManager().get_system_config(system)
        self._selected_emu = str(EMU_PATH / system / config.launch)

        if len(config.launchlist) <= 1:
            self.content.remove_item("EMU_SELECTOR")
            return
        actions: list[MenuAction] = []
        current = 0
        for index, item in enumerate(config.launchlist):
            if item.launch == config.launch:
                current = index
            if (script := EMU_PATH / system / item.launch).is_file():
                actions.append(
                    MenuAction(
                        item.name.upper(),
                        partial(self._set_selected_emu, str(script)),
                    ),
                )
        menu_item = MenuItemMulti(
            Strings().emu,
            actions,
            current,
            SidePane(Strings().emu, [item.text for item in actions]),
        )
        self.content.update_item("EMU_SELECTOR", menu_item)

    def _dynamic_menu_default_items(self) -> None:
        pass
