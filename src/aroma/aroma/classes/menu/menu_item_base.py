"""Defines the abstract base class for menu items."""

from abc import ABC, abstractmethod

from classes.base.class_base import ClassBase
from classes.menu.menu_action import MenuAction
from model.side_pane import SidePane


class MenuItemBase(ClassBase, ABC):
    """Abstract base class for menu items."""

    def __init__(
        self,
        side_pane: SidePane | None = None,
        *,
        selected: bool = False,
        deactivated: bool = False,
    ) -> None:
        super().__init__()
        self.selected: bool = selected
        self._side_pane: SidePane | None = side_pane
        self.deactivated: bool = deactivated

    @abstractmethod
    def get_actions(self) -> list[MenuAction]:
        """Return the list of actions for the menu item."""

    @abstractmethod
    def get_action(self) -> MenuAction:
        """Return the list of actions for the menu item."""

    def run_action(self) -> None:
        """TODO."""
        if self.deactivated:
            return
        self._run_action()

    @abstractmethod
    def _run_action(self) -> None:
        """Run selected an action (either single or from a list)."""

    @abstractmethod
    def get_text(self) -> str:
        """Return selectable option text."""

    @abstractmethod
    def get_prefix_text(self) -> str | None:
        """Return option prefix text."""

    @property
    def side_pane(self) -> SidePane | None:
        """Return menu item side pane, combining action and item panes."""
        return SidePane.merge(self._get_action_side_pane(), self._side_pane)

    @abstractmethod
    def _get_action_side_pane(self) -> SidePane | None:
        """Return the side pane associated with the selected action."""
