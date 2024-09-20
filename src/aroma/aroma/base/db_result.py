"""Database result handling module."""

from dataclasses import dataclass
from typing import Self

import apsw


@dataclass
class DBResult:
    """Represents a result row from the database."""

    @classmethod
    def factory(
        cls,
        row: tuple["apsw.SQLiteValue", ...]
    ) -> Self:
        """Creates a DBResult instance from a database row."""
        return cls(*row)
