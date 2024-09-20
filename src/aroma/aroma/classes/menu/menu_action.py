"""
Defines data structures for handling menu actions.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from classes.base.class_base import ClassBase
from constants import RUNNING_ON_TSP
from model.side_pane import SidePane
from tools import util


@dataclass
class MenuAction(ClassBase):  # type: ignore[misc]
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
        logger = MenuAction.get_static_logger()
        if not RUNNING_ON_TSP and self.non_tsp_skip:
            logger.info("Skipping action for non-TSP system")
            return
        if self.action:
            logger.info(
                "Executing action %s(%s)",
                util.get_callable_name(self.action),
                self.text
            )
            self.action()
