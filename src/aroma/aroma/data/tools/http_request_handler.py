"""Handles generic HTTP requests and response parsing."""

import json
from typing import Any

import requests
from shared.classes.class_singleton import ClassSingleton


class HttpRequestHandler(ClassSingleton):
    """Handles generic HTTP requests and response parsing."""

    @staticmethod
    def _log_error(message: str, error: Exception) -> None:
        """Log an error with details."""
        HttpRequestHandler.get_static_logger().debug(
            "%s: %s", message, str(error)
        )

    @classmethod
    def get(  # type: ignore[misc]
        cls, url: str, params: dict[str, Any] | None = None, timeout: int = 10
    ) -> requests.Response | None:
        """Make a GET request."""
        try:
            response = requests.get(url, params=params, timeout=timeout)
        except requests.exceptions.RequestException as e:
            HttpRequestHandler._log_error("GET request failed", e)
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            HttpRequestHandler._log_error("HTTP error in GET request", e)
            return None

        return response

    @classmethod
    def post(  # type: ignore[misc]
        cls,
        url: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> requests.Response | None:
        """Make a POST request."""
        try:
            response = requests.post(
                url, data=data, json=json_data, timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            HttpRequestHandler._log_error("POST request failed", e)
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            HttpRequestHandler._log_error("HTTP error in POST request", e)
            return None

        return response

    @classmethod
    def parse_json(cls, response: requests.Response) -> dict[str, Any] | None:  # type: ignore[misc]
        """Parse the JSON response content."""
        try:
            return response.json()  # type: ignore[no-any-return]
        except json.JSONDecodeError as e:
            HttpRequestHandler._log_error("Failed to decode JSON: %s", e)
            return None
