"""Defines a menu for creating a new collection."""

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collection_remove_keyword import (
    MenuCollectionRemoveKeyword,
)
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from data.model.collection_config import CollectionConfig
from manager.collection_manager import CollectionManager
from manager.rom_manager import RomManager
from shared.constants import COLLECTION_PATH

if TYPE_CHECKING:
    from app.menu.menu_item_base import MenuItemBase


class MenuCollectionEdit(MenuBase):
    """Manages the menu for creating a new collection."""

    def __init__(self) -> None:
        self.remove_words = MenuCollectionRemoveKeyword()
        self.menu_stack = MenuStack()
        self.collection = CollectionManager()
        super().__init__(Strings().new_collection, OrderedDict())

    def _set_separation_status(
        self, collection: Path, config: CollectionConfig
    ) -> MenuItemSingle:
        """TODO."""

        def set_status() -> None:
            self.collection.operations.set_systems_separated(
                collection, separated=not config.systems_separated
            )
            self.regenerate_dynamic_menu()

        if config.systems_separated:
            label = Strings().collapse_collection_systems
            desc = Strings().collapse_collection_systems_desc
        else:
            label = Strings().separate_collection_systems
            desc = Strings().separate_collection_systems_desc

        return MenuItemSingle(label, set_status, SidePane(label, desc))

    def _delete_collection(self, collection: Path) -> MenuItemSingle:
        """TODO."""

        def delete_and_nav() -> None:
            self.collection.operations.delete_collection(collection)
            self.menu_stack.pop(regenerate_all=True)

        return MenuItemSingle(
            Strings().delete_collection,
            delete_and_nav,
            SidePane(
                Strings().delete_collection, Strings().delete_collection_desc
            ),
        )

    @staticmethod
    def _refresh_collection(collection: CollectionConfig) -> MenuItemSingle:
        """TODO."""

        def refresh() -> None:
            RomManager().refresh_collection(collection)

        def work() -> None:
            BackgroundWorker().do_work(
                refresh, Strings().refreshing_collection
            )

        return MenuItemSingle(
            Strings().refresh_collection,
            work,
            SidePane(
                Strings().refresh_collection, Strings().refresh_collection_desc
            ),
        )

    def _rename_collection(self, collection: Path) -> MenuItemSingle:
        """TODO."""

        def rename_and_nav(new_name: str) -> None:
            new_config = self.collection.operations.rename_collection(
                collection, new_name
            )
            if not new_config:
                return
            self.menu_stack.pop(regenerate_all=True)
            self.init_dynamic_menu(
                new_config.format_label,
                COLLECTION_PATH / new_config.directory,
                None,
            )
            self.menu_stack.push(self)

        return self._generate_keyboard_menu_item(
            rename_and_nav,
            Strings().rename_collection,
            Strings().rename_collection_desc,
            Strings().rename_collection_prompt,
            collection.name,
        )

    def _edit_keywords(
        self, collection: Path, current: list[str], *, exclude: bool = False
    ) -> MenuItemSingle:
        """TODO."""

        def add_keywords(keywords: str) -> None:
            self.collection.operations.add_comma_separated_keywords(
                collection, keywords, exclude_words=exclude
            )
            self.menu_stack.regenerate_stack()

        if exclude:
            label = Strings().collection_add_exclude_words
            desc = Strings().append_list(
                "collection_add_exclude_words_desc", current
            )
            prompt = Strings().collection_exclude_words_prompt
        else:
            label = Strings().collection_add_include_words
            desc = Strings().append_list(
                "collection_add_include_words_desc", current
            )
            prompt = Strings().collection_include_words_prompt

        return self._generate_keyboard_menu_item(
            add_keywords,
            label,
            desc,
            prompt,
            keep_open=True,
            on_close=self.regenerate_dynamic_menu,
        )

    def _remove_keywords(
        self, collection: Path, current: list[str], *, exclude: bool = False
    ) -> MenuItemSingle:
        """TODO."""
        if exclude:
            label = Strings().collection_remove_exclude_words
            desc = Strings().append_list(
                "collection_remove_exclude_words_desc", current
            )
            identifier = "exclude"
        else:
            label = Strings().collection_remove_include_words
            desc = Strings().append_list(
                "collection_remove_include_words_desc", current
            )
            identifier = "include"

        return self.dynamic_sub_menu(
            label,
            collection,
            identifier,
            self.remove_words,
            self.menu_stack.push,
            side_pane=SidePane(label, desc),
        )

    def _clear_keywords(
        self, collection: Path, current: list[str], *, exclude: bool = False
    ) -> MenuItemSingle:
        """TODO."""

        def clear() -> None:
            self.collection.operations.clear_keywords(
                collection, exclude_words=exclude
            )
            self.menu_stack.regenerate_stack()

        if exclude:
            label = Strings().collection_clear_exclude_words
            desc = Strings().append_list(
                "collection_clear_exclude_words_desc", current
            )
        else:
            label = Strings().collection_clear_include_words
            desc = Strings().append_list(
                "collection_clear_include_words_desc", current
            )

        return MenuItemSingle(label, clear, SidePane(label, desc))

    def _group_method_override(
        self, path: Path, *, current: bool
    ) -> MenuItemMulti:
        """TODO."""

        def set_override(override: bool) -> None:  # noqa: FBT001
            self.collection.operations.set_group_method_override(
                path, override=override
            )
            self.regenerate_dynamic_menu()

        data: dict[bool, str] = {
            True: Strings().custom,
            False: Strings().inherit,
        }
        options = list(data.keys())
        default = options.index(current)
        actions = self._generate_actions(data, set_override)
        return MenuItemMulti(
            Strings().collection_group_method_override,
            actions,
            default,
            side_pane=SidePane(
                Strings().collection_group_method_override,
                Strings().collection_group_method_override_desc,
            ),
        )

    def _group_method(self, config: CollectionConfig) -> MenuItemSingle:
        """Create a menu item for setting collection item name format."""

        def set_group_method(new_name: str) -> None:
            self.collection.operations.set_group_method(config, new_name)
            self.regenerate_dynamic_menu()

        help_text = ", ".join(Strings().get_format_mapping())

        return self._generate_keyboard_menu_item(
            set_group_method,
            Strings().collection_custom_group_method,
            [
                f"{Strings().current}: {config.custom_group_method}",
                Strings().get_mapped_name_format(
                    config.custom_group_method,
                    include_prefix=True,
                ),
                "",
                *Strings().collection_custom_group_method_desc,
                "",
                help_text,
            ],
            Strings().group_method_prompt,
            config.custom_group_method,
            help_info=[help_text],
        )

    def _dynamic_menu_default_items(self) -> None:
        pass

    def _build_grouping_menu(
        self, path: Path, config: CollectionConfig
    ) -> None:
        """TODO."""
        grouping: list[tuple[str, MenuItemBase]] = [
            (
                "GROUP_METHOD_OVERRIDE",
                self._group_method_override(
                    path, current=config.override_group_method
                ),
            )
        ]
        if config.override_group_method:
            grouping.append(("GROUP_METHOD", self._group_method(config)))
        self.content.add_section(*grouping)

    def _build_include_menu(
        self, path: Path, config: CollectionConfig
    ) -> None:
        """TODO."""
        include: list[tuple[str, MenuItemBase]] = [
            ("ADD_INCLUDE", self._edit_keywords(path, config.include))
        ]
        if config.include:
            include.append(
                ("REMOVE_INCLUDE", self._remove_keywords(path, config.include))
            )
            include.append(
                ("CLEAR_INCLUDE", self._clear_keywords(path, config.include))
            )
        self.content.add_section(*include)

    def _build_exclude_menu(
        self, path: Path, config: CollectionConfig
    ) -> None:
        """TODO."""
        exclude: list[tuple[str, MenuItemBase]] = [
            (
                "ADD_EXCLUDE",
                self._edit_keywords(path, config.exclude, exclude=True),
            )
        ]
        if config.exclude:
            exclude.append(
                (
                    "REMOVE_EXCLUDE",
                    self._remove_keywords(path, config.exclude, exclude=True),
                )
            )
            exclude.append(
                (
                    "CLEAR_EXCLUDE",
                    self._clear_keywords(path, config.exclude, exclude=True),
                )
            )
        self.content.add_section(*exclude)

    def _build_dynamic_menu(
        self,
        path: Path | None,
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        if not path:
            raise FileNotFoundError
        config = self.collection.config.get_collection(path)

        if config.is_aroma_collection:
            self.content.add_section(
                ("REFRESH_COLLECTION", self._refresh_collection(config)),
                ("SET_SEPARATION", self._set_separation_status(path, config)),
            )
            self._build_grouping_menu(path, config)

        self.content.add_section(
            ("RENAME_COLLECTION", self._rename_collection(path)),
            ("DELETE_COLLECTION", self._delete_collection(path)),
        )
        self._build_include_menu(path, config)
        self._build_exclude_menu(path, config)
