"""Utility functions."""

import binascii
import json
import logging
import re
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any, TypeVar
from zipfile import ZIP_LZMA, ZipFile, ZipInfo

from model.file_crc import FileCrc
from py7zr import FileInfo, SevenZipFile
from sdl2.ext import Color

T = TypeVar("T", int, float)


def clamp(value: T, min_value: T, max_value: T) -> T:
    """Clamps a value between a minimum and maximum range."""
    return max(min_value, min(value, max_value))


def tuple_to_sdl_color(rgb: tuple[int, int, int]) -> Color:
    """Convert a tuple of RGB values to an SDL2 Color object."""
    return Color(rgb[0], rgb[1], rgb[2])


def files_to_zip(
    file_paths: list[Path],
    zip_path: Path,
    compresslevel: int = 9,
) -> None:
    """Compress multiple files into a zip archive."""
    logging.info("Creating zip file: %s", zip_path)
    with ZipFile(
        zip_path,
        "w",
        compression=ZIP_LZMA,
        compresslevel=compresslevel,
    ) as zipf:
        for file in file_paths:
            logging.info("Adding file to zip: %s", file)
            zipf.write(file, arcname=file.name)
    logging.info("Created zip file: %s", zip_path)


def extract_from_zip(
    zip_path: Path,
    file_name: str,
    output_path: Path,
) -> None:
    """Extract specific file from a zip archive to a specified output path."""
    logging.info(
        "Extracting %s from %s to %s",
        file_name,
        zip_path,
        output_path,
    )
    with ZipFile(zip_path, "r") as zipf:
        if file_name in zipf.namelist():
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            if output_path.exists():
                output_path.unlink()
            with zipf.open(file_name) as src, output_path.open("wb") as tar:
                tar.write(src.read())
                logging.info(
                    "Extracted %s to %s",
                    file_name,
                    output_path,
                )
        else:
            logging.error(
                "File %s not found in zip archive %s",
                file_name,
                zip_path,
            )


def bytes_from_zip(
    zip_path: Path,
    file_name: str,
) -> bytes | None:
    """Retrieve the contents of a specified file from a zip archive."""
    buffer = None
    logging.info("Extracting %s from %s", file_name, zip_path)
    with ZipFile(zip_path, "r") as zipf:
        if file_name in zipf.namelist():
            with zipf.open(file_name) as source_file:
                buffer = source_file.read()
                logging.info(
                    "Extracted %s",
                    file_name,
                )
        else:
            logging.error(
                "File %s not found in zip archive %s",
                file_name,
                zip_path,
            )
    return buffer


def get_zip_info(
    zip_path: Path,
) -> list[FileCrc]:
    """Retrieve CRC information for all files in a zip archive."""
    with ZipFile(zip_path, "r") as archive:
        file_list: list[ZipInfo] = archive.filelist
    return [FileCrc(zf.filename, f"{zf.CRC:08x}") for zf in file_list]


def get_7z_info(
    archive_path: Path,
) -> list[FileCrc]:
    """Retrieve CRC information for all files in a 7z archive."""
    with SevenZipFile(archive_path, mode="r") as archive:
        file_list: list[FileInfo] = archive.list()
    return [FileCrc(zf.filename, f"{zf.crc32:08x}") for zf in file_list]


def get_archive_info(
    archive_path: Path,
) -> list[FileCrc]:
    """Determine the type of archive and retrieves file CRC information."""
    extractors: dict[str, Callable[[Path], list[FileCrc]]] = {
        ".7z": get_7z_info,
        ".zip": get_zip_info,
    }
    if x := extractors.get(archive_path.suffix):
        return x(archive_path)
    return []


def check_crc(data: Path | bytes) -> str:
    """Calculate and returns the CRC32 checksum of a file."""
    logging.debug("Calculating CRC32 checksum for file: %s", data)
    if isinstance(data, Path):
        with Path.open(data, "rb") as f:  # pylint: disable=unspecified-encoding
            data = f.read()
    crc: int = binascii.crc32(data) & 0xFFFFFFFF
    logging.debug("CRC32 checksum: %s", crc)
    return f"{crc:08x}"


def delete_file(file: Path) -> None:
    """Delete the specified file if it exists."""
    logging.info("Attempting to delete file: %s", file)
    try:
        file.unlink()
        logging.info("Successfully removed file: %s", file)
    except FileNotFoundError:
        logging.exception("File not found: %s", file)
    except PermissionError:
        logging.exception("Permission denied: %s", file)
    except OSError:
        logging.exception("OS error occurred while removing file %s", file)


def rename_file(file: Path, new_name: Path) -> None:
    """Rename the specified file to a new name."""
    logging.info("Attempting to rename file: %s to %s", file, new_name)
    try:
        file.rename(new_name)
        logging.info("Successfully renamed file %s to %s", file, new_name)
    except FileNotFoundError:
        logging.exception("File not found: %s", file)
    except PermissionError:
        logging.exception("Permission denied: %s", file)
    except OSError:
        logging.exception("OS error occurred while renaming file %s", file)


def get_callable_name(func: Callable[..., Any]) -> str:
    """Return the fully qualified name of a callable object."""
    func = func.func if isinstance(func, partial) else func
    return f"{func.__module__}.{func.__name__}"


def load_simple_json(path: Path) -> dict[str, Any]:
    """Load a simple JSON file as a dictionary of strings."""
    if not path.is_file():
        return {}
    try:
        with path.open("r", encoding="utf8") as file:
            data: dict[str, Any] = json.load(file)
    except json.JSONDecodeError:
        logging.exception("JSON decode error")
        data = {}
    return data


def remove_loop(text: str, pattern: re.Pattern[str]) -> str:
    """Recursively remove text matching the pattern."""
    new_text, n = re.subn(pattern, "", text)
    return remove_loop(new_text, pattern) if n > 0 else new_text.strip()


def is_relative_path(path: Path, base_path: Path) -> bool:
    """Check whether a path is a sub-path of base path."""
    return str(path).startswith(str(base_path))
