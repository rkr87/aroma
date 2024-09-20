"""TODO"""

from dataclasses import dataclass
from typing import Self

import apsw


@dataclass
class DBResult:
    """TODO"""

    @classmethod
    def factory(
        cls,
        row: tuple["apsw.SQLiteValue", ...]
    ) -> Self:
        """TODO"""
        return cls(*row)
