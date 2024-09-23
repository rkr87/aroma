"""Defines the Image Management preferences menu."""

from collections import OrderedDict
from enum import Enum, auto

from classes.menu.menu_base import MenuBase
from classes.menu.menu_item_base import MenuItemBase
from classes.menu.menu_item_multi import MenuItemMulti
from classes.menu.menu_item_single import MenuItemSingle
from manager.rom_manager import RomManager
from model.side_pane import SidePane
from model.strings import Strings


class MenuImageManagement(MenuBase):
    """A menu for managing Image Management preferences."""

    class _Options(Enum):
        """Defines the options available in this menu."""

        REMOVE_BROKEN = auto()
        REMOVE_BROKEN_REFRESH = auto()

    @property
    def option(self) -> type[_Options]:
        """Provides the enum class for this menu's options."""
        return self._Options

    def __init__(self) -> None:
        super().__init__(Strings().image_management, self._build_menu())

    def _build_menu(self) -> OrderedDict[Enum, MenuItemBase]:
        """Build the menu."""
        logger = MenuImageManagement.get_static_logger()
        logger.debug("Building Image Management menu options.")

        options: OrderedDict[Enum, MenuItemBase] = OrderedDict(
            [
                (self.option.REMOVE_BROKEN, self._remove_broken_images()),
                (self.option.REMOVE_BROKEN_REFRESH, self._remove_on_refresh()),
            ],
        )
        return options

    @staticmethod
    def _remove_on_refresh() -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = MenuImageManagement._generate_config_actions(
            data, "remove_broken_images_on_refresh"
        )
        return MenuItemMulti(
            Strings().remove_broken_refresh,
            actions,
            current,
            SidePane(
                Strings().remove_broken_refresh,
                Strings().remove_broken_refresh_desc,
            ),
        )

    @staticmethod
    def _remove_broken_images() -> MenuItemSingle:
        """TODO."""
        return MenuItemSingle(
            Strings().remove_broken,
            RomManager().remove_broken_images,
            SidePane(Strings().remove_broken, Strings().remove_broken_desc),
        )
