"""Defines a menu for creating a new collection."""

from collections import OrderedDict
from pathlib import Path

from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collection_edit import MenuCollectionEdit
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from data.model.collection_config import CollectionConfig
from manager.collection_manager import CollectionManager
from shared.constants import COLLECTION_PATH


class MenuCollectionCollagen(MenuBase):
    """TODO."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        super().__init__(Strings().new_collection, OrderedDict())
        self.edit_menu = MenuCollectionEdit()
        super().__init__(Strings().new_collection, OrderedDict())
        self.collection = CollectionManager()
        self._collagen_list: list[CollectionConfig] = []

    def _dynamic_menu_default_items(self) -> None:
        """TODO."""
        self._collagen_list = sorted(
            self.collection.config.get_collagen_collections(),
            key=lambda item: item.label,
        )
        self.content.add_section(
            ("IMPORT_ALL", self._import_collagen_collections()),
        )

    def _nav_to_imported_collection(self) -> None:
        """TODO."""
        self.menu_stack.pop(regenerate_all=True)
        self.menu_stack.push(self.edit_menu)

    def _import_collagen_collections(self) -> MenuItemSingle:
        """TODO."""

        def create_collagen() -> None:
            self.collection.bulk.create_collagen_collections()
            self.menu_stack.pop(regenerate_all=True)

        desc = [
            item.label
            for item in self._collagen_list
            if not self.collection.config.collection_exists(
                item.directory, aroma_only=True
            )
        ]

        return MenuItemSingle(
            Strings().collagen_import_all,
            create_collagen,
            side_pane=SidePane(
                Strings().collagen_import_all,
                Strings().append_list("collagen_import_all_desc", desc),
            ),
        )

    def _build_dynamic_menu(
        self,
        path: Path | None,  # noqa: ARG002
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        for collection in self._collagen_list:
            self._create_collagen_menu_item(collection)

    def _create_collagen_menu_item(self, collagen: CollectionConfig) -> None:
        """TODO."""
        coll_path = COLLECTION_PATH / collagen.directory
        side_pane = SidePane(
            header=collagen.format_label,
            img=str(coll_path / collagen.icon),
            bg_img=str(coll_path / collagen.background),
            content=Strings().collection_description(
                collagen.label,
                collagen.include,
                collagen.exclude,
            ),
        )

        def create_from_collagen() -> None:
            self.collection.operations.create_collagen_collection(collagen)
            self.edit_menu.init_dynamic_menu(
                collagen.format_label,
                COLLECTION_PATH / collagen.directory,
                None,
                side_pane=side_pane,
            )
            self._nav_to_imported_collection()

        menu_item = MenuItemSingle(
            collagen.format_label,
            create_from_collagen,
            side_pane=side_pane,
        )
        menu_item.deactivated = self.collection.config.collection_exists(
            collagen.directory, aroma_only=True
        )
        self.content.add_item(collagen.label, menu_item)
