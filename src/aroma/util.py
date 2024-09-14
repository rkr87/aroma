"""
Utility functions.
"""
import binascii
import logging
import os
import subprocess
from collections.abc import Callable
from functools import partial
from typing import Any, overload
from zipfile import ZIP_LZMA, ZipFile

from sdl2.ext import Color


@overload
def clamp(value: int, min_value: int, max_value: int) -> int: ...
@overload
def clamp(value: float, min_value: float, max_value: float) -> float: ...


def clamp(
    value: int | float,
    min_value: int | float,
    max_value: int | float
) -> int | float:
    """
    Clamps a value between a minimum and maximum range.
    """
    return max(min_value, min(value, max_value))


def tuple_to_sdl_color(rgb: tuple[int, int, int]) -> Color:
    """
    Converts a tuple of RGB values to an SDL2 Color object.
    """
    return Color(rgb[0], rgb[1], rgb[2])


def files_to_zip(file_paths: list[str], zip_path: str) -> None:
    """
    Compresses multiple files into a zip archive.
    """
    logging.info("Creating zip file: %s", zip_path)
    with ZipFile(zip_path, "w", compression=ZIP_LZMA, compresslevel=9) as zipf:
        for file in file_paths:
            logging.info("Adding file to zip: %s", file)
            zipf.write(file, arcname=os.path.basename(file))
    logging.info("Created zip file: %s", zip_path)


def extract_from_zip(zip_path: str, file_name: str, output_path: str) -> None:
    """
    Extracts a specific file from a zip archive to a specified output path.
    """
    logging.info(
        "Extracting %s from %s to %s", file_name, zip_path, output_path
    )
    with ZipFile(zip_path, 'r') as zipf:
        if file_name in zipf.namelist():
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if os.path.isfile(output_path):
                os.remove(output_path)
            with zipf.open(file_name) as source_file:
                with open(output_path, 'wb') as target_file:
                    target_file.write(source_file.read())
                    logging.info(
                        "Extracted %s to %s", file_name, output_path
                    )
        else:
            logging.error(
                "File %s not found in zip archive %s", file_name, zip_path
            )


def check_crc(file_path: str) -> str:
    """
    Calculates and returns the CRC32 checksum of a file.
    """
    logging.info("Calculating CRC32 checksum for file: %s", file_path)
    with open(file_path, "rb") as f:
        file_data: bytes = f.read()
        crc: int = binascii.crc32(file_data)
    checksum = hex(crc)
    logging.info("CRC32 checksum for file %s: %s", file_path, checksum)
    return checksum


def reboot() -> None:
    """Force a reboot on Unix-like systems (Linux, macOS)."""
    logging.info("Rebooting the system.")
    subprocess.run(['reboot'], check=False)
    logging.info("System reboot command issued.")


def delete_file(file: str) -> None:
    """
    Deletes the specified file if it exists. Logs information about the removal
    and any errors that occur during the process.
    """
    logging.info("Attempting to delete file: %s", file)
    try:
        os.remove(file)
        logging.info("Successfully removed file: %s", file)
    except FileNotFoundError:
        logging.error("File not found: %s", file)
    except PermissionError:
        logging.error("Permission denied: %s", file)
    except OSError as e:
        logging.error("OS error occurred while removing file %s: %s", file, e)


def rename_file(file: str, new_name: str) -> None:
    """
    Renames the specified file to a new name. Logs the process and errors.
    """
    logging.info("Attempting to rename file: %s to %s", file, new_name)
    try:
        os.rename(file, new_name)
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
