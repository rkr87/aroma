"""Custom JSON encoder for dataclass serialization."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any

from data.custom_types.is_data_class import IsDataclass


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder for serializing dataclass instances."""

    def default(self, o: Any) -> Any:  # noqa: ANN401
        """Convert dataclass instances to dictionaries."""
        if isinstance(o, IsDataclass):
            return {k: v for k, v in dataclasses.asdict(o).items() if v}
        if isinstance(o, Path):
            return str(o)
        return super().default(o)
