from ctypes import Structure, Union, c_int, c_void_p

from _typeshed import Incomplete

__all__ = ['SDL_GameController', 'SDL_GameControllerButtonBind', 'SDL_GameControllerType', 'SDL_CONTROLLER_TYPE_UNKNOWN', 'SDL_CONTROLLER_TYPE_XBOX360', 'SDL_CONTROLLER_TYPE_XBOXONE', 'SDL_CONTROLLER_TYPE_PS3', 'SDL_CONTROLLER_TYPE_PS4', 'SDL_CONTROLLER_TYPE_NINTENDO_SWITCH_PRO', 'SDL_CONTROLLER_TYPE_VIRTUAL', 'SDL_CONTROLLER_TYPE_PS5', 'SDL_CONTROLLER_TYPE_AMAZON_LUNA', 'SDL_CONTROLLER_TYPE_GOOGLE_STADIA', 'SDL_GameControllerBindType', 'SDL_CONTROLLER_BINDTYPE_NONE', 'SDL_CONTROLLER_BINDTYPE_BUTTON', 'SDL_CONTROLLER_BINDTYPE_AXIS', 'SDL_CONTROLLER_BINDTYPE_HAT', 'SDL_GameControllerAxis', 'SDL_CONTROLLER_AXIS_INVALID', 'SDL_CONTROLLER_AXIS_LEFTX', 'SDL_CONTROLLER_AXIS_LEFTY', 'SDL_CONTROLLER_AXIS_RIGHTX', 'SDL_CONTROLLER_AXIS_RIGHTY', 'SDL_CONTROLLER_AXIS_TRIGGERLEFT', 'SDL_CONTROLLER_AXIS_TRIGGERRIGHT', 'SDL_CONTROLLER_AXIS_MAX', 'SDL_GameControllerButton', 'SDL_CONTROLLER_BUTTON_INVALID', 'SDL_CONTROLLER_BUTTON_A', 'SDL_CONTROLLER_BUTTON_B', 'SDL_CONTROLLER_BUTTON_X', 'SDL_CONTROLLER_BUTTON_Y', 'SDL_CONTROLLER_BUTTON_BACK', 'SDL_CONTROLLER_BUTTON_GUIDE', 'SDL_CONTROLLER_BUTTON_START', 'SDL_CONTROLLER_BUTTON_LEFTSTICK', 'SDL_CONTROLLER_BUTTON_RIGHTSTICK', 'SDL_CONTROLLER_BUTTON_LEFTSHOULDER', 'SDL_CONTROLLER_BUTTON_RIGHTSHOULDER', 'SDL_CONTROLLER_BUTTON_DPAD_UP', 'SDL_CONTROLLER_BUTTON_DPAD_DOWN', 'SDL_CONTROLLER_BUTTON_DPAD_LEFT', 'SDL_CONTROLLER_BUTTON_DPAD_RIGHT', 'SDL_CONTROLLER_BUTTON_MISC1', 'SDL_CONTROLLER_BUTTON_PADDLE1', 'SDL_CONTROLLER_BUTTON_PADDLE2', 'SDL_CONTROLLER_BUTTON_PADDLE3', 'SDL_CONTROLLER_BUTTON_PADDLE4', 'SDL_CONTROLLER_BUTTON_TOUCHPAD', 'SDL_CONTROLLER_BUTTON_MAX', 'SDL_GameControllerAddMappingsFromFile', 'SDL_GameControllerAddMappingsFromRW', 'SDL_GameControllerAddMapping', 'SDL_GameControllerNumMappings', 'SDL_GameControllerMappingForIndex', 'SDL_GameControllerMappingForGUID', 'SDL_GameControllerMapping', 'SDL_IsGameController', 'SDL_GameControllerNameForIndex', 'SDL_GameControllerPathForIndex', 'SDL_GameControllerTypeForIndex', 'SDL_GameControllerMappingForDeviceIndex', 'SDL_GameControllerOpen', 'SDL_GameControllerFromInstanceID', 'SDL_GameControllerFromPlayerIndex', 'SDL_GameControllerName', 'SDL_GameControllerPath', 'SDL_GameControllerGetType', 'SDL_GameControllerGetPlayerIndex', 'SDL_GameControllerSetPlayerIndex', 'SDL_GameControllerGetVendor', 'SDL_GameControllerGetProduct', 'SDL_GameControllerGetProductVersion', 'SDL_GameControllerGetFirmwareVersion', 'SDL_GameControllerGetSerial', 'SDL_GameControllerGetAttached', 'SDL_GameControllerGetJoystick', 'SDL_GameControllerEventState', 'SDL_GameControllerUpdate', 'SDL_GameControllerGetAxisFromString', 'SDL_GameControllerGetStringForAxis', 'SDL_GameControllerGetBindForAxis', 'SDL_GameControllerHasAxis', 'SDL_GameControllerGetAxis', 'SDL_GameControllerGetButtonFromString', 'SDL_GameControllerGetStringForButton', 'SDL_GameControllerGetBindForButton', 'SDL_GameControllerHasButton', 'SDL_GameControllerGetButton', 'SDL_GameControllerGetNumTouchpads', 'SDL_GameControllerGetNumTouchpadFingers', 'SDL_GameControllerGetTouchpadFinger', 'SDL_GameControllerHasSensor', 'SDL_GameControllerSetSensorEnabled', 'SDL_GameControllerIsSensorEnabled', 'SDL_GameControllerGetSensorDataRate', 'SDL_GameControllerGetSensorData', 'SDL_GameControllerGetSensorDataWithTimestamp', 'SDL_GameControllerRumble', 'SDL_GameControllerRumbleTriggers', 'SDL_GameControllerHasLED', 'SDL_GameControllerHasRumble', 'SDL_GameControllerHasRumbleTriggers', 'SDL_GameControllerSetLED', 'SDL_GameControllerSendEffect', 'SDL_GameControllerClose', 'SDL_GameControllerGetAppleSFSymbolsNameForButton', 'SDL_GameControllerGetAppleSFSymbolsNameForAxis']

