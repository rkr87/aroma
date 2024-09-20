"""
Defines the SidePane class for representing a sidebar or a pane with a header
and content.
"""
from dataclasses import dataclass

from classes.base.class_base import ClassBase


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
        logger = SidePane.get_static_logger()

        if not secondary:
            logger.debug("Returning primary pane as secondary is None.")
            return primary

        if not primary:
            logger.debug("Returning secondary pane as primary is None.")
            return secondary

        logger.debug("Merging panes. Primary header: %s, content: %s.",
                     primary.header, primary.content)
        logger.debug("Secondary header: %s, content: %s.",
                     secondary.header, secondary.content)

        primary.header = primary.header or secondary.header
        primary.content = primary.content or secondary.content

        logger.debug("Merged pane header: %s, content: %s.",
                     primary.header, primary.content)

        return primary
