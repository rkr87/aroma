"""Custom JSON encoder for dataclass serialization."""

from __future__ import annotations

import dataclasses
import json
from typing import Any

from custom_types.is_data_class import IsDataclass


class DataclassEncoder(json.JSONEncoder):
    """JSON encoder for serializing dataclass instances."""

    def default(self, o: Any) -> dict[str, Any] | Any:
        """
        Converts dataclass instances to dictionaries, omitting None values.
        """
        if isinstance(o, IsDataclass):
            return {k: v for k, v in dataclasses.asdict(o).items() if v}
        return super().default(o)
