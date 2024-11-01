"""Defines a menu for managing collections."""

from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from app.background_worker import BackgroundWorker
from app.menu.menu_base import MenuBase
from app.menu.menu_item_multi import MenuItemMulti
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collection_edit import MenuCollectionEdit
from app.navigation.menu_collection_new import MenuCollectionNew
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from manager.collection_manager import CollectionManager
from manager.rom_manager import RomManager
from shared.app_config import AppConfig
from shared.constants import COLLECTION_PATH

if TYPE_CHECKING:
    from app.menu.menu_item_base import MenuItemBase


class MenuCollectionManagement(MenuBase):  # pylint: disable=too-many-instance-attributes
    """Manages a menu for collections."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        self.new_collection = MenuCollectionNew()
        self.edit_collection = MenuCollectionEdit()
        self.collection = CollectionManager()
        super().__init__(Strings().collection_management, OrderedDict())
        self._aroma_collection_names: list[str] = []

    def _dynamic_menu_default_items(self) -> None:
        """TODO."""
        self.content.add_section(
            ("NEW_COLLECTION", self._new_collection()),
        )
        separation: list[tuple[str, MenuItemBase]] = [
            ("DEFAULT_SEPARATION", self._set_collections_separated())
        ]
        refresh: list[tuple[str, MenuItemBase]] = [
            ("REFRESH_ON_REFRESH", self._set_refresh_collections_on_refresh())
        ]
        if colls := self.collection.config.get_collections(aroma_only=True):
            self._aroma_collection_names = [coll.label for coll in colls]
            refresh.insert(
                0, (("REFRESH_COLLECTIONS", self._refresh_collections()))
            )

            separation.append(("SEPARATE_ALL", self._set_all_separated()))
            separation.append(
                ("COLLAPSE_ALL", self._set_all_separated(separated=False))
            )
        self.content.add_section(*refresh)
        self.content.add_section(*separation)
        grouping: list[tuple[str, MenuItemBase]] = [
            ("GROUP_METHOD_OVERRIDE", self._group_method_override())
        ]
        if AppConfig().override_collection_group_method:
            grouping.append(("GROUP_METHOD", self._group_method()))
        if colls:
            self.content.add_section(
                ("DELETE_COLLECTIONS", self._delete_collections()),
            )
        self.content.add_section(*grouping)

    def _set_all_separated(self, *, separated: bool = True) -> MenuItemSingle:
        """TODO."""

        def action() -> None:
            self.collection.bulk.set_systems_separated_all_collections(
                separated=separated
            )

        if separated:
            label = Strings().separate_all_collections
            desc = Strings().append_list(
                "separate_all_collections_desc", self._aroma_collection_names
            )
        else:
            label = Strings().collapse_all_collections
            desc = Strings().append_list(
                "collapse_all_collections_desc", self._aroma_collection_names
            )
        return MenuItemSingle(label, action, side_pane=SidePane(label, desc))

    def _group_method_override(self) -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().custom,
            False: Strings().inherit,
        }
        actions, current = self._generate_config_actions(
            data,
            "override_collection_group_method",
            self.regenerate_dynamic_menu,
        )
        return MenuItemMulti(
            Strings().collections_group_method_override,
            actions,
            current,
            SidePane(
                Strings().collections_group_method_override,
                Strings().collections_group_method_override_desc,
            ),
        )

    def _group_method(self) -> MenuItemSingle:
        """Create a menu item for setting collection item name format."""
        return self._generate_keyboard_config_item(
            "custom_collection_group_method",
            Strings().collections_custom_group_method,
            [
                Strings().get_mapped_name_format(
                    AppConfig().custom_collection_group_method,
                    include_prefix=True,
                ),
                "",
                *Strings().collections_custom_group_method_desc,
                "",
                *Strings().get_format_mapping(": "),
            ],
            Strings().group_method_prompt,
            help_info=[", ".join(Strings().get_format_mapping())],
        )

    @staticmethod
    def _set_collections_separated() -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().separated,
            False: Strings().collapsed,
        }
        actions, current = MenuCollectionManagement._generate_config_actions(
            data, "separate_collections_by_system_default"
        )
        return MenuItemMulti(
            Strings().collections_separated_systems_default,
            actions,
            current,
            SidePane(
                Strings().collections_separated_systems_default,
                Strings().collections_separated_systems_default_desc,
            ),
        )

    @staticmethod
    def _set_refresh_collections_on_refresh() -> MenuItemMulti:
        """TODO."""
        data: dict[bool, str] = {
            True: Strings().yes,
            False: Strings().no,
        }
        actions, current = MenuCollectionManagement._generate_config_actions(
            data, "refresh_collections_on_refresh"
        )
        return MenuItemMulti(
            Strings().refresh_collections_refresh,
            actions,
            current,
            SidePane(
                Strings().refresh_collections_refresh,
                Strings().refresh_collections_refresh_desc,
            ),
        )

    def _new_collection(self) -> MenuItemSingle:
        """TODO."""
        return self.dynamic_sub_menu(
            Strings().new_collection,
            None,
            None,
            self.new_collection,
            MenuStack().push,
            side_pane=SidePane(
                Strings().new_collection, Strings().new_collection_desc
            ),
        )

    def _delete_collections(self) -> MenuItemSingle:
        """TODO."""

        def delete_and_refresh() -> None:
            self.collection.bulk.delete_all_collections()
            self.regenerate_dynamic_menu()

        return MenuItemSingle(
            Strings().delete_all_collections,
            delete_and_refresh,
            side_pane=SidePane(
                Strings().delete_all_collections,
                Strings().append_list(
                    "delete_all_collections_desc", self._aroma_collection_names
                ),
            ),
        )

    def _refresh_collections(self) -> MenuItemSingle:
        """TODO."""

        def refresh() -> None:
            BackgroundWorker().do_work(
                RomManager().refresh_collections,
                Strings().refreshing_collections,
            )

        return MenuItemSingle(
            Strings().refresh_all_collections,
            refresh,
            side_pane=SidePane(
                Strings().refresh_all_collections,
                Strings().append_list(
                    "refresh_all_collections_desc",
                    self._aroma_collection_names,
                ),
            ),
        )

    def _build_dynamic_menu(
        self,
        path: Path | None,  # noqa: ARG002
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        for collection in sorted(
            self.collection.config.get_collections(),
            key=lambda item: item.label,
        ):
            collection_path = COLLECTION_PATH / collection.directory
            self.content.add_item(
                collection.label,
                self.dynamic_sub_menu(
                    collection.format_label,
                    collection_path,
                    None,
                    self.edit_collection,
                    self.menu_stack.push,
                    side_pane=SidePane(
                        header=collection.format_label,
                        img=str(collection_path / collection.icon),
                        bg_img=str(collection_path / collection.background),
                        content=Strings().collection_description(
                            collection.label,
                            collection.include,
                            collection.exclude,
                        ),
                    ),
                    children_side_pane=SidePane(
                        img=str(collection_path / collection.icon),
                        bg_img=str(collection_path / collection.background),
                    ),
                ),
            )
