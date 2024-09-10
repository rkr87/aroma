"""
Defines data structures for handling menu actions.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from constants import RUNNING_ON_TSP
from model.side_pane import SidePane


@dataclass
class MenuAction:  # type: ignore
    """
    Represents a menu action with associated text, an optional action to be
    executed, and optional side pane behavior. Skips the action if conditions
    are not met for non-TSP systems.
    """
    text: str
    action: Callable[..., Any] | None
    side_pane: SidePane | None = None
    non_tsp_skip: bool = False

    def run(self) -> None:
        """
        Executes the associated action if not skipped and an action is defined.
        """
        if not RUNNING_ON_TSP and self.non_tsp_skip:
            return
        if self.action:
            self.action()
