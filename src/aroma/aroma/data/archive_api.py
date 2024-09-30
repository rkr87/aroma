"""TODO."""

import platform
import sys
from pathlib import Path
from typing import Any

from constants import ARCHIVE_AUTH_CONFIG
from requests import Response
from requests.auth import HTTPBasicAuth
from requests.cookies import (
    create_cookie,  # pyright: ignore[reportUnknownVariableType]
)
from requests.sessions import Session
from requests.utils import default_headers
from tools import util
from tools.app_config import AppConfig


def download_file(
    archive_id: str, archive_path: str, save_path: Path, *, auth_req: bool
) -> bool:
    """TODO.."""
    with ArchiveAPISession() as session:
        if (
            data := session.make_request(
                f"/download/{archive_id}{archive_path}", auth_req=auth_req
            )
        ) is None:
            return False
        with save_path.open(mode="wb") as f:
            f.write(data.content)
        return save_path.is_file()


class ArchiveAPISession(Session):
    """TODO."""

    BASE_URL = "https://archive.org"

    def __init__(self) -> None:
        super().__init__()
        self._auth: dict[str, Any] = self._get_auth_config()
        for ck, cv in self._auth.get("cookies", {}).items():
            raw_cookie = f"{ck}={cv}"
            cookie_dict = self._parse_dict_cookies(raw_cookie)
            if not cookie_dict.get(ck):
                continue
            cookie = create_cookie(  # type: ignore[no-untyped-call]
                ck,
                cookie_dict[ck],
                domain=cookie_dict.get("domain", ".archive.org"),
                path=cookie_dict.get("path", "/"),
            )
            self.cookies.set_cookie(cookie)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        self._access_key: str = self._auth.get("auth", {}).get("access", "")
        self._secret_key: str = self._auth.get("auth", {}).get("secret", "")
        self.headers = default_headers()  # type: ignore[assignment]
        self.headers.update({"User-Agent": self._get_user_agent_string()})
        self.headers.update({"Connection": "close"})

    def make_request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        *,
        auth_req: bool,
    ) -> Response | None:
        """TODO."""
        auth = None
        if auth_req:
            if self._access_key and self._secret_key:
                auth = HTTPBasicAuth(self._access_key, self._secret_key)
            else:
                return None
        return self.get(
            f"{self.BASE_URL}{path}",
            params=params if params else {},
            auth=auth,
        )

    def _get_auth_config(self) -> dict[str, Any]:
        """TODO."""
        if not ARCHIVE_AUTH_CONFIG.is_file():
            return self._authenticate()
        auth_config = util.load_simple_json(ARCHIVE_AUTH_CONFIG)
        if auth_config["date"] < util.get_datestamp() - 300:
            return self._authenticate()
        return auth_config

    def _authenticate(self) -> dict[str, Any]:
        """TODO."""
        if not (AppConfig().archive_userid) or not (
            AppConfig().archive_password
        ):
            return {}
        url = f"{self.BASE_URL}/services/xauthn/"
        params = {"op": "login"}
        data = {
            "email": AppConfig().archive_userid,
            "password": AppConfig().archive_password,
        }
        if not (r := self.post(url, params=params, data=data)):
            return {}
        j = r.json()
        if not j.get("success"):
            return {}
        auth_config = {
            "date": util.get_datestamp(),
            "auth": {
                "access": j["values"]["s3"]["access"],
                "secret": j["values"]["s3"]["secret"],
            },
            "cookies": {
                "logged-in-user": j["values"]["cookies"]["logged-in-user"],
                "logged-in-sig": j["values"]["cookies"]["logged-in-sig"],
            },
        }
        util.save_simple_json(auth_config, ARCHIVE_AUTH_CONFIG)
        return auth_config

    @staticmethod
    def _parse_dict_cookies(value: str) -> dict[str, str | None]:
        """TODO."""
        result: dict[str, str | None] = {}
        for item in value.split(";"):
            if not (item := item.strip()):
                continue
            if len(i := item.split("=", 1)) <= 1:
                result[item] = None
                continue
            result[i[0]] = i[1]
        return result

    def _get_user_agent_string(self) -> str:
        """Generate a User-Agent string to be sent with every request."""
        uname = platform.uname()
        py_version = "{}.{}.{}".format(*sys.version_info)  # pylint: disable=consider-using-f-string
        return (
            "internetarchive/4.1.0"
            f"({uname[0]} {uname[-1]}; N; ; {self._access_key}) "
            f"Python/{py_version}"
        )
