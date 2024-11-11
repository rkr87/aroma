"""TODO."""

import io
import zipfile
from pathlib import Path

from data.tools.http_request_handler import HttpRequestHandler
from packaging import version
from shared.classes.class_singleton import ClassSingleton

_REPO_PATH = "rkr87/aroma/releases/latest"
_LATEST_RELEASE = f"https://api.github.com/repos/{_REPO_PATH}"
_ASSET = f"https://github.com/{_REPO_PATH}/download/aroma.zip"

VERSION = "0.4.0a10"


class Updater(ClassSingleton):
    """TODO."""

    @staticmethod
    def check_for_update() -> bool:
        """Check if a new version is available."""
        http = HttpRequestHandler()
        if not (response := http.get(_LATEST_RELEASE)):
            return False
        if not (data := http.parse_json(response)):
            return False
        if not (latest := data.get("tag_name")):
            return False
        return Updater._compare_versions(VERSION, latest)

    @staticmethod
    def _compare_versions(current: str, latest: str) -> bool:
        """TODO."""
        return version.parse(latest) > version.parse(current)

    @staticmethod
    def download_and_extract_release() -> None:
        """TODO."""
        if not (response := HttpRequestHandler.get(_ASSET)):
            return
        zip_data = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_data) as zip_file:
            zip_file.extractall(Path.cwd().parent)
