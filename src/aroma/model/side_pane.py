"""
Defines the SidePane class for representing a sidebar or a pane with a header
and content.
"""
from dataclasses import dataclass


@dataclass
class SidePane:
    """
    Represents a side pane with an optional header and content.
    """
    header: str | None = None
    content: str | None = None
