"""
Defines the abstract base class for menu items, including methods for
handling actions, text, and side pane attributes.
"""

from abc import ABC, abstractmethod

from base.class_base import ClassBase
from menu.menu_action import MenuAction
from model.side_pane import SidePane


class MenuItemBase(ClassBase, ABC):
    """
    Abstract base class for menu items. Defines the interface and common
    attributes for menu items, including selection state and side pane
    handling.
    """

    def __init__(
        self,
        selected: bool = False,
        side_pane: SidePane | None = None
    ) -> None:
        """
        Initialize the menu item with optional selection state and side pane.
        """
        super().__init__()
        self.selected: bool = selected
        self._side_pane: SidePane | None = side_pane

    @abstractmethod
    def get_actions(self) -> list[MenuAction]:
        """Return the list of actions for the menu item."""

    @abstractmethod
    def get_action(self) -> MenuAction:
        """Return the list of actions for the menu item."""

    @abstractmethod
    def run_action(self) -> None:
        """Run selected an action (either single or from a list)."""

    @abstractmethod
    def get_text(self) -> str:
        """Return selectable option text"""

    @abstractmethod
    def get_prefix_text(self) -> str | None:
        """Return option prefix text"""

    @property
    def side_pane(self) -> SidePane | None:
        """
        Return the merged side pane for the menu item, combining action and
        item panes.
        """
        return SidePane.merge(self._get_action_side_pane(), self._side_pane)

    @abstractmethod
    def _get_action_side_pane(self) -> SidePane | None:
        """Return the side pane associated with the selected action."""
