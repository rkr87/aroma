"""
Base module for abstract class definitions.
"""
from abc import ABC
from logging import Logger, getLogger


class ClassBase(ABC):
    """
    Abstract base class with a logger instance.
    """

    def __init__(self) -> None:
        """
        Initializes the logger for the class.
        """
        super().__init__()
        self._logger: Logger = getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

    @classmethod
    def get_static_logger(cls) -> Logger:
        """
        Returns a logger for static methods, based on the class name.
        """
        return getLogger(f"{cls.__module__}.{cls.__name__}")
