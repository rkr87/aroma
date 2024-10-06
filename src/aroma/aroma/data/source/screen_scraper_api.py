"""Defines the ScreenScraper API class for fetching game media data."""

from typing import Any

from data.model.media_item import MediaItem
from data.tools.http_request_handler import HttpRequestHandler
from shared.app_config import AppConfig


class ScreenScraperAPI(HttpRequestHandler):
    """Provides methods to interact with the ScreenScraper API."""

    BASE_URL = "https://www.screenscraper.fr/api2/"

    def _make_request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a request to the ScreenScraper API."""
        if params is None:
            params = {}
        params.update(
            {
                "devid": "Schmurtz",
                "devpassword": "KH0ocJ3xt5N",
                "softname": "crossmix",
                "output": "json",
                "romtype": "rom",
                "ssid": AppConfig().screenscraper_userid,
                "sspassword": AppConfig().screenscraper_password,
            }
        )
        url = f"{self.BASE_URL}{endpoint}"
        if response := self.get(url, params=params):
            return self.parse_json(response) or {}

        return {}

    def _get_game_media(
        self, params: dict[str, str], region_priority: dict[str, int]
    ) -> list[MediaItem] | None:
        """Fetch game media data based on the given parameters."""
        result = self._make_request("jeuInfos.php", params)
        try:
            return MediaItem.from_list(
                result["response"]["jeu"]["medias"], region_priority
            )
        except KeyError as e:
            ScreenScraperAPI.get_static_logger().debug(
                "Key error while accessing media data: %s", str(e)
            )
            return None

    def get_game_media_by_name(
        self, name: str, system: str | None, region_priority: dict[str, int]
    ) -> list[MediaItem] | None:
        """Retrieve game media by name and optional system."""
        params = {"romnom": name}
        if system:
            params["systemeid"] = system
        return self._get_game_media(params, region_priority)

    def get_game_media_by_crc(
        self, crc: str, region_priority: dict[str, int]
    ) -> list[MediaItem] | None:
        """Retrieve game media by CRC value."""
        params = {"crc": crc}
        return self._get_game_media(params, region_priority)
