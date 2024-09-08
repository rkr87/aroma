from ctypes import Structure, c_int, c_void_p

from _typeshed import Incomplete

from .stdinc import Sint32

__all__ = ['SDL_Joystick', 'SDL_JoystickGUID', 'SDL_VirtualJoystickDesc', 'SDL_JoystickID', 'SDL_HAT_CENTERED', 'SDL_HAT_UP', 'SDL_HAT_RIGHT', 'SDL_HAT_DOWN', 'SDL_HAT_LEFT', 'SDL_HAT_RIGHTUP', 'SDL_HAT_RIGHTDOWN', 'SDL_HAT_LEFTUP', 'SDL_HAT_LEFTDOWN', 'SDL_IPHONE_MAX_GFORCE', 'SDL_VIRTUAL_JOYSTICK_DESC_VERSION', 'SDL_JoystickType', 'SDL_JOYSTICK_TYPE_UNKNOWN', 'SDL_JOYSTICK_TYPE_GAMECONTROLLER', 'SDL_JOYSTICK_TYPE_WHEEL', 'SDL_JOYSTICK_TYPE_ARCADE_STICK', 'SDL_JOYSTICK_TYPE_FLIGHT_STICK', 'SDL_JOYSTICK_TYPE_DANCE_PAD', 'SDL_JOYSTICK_TYPE_GUITAR', 'SDL_JOYSTICK_TYPE_DRUM_KIT', 'SDL_JOYSTICK_TYPE_ARCADE_PAD', 'SDL_JOYSTICK_TYPE_THROTTLE', 'SDL_JoystickPowerLevel', 'SDL_JOYSTICK_POWER_UNKNOWN', 'SDL_JOYSTICK_POWER_EMPTY', 'SDL_JOYSTICK_POWER_LOW', 'SDL_JOYSTICK_POWER_MEDIUM', 'SDL_JOYSTICK_POWER_FULL', 'SDL_JOYSTICK_POWER_WIRED', 'SDL_JOYSTICK_POWER_MAX', 'SDL_LockJoysticks', 'SDL_UnlockJoysticks', 'SDL_NumJoysticks', 'SDL_JoystickNameForIndex', 'SDL_JoystickPathForIndex', 'SDL_JoystickGetDevicePlayerIndex', 'SDL_JoystickGetDeviceGUID', 'SDL_JoystickGetDeviceVendor', 'SDL_JoystickGetDeviceProduct', 'SDL_JoystickGetDeviceProductVersion', 'SDL_JoystickGetDeviceType', 'SDL_JoystickGetDeviceInstanceID', 'SDL_JoystickOpen', 'SDL_JoystickFromInstanceID', 'SDL_JoystickFromPlayerIndex', 'SDL_JoystickAttachVirtual', 'SDL_JoystickAttachVirtualEx', 'SDL_JoystickDetachVirtual', 'SDL_JoystickIsVirtual', 'SDL_JoystickSetVirtualAxis', 'SDL_JoystickSetVirtualButton', 'SDL_JoystickSetVirtualHat', 'SDL_JoystickName', 'SDL_JoystickPath', 'SDL_JoystickGetPlayerIndex', 'SDL_JoystickSetPlayerIndex', 'SDL_JoystickGetGUID', 'SDL_JoystickGetVendor', 'SDL_JoystickGetProduct', 'SDL_JoystickGetProductVersion', 'SDL_JoystickGetFirmwareVersion', 'SDL_JoystickGetSerial', 'SDL_JoystickGetType', 'SDL_JoystickGetGUIDString', 'SDL_JoystickGetGUIDFromString', 'SDL_GetJoystickGUIDInfo', 'SDL_JoystickGetAttached', 'SDL_JoystickInstanceID', 'SDL_JoystickNumAxes', 'SDL_JoystickNumBalls', 'SDL_JoystickNumHats', 'SDL_JoystickNumButtons', 'SDL_JoystickUpdate', 'SDL_JoystickEventState', 'SDL_JoystickGetAxis', 'SDL_JoystickGetAxisInitialState', 'SDL_JoystickGetHat', 'SDL_JoystickGetBall', 'SDL_JoystickGetButton', 'SDL_JoystickRumble', 'SDL_JoystickRumbleTriggers', 'SDL_JoystickHasLED', 'SDL_JoystickHasRumble', 'SDL_JoystickHasRumbleTriggers', 'SDL_JoystickSetLED', 'SDL_JoystickSendEffect', 'SDL_JoystickClose', 'SDL_JoystickCurrentPowerLevel']

