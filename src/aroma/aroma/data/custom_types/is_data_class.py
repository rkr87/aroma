"""Protocol for checking if an object is a dataclass."""

import dataclasses
from typing import Any, ClassVar, Protocol, runtime_checkable


@runtime_checkable
@dataclasses.dataclass
class IsDataclass(Protocol):
    """Protocol for verifying dataclass properties."""
    __dataclass_fields__: ClassVar[dict[str, Any]]
