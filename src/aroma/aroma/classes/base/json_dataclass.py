"""Provides a JSON data singleton that loads data from a file."""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Self

from classes.base.class_singleton import ClassSingleton


@dataclass
class JsonDataClass(ClassSingleton):
    """A singleton class for loading and storing JSON data."""

    _file_path: Path = Path()

    def __post_init__(self) -> None:
        """Initiate logged after data class initialisation."""
        self._logger = logging.getLogger(f"{self.__class__.__module__}")

    @classmethod
    def load(cls, file_path: Path) -> Self:
        """Load data from a JSON file into an instance of JsonDataClass."""
        logger = cls.get_static_logger()
        logger.info("Loading JSON data from file: %s", file_path)

        try:
            with Path.open(file_path, encoding="utf-8") as f:
                data: dict[str, str | list[str]] = json.load(f)
        except FileNotFoundError:
            logger.exception("File not found: %s", file_path)
            raise
        except json.JSONDecodeError:
            logger.exception("Error decoding JSON from file: %s", file_path)
            raise

        new_dict: dict[str, str | Path] = {
            k: "\n".join(v) if isinstance(v, list) else v
            for k, v in data.items()
        }

        new_dict["_file_path"] = file_path

        logger.info(
            "Successfully loaded and processed data from file: %s",
            file_path,
        )
        return cls.reset_instance(**new_dict)

    def save(self) -> None:
        """Save the current instance data to file."""
        data_dict = asdict(self)
        file_path = data_dict.pop("_file_path")
        with Path.open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    def update_value(self, attribute: str, value: str) -> None:
        """Update provided attribute and save data to file."""
        JsonDataClass.get_static_logger().info(
            "Updating %s.%s=%s",
            self.__class__.__name__,
            attribute,
            value,
        )
        setattr(self, attribute, value)
        self.save()

    def get_value(self, attribute: str) -> str:
        """Retrieve the value of provided attribute from the instance."""
        return str(getattr(self, attribute))
