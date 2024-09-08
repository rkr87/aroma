from ctypes import Structure, Union, c_int

from _typeshed import Incomplete

from .syswm import SDL_SysWMmsg as SDL_SysWMmsg

SDL_RELEASED: int
SDL_PRESSED: int
SDL_EventType = int
SDL_FIRSTEVENT: int
SDL_QUIT: int
SDL_APP_TERMINATING: int
SDL_APP_LOWMEMORY: int
SDL_APP_WILLENTERBACKGROUND: int
SDL_APP_DIDENTERBACKGROUND: int
SDL_APP_WILLENTERFOREGROUND: int
SDL_APP_DIDENTERFOREGROUND: int
SDL_LOCALECHANGED: int
SDL_DISPLAYEVENT: int
SDL_WINDOWEVENT: int
SDL_SYSWMEVENT: int
SDL_KEYDOWN: int
SDL_KEYUP: int
SDL_TEXTEDITING: int
SDL_TEXTINPUT: int
SDL_KEYMAPCHANGED: int
SDL_TEXTEDITING_EXT: int
SDL_MOUSEMOTION: int
SDL_MOUSEBUTTONDOWN: int
SDL_MOUSEBUTTONUP: int
SDL_MOUSEWHEEL: int
SDL_JOYAXISMOTION: int
SDL_JOYBALLMOTION: int
SDL_JOYHATMOTION: int
SDL_JOYBUTTONDOWN: int
SDL_JOYBUTTONUP: int
SDL_JOYDEVICEADDED: int
SDL_JOYDEVICEREMOVED: int
SDL_JOYBATTERYUPDATED: int
SDL_CONTROLLERAXISMOTION: int
SDL_CONTROLLERBUTTONDOWN: int
SDL_CONTROLLERBUTTONUP: int
SDL_CONTROLLERDEVICEADDED: int
SDL_CONTROLLERDEVICEREMOVED: int
SDL_CONTROLLERDEVICEREMAPPED: int
SDL_CONTROLLERTOUCHPADDOWN: int
SDL_CONTROLLERTOUCHPADMOTION: int
SDL_CONTROLLERTOUCHPADUP: int
SDL_CONTROLLERSENSORUPDATE: int
SDL_FINGERDOWN: int
SDL_FINGERUP: int
SDL_FINGERMOTION: int
SDL_DOLLARGESTURE: int
SDL_DOLLARRECORD: int
SDL_MULTIGESTURE: int
SDL_CLIPBOARDUPDATE: int
SDL_DROPFILE: int
SDL_DROPTEXT: int
SDL_DROPBEGIN: int
SDL_DROPCOMPLETE: int
SDL_AUDIODEVICEADDED: int
SDL_AUDIODEVICEREMOVED: int
SDL_SENSORUPDATE: int
SDL_RENDER_TARGETS_RESET: int
SDL_RENDER_DEVICE_RESET: int
SDL_POLLSENTINEL: int
SDL_USEREVENT: int
SDL_LASTEVENT: int
SDL_eventaction = c_int
SDL_ADDEVENT: int
SDL_PEEKEVENT: int
SDL_GETEVENT: int
SDL_TEXTEDITINGEVENT_TEXT_SIZE: int
SDL_TEXTINPUTEVENT_TEXT_SIZE: int
SDL_QUERY: int
SDL_IGNORE: int
SDL_DISABLE: int
SDL_ENABLE: int

class SDL_CommonEvent(Structure): ...
class SDL_DisplayEvent(Structure): ...
class SDL_WindowEvent(Structure): ...
class SDL_KeyboardEvent(Structure): ...
class SDL_TextEditingEvent(Structure): ...
class SDL_TextEditingExtEvent(Structure): ...
class SDL_TextInputEvent(Structure): ...
class SDL_MouseMotionEvent(Structure): ...
class SDL_MouseButtonEvent(Structure): ...
class SDL_MouseWheelEvent(Structure): ...
class SDL_JoyAxisEvent(Structure): ...
class SDL_JoyBallEvent(Structure): ...
class SDL_JoyHatEvent(Structure): ...
class SDL_JoyButtonEvent(Structure): ...
class SDL_JoyDeviceEvent(Structure): ...
class SDL_JoyBatteryEvent(Structure): ...
class SDL_ControllerAxisEvent(Structure): ...
class SDL_ControllerButtonEvent(Structure): ...
class SDL_ControllerDeviceEvent(Structure): ...
class SDL_ControllerTouchpadEvent(Structure): ...
class SDL_ControllerSensorEvent(Structure): ...
class SDL_AudioDeviceEvent(Structure): ...
class SDL_TouchFingerEvent(Structure): ...
class SDL_MultiGestureEvent(Structure): ...
class SDL_DollarGestureEvent(Structure): ...
class SDL_DropEvent(Structure): ...
class SDL_SensorEvent(Structure): ...
class SDL_QuitEvent(Structure): ...
class SDL_OSEvent(Structure): ...
class SDL_UserEvent(Structure): ...
class SDL_SysWMEvent(Structure): ...
class SDL_Event(Union):
    type: SDL_EventType

SDL_EventFilter: Incomplete
SDL_PumpEvents: Incomplete
SDL_PeepEvents: Incomplete
SDL_HasEvent: Incomplete
SDL_HasEvents: Incomplete
SDL_FlushEvent: Incomplete
SDL_FlushEvents: Incomplete
def SDL_PollEvent(event: SDL_Event) -> int: ...
SDL_WaitEvent: Incomplete
SDL_WaitEventTimeout: Incomplete
SDL_PushEvent: Incomplete
SDL_SetEventFilter: Incomplete
SDL_GetEventFilter: Incomplete
SDL_AddEventWatch: Incomplete
SDL_DelEventWatch: Incomplete
SDL_FilterEvents: Incomplete
SDL_EventState: Incomplete
SDL_GetEventState: Incomplete
SDL_RegisterEvents: Incomplete
