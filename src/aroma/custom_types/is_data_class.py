"""TODO"""
import dataclasses
from typing import Any, ClassVar, Protocol, runtime_checkable


@runtime_checkable
@dataclasses.dataclass
class IsDataclass(Protocol):
    """TODO"""
    __dataclass_fields__: ClassVar[dict[str, Any]]
