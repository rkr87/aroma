from ctypes import Structure

class SDL_Surface(Structure):
    w: int
    h: int
