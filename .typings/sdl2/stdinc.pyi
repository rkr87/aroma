from ctypes import (c_int, c_int8, c_int16, c_int32, c_int64, c_uint8,
                    c_uint16, c_uint32, c_uint64)

from _typeshed import Incomplete

SDL_FLT_EPSILON: Incomplete
SDL_bool = c_int
SDL_FALSE: int
SDL_TRUE: int
Sint8 = c_int8
Uint8 = c_uint8
Sint16 = c_int16
Uint16 = c_uint16
Sint32 = c_int32
Uint32 = c_uint32
Sint64 = c_int64
Uint64 = c_uint64
SDL_min = min
SDL_max = max

SDL_malloc: Incomplete
SDL_calloc: Incomplete
SDL_realloc: Incomplete
SDL_free: Incomplete
SDL_getenv: Incomplete
SDL_setenv: Incomplete
SDL_abs: Incomplete
SDL_memset: Incomplete
SDL_memcpy: Incomplete