SDL_GameControllerBindType = c_int
SDL_CONTROLLER_BINDTYPE_NONE: int
SDL_CONTROLLER_BINDTYPE_BUTTON: int
SDL_CONTROLLER_BINDTYPE_AXIS: int
SDL_CONTROLLER_BINDTYPE_HAT: int
SDL_GameControllerType = c_int
SDL_CONTROLLER_TYPE_UNKNOWN: int
SDL_CONTROLLER_TYPE_XBOX360: int
SDL_CONTROLLER_TYPE_XBOXONE: int
SDL_CONTROLLER_TYPE_PS3: int
SDL_CONTROLLER_TYPE_PS4: int
SDL_CONTROLLER_TYPE_NINTENDO_SWITCH_PRO: int
SDL_CONTROLLER_TYPE_VIRTUAL: int
SDL_CONTROLLER_TYPE_PS5: int
SDL_CONTROLLER_TYPE_AMAZON_LUNA: int
SDL_CONTROLLER_TYPE_GOOGLE_STADIA: int
SDL_GameControllerAxis = c_int
SDL_CONTROLLER_AXIS_INVALID: int
SDL_CONTROLLER_AXIS_LEFTX: int
SDL_CONTROLLER_AXIS_LEFTY: int
SDL_CONTROLLER_AXIS_RIGHTX: int
SDL_CONTROLLER_AXIS_RIGHTY: int
SDL_CONTROLLER_AXIS_TRIGGERLEFT: int
SDL_CONTROLLER_AXIS_TRIGGERRIGHT: int
SDL_CONTROLLER_AXIS_MAX: int
SDL_GameControllerButton = c_int
SDL_CONTROLLER_BUTTON_INVALID: int
SDL_CONTROLLER_BUTTON_A: int
SDL_CONTROLLER_BUTTON_B: int
SDL_CONTROLLER_BUTTON_X: int
SDL_CONTROLLER_BUTTON_Y: int
SDL_CONTROLLER_BUTTON_BACK: int
SDL_CONTROLLER_BUTTON_GUIDE: int
SDL_CONTROLLER_BUTTON_START: int
SDL_CONTROLLER_BUTTON_LEFTSTICK: int
SDL_CONTROLLER_BUTTON_RIGHTSTICK: int
SDL_CONTROLLER_BUTTON_LEFTSHOULDER: int
SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: int
SDL_CONTROLLER_BUTTON_DPAD_UP: int
SDL_CONTROLLER_BUTTON_DPAD_DOWN: int
SDL_CONTROLLER_BUTTON_DPAD_LEFT: int
SDL_CONTROLLER_BUTTON_DPAD_RIGHT: int
SDL_CONTROLLER_BUTTON_MISC1: int
SDL_CONTROLLER_BUTTON_PADDLE1: int
SDL_CONTROLLER_BUTTON_PADDLE2: int
SDL_CONTROLLER_BUTTON_PADDLE3: int
SDL_CONTROLLER_BUTTON_PADDLE4: int
SDL_CONTROLLER_BUTTON_TOUCHPAD: int
SDL_CONTROLLER_BUTTON_MAX: int

