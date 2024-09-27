"""Database result handling module."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    import apsw


@dataclass
class DBResult:
    """Represents a result row from the database."""

    @classmethod
    def factory(
        cls,
        row: tuple["apsw.SQLiteValue", ...],
    ) -> Self:
        """Create a DBResult instance from a database row."""
        return cls(*row)
