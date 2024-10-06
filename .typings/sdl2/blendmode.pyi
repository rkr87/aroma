from ctypes import c_int

__all__ = [
    "SDL_BlendMode",
    "SDL_BLENDMODE_NONE",
    "SDL_BLENDMODE_BLEND",
    "SDL_BLENDMODE_ADD",
    "SDL_BLENDMODE_MOD",
    "SDL_BLENDMODE_MUL",
    "SDL_BLENDMODE_INVALID",
    "SDL_BlendOperation",
    "SDL_BLENDOPERATION_ADD",
    "SDL_BLENDOPERATION_SUBTRACT",
    "SDL_BLENDOPERATION_REV_SUBTRACT",
    "SDL_BLENDOPERATION_MINIMUM",
    "SDL_BLENDOPERATION_MAXIMUM",
    "SDL_BlendFactor",
    "SDL_BLENDFACTOR_ZERO",
    "SDL_BLENDFACTOR_ONE",
    "SDL_BLENDFACTOR_SRC_COLOR",
    "SDL_BLENDFACTOR_ONE_MINUS_SRC_COLOR",
    "SDL_BLENDFACTOR_SRC_ALPHA",
    "SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA",
    "SDL_BLENDFACTOR_DST_COLOR",
    "SDL_BLENDFACTOR_ONE_MINUS_DST_COLOR",
    "SDL_BLENDFACTOR_DST_ALPHA",
    "SDL_BLENDFACTOR_ONE_MINUS_DST_ALPHA",
]

SDL_BlendMode = c_int
SDL_BLENDMODE_NONE: int
SDL_BLENDMODE_BLEND: int
SDL_BLENDMODE_ADD: int
SDL_BLENDMODE_MOD: int
SDL_BLENDMODE_MUL: int
SDL_BLENDMODE_INVALID: int
SDL_BlendOperation = c_int
SDL_BLENDOPERATION_ADD: int
SDL_BLENDOPERATION_SUBTRACT: int
SDL_BLENDOPERATION_REV_SUBTRACT: int
SDL_BLENDOPERATION_MINIMUM: int
SDL_BLENDOPERATION_MAXIMUM: int
SDL_BlendFactor = c_int
SDL_BLENDFACTOR_ZERO: int
SDL_BLENDFACTOR_ONE: int
SDL_BLENDFACTOR_SRC_COLOR: int
SDL_BLENDFACTOR_ONE_MINUS_SRC_COLOR: int
SDL_BLENDFACTOR_SRC_ALPHA: int
SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA: int
SDL_BLENDFACTOR_DST_COLOR: int
SDL_BLENDFACTOR_ONE_MINUS_DST_COLOR: int
SDL_BLENDFACTOR_DST_ALPHA: int
SDL_BLENDFACTOR_ONE_MINUS_DST_ALPHA: int