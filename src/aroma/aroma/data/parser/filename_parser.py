"""Parses filenames to extract ROM details."""

import re
from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import (
    NAMING_DISC_PATTERN,
    NAMING_EXCLUDE_SYSTEMS,
    NAMING_FORMAT_PATTERN,
    NAMING_REGION_RESOURCE,
    NAMING_REMOVE_PATTERN,
    NAMING_SEARCH_PATTERN,
)
from model.rom_detail import RomDetail
from tools import util

REPLACE_STRINGS = {
    "New Zealand": "New|Zealand",
    "Hong Kong": "Hong|Kong",
    "United Kingdom": "United|Kingdom",
}


class FilenameParser(ClassSingleton):
    """Handles parsing of filenames to extract ROM details."""

    def __init__(self) -> None:
        super().__init__()
        self._region_map = util.load_simple_json(NAMING_REGION_RESOURCE)
        self._region_set = set(self._region_map.keys())

    @staticmethod
    def _replace_strings(value: str) -> str:
        """Replace all occurrences of keys in REPLACE_STRINGS."""
        for old, new in REPLACE_STRINGS.items():
            value = re.sub(old, new, value, flags=re.IGNORECASE)
        return value

    @staticmethod
    def _split_and_normalise(value: str) -> list[str]:
        """Split a string by commas, hyphens, and spaces."""
        items = re.split(r"[,\-\s]+", value)
        return [item.strip() for item in items if item.strip()]

    def _check_regions(self, items: list[str]) -> list[str]:
        """Check if provided items exist in the region map."""
        matched: list[str] = []
        for item in items:
            if item in self._region_map:
                matched.extend(self._region_map[item].split("|"))
        return matched

    @staticmethod
    def _check_disc(text: str) -> list[str]:
        """Extract disc information from the text."""
        matched = NAMING_DISC_PATTERN.findall(text)
        return [f"{term[0]} {term[1]}".upper() for term in matched]

    @staticmethod
    def _check_format(text: str) -> list[str]:
        """Extract format information from the text."""
        matched = NAMING_FORMAT_PATTERN.findall(text)
        return [term.upper() for term in matched]

    @staticmethod
    def _clean_name(text: str) -> str:
        """Clean and normalizes the ROM name."""
        clean = util.remove_loop(text, NAMING_REMOVE_PATTERN)
        return " ".join(clean.split())

    def parse(self, path: Path, crc: str | None = None) -> RomDetail:
        """Parse the filename to extract ROM details."""
        stem = self._replace_strings(path.stem)
        region: set[str] = set()
        disc: set[str] = set()
        vf: set[str] = set()
        for content in NAMING_SEARCH_PATTERN.findall(stem):
            items = self._split_and_normalise(content)
            region.update(self._check_regions(items))
            disc.update(self._check_disc(content))
            vf.update(self._check_format(content))

        return RomDetail(
            title=path.stem,
            name=self._clean_name(path.stem),
            source="file_name",
            id_method="" if path.parts[0] in NAMING_EXCLUDE_SYSTEMS else "crc",
            id=crc or "",
            region=list(region),
            disc=list(disc),
            format=list(vf),
        )
