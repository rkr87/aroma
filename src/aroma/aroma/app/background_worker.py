"""TODO."""

import threading
from collections.abc import Callable
from typing import Any

from classes.base.class_singleton import ClassSingleton


class BackgroundWorker(ClassSingleton):
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self.busy = False
        self.message = ""

    def do_work(self, function: Callable[..., Any], message: str) -> None:
        """TODO."""

        def worker() -> None:
            self.busy = True
            self.message = message
            self._logger.info("Started work: %s", message)
            try:
                function()
            finally:
                self.busy = False
                self.message = ""
                self._logger.info("Finished work: %s", message)

        thread = threading.Thread(target=worker)
        thread.start()
