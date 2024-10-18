"""TODO."""

from dataclasses import dataclass


@dataclass
class KeyboardButton:
    """TODO."""

    key: str
    weight: int = 1
    toggled: bool = False
    hint_img: str | None = None
