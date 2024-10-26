"""Defines the SidePane class for representing a sidebar."""

from dataclasses import dataclass

from shared.classes.class_base import ClassBase


@dataclass
class SidePane(ClassBase):  # pylint: disable=too-many-instance-attributes
    """Represents a side pane with an optional header and content."""

    header: str | None = None
    content: str | list[str] | None = None
    bg_img: str | None = None
    img: str | None = None
    trim_long_lines: bool = False

    @staticmethod
    def merge(
        primary: "SidePane | None",
        secondary: "SidePane | None",
    ) -> "SidePane | None":
        """Merge two side panes, primary pane content takes precedence."""
        logger = SidePane.get_static_logger()

        if not secondary:
            logger.debug("Returning primary pane as secondary is None.")
            return primary

        if not primary:
            logger.debug("Returning secondary pane as primary is None.")
            return secondary

        logger.debug(
            "Merging panes. Primary header: %s, content: %s.",
            primary.header,
            primary.content,
        )
        logger.debug(
            "Secondary header: %s, content: %s.",
            secondary.header,
            secondary.content,
        )

        primary.header = primary.header or secondary.header
        primary.content = primary.content or secondary.content

        logger.debug(
            "Merged pane header: %s, content: %s.",
            primary.header,
            primary.content,
        )

        return primary
