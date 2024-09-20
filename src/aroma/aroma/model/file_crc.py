"""Represents a file's CRC (Cyclic Redundancy Check) information."""

from dataclasses import dataclass


@dataclass
class FileCrc:
    """Data class for storing a file's name and its CRC checksum."""

    filename: str
    crc: str
