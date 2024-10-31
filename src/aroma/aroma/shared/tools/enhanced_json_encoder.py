"""Custom JSON encoder for dataclass serialization."""

from __future__ import annotations

import dataclasses
import json
from enum import Enum
from pathlib import Path
from typing import Any

from data.custom_types.is_data_class import IsDataclass

EXCLUDE_FROM_SERIALIZATION = "exclude_from_serialization"


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder for serializing dataclass instances."""

    def default(self, o: Any) -> Any:  # noqa: ANN401
        """Convert dataclass instances to dictionaries."""
        if isinstance(o, IsDataclass):
            return {
                k: v
                for k, v in dataclasses.asdict(o).items()
                if v and not self._is_excluded(k, o)
            }
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

    @staticmethod
    def _is_excluded(field_name: str, instance: IsDataclass) -> bool:
        """Check if a field should be excluded from serialization."""
        field_info = dataclasses.fields(instance.__class__)
        for field in field_info:
            if field.name == field_name:
                return field.metadata.get(EXCLUDE_FROM_SERIALIZATION, False)
        return False
