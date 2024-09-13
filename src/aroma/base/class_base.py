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
        self._logger: Logger = getLogger(self.__class__.__module__)
        super().__init__()
