"""
Utility functions.
"""
import binascii
import json
import logging
import subprocess
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any, TypeVar
from zipfile import ZIP_LZMA, ZipFile, ZipInfo

from py7zr import FileInfo, SevenZipFile
from sdl2.ext import Color

from model.file_crc import FileCrc

T = TypeVar('T', int, float)


def clamp(value: T, min_value: T, max_value: T) -> T:
    """Clamps a value between a minimum and maximum range."""
    return max(min_value, min(value, max_value))


def tuple_to_sdl_color(rgb: tuple[int, int, int]) -> Color:
    """
    Converts a tuple of RGB values to an SDL2 Color object.
    """
    return Color(rgb[0], rgb[1], rgb[2])


def files_to_zip(
    file_paths: list[Path],
    zip_path: Path,
    compresslevel: int = 9
) -> None:
    """
    Compresses multiple files into a zip archive.
    """
    logging.info("Creating zip file: %s", zip_path)
    with ZipFile(
        zip_path,
        "w",
        compression=ZIP_LZMA,
        compresslevel=compresslevel
    ) as zipf:
        for file in file_paths:
            logging.info("Adding file to zip: %s", file)
            zipf.write(file, arcname=file.name)
    logging.info("Created zip file: %s", zip_path)


def extract_from_zip(
    zip_path: Path,
    file_name: str,
    output_path: Path
) -> None:
    """
    Extracts a specific file from a zip archive to a specified output path.
    """
    logging.info(
        "Extracting %s from %s to %s", file_name, zip_path, output_path
    )
    with ZipFile(zip_path, 'r') as zipf:
        if file_name in zipf.namelist():
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            if output_path.exists():
                output_path.unlink()
            with zipf.open(file_name) as source_file:
                with output_path.open('wb') as target_file:
                    target_file.write(source_file.read())
                    logging.info(
                        "Extracted %s to %s", file_name, output_path
                    )
        else:
            logging.error(
                "File %s not found in zip archive %s", file_name, zip_path
            )


def bytes_from_zip(
    zip_path: Path,
    file_name: str
) -> bytes | None:
    """
    TODO
    """
    buffer = None
    logging.info("Extracting %s from %s", file_name, zip_path)
    with ZipFile(zip_path, 'r') as zipf:
        if file_name in zipf.namelist():
            with zipf.open(file_name) as source_file:
                buffer = source_file.read()
                logging.info(
                    "Extracted %s", file_name
                )
        else:
            logging.error(
                "File %s not found in zip archive %s", file_name, zip_path
            )
    return buffer


def get_zip_info(
    zip_path: Path,
) -> list[FileCrc]:
    """
    TODO
    """
    with ZipFile(zip_path, 'r') as archive:
        file_list: list[ZipInfo] = archive.filelist
    return [
        FileCrc(zf.filename, f"{zf.CRC:08x}")
        for zf in file_list
    ]


def get_7z_info(
    archive_path: Path,
) -> list[FileCrc]:
    """
    TODO
    """
    with SevenZipFile(archive_path, mode='r') as archive:
        file_list: list[FileInfo] = archive.list()
    return [
        FileCrc(zf.filename, f"{zf.crc32:08x}")
        for zf in file_list
    ]


def get_archive_info(
    archive_path: Path,
) -> list[FileCrc]:
    """
    TODO
    """
    extractors: dict[str, Callable[[Path], list[FileCrc]]] = {
        ".7z": get_7z_info,
        ".zip": get_zip_info
    }
    if x := extractors.get(archive_path.suffix):
        return x(archive_path)
    return []


def check_crc(data: Path | bytes) -> str:
    """
    Calculates and returns the CRC32 checksum of a file.
    """
    logging.info("Calculating CRC32 checksum for file: %s", data)
    if isinstance(data, Path):
        with open(data, "rb") as f:
            data = f.read()
    crc: int = binascii.crc32(data) & 0xFFFFFFFF
    logging.info("CRC32 checksum: %s", crc)
    return f"{crc:08x}"


def reboot() -> None:
    """Force a reboot on Unix-like systems (Linux, macOS)."""
    logging.info("Rebooting the system.")
    subprocess.run(['reboot'], check=False)
    logging.info("System reboot command issued.")


def delete_file(file: Path) -> None:
    """
    Deletes the specified file if it exists. Logs information about the removal
    and any errors that occur during the process.
    """
    logging.info("Attempting to delete file: %s", file)
    try:
        file.unlink()
        logging.info("Successfully removed file: %s", file)
    except FileNotFoundError:
        logging.error("File not found: %s", file)
    except PermissionError:
        logging.error("Permission denied: %s", file)
    except OSError as e:
        logging.error("OS error occurred while removing file %s: %s", file, e)


def rename_file(file: Path, new_name: Path) -> None:
    """
    Renames the specified file to a new name. Logs the process and errors.
    """
    logging.info("Attempting to rename file: %s to %s", file, new_name)
    try:
        file.rename(new_name)
        logging.info("Successfully renamed file %s to %s", file, new_name)
    except FileNotFoundError:
        logging.error("File not found: %s", file)
    except PermissionError:
        logging.error("Permission denied: %s", file)
    except OSError as e:
        logging.error("OS error occurred while renaming file %s: %s", file, e)


def get_callable_name(func: Callable[..., Any]) -> str:
    """
    Returns the fully qualified name of a callable object.
    """
    func = func.func if isinstance(func, partial) else func
    return f"{func.__module__}.{func.__name__}"


def load_simple_json(path: Path) -> dict[str, Any]:
    """
    Loads a simple JSON file as a dictionary of strings.
    """
    if not path.is_file():
        return {}
    try:
        with path.open("r", encoding="utf8") as file:
            data: dict[str, Any] = json.load(file)
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
        data = {}
    return data
