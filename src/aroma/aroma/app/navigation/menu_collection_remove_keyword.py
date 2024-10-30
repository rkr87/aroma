"""TODO."""

from collections import OrderedDict
from functools import partial
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from manager.collection_manager import CollectionManager


class MenuCollectionRemoveKeyword(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.collection = CollectionManager()
        super().__init__("REMOVE KEYWORD", OrderedDict())

    def _dynamic_menu_default_items(self) -> None:
        pass

    def _build_dynamic_menu(
        self, path: Path | None, identifier: str | None
    ) -> None:
        valid_identifiers = ["include", "exclude"]
        if not path or not identifier or identifier not in valid_identifiers:
            raise FileNotFoundError
        config = self.collection.config.get_collection(path)
        exclude = identifier == valid_identifiers[1]
        self.breadcrumb = (
            Strings().collection_remove_exclude_words
            if exclude
            else Strings().collection_remove_include_words
        )
        words: list[str] = getattr(config, identifier)

        def remove(keyword: str) -> None:
            self.collection.operations.delete_keyword(
                config, keyword, exclude_words=exclude
            )
            if words:
                self.menu_stack.regenerate_stack()
            else:
                self.menu_stack.pop(regenerate_all=True)

        for word in words:
            menu_item = MenuItemSingle(
                word.upper(),
                partial(remove, word),
            )
            self.content.add_item(word.upper(), menu_item)
