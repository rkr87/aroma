"""TODO."""

from collections import OrderedDict
from pathlib import Path

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_base import MenuItemBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_emu_config import MenuEmuConfig
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from manager.emu_manager import EmuManager
from manager.rom_manager import RomManager


class MenuEmuManagement(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.emu_config: MenuEmuConfig = MenuEmuConfig()
        super().__init__(Strings().emu_management, self.default_items())

    def default_items(self) -> OrderedDict[str, MenuItemBase]:
        """TODO."""
        return OrderedDict(
            [
                ("CLEAN_EMUS", self._clean_emus()),
                ("CLEAN_EMUS_REFRESH", self._clean_emus_on_refresh()),
            ]
        )

    def _clean_emus(self) -> MenuItemSingle:
        """TODO."""

        def clean_emus() -> None:
            BackgroundWorker().do_work(
                RomManager().clean_emus, Strings().cleaning_emus
            )
            self.build_dynamic_menu(self.breadcrumb)

        return MenuItemSingle(
            Strings().clean_emus,
            clean_emus,
            SidePane(Strings().clean_emus, Strings().clean_emus_desc),
        )

    @staticmethod
    def _clean_emus_on_refresh() -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = MenuEmuManagement._generate_config_actions(
            data, "clean_emu_on_refresh"
        )
        return MenuItemMulti(
            Strings().clean_emus_refresh,
            actions,
            current,
            SidePane(
                Strings().clean_emus_refresh,
                Strings().clean_emus_refresh_desc,
            ),
        )

    def build_dynamic_menu(  # noqa: D102  # Ignore missing docstring, it's inherited
        self,
        breadcrumb: str,
        path: Path | None = None,  # noqa: ARG002
        identifier: str | None = None,  # noqa: ARG002
    ) -> None:
        logger = MenuEmuManagement.get_static_logger()
        logger.debug("Building Emu Management menu options.")

        self.breadcrumb = breadcrumb
        self.content.clear_items()
        self.content.items = self.default_items()
        for emu in sorted(
            EmuManager.get_configurable_systems(), key=lambda item: item.label
        ):
            self.content.add_item(
                emu.system.name.upper(),
                self.dynamic_sub_menu(
                    emu.format_label,
                    emu.system,
                    None,
                    self.emu_config,
                    self.menu_stack.push,
                    side_pane=SidePane(
                        header=emu.format_label,
                        img=emu.icon,
                        bg_img=emu.background,
                    ),
                ),
            )
