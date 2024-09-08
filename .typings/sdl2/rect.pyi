from ctypes import Structure

class SDL_Point(Structure):
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0) -> None: ...

class SDL_FPoint(Structure):
    x: float
    y: float
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None: ...

class SDL_Rect(Structure):
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0) -> None: ...

class SDL_FRect(Structure):
    x: float
    y: float
    w: float
    h: float
    def __init__(self, x: float = 0.0, y: float = 0.0, w: float = 0.0, h: float = 0.0) -> None: ...
