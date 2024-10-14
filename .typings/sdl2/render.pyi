from ctypes import Structure, c_int, c_void_p

from _typeshed import Incomplete
from sdl2 import SDL_Rect, SDL_Surface

SDL_RendererFlags = c_int
SDL_RENDERER_SOFTWARE: int
SDL_RENDERER_ACCELERATED: int
SDL_RENDERER_PRESENTVSYNC: int
SDL_RENDERER_TARGETTEXTURE: int
SDL_ScaleMode = c_int
SDL_ScaleModeNearest: int
SDL_ScaleModeLinear: int
SDL_ScaleModeBest: int
SDL_TextureAccess = c_int
SDL_TEXTUREACCESS_STATIC: int
SDL_TEXTUREACCESS_STREAMING: int
SDL_TEXTUREACCESS_TARGET: int
SDL_TextureModulate = c_int
SDL_TEXTUREMODULATE_NONE: int
SDL_TEXTUREMODULATE_COLOR: int
SDL_TEXTUREMODULATE_ALPHA: int
SDL_RendererFlip = c_int
SDL_FLIP_NONE: int
SDL_FLIP_HORIZONTAL: int
SDL_FLIP_VERTICAL: int

class SDL_RendererInfo(Structure): ...
class SDL_Renderer(c_void_p): ...
class SDL_Texture(c_void_p): ...

SDL_GetNumRenderDrivers: Incomplete
SDL_GetRenderDriverInfo: Incomplete
SDL_CreateWindowAndRenderer: Incomplete
SDL_CreateRenderer: Incomplete
SDL_CreateSoftwareRenderer: Incomplete
SDL_GetRenderer: Incomplete
SDL_RenderGetWindow: Incomplete
SDL_GetRendererInfo: Incomplete
SDL_GetRendererOutputSize: Incomplete
SDL_CreateTexture: Incomplete

def SDL_CreateTextureFromSurface(
    renderer: SDL_Renderer, surface: SDL_Surface
) -> SDL_Texture | None: ...

SDL_QueryTexture: Incomplete
SDL_SetTextureColorMod: Incomplete
SDL_GetTextureColorMod: Incomplete
SDL_SetTextureAlphaMod: Incomplete
SDL_GetTextureAlphaMod: Incomplete
SDL_SetTextureBlendMode: Incomplete
SDL_GetTextureBlendMode: Incomplete
SDL_SetTextureScaleMode: Incomplete
SDL_GetTextureScaleMode: Incomplete
SDL_SetTextureUserData: Incomplete
SDL_GetTextureUserData: Incomplete
SDL_UpdateTexture: Incomplete
SDL_UpdateYUVTexture: Incomplete
SDL_UpdateNVTexture: Incomplete
SDL_LockTexture: Incomplete
SDL_LockTextureToSurface: Incomplete
SDL_UnlockTexture: Incomplete
SDL_RenderTargetSupported: Incomplete
SDL_SetRenderTarget: Incomplete
SDL_GetRenderTarget: Incomplete
SDL_RenderSetLogicalSize: Incomplete
SDL_RenderGetLogicalSize: Incomplete
SDL_RenderSetIntegerScale: Incomplete
SDL_RenderGetIntegerScale: Incomplete
SDL_RenderSetViewport: Incomplete
SDL_RenderGetViewport: Incomplete
SDL_RenderGetClipRect: Incomplete
SDL_RenderSetClipRect: Incomplete
SDL_RenderIsClipEnabled: Incomplete
SDL_RenderSetScale: Incomplete
SDL_RenderGetScale: Incomplete
SDL_RenderWindowToLogical: Incomplete
SDL_RenderLogicalToWindow: Incomplete
SDL_SetRenderDrawColor: Incomplete
SDL_GetRenderDrawColor: Incomplete

def SDL_SetRenderDrawBlendMode(
    renderer: SDL_Renderer, blendmode: int
) -> int: ...

SDL_GetRenderDrawBlendMode: Incomplete
SDL_RenderClear: Incomplete
SDL_RenderDrawPoint: Incomplete
SDL_RenderDrawPoints: Incomplete
SDL_RenderDrawLine: Incomplete
SDL_RenderDrawLines: Incomplete
SDL_RenderDrawRect: Incomplete
SDL_RenderDrawRects: Incomplete
SDL_RenderFillRect: Incomplete
SDL_RenderFillRects: Incomplete

def SDL_RenderCopy(
    renderer: SDL_Renderer,
    texture: SDL_Texture,
    r1: SDL_Rect | None = None,
    r2: SDL_Rect | None = None,
) -> int | None: ...

SDL_RenderCopyEx: Incomplete
SDL_RenderDrawPointF: Incomplete
SDL_RenderDrawPointsF: Incomplete
SDL_RenderDrawLineF: Incomplete
SDL_RenderDrawLinesF: Incomplete
SDL_RenderDrawRectF: Incomplete
SDL_RenderDrawRectsF: Incomplete
SDL_RenderFillRectF: Incomplete
SDL_RenderFillRectsF: Incomplete
SDL_RenderCopyF: Incomplete
SDL_RenderCopyExF: Incomplete
SDL_RenderGeometry: Incomplete
SDL_RenderGeometryRaw: Incomplete
SDL_RenderReadPixels: Incomplete
SDL_RenderPresent: Incomplete
SDL_DestroyTexture: Incomplete
SDL_DestroyRenderer: Incomplete
SDL_RenderFlush: Incomplete
SDL_GL_BindTexture: Incomplete
SDL_GL_UnbindTexture: Incomplete
SDL_RenderGetMetalLayer: Incomplete
SDL_RenderGetMetalCommandEncoder: Incomplete
SDL_RenderSetVSync: Incomplete