class _gchat(Structure): ...
class _gcvalue(Union): ...
class SDL_GameControllerButtonBind(Structure): ...
class SDL_GameController(c_void_p): ...

SDL_GameControllerAddMapping: Incomplete
SDL_GameControllerMapping: Incomplete
SDL_IsGameController: Incomplete
SDL_GameControllerNameForIndex: Incomplete
SDL_GameControllerPathForIndex: Incomplete
SDL_GameControllerTypeForIndex: Incomplete
def SDL_GameControllerOpen(index: int) -> SDL_GameController: ...
SDL_GameControllerName: Incomplete
SDL_GameControllerPath: Incomplete
SDL_GameControllerGetType: Incomplete
SDL_GameControllerGetAttached: Incomplete
SDL_GameControllerGetJoystick: Incomplete
SDL_GameControllerEventState: Incomplete
SDL_GameControllerUpdate: Incomplete
SDL_GameControllerGetAxisFromString: Incomplete
SDL_GameControllerGetStringForAxis: Incomplete
SDL_GameControllerGetBindForAxis: Incomplete
SDL_GameControllerHasAxis: Incomplete
SDL_GameControllerGetAxis: Incomplete
SDL_GameControllerGetButtonFromString: Incomplete
SDL_GameControllerGetStringForButton: Incomplete
SDL_GameControllerGetBindForButton: Incomplete
SDL_GameControllerHasButton: Incomplete
SDL_GameControllerGetButton: Incomplete
SDL_GameControllerGetNumTouchpads: Incomplete
SDL_GameControllerGetNumTouchpadFingers: Incomplete
SDL_GameControllerGetTouchpadFinger: Incomplete
SDL_GameControllerHasSensor: Incomplete
SDL_GameControllerSetSensorEnabled: Incomplete
SDL_GameControllerIsSensorEnabled: Incomplete
SDL_GameControllerGetSensorDataRate: Incomplete
SDL_GameControllerGetSensorData: Incomplete
SDL_GameControllerGetSensorDataWithTimestamp: Incomplete
SDL_GameControllerAddMappingsFromRW: Incomplete
SDL_GameControllerAddMappingsFromFile: Incomplete
SDL_GameControllerFromInstanceID: Incomplete
SDL_GameControllerFromPlayerIndex: Incomplete
SDL_GameControllerGetPlayerIndex: Incomplete
SDL_GameControllerSetPlayerIndex: Incomplete
SDL_GameControllerGetVendor: Incomplete
SDL_GameControllerGetProduct: Incomplete
SDL_GameControllerGetProductVersion: Incomplete
SDL_GameControllerGetFirmwareVersion: Incomplete
SDL_GameControllerGetSerial: Incomplete
SDL_GameControllerNumMappings: Incomplete
SDL_GameControllerMappingForIndex: Incomplete
SDL_GameControllerMappingForDeviceIndex: Incomplete
SDL_GameControllerRumble: Incomplete
SDL_GameControllerRumbleTriggers: Incomplete
SDL_GameControllerHasLED: Incomplete
SDL_GameControllerHasRumble: Incomplete
SDL_GameControllerHasRumbleTriggers: Incomplete
SDL_GameControllerSetLED: Incomplete
SDL_GameControllerSendEffect: Incomplete
SDL_GameControllerClose: Incomplete
SDL_GameControllerGetAppleSFSymbolsNameForButton: Incomplete
SDL_GameControllerGetAppleSFSymbolsNameForAxis: Incomplete
SDL_GameControllerMappingForGUID: Incomplete
