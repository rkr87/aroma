"""Manages image files associated with ROMs."""

from pathlib import Path

from classes.base.class_singleton import ClassSingleton
from constants import IMG_PATH, ROM_PATH
from tools import util


class ImageManager(ClassSingleton):
    """Manages image files associated with ROMs."""

    @staticmethod
    def remove_broken_images(valid_rom_paths: list[str] | list[Path]) -> None:
        """Remove images not associated with valid ROM paths."""
        valid_images: set[Path] = {
            ImageManager.get_rom_img_relpath(path) for path in valid_rom_paths
        }
        for path in IMG_PATH.rglob("*.png"):
            if path.relative_to(IMG_PATH) in valid_images:
                continue
            util.delete_file(path)
            ImageManager.get_static_logger().info(
                "Deleted broken image: %s", path
            )

    @staticmethod
    def get_rom_img_relpath(rom_path: Path | str) -> Path:
        """Get the relative image path for a given ROM path."""
        if isinstance(rom_path, str):
            rom_path = Path(rom_path)
        if util.is_relative_path(rom_path, ROM_PATH):
            rom_path = rom_path.relative_to(ROM_PATH)
        return Path(rom_path.parts[0]) / rom_path.with_suffix(".png").name
