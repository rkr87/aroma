"""Defines data structures for managing a stack of menus."""

from dataclasses import dataclass, field

from app.menu.menu_base import MenuBase
from app.model.current_menu import CurrentMenu
from shared.classes.class_singleton import ClassSingleton


@dataclass
class MenuStack(ClassSingleton):
    """Manages a stack of menus and provides methods to navigate them."""

    menus: list[MenuBase] = field(default_factory=list)

    def push(self, item: MenuBase) -> CurrentMenu:
        """Add a new menu to the stack and returns the current menu state."""
        logger = MenuStack.get_static_logger()
        logger.info("Menu pushed: %s", item.breadcrumb)
        self.menus.append(item)
        return CurrentMenu(
            self.menus[-1],
            [x.breadcrumb for x in self.menus],
            update_required=True,
        )

    def rebuild_menu_stack(self) -> None:
        """Rebuilds all menus in the stack."""
        for menu in self.menus:
            menu.reset_menu()

    def pop(self, *, regenerate: bool = False) -> None:
        """Remove the top menu from the stack, if more than one menu exists."""
        logger = MenuStack.get_static_logger()
        if len(self.menus) > 1:
            logger.info("Menu popped: %s", self.menus[-1].breadcrumb)
            self.menus[-1].select.state.reset()
            self.menus.pop()
            if regenerate:
                self.menus[-1].regenerate_dynamic_menu()

    def clear(self) -> None:
        """Clear all menus from the stack."""
        logger = MenuStack.get_static_logger()
        logger.debug("Clearing menu stack")
        self.menus.clear()

    def get_current(
        self,
        *,
        update_required: bool = False,
    ) -> CurrentMenu | None:
        """Retrieve the current menu state."""
        logger = MenuStack.get_static_logger()
        if not self.menus:
            logger.debug("Menu stack is empty")
            return None
        return CurrentMenu(
            self.menus[-1],
            [x.breadcrumb for x in self.menus],
            update_required,
        )
