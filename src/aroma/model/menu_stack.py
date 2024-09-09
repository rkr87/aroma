"""
Defines data structures for managing a stack of menus and their navigation
history.
"""
from dataclasses import dataclass, field

from model.current_menu import CurrentMenu
from navigation.base_menu import BaseMenu


@dataclass
class MenuStack:
    """
    Manages a stack of menus and provides methods to navigate through them.
    """

    menus: list[BaseMenu] = field(default_factory=list)

    def push(self, item: BaseMenu) -> CurrentMenu:
        """
        Adds a new menu to the stack and returns the current menu state.
        """
        self.menus.append(item)
        return CurrentMenu(
            self.menus[-1],
            [x.breadcrumb for x in self.menus],
            True
        )

    def pop(self) -> None:
        """
        Removes the top menu from the stack, if more than one menu exists.
        """
        if len(self.menus) > 1:
            self.menus.pop()

    def clear(self) -> None:
        """
        Clears all menus from the stack.
        """
        self.menus.clear()

    def get_current(self, update_req: bool = False) -> CurrentMenu | None:
        """
        Retrieves the current menu state.
        """
        if not self.menus:
            return None
        return CurrentMenu(
            self.menus[-1],
            [x.breadcrumb for x in self.menus],
            update_req
        )
