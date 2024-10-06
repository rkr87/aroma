"""TODO."""

from classes.base.class_singleton import ClassSingleton
from model.emu_config import EmuConfig


class EmuConfigHandler(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self._config_cache: dict[str, EmuConfig] = {}

    def get(self, system: str) -> EmuConfig:
        """TODO."""
        self._check_cache(system)
        return self._config_cache[system]

    def _check_cache(self, system: str) -> None:
        """TODO."""
        if system in self._config_cache:
            return
        self._config_cache[system] = EmuConfig.get_system(system)
