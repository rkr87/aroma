"""Defines a menu for creating a new collection."""

from collections import OrderedDict
from pathlib import Path

from app.input.keyboard import Keyboard
from app.menu.menu_base import MenuBase
from app.menu.menu_item_single import MenuItemSingle
from app.model.side_pane import SidePane
from app.navigation.menu_collection_edit import MenuCollectionEdit
from app.navigation.menu_stack import MenuStack
from app.strings import Strings
from data.model.collection_config import CollectionConfig
from manager.collection_manager import CollectionManager
from shared.constants import COLLECTION_DEFAULTS, COLLECTION_PATH


class MenuCollectionNew(MenuBase):
    """Manages the menu for creating a new collection."""

    def __init__(self) -> None:
        self.menu_stack: MenuStack = MenuStack()
        super().__init__(Strings().new_collection, OrderedDict())
        self.edit_collection = MenuCollectionEdit()
        self.collection = CollectionManager()
        self._template_list: list[CollectionConfig] = []

    def _dynamic_menu_default_items(self) -> None:
        """TODO."""
        self._template_list = sorted(
            self.collection.config.get_templates(),
            key=lambda item: item.label,
        )
        self.content.add_section(
            ("CUSTOM_COLLECTION", self._custom_collection()),
            ("CREATE_TEMPLATES", self._create_all_templates()),
        )

    def _custom_collection_keywords(self, collection: Path) -> None:
        """TODO."""

        def add_keywords(keywords: str) -> None:
            self.collection.operations.add_comma_separated_keywords(
                collection, keywords
            )

        Keyboard().open(
            Strings().collection_include_words_prompt, add_keywords
        )

    def _nav_to_new_collection(self) -> None:
        """TODO."""
        self.menu_stack.pop(regenerate_all=True)
        self.menu_stack.push(self.edit_collection)

    def _create_all_templates(self) -> MenuItemSingle:
        """TODO."""

        def create_templates() -> None:
            self.collection.bulk.create_template_collections()
            self.menu_stack.pop(regenerate_all=True)

        desc = [
            item.label
            for item in self._template_list
            if not self.collection.config.template_exists(item.directory)
        ]

        return MenuItemSingle(
            Strings().create_all_template_collections,
            create_templates,
            side_pane=SidePane(
                Strings().create_all_template_collections,
                Strings().append_list(
                    "create_all_template_collections_desc", desc
                ),
            ),
        )

    def _custom_collection(self) -> MenuItemSingle:
        """TODO."""
        collection_name: str = ""

        side_pane = SidePane(
            img=str(COLLECTION_DEFAULTS / "icon.png"),
            bg_img=str(COLLECTION_DEFAULTS / "background.png"),
        )

        def on_close() -> None:
            if collection_name:
                self.edit_collection.init_dynamic_menu(
                    collection_name,
                    COLLECTION_PATH / collection_name,
                    None,
                    side_pane=side_pane,
                )
                self._nav_to_new_collection()

        def create_collection(name: str) -> None:
            nonlocal collection_name
            collection_name = name
            if self.collection.operations.create_custom_collection(name):
                self._custom_collection_keywords(COLLECTION_PATH / name)
            else:
                Keyboard().close(force_close=True)

        return self._generate_keyboard_menu_item(
            create_collection,
            Strings().custom_collection,
            Strings().custom_collection_desc,
            Strings().custom_collection_prompt,
            keep_open=True,
            on_close=on_close,
            side_pane=side_pane,
        )

    def _build_dynamic_menu(
        self,
        path: Path | None,  # noqa: ARG002
        identifier: str | None,  # noqa: ARG002
    ) -> None:
        for collection in self._template_list:
            self._create_template_menu_item(collection)

    def _create_template_menu_item(
        self, template_config: CollectionConfig
    ) -> None:
        """TODO."""
        icon = self.collection.operations.get_default_file(
            template_config.icon,
            template_config.directory,
            from_template=True,
        )
        background = self.collection.operations.get_default_file(
            template_config.background,
            template_config.directory,
            from_template=True,
        )
        side_pane = SidePane(
            header=template_config.format_label,
            img=str(icon),
            bg_img=str(background),
            content=Strings().collection_description(
                template_config.label,
                template_config.include,
                template_config.exclude,
            ),
        )

        def create_from_template() -> None:
            self.collection.operations.create_template_collection(
                template_config
            )
            self.edit_collection.init_dynamic_menu(
                template_config.format_label,
                COLLECTION_PATH / template_config.directory,
                None,
                side_pane=side_pane,
            )
            self._nav_to_new_collection()

        menu_item = MenuItemSingle(
            template_config.format_label,
            create_from_template,
            side_pane=side_pane,
        )
        menu_item.deactivated = self.collection.config.template_exists(
            template_config.directory
        )
        self.content.add_item(template_config.label, menu_item)
