"""
Defines data structures for handling menu actions.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from model.side_pane import SidePane


@dataclass
class MenuAction:  # type: ignore
    """
    Represents a menu action with associated text and an optional action to be
    executed.
    """
    text: str
    action: Callable[..., Any] | None
    side_pane: SidePane | None = None
    non_tsp_skip: bool = False
