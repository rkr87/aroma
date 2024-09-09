"""
Utility functions.
"""
import binascii
import os
import subprocess
from typing import overload
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
    with ZipFile(zip_path, "w", compression=ZIP_LZMA, compresslevel=9) as zipf:
        for file in file_paths:
            zipf.write(file, arcname=os.path.basename(file))


def extract_from_zip(zip_path: str, file_name: str, output_path: str) -> None:
    """
    Extracts a specific file from a zip archive to a specified output path.
    """
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


def check_crc(file_path: str) -> str:
    """
    Calculates and returns the CRC32 checksum of a file.
    """
    with open(file_path, "rb") as f:
        file_data: bytes = f.read()
        crc: int = binascii.crc32(file_data)
    return hex(crc)


def reboot() -> None:
    """Force a reboot on Unix-like systems (Linux, macOS)."""
    subprocess.run(['reboot'], check=False)
