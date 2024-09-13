"""
Module for managing menu selection state and navigation in a paginated menu
system.

This module defines the `SelectionManager` class, which handles the logic for
navigating through menu items, managing pagination, and tracking the current
selection state.
"""

from dataclasses import dataclass
from enum import Enum, auto

from base.class_base import ClassBase
from constants import MAX_ITEMS_PER_PAGE
from util import clamp


class _MenuPos(Enum):
    """
    Enum to represent the position of the menu relative to the visible page.
    """
    BOTTOM = auto()
    TOP = auto()


class SelectionManager(ClassBase):
    """Manages selection and pagination for menu items."""

    @dataclass
    class _SelectionState:
        """Stores metadata about the selection state and pagination."""
        total: int
        selected: int = 0
        pos: _MenuPos = _MenuPos.BOTTOM
        start: int = 0

        @property
        def max(self) -> int:
            """Return the maximum number of visible items per page."""
            return min(self.total, MAX_ITEMS_PER_PAGE)

        @property
        def end(self) -> int:
            """Return the end index of the visible slice."""
            return self.start + self.max

        @property
        def max_start(self) -> int:
            """Return the maximum start index for pagination."""
            return self.total - self.max

        @property
        def selected_in_slice(self) -> bool:
            """
            Check if the selected item is within the current visible slice.
            """
            return self.start <= self.selected < self.end

        def reset(self) -> None:
            """Reset the selection state to its initial values."""
            self.selected = 0
            self.start = 0
            self.pos = _MenuPos.BOTTOM

    def __init__(self, total_items: int):
        """Initialize with the total number of items."""
        super().__init__()
        self.state = self._SelectionState(total_items)

    def cycle_items(
        self,
        delta: int,
        total_items: int,
        recycle: bool = True
    ) -> None:
        """Cycle through items, with optional recycling of indices."""
        new_index: int = self.state.selected + delta

        if recycle:
            self.state.selected = new_index % total_items
        else:
            self.state.selected = clamp(new_index, 0, total_items - 1)

    def next_page(self) -> None:
        """Move to the next page of items."""
        self.cycle_items(self.state.max, self.state.total, False)
        self.state.pos = _MenuPos.TOP

    def prev_page(self) -> None:
        """Move to the previous page of items."""
        self.cycle_items(-self.state.max, self.state.total, False)
        self.state.pos = _MenuPos.TOP

    def next_item(self) -> None:
        """Select the next menu item."""
        self.cycle_items(1, self.state.total)
        self.state.pos = _MenuPos.BOTTOM

    def prev_item(self) -> None:
        """Select the previous menu item."""
        self.cycle_items(-1, self.state.total)
        self.state.pos = _MenuPos.TOP