SDL_JoystickPowerLevel = c_int
SDL_JOYSTICK_POWER_UNKNOWN: int
SDL_JOYSTICK_POWER_EMPTY: int
SDL_JOYSTICK_POWER_LOW: int
SDL_JOYSTICK_POWER_MEDIUM: int
SDL_JOYSTICK_POWER_FULL: int
SDL_JOYSTICK_POWER_WIRED: int
SDL_JOYSTICK_POWER_MAX: int
SDL_JoystickType = c_int
SDL_JOYSTICK_TYPE_UNKNOWN: int
SDL_JOYSTICK_TYPE_GAMECONTROLLER: int
SDL_JOYSTICK_TYPE_WHEEL: int
SDL_JOYSTICK_TYPE_ARCADE_STICK: int
SDL_JOYSTICK_TYPE_FLIGHT_STICK: int
SDL_JOYSTICK_TYPE_DANCE_PAD: int
SDL_JOYSTICK_TYPE_GUITAR: int
SDL_JOYSTICK_TYPE_DRUM_KIT: int
SDL_JOYSTICK_TYPE_ARCADE_PAD: int
SDL_JOYSTICK_TYPE_THROTTLE: int
SDL_IPHONE_MAX_GFORCE: float
SDL_HAT_CENTERED: int
SDL_HAT_UP: int
SDL_HAT_RIGHT: int
SDL_HAT_DOWN: int
SDL_HAT_LEFT: int
SDL_HAT_RIGHTUP: int
SDL_HAT_RIGHTDOWN: int
SDL_HAT_LEFTUP: int
SDL_HAT_LEFTDOWN: int
SDL_VIRTUAL_JOYSTICK_DESC_VERSION: int
SDL_JoystickID = Sint32

class SDL_JoystickGUID(Structure): ...
class SDL_Joystick(c_void_p): ...
class SDL_VirtualJoystickDesc(Structure): ...

SDL_NumJoysticks: Incomplete
SDL_JoystickNameForIndex: Incomplete
SDL_JoystickPathForIndex: Incomplete
SDL_JoystickOpen: Incomplete
SDL_JoystickName: Incomplete
SDL_JoystickPath: Incomplete
SDL_JoystickGetDeviceGUID: Incomplete
SDL_JoystickGetGUID: Incomplete
SDL_JoystickGetGUIDFromString: Incomplete
SDL_JoystickGetAttached: Incomplete
SDL_JoystickInstanceID: Incomplete
SDL_JoystickNumAxes: Incomplete
SDL_JoystickNumBalls: Incomplete
SDL_JoystickNumHats: Incomplete
SDL_JoystickNumButtons: Incomplete
SDL_JoystickUpdate: Incomplete
SDL_JoystickEventState: Incomplete
SDL_JoystickGetAxis: Incomplete
SDL_JoystickGetHat: Incomplete
SDL_JoystickGetBall: Incomplete
SDL_JoystickGetButton: Incomplete
SDL_JoystickClose: Incomplete
SDL_JoystickCurrentPowerLevel: Incomplete
SDL_JoystickFromInstanceID: Incomplete
SDL_JoystickFromPlayerIndex: Incomplete
SDL_JoystickAttachVirtual: Incomplete
SDL_JoystickAttachVirtualEx: Incomplete
SDL_JoystickDetachVirtual: Incomplete
SDL_JoystickIsVirtual: Incomplete
SDL_JoystickSetVirtualAxis: Incomplete
SDL_JoystickSetVirtualButton: Incomplete
SDL_JoystickSetVirtualHat: Incomplete
SDL_JoystickGetVendor: Incomplete
SDL_JoystickGetProduct: Incomplete
SDL_JoystickGetProductVersion: Incomplete
SDL_JoystickGetFirmwareVersion: Incomplete
SDL_JoystickGetSerial: Incomplete
SDL_JoystickGetAxisInitialState: Incomplete
SDL_JoystickGetType: Incomplete
SDL_JoystickGetDeviceVendor: Incomplete
SDL_JoystickGetDeviceProduct: Incomplete
SDL_JoystickGetDeviceProductVersion: Incomplete
SDL_JoystickGetDeviceType: Incomplete
SDL_JoystickGetDeviceInstanceID: Incomplete
SDL_LockJoysticks: Incomplete
SDL_UnlockJoysticks: Incomplete
SDL_JoystickGetPlayerIndex: Incomplete
SDL_JoystickSetPlayerIndex: Incomplete
SDL_JoystickGetDevicePlayerIndex: Incomplete
SDL_JoystickRumble: Incomplete
SDL_JoystickRumbleTriggers: Incomplete
SDL_JoystickHasLED: Incomplete
SDL_JoystickHasRumble: Incomplete
SDL_JoystickHasRumbleTriggers: Incomplete
SDL_JoystickSetLED: Incomplete
SDL_JoystickSendEffect: Incomplete
SDL_JoystickGetGUIDString: Incomplete
SDL_GetJoystickGUIDInfo: Incomplete
