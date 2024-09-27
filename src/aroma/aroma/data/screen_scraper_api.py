"""Defines the ScreenScraper API class for fetching game media data."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from classes.base.class_singleton import ClassSingleton
from model.media_item import MediaItem
from tools.app_config import AppConfig


class ScreenScraperAPI(ClassSingleton):
    """Provides methods to interact with the ScreenScraper API."""

    BASE_URL = "https://www.screenscraper.fr/api2/"

    @staticmethod
    def _load_json(response_data: bytes) -> dict[str, Any]:  # type: ignore[misc]
        """Load JSON data from bytes."""
        try:
            result: dict[str, Any] = json.loads(response_data.decode("utf-8"))
        except json.JSONDecodeError as e:
            ScreenScraperAPI.get_static_logger().error(
                "JSON decode error: %s", str(e)
            )
            return {}
        return result

    def _make_request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a request to the ScreenScraper API using urllib."""
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
        url = f"{self.BASE_URL}{endpoint}?" + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                response_data = response.read()
        except urllib.error.HTTPError as e:
            ScreenScraperAPI.get_static_logger().error(
                "HTTP error occurred: %s - %s", e.code, e.reason
            )
            return {}
        except urllib.error.URLError as e:
            ScreenScraperAPI.get_static_logger().error(
                "URL error occurred: %s", str(e.reason)
            )
            return {}
        return self._load_json(response_data)

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
            ScreenScraperAPI.get_static_logger().error(
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
