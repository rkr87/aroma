"""
Defines the SidePane class for representing a sidebar or a pane with a header
and content.
"""
from dataclasses import dataclass

from base.class_base import ClassBase


@dataclass
class SidePane(ClassBase):
    """
    Represents a side pane with an optional header and content, allowing for
    merging of multiple panes.
    """
    header: str | None = None
    content: str | None = None

    @staticmethod
    def merge(
        primary: "SidePane | None",
        secondary: "SidePane | None"
    ) -> "SidePane | None":
        """
        Merge two side panes, with primary pane content taking precedence
        """
        if not secondary:
            return primary
        if not primary:
            return secondary
        primary.header = primary.header or secondary.header
        primary.content = primary.content or secondary.content
        return primary
