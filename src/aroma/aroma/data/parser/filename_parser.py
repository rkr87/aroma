"""Parses filenames to extract ROM details."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from data.model.rom_detail import RomDetail
from shared.classes.base.class_singleton import ClassSingleton
from shared.constants import (
    FILE_ID_METHOD,
    NAMING_DISC_PATTERN,
    NAMING_EXCLUDE_SYSTEMS,
    NAMING_FORMAT_PATTERN,
    NAMING_REGION_RESOURCE,
    NAMING_REMOVE_PATTERN,
    NAMING_SEARCH_PATTERN,
    NAMING_VERSION_PATTERN,
    NAMING_YEAR_PATTERN,
)
from shared.tools import util

REPLACE_STRINGS = {
    "New Zealand": "New|Zealand",
    "Hong Kong": "Hong|Kong",
    "United Kingdom": "United|Kingdom",
}

YEAR_RANGE = (1970, 2024)
UNKNOWN_YEAR_TEXT = "x"
IGNORE_ADDITIONAL = ["of"]


class FilenameParser(ClassSingleton):
    """Handles parsing of filenames to extract ROM details."""

    @dataclass()
    class _ParserResult:  # pylint: disable=too-many-instance-attributes
        """Stores the results of parsing a filename."""

        content: str = ""
        region: set[str] = field(default_factory=set)
        disc: set[str] = field(default_factory=set)
        vf: set[str] = field(default_factory=set)
        year: str | None = None
        version: str | None = None
        additional: set[str] = field(default_factory=set)

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

    @staticmethod
    def _strip_item_from_text(text: str, item: str) -> str:
        """Remove an item from the text."""
        return re.sub(re.escape(item), "", text, flags=re.IGNORECASE).strip()

    def _check_regions(self, result: "_ParserResult") -> None:
        """Check if provided items exist in the region map."""
        items = self._split_and_normalise(result.content)
        matched: list[str] = []
        for item in items:
            if item in self._region_map:
                matched.extend(self._region_map[item].split("|"))
                self._logger.debug("Matched region: %s", item)
                result.content = self._strip_item_from_text(
                    result.content, item
                )
        result.region.update(matched)

    @staticmethod
    def _check_disc(result: "_ParserResult") -> None:
        """Extract disc information from the text."""
        matched = NAMING_DISC_PATTERN.findall(result.content)
        result.disc.update([f"{m[0]} {m[1]}".upper() for m in matched])
        result.content = NAMING_DISC_PATTERN.sub("", result.content).strip()

    @staticmethod
    def _check_format(result: "_ParserResult") -> None:
        """Extract format information from the text."""
        matched = NAMING_FORMAT_PATTERN.findall(result.content)
        result.vf.update([term.upper() for term in matched])
        result.content = NAMING_FORMAT_PATTERN.sub("", result.content).strip()

    @staticmethod
    def _check_year(result: "_ParserResult") -> None:
        """Extract year information from the text."""
        matched: list[str] = NAMING_YEAR_PATTERN.findall(result.content)
        for m in matched:
            valid_year = m[-1].lower() == UNKNOWN_YEAR_TEXT or (
                m.isdigit() and YEAR_RANGE[0] < int(m) < YEAR_RANGE[1]
            )
            if not valid_year:
                continue
            result.year = m.upper()
            result.content = FilenameParser._strip_item_from_text(
                result.content, m
            )
            break

    @staticmethod
    def _check_version(result: "_ParserResult") -> None:
        """Extract version information from the text."""
        if match := NAMING_VERSION_PATTERN.search(result.content):
            result.version = match.group(0).lower()
            result.content = FilenameParser._strip_item_from_text(
                result.content, match.group(0)
            )

    @staticmethod
    def _get_additional(result: "_ParserResult") -> None:
        """Extract any additional information that remains."""
        if any(
            word.lower() in result.content.lower()
            for word in IGNORE_ADDITIONAL
        ):
            return
        temp_list: list[str] = []
        for item in re.split(r"[,\s]", result.content):
            clean: str = re.sub(r"(?<!\d)-\d{2}(?!\d)(?:-\d{2})?", "", item)
            clean = re.sub(r"-+", "", clean)
            clean = re.sub(r"\s+", " ", clean).strip()
            if len(clean) > 1:
                temp_list.append(clean)
        if temp_list:
            result.additional.add(" ".join(temp_list))

    @staticmethod
    def _clean_name(text: str) -> str:
        """Clean and normalise the ROM name."""
        clean = util.remove_loop(text, NAMING_REMOVE_PATTERN)
        return " ".join(clean.split())

    def _process_content(self, result: "_ParserResult") -> None:
        """Process content to extract ROM details."""
        self._check_regions(result)
        self._check_disc(result)
        self._check_format(result)
        if not result.year:
            self._check_year(result)
        if not result.version:
            self._check_version(result)
        self._get_additional(result)

    @staticmethod
    def _get_id_method(system: str, crc: list[str] | None) -> str:
        """Determine the ID method based on system and CRC."""
        if system in NAMING_EXCLUDE_SYSTEMS or not crc:
            return ""
        return FILE_ID_METHOD

    def parse(self, path: Path, crc: list[str] | None = None) -> RomDetail:
        """Parse the filename to extract ROM details."""
        stem = self._replace_strings(path.stem)
        self._logger.debug("Parsing filename: %s", stem)
        result = self._ParserResult()
        for content in NAMING_SEARCH_PATTERN.findall(stem):
            result.content = content
            self._process_content(result)
        self._logger.debug("Parsed ROM details: title=%s", path.stem)
        return RomDetail(
            title=path.stem,
            name=self._clean_name(path.stem),
            source="file_name",
            id_method=self._get_id_method(path.parts[0], crc),
            id=str(crc) if crc else "",
            region=list(result.region),
            disc=list(result.disc),
            format=list(result.vf),
            version=result.version,
            year=result.year,
            additional=list(result.additional),
        )
