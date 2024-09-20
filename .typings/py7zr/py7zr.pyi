
import pathlib
import types
from typing import Any, BinaryIO

class FileInfo:
    filename: str
    crc32: int


class SevenZipFile:
    def __enter__(self) -> Any: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None
    ) -> None: ...
    def __init__(
        self,
        file: BinaryIO | str | pathlib.Path,
        mode: str = 'r', *,
        filters: list[dict[str, int]] | None = None,
        dereference: bool = False,
        password: str | None = None,
        header_encryption: bool = False,
        blocksize: int | None = None,
        mp: bool = False
    ) -> None: ...
    def list(self) -> list[FileInfo]: ...
