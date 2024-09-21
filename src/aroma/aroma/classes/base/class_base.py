"""Base module for abstract class definitions."""

from logging import Logger, getLogger


class ClassBase:
    """Abstract base class with a logger instance."""

    def __init__(self) -> None:
        super().__init__()
        self._logger: Logger = getLogger(self.__class__.__module__)

    @classmethod
    def get_static_logger(cls) -> Logger:
        """Return a logger for static methods, based on the class name."""
        return getLogger(cls.__module__)
