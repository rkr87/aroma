"""Provides a JSON data singleton that loads data from a file."""

import json
import logging
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Self

from shared.classes.class_singleton import ClassSingleton
from shared.tools import util


@dataclass
class JsonDataClass(ClassSingleton):
    """A singleton class for loading and storing JSON data."""

    _file_path: Path = Path()

    def __post_init__(self) -> None:
        """Initiate logged after data class initialisation."""
        self._logger = logging.getLogger(f"{self.__class__.__module__}")

    @classmethod
    def load(cls, file_path: Path, default: Path | None = None) -> Self:
        """Load data from a JSON file into an instance of JsonDataClass."""
        logger = cls.get_static_logger()
        logger.info("Loading JSON data from file: %s", file_path)

        data = util.load_simple_json(default) if default else {}
        data.update(util.load_simple_json(file_path))
        data["_file_path"] = file_path

        logger.info(
            "Successfully loaded and processed data from file: %s",
            file_path,
        )
        class_fields = [field.name for field in fields(cls)]
        data = {k: v for k, v in data.items() if k in class_fields}
        return cls.reset_instance(**data)

    def save(self) -> None:
        """Save the current instance data to file."""
        data_dict = asdict(self)
        file_path = data_dict.pop("_file_path")
        with Path(file_path).open("w", encoding="utf-8") as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    def update_value(self, attribute: str, value: str | int | bool) -> None:
        """Update provided attribute and save data to file."""
        self._check_attr(attribute)
        current_value = getattr(self, attribute)
        if not isinstance(value, type(current_value)):
            JsonDataClass.get_static_logger().exception(
                "Type mismatch: %s.%s expected %s but got %s",
                self.__class__.__name__,
                attribute,
                type(current_value).__name__,
                type(value).__name__,
            )
            return
        JsonDataClass.get_static_logger().info(
            "Updating %s.%s=%s",
            self.__class__.__name__,
            attribute,
            value,
        )
        setattr(self, attribute, value)
        self.save()

    def get_value(self, attribute: str) -> str | int | bool:
        """Retrieve the value of provided attribute from the instance."""
        self._check_attr(attribute)
        value = getattr(self, attribute)
        if not isinstance(value, (str | int | bool)):
            JsonDataClass.get_static_logger().warning(
                "Invalid type: %s.%s is of invalid type %s",
                self.__class__.__name__,
                attribute,
                type(value).__name__,
            )
            raise TypeError
        return value

    def _check_attr(self, attribute: str) -> None:
        """Check provided attribute exists."""
        if not hasattr(self, attribute):
            JsonDataClass.get_static_logger().exception(
                "Attempted to access non-existent attribute %s.%s",
                self.__class__.__name__,
                attribute,
            )
            raise AttributeError
