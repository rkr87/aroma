"""TODO."""

from collections import OrderedDict
from collections.abc import Callable

from app.model.keyboard_button import KeyboardButton
from shared.classes.class_singleton import ClassSingleton
from shared.constants import RESOURCES

_SYMBOL_MAP: OrderedDict[str, str] = OrderedDict(
    [
        ("1", "!"),
        ("2", '"'),
        ("3", "£"),
        ("4", "$"),
        ("5", "%"),
        ("6", "^"),
        ("7", "&"),
        ("8", "*"),
        ("9", "("),
        ("0", ")"),
        ("-", "_"),
        ("=", "+"),
        ("`", "¬"),
        ("[", "{"),
        ("]", "}"),
        ("\\", "|"),
        (";", ":"),
        ("'", "@"),
        ("#", "~"),
        (",", "<"),
        (".", ">"),
        ("/", "?"),
    ]
)


class Keyboard(ClassSingleton):  # pylint: disable=too-many-instance-attributes
    """TODO."""

    def __init__(self) -> None:
        super().__init__()
        self.caps_on = False
        self.shift_on = False
        self.is_open = False
        self.current_input = ""
        self.on_submit: Callable[[str], None] | None = None
        self.prompt = ""
        self.update_req = False

    def open(
        self,
        prompt: str,
        on_submit: Callable[[str], None] | None = None,
        current_val: str = "",
    ) -> None:
        """TODO."""
        self.current_input = current_val
        self.prompt = prompt
        self.on_submit = on_submit
        self.update_req = True
        self.is_open = True

    def toggle_capslock(self) -> None:
        """TODO."""
        self.caps_on = not self.caps_on

    def toggle_shift(self) -> None:
        """TODO."""
        self.shift_on = not self.shift_on

    def backspace(self) -> None:
        """TODO."""
        self.current_input = self.current_input[:-1]

    def space(self) -> None:
        """TODO."""
        self.current_input = f"{self.current_input} "

    def handle_key(self, button: KeyboardButton) -> None:
        """Handle a key press."""
        special_actions: dict[str, Callable[..., None]] = {
            "ENTER": self.submit,
            "BKSP": self.backspace,
            "CAPS": self.toggle_capslock,
            "SHIFT": self.toggle_shift,
            "SPACE": self.space,
        }

        if button.key in special_actions:
            special_actions[button.key]()
            return
        self.current_input += button.key
        if self.shift_on:
            self.toggle_shift()

    def close(self) -> None:
        """TODO."""
        self.current_input = ""
        self.prompt = ""
        self.on_submit = None
        self.update_req = True
        self.is_open = False

    def submit(self) -> None:
        """Submit the current input and clear it."""
        if self.on_submit:
            self.on_submit(self.current_input)
        self.close()

    def get_current_input(self) -> str:
        """Return the current input string."""
        return self.current_input

    def _map_keys(
        self,
        keys: list[str],
    ) -> list[KeyboardButton]:
        """TODO."""
        new_keys: list[KeyboardButton] = []
        for key in keys:
            mapped_key = (
                _SYMBOL_MAP[key]
                if key in _SYMBOL_MAP and self.shift_on
                else key
            )
            mapped_key = (
                mapped_key.upper()
                if (int(self.caps_on) + int(self.shift_on)) % 2 == 1
                else mapped_key
            )
            new_keys.append(KeyboardButton(mapped_key))
        return new_keys

    def available_keys(self) -> list[list[KeyboardButton]]:
        """Return a list of keys available in the current layout."""
        top_row = self._map_keys(list(_SYMBOL_MAP.keys())[:12])
        row_1 = self._map_keys(list("qwertyuiop[]"))
        row_2 = self._map_keys(list("asdfghjkl;'#"))
        row_3 = self._map_keys(list("\\zxcvbnm,./`"))
        common_keys: list[KeyboardButton] = [
            KeyboardButton(
                "SHIFT", 2, self.shift_on, f"{RESOURCES}/ui/button-L.png"
            ),
            KeyboardButton(
                "CAPS", 2, self.caps_on, f"{RESOURCES}/ui/button-R.png"
            ),
            KeyboardButton(
                "SPACE", 4, hint_img=f"{RESOURCES}/ui/button-X.png"
            ),
            KeyboardButton("BKSP", 2, hint_img=f"{RESOURCES}/ui/button-Y.png"),
            KeyboardButton(
                "ENTER", 2, hint_img=f"{RESOURCES}/ui/button-START.png"
            ),
        ]
        return [top_row, row_1, row_2, row_3, common_keys]
