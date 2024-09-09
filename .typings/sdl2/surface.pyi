from ctypes import Structure

from sdl2 import SDL_Rect

class SDL_Surface(Structure):
    w: int
    h: int

def SDL_CreateRGBSurface(some_int: int, height: int, width: int, another_int: int, rmask: int, gmask: int, bmask: int, amask:int) ->SDL_Surface: ...
def SDL_UpperBlit(surface: SDL_Surface, rect: SDL_Rect | None, surface2: SDL_Surface, rect2: SDL_Rect) -> int: ...
SDL_BlitSurface = SDL_UpperBlit