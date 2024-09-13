"""
Module for defining Singleton pattern using metaclasses.
"""
from abc import ABCMeta
from typing import Any, Generic, Self, TypeVar

from base.class_base import ClassBase

_T = TypeVar("_T")


class _SingletonMeta(ABCMeta, Generic[_T]):
    """
    Metaclass for implementing the Singleton pattern.
    """
    _instances: dict["_SingletonMeta[_T]", _T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> _T:
        """
        Creates a singleton instance if it does not exist, or returns the
        existing instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def add_instance(cls, instance: Any) -> _T:
        """
        Add a new instance to the singleton registry.
        """
        if cls not in cls._instances and isinstance(instance, cls):
            cls._instances[cls] = instance
        return cls._instances[cls]

    def instance_exists(cls) -> bool:
        """
        Check if a singleton instance exists.
        """
        return cls in cls._instances

    def get_instance(cls) -> _T:
        """
        Get the existing singleton instance.
        """
        return cls._instances[cls]


class ClassSingleton(ClassBase, metaclass=_SingletonMeta):   # pyright: ignore[reportMissingTypeArgument]
    """
    A singleton class that inherits from ClassBase and uses SingletonMeta
    as its metaclass.
    """
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # pylint: disable=W0613
        """
        Create a new instance of the singleton class if it doesn't exist,
        or return the existing instance.
        """
        if cls.instance_exists():
            return cls.get_instance()  # type: ignore[return-value]
        return cls.add_instance(super().__new__(cls))  # type: ignore[return-value]
