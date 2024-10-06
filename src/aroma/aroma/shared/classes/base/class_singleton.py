"""Module for defining Singleton pattern using metaclasses."""

from abc import ABCMeta
from collections import OrderedDict
from typing import Any, Generic, Self, TypeVar

from shared.classes.base.class_base import ClassBase

_T = TypeVar("_T")


class _SingletonMeta(ABCMeta, Generic[_T]):
    """Metaclass for implementing the Singleton pattern."""

    _instances: OrderedDict["_SingletonMeta[_T]", _T] = OrderedDict()  # noqa: RUF012
    _disable_singleton: dict["_SingletonMeta[_T]", bool] = {}  # noqa: RUF012

    def __call__(cls, *args: Any, **kwargs: Any) -> _T:  # noqa: ANN401
        """Return singleton instance if it exists, otherwise create it."""
        if cls._disable_singleton.get(cls, False):
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            instance = cls._instances[cls]
        return cls._instances[cls]

    def add_instance(cls, instance: Any) -> _T:  # noqa: ANN401
        """Add a new instance to the singleton registry."""
        if cls not in cls._instances and isinstance(instance, cls):
            cls._instances[cls] = instance
        return cls._instances[cls]

    def instance_exists(cls) -> bool:
        """Check if a singleton instance exists."""
        return cls in cls._instances

    def get_instance(cls) -> _T:
        """Get the existing singleton instance."""
        return cls._instances[cls]

    def replace_instance(cls, instance: Any) -> _T:  # noqa: ANN401
        """Replace the current singleton instance with a new instance."""
        if isinstance(instance, cls):
            cls._instances[cls] = instance
        return cls._instances[cls]

    def disable_singleton(cls) -> None:
        """Disable singleton behavior for instance creation."""
        cls._disable_singleton[cls] = True

    def enable_singleton(cls) -> None:
        """Re-enable singleton behavior."""
        cls._disable_singleton[cls] = False

    def get_instances(cls) -> dict["_SingletonMeta[_T]", _T]:
        """Get all instances registered with this metaclass."""
        return cls._instances


_CT = TypeVar("_CT", bound="ClassSingleton")


class ClassSingleton(ClassBase, metaclass=_SingletonMeta):  # pyright: ignore[reportMissingTypeArgument]
    """A singleton class."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # pylint: disable=unused-argument  # noqa: ANN401, ARG003
        """Return singleton instance if it exists, otherwise create it."""
        if cls.instance_exists():
            return cls.get_instance()  # type: ignore[return-value]
        return cls.add_instance(super().__new__(cls))  # type: ignore[return-value]

    @classmethod  # type: ignore[misc]
    def _force_new_instance(cls, *args: Any, **kwargs: Any) -> Self:  # pylint: disable=unused-argument  # noqa: ANN401
        """Force the creation of a new instance, bypassing singleton logic."""
        cls.disable_singleton()
        try:
            return cls(*args, **kwargs)
        finally:
            cls.enable_singleton()

    @classmethod  # type: ignore[misc]
    def reset_instance(cls, *args: Any, **kwargs: Any) -> Self:  # noqa: ANN401
        """Replace the current singleton instance with a new one."""
        new_instance = cls._force_new_instance(*args, **kwargs)
        return cls.replace_instance(new_instance)  # type: ignore[return-value]

    @classmethod
    def _get_all_instances_of_type(cls, cls_type: type[_T]) -> list[_T]:
        """Get all instances of a specified type."""
        return [
            i
            for i in cls.get_instances().values()  # pyright: ignore[reportUnknownVariableType]
            if isinstance(i, cls_type)
        ]

    @classmethod
    def get_children(cls: type[_CT]) -> list[_CT]:
        """Get all children of self."""
        return cls._get_all_instances_of_type(cls)
