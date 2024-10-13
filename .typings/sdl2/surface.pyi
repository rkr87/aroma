from ctypes import Structure

from sdl2 import SDL_Rect

class SDL_Surface(Structure):
    w: int
    h: int

def SDL_CreateRGBSurface(
    some_int: int,
    height: int,
    width: int,
    another_int: int,
    rmask: int,
    gmask: int,
    bmask: int,
    amask: int,
) -> SDL_Surface: ...
def SDL_UpperBlit(
    surface: SDL_Surface,
    rect: SDL_Rect | None,
    surface2: SDL_Surface,
    rect2: SDL_Rect | None,
) -> int: ...
def SDL_CreateRGBSurfaceWithFormat(
    huh: int, width: int, height: int, another: int, fmt: int
) -> SDL_Surface: ...
def SDL_SetSurfaceBlendMode(surface: SDL_Surface, blend_mode: int) -> int: ...
def SDL_BlitScaled(
    surface: SDL_Surface,
    rect: SDL_Rect | None,
    surface2: SDL_Surface,
    rect2: SDL_Rect | None,
) -> int: ...

SDL_BlitSurface = SDL_UpperBlit

def SDL_FreeSurface(surface: SDL_Surface) -> None: ...
