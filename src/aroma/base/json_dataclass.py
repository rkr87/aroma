"""
This module provides a JSON data class that loads data from a file and supports
singleton instantiation. The data can contain either strings or lists of
strings, with lists being converted to newline-separated strings.
"""
import json
import logging
from abc import ABC
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Self

from base.class_singleton import ClassSingleton


@dataclass
class JsonDataClass(ClassSingleton, ABC):
    """
    A abstract singleton class for loading and storing JSON data. Data values
    can be either strings or lists of strings, with lists being converted to
    newline-separated strings.
    """

    _file_path: Path = Path()

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__module__}")

    @classmethod
    def load(cls, file_path: Path) -> Self:
        """
        Loads data from a JSON file into an instance of JsonDataClass. The data
        is expected to be a dictionary where values can be either strings or
        lists of strings. Lists are converted to newline-separated strings.
        """
        logger = cls.get_static_logger()
        logger.info("Loading JSON data from file: %s", file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data: dict[str, str | list[str]] = json.load(f)
        except FileNotFoundError as e:
            logger.error("File not found: %s", file_path)
            raise e
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON from file: %s", file_path)
            raise e

        new_dict: dict[str, str | Path] = {
            k: '\n'.join(v) if isinstance(v, list) else v
            for k, v in data.items()
        }

        new_dict["_file_path"] = file_path

        logger.info(
            "Successfully loaded and processed data from file: %s", file_path
        )
        return cls.reset_instance(**new_dict)

    def save(self) -> None:
        """
        Saves the current instance data to the JSON file specified by
        _file_path. The data is converted to a dictionary with
        newline-separated strings for lists.
        """
        data_dict = asdict(self)
        file_path = data_dict.pop("_file_path")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    def update_value(self, attribute: str, value: str) -> None:
        """
        Updates a specific attribute of the instance and saves the updated data
        to the JSON file.
        """
        JsonDataClass.get_static_logger().info(
            "Updating %s.%s=%s", self.__class__.__name__, attribute, value
        )
        setattr(self, attribute, value)
        self.save()

    def get_value(self, attribute: str) -> str:
        """
        Retrieves the value of a specific attribute from the instance.
        """
        return str(getattr(self, attribute))
