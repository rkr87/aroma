from _typeshed import Incomplete
from sdl2 import SDL_Surface

class Window:
    DEFAULTFLAGS: Incomplete
    DEFAULTPOS: Incomplete
    window: Incomplete
    def __init__(self, title: str, size: tuple[int,int], position: tuple[int,int] | None = None, flags: int | None = None) -> None: ...
    def __del__(self) -> None: ...
    @property
    def position(self) -> tuple[int,int]: ...
    @position.setter
    def position(self, value: tuple[int,int]) -> None: ...
    @property
    def title(self) -> str: ...
    @title.setter
    def title(self, value: str) -> None: ...
    @property
    def size(self)-> tuple[int,int]: ...
    @size.setter
    def size(self, value: tuple[int,int]) -> None: ...
    def create(self) -> None: ...
    def open(self) -> None: ...
    def close(self) -> None: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...
    def maximize(self) -> None: ...
    def minimize(self) -> None: ...
    def restore(self) -> None: ...
    def refresh(self) -> None: ...
    def get_surface(self)-> SDL_Surface: ...
