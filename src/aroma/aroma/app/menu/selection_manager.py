"""Module for managing menu selection state and navigation."""

from dataclasses import dataclass
from enum import Enum, auto

from shared.classes.class_base import ClassBase
from shared.constants import MAX_ITEMS_PER_PAGE
from shared.tools.util import clamp


class _MenuPos(Enum):
    """Enum to represent the position of the menu relative to page."""

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
        _start: int = 0

        def cycle_items(
            self,
            delta: int,
            *,
            recycle: bool = True,
        ) -> None:
            """Cycle through items, with optional recycling of indices."""
            new_index: int = self.selected + delta

            if recycle:
                self.selected = new_index % self.total
                return

            if self.selected > self._start and delta < 0:
                self.selected = self._start
                return

            if self._start == self.max_start and delta > 0:
                self.selected = self.total - 1
                return

            self._start = clamp(new_index, 0, self.max_start)
            if not self._start <= self.selected < self.end or delta < 0:
                self.selected = self._start

        @property
        def max(self) -> int:
            """Return the maximum number of visible items per page."""
            return min(self.total, MAX_ITEMS_PER_PAGE)

        @property
        def start(self) -> int:
            """TODO."""
            if self.pos == _MenuPos.BOTTOM and self.selected >= self.end:
                self._start = self.selected - self.max + 1
                return self._start
            if self.selected < self._start or self.selected >= self.end:
                self._start = self.selected
                return self._start
            self._start = min(self._start, self.total - self.max)
            return self._start

        @property
        def end(self) -> int:
            """Return the end index of the visible slice."""
            return self._start + self.max

        @property
        def max_start(self) -> int:
            """Return the maximum start index for pagination."""
            return self.total - self.max

        def reset(self) -> None:
            """Reset the selection state to its initial values."""
            self.selected = 0
            self.pos = _MenuPos.TOP

    def __init__(self, total_items: int) -> None:
        super().__init__()
        self.state = self._SelectionState(total_items)

    def next_page(self) -> None:
        """Move to the next page of items."""
        self.state.cycle_items(self.state.max, recycle=False)
        self.state.pos = _MenuPos.TOP
        self._logger.debug(
            "Moved to next page. Current position: %s",
            self.state.pos,
        )

    def prev_page(self) -> None:
        """Move to the previous page of items."""
        self.state.cycle_items(-self.state.max, recycle=False)
        self.state.pos = _MenuPos.TOP
        self._logger.debug(
            "Moved to previous page. Current position: %s",
            self.state.pos,
        )

    def next_item(self) -> None:
        """Select the next menu item."""
        self.state.cycle_items(1)
        self.state.pos = _MenuPos.BOTTOM
        self._logger.debug(
            "Selected next item. Current position: %s",
            self.state.pos,
        )

    def prev_item(self) -> None:
        """Select the previous menu item."""
        self.state.cycle_items(-1)
        self.state.pos = _MenuPos.TOP
        self._logger.debug(
            "Selected previous item. Current position: %s",
            self.state.pos,
        )
