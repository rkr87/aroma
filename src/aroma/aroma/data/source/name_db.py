"""Handles ROM name queries from databases."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import apsw
from data.model.rom_detail import RomDetail
from shared.classes.class_singleton import ClassSingleton
from shared.constants import (
    ARCADE_ID_METHOD,
    ARCADE_NAMES_DB,
    CONSOLE_ID_METHOD,
    CONSOLE_NAMES_DB,
    NAMES_APP_RESOURCE,
)
from shared.tools import util

DB_ID_METHOD = {
    ARCADE_NAMES_DB: ARCADE_ID_METHOD,
    CONSOLE_NAMES_DB: CONSOLE_ID_METHOD,
}

ROM_QUERY = """
        SELECT id, title, name, source, val, hack, version, year
        FROM rom
        WHERE val IN (%s)
    """
SUBTABLE_QUERY = """
        SELECT rom_id, name
        FROM %s
        WHERE rom_id IN (%s)
    """


@dataclass
class _DBResult:
    """Represents a result row from the database."""

    @classmethod
    def factory(
        cls,
        row: tuple["apsw.SQLiteValue", ...],
    ) -> Self:
        """Create a DBResult instance from a database row."""
        return cls(*row)


class NameDB(ClassSingleton):
    """A singleton class to handle ROM name queries from databases."""

    @dataclass
    class _RomResult(_DBResult):  # pylint: disable=too-many-instance-attributes
        """Represents a result from the ROM table in the database."""

        row_id: int
        title: str
        name: str
        source: str
        rom_id: str
        hack: str | None
        version: str | None
        year: str | None

    @dataclass
    class _SubtableResult(_DBResult):
        """Represents a result from subtables."""

        row_id: int
        name: str

    @dataclass
    class _QueryResult:  # pylint: disable=too-many-instance-attributes
        """Holds the results of a query."""

        query: dict[str, list[str]] = field(default_factory=dict)
        roms: list["NameDB._RomResult"] = field(default_factory=list)
        region: dict[int, list[str]] = field(default_factory=dict)
        disc: dict[int, list[str]] = field(default_factory=dict)
        format: dict[int, list[str]] = field(default_factory=dict)
        additional: dict[int, list[str]] = field(default_factory=dict)
        black_list: set[str] = field(default_factory=set)
        processed: dict[str, RomDetail] = field(default_factory=dict)

        @property
        def terms(self) -> set[str]:
            """Extract unique search terms from the query dictionary."""
            return {val for vals in self.query.values() for val in vals}

        @property
        def row_ids(self) -> list[int]:
            """Extract ROM IDs from the fetched ROM details."""
            return [rom.row_id for rom in self.roms]

        @property
        def rom_vals(self) -> list[str]:
            """Extract ROM values from the fetched ROM details."""
            return [rom.rom_id for rom in self.roms]

    @staticmethod
    def _get_db(db: Path) -> None:
        """Ensure the database file exists by extracting it from a resource."""
        if db.is_file():
            NameDB.get_static_logger().debug("Database file exists: %s", db)
            return
        NameDB.get_static_logger().info(
            "Extracting database file: %s", db.name
        )
        util.extract_from_zip(NAMES_APP_RESOURCE, db.name, db)

    @staticmethod
    def remove_db() -> None:
        """Remove the database files for arcade and console ROMs."""
        for db in (ARCADE_NAMES_DB, CONSOLE_NAMES_DB):
            if db.is_file():
                NameDB.get_static_logger().info(
                    "Removing database file: %s", db
                )
                db.unlink()

    @staticmethod
    def _query_subtables(
        cursor: apsw.Cursor,
        result: _QueryResult,
    ) -> None:
        """Query a subtable for the provided ROM IDs and update the results."""
        table_map = {
            "region": result.region,
            "disc": result.disc,
            "format": result.format,
            "additional": result.additional,
        }
        for table, target in table_map.items():
            placeholders = ", ".join("?" for _ in result.row_ids)
            query = SUBTABLE_QUERY % (table, placeholders)
            NameDB.get_static_logger().debug(
                "Executing query on %s for row IDs: %s", table, result.row_ids
            )
            cursor.execute(query, result.row_ids)
            if not (results := cursor.fetchall()):
                NameDB.get_static_logger().debug(
                    "No results found for table %s with row IDs: %s",
                    table,
                    result.row_ids,
                )
                continue
            for row in [NameDB._SubtableResult.factory(r) for r in results]:
                target.setdefault(row.row_id, []).append(row.name)
                NameDB.get_static_logger().debug(
                    "Added %s to %s for row ID %d", row.name, table, row.row_id
                )

    @staticmethod
    def _fetch_rom_details(
        cursor: apsw.Cursor,
        query_vals: set[str],
    ) -> list["NameDB._RomResult"]:
        """Fetch ROM details from database for provided query values."""
        query = ROM_QUERY % ", ".join("?" for _ in query_vals)
        NameDB.get_static_logger().debug(
            "Executing fetch ROM details query for values: %s", query_vals
        )
        cursor.execute(query, list(query_vals))
        results = [NameDB._RomResult.factory(r) for r in cursor.fetchall()]
        NameDB.get_static_logger().debug(
            "Fetched %d ROM details.", len(results)
        )
        return results

    @staticmethod
    def _check_result(result: _QueryResult, rom_id: str, path: str) -> bool:
        """Check if a rom result is valid for processing."""
        if rom_id not in result.rom_vals:
            NameDB.get_static_logger().debug(
                "ROM ID %s not in result values.", rom_id
            )
            return False
        if path in result.black_list:
            NameDB.get_static_logger().debug(
                "Path %s is in the blacklist.", path
            )
            return False
        if path in result.processed:
            NameDB.get_static_logger().debug(
                "Path %s has already been processed.", path
            )
            result.black_list.add(path)
            result.processed.pop(path)
            return False
        return True

    @classmethod
    def _process_result(
        cls,
        result: _QueryResult,
        rom_id: str,
        path: str,
        id_method: str,
    ) -> None:
        """Process the result for a given ROM ID and path."""
        if not cls._check_result(result, rom_id, path):
            NameDB.get_static_logger().debug(
                "Skipping processing for ROM ID %s and path %s.", rom_id, path
            )
            return
        rom = result.roms[result.rom_vals.index(rom_id)]
        result.processed[path] = RomDetail(
            title=rom.title,
            parent=Path(path).parts[0],
            item_path=path,
            name=rom.name,
            source=rom.source,
            id="" if id_method == ARCADE_ID_METHOD else rom.rom_id,
            id_method=id_method,
            year=rom.year,
            version=rom.version,
            hack=rom.hack,
            region=result.region.get(rom.row_id, []),
            disc=result.disc.get(rom.row_id, []),
            format=result.format.get(rom.row_id, []),
            additional=result.additional.get(rom.row_id, []),
        )
        NameDB.get_static_logger().debug(
            "Processed result for path %s: %s", path, result.processed[path]
        )

    @classmethod
    def query(
        cls,
        db: Path,
        query_vals: dict[str, list[str]],
    ) -> dict[str, RomDetail]:
        """Query ROM details from database based on provided query values."""
        if not query_vals:
            NameDB.get_static_logger().info(
                "No query values provided, returning empty dictionary."
            )
            return {}
        NameDB._get_db(db)
        result = cls._QueryResult(query_vals)
        with apsw.Connection(str(db)) as conn:
            cursor = conn.cursor()
            result.roms = NameDB._fetch_rom_details(cursor, result.terms)
            NameDB._query_subtables(cursor, result)
            for path, ids in result.query.items():
                for rom_id in ids:
                    cls._process_result(result, rom_id, path, DB_ID_METHOD[db])
        NameDB.get_static_logger().debug(
            "Query completed with processed results: %s",
            result.processed.keys(),
        )
        return result.processed
