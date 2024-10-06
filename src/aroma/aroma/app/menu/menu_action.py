"""Defines data structures for handling menu actions."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.model.side_pane import SidePane
from shared.classes.class_base import ClassBase
from shared.constants import RUNNING_ON_TSP
from shared.tools import util


@dataclass
class MenuAction(ClassBase):  # type: ignore[misc]
    """Represents a menu action with associated text, actions and side pane."""

    text: str
    action: Callable[..., Any] | None
    side_pane: SidePane | None = None
    non_tsp_skip: bool = False

    def run(self) -> None:
        """Execute the associated action."""
        logger = MenuAction.get_static_logger()
        if not RUNNING_ON_TSP and self.non_tsp_skip:
            logger.info("Skipping action for non-TSP system")
            return
        if self.action:
            logger.info(
                "Executing action %s(%s)",
                util.get_callable_name(self.action),
                self.text,
            )
            self.action()
