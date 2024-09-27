"""Module for managing media items."""

from dataclasses import dataclass

from constants import (
    SCRAPER_MAX_HEIGHT,
    SCRAPER_MAX_WIDTH,
)
from tools.app_config import AppConfig


@dataclass
class MediaItem:
    """Represents a media item, such as a game image."""

    type: str
    _base_url: str
    region: str

    @property
    def url(self) -> str:
        """Return the item's URL with the max allowed width and height."""
        params = f"maxwidth={SCRAPER_MAX_WIDTH}&maxheight={SCRAPER_MAX_HEIGHT}"
        return f"{self._base_url}&{params}"

    @staticmethod
    def from_dict(obj: dict[str, str]) -> "MediaItem":
        """Create a MediaItem instance from a dictionary."""
        _type = str(obj.get("type"))
        _url = str(obj.get("url"))
        _region = str(obj.get("region"))
        return MediaItem(_type, _url, _region)

    @staticmethod
    def from_list(
        obj: list[dict[str, str]], region_priority: dict[str, int]
    ) -> list["MediaItem"]:
        """Create a list of MediaItems and sort them by region priority."""
        valid_items = [
            mi
            for o in obj
            if (mi := MediaItem.from_dict(o))
            and mi.type == AppConfig().scrape_media_type
        ]
        if len(valid_items) <= 1:
            return valid_items
        return sorted(
            valid_items,
            key=lambda d: region_priority.get(d.region, len(region_priority)),
        )
