"""Manages image files associated with ROMs."""

import asyncio
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from classes.base.class_singleton import ClassSingleton
from constants import (
    ARCADE_NAMING_SYSTEMS,
    CONSOLE_ID_METHOD,
    IMG_PATH,
    ROM_PATH,
    SCRAPER_LOG_RESOURCE,
    SCRAPER_REGION_TREE,
    SCRAPER_SYSTEM_MAP,
)
from data.screen_scraper_api import ScreenScraperAPI
from model.app_config import AppConfig
from model.media_item import MediaItem
from model.rom_detail import RomDetail
from tools import util

if TYPE_CHECKING:
    from collections.abc import Awaitable


class ImageManager(ClassSingleton):
    """Manages image files associated with ROMs."""

    RATE_LIMIT = 50
    CONNECTION_LIMIT = 50

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

    @staticmethod
    def _get_unscraped_image_paths(
        rom_db: dict[str, RomDetail],
    ) -> dict[Path, RomDetail]:
        """Get paths of images that have not been scraped."""
        return {
            img_path: rom
            for path, rom in rom_db.items()
            if (img_path := ImageManager.get_rom_img_relpath(path))
            and not (IMG_PATH / img_path).is_file()
        }

    @staticmethod
    def _check_last_scraped(rom_last_scrape: int | None) -> bool:
        """Check last scrape date is valid based on the attempt interval."""
        if rom_last_scrape is None:
            return True
        if (days := AppConfig().days_until_scrape_attempt) < 0:
            return False
        return rom_last_scrape <= util.get_datestamp() - days

    @staticmethod
    async def _download_image(
        url: str, save_path: Path, executor: ThreadPoolExecutor
    ) -> None:
        """Download the image asynchronously using urllib."""
        save_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            await asyncio.get_running_loop().run_in_executor(
                executor,
                lambda: urllib.request.urlretrieve(url, save_path),
            )
        except (urllib.error.URLError, FileNotFoundError) as e:
            ImageManager.get_static_logger().error(
                "Error downloading image from %s: %s", url, str(e)
            )

    @staticmethod
    async def _fetch_image_data(
        scraper: ScreenScraperAPI,
        path: Path,
        rom: RomDetail,
        region_priority: dict[str, int],
        executor: ThreadPoolExecutor,
    ) -> list[MediaItem] | None:
        """Fetch image data for the given ROM asynchronously."""
        system_id = SCRAPER_SYSTEM_MAP.get(system := path.parts[0], None)
        result: list[MediaItem] | None = None

        if rom.id_method == CONSOLE_ID_METHOD:
            result = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: scraper.get_game_media_by_crc(rom.id, region_priority),
            )
        if not result and system in ARCADE_NAMING_SYSTEMS:
            result = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: scraper.get_game_media_by_name(
                    path.with_suffix(".zip").name, system_id, region_priority
                ),
            )
        if not result:
            result = await asyncio.get_event_loop().run_in_executor(
                executor,
                lambda: scraper.get_game_media_by_name(
                    rom.name_url_encoded, system_id, region_priority
                ),
            )
        return result

    @staticmethod
    async def _scrape_image(
        path: Path,
        rom: RomDetail,
        region_priority: dict[str, int],
        semaphore: asyncio.Semaphore,
        executor: ThreadPoolExecutor,
    ) -> tuple[Path, bool]:
        """Scrape an image associated with a given ROM asynchronously."""
        async with semaphore:
            await asyncio.sleep(1 / ImageManager.RATE_LIMIT)
            scraper = ScreenScraperAPI()
            result = await ImageManager._fetch_image_data(
                scraper, path, rom, region_priority, executor
            )
            if result:
                await ImageManager._download_image(
                    result[0].url, IMG_PATH / path, executor
                )
                return path, (IMG_PATH / path).is_file()
            return path, False

    @staticmethod
    async def _scrape_missing_images(rom_db: dict[str, RomDetail]) -> None:
        """Scrape missing images for ROMs in the database asynchronously."""
        missing = ImageManager._get_unscraped_image_paths(rom_db)
        scraper_log = ImageManager._load_scraper_log(missing)

        region_priority = {
            region: i
            for i, region in enumerate(
                SCRAPER_REGION_TREE[AppConfig().scrape_preferred_region]
            )
        }
        semaphore = asyncio.Semaphore(ImageManager.CONNECTION_LIMIT)
        tasks: list[Awaitable[tuple[Path, bool]]] = []
        with ThreadPoolExecutor(
            max_workers=AppConfig().scrape_cpu_threads
        ) as executor:
            for path, rom in missing.items():
                if not ImageManager._check_last_scraped(scraper_log.get(path)):
                    ImageManager.get_static_logger().info(
                        "Skip Scrape: %s", path
                    )
                    continue
                tasks.append(
                    ImageManager._scrape_image(
                        path, rom, region_priority, semaphore, executor
                    )
                )
            results = await asyncio.gather(*tasks)
        await ImageManager._handle_scraping_results(results, scraper_log)

    @staticmethod
    def _load_scraper_log(missing: dict[Path, RomDetail]) -> dict[Path, int]:
        """Load the scraper log for the missing images."""
        return {
            path: v
            for k, v in util.load_simple_json(SCRAPER_LOG_RESOURCE).items()
            if (path := Path(k)) in missing
        }

    @staticmethod
    async def _handle_scraping_results(
        results: list[tuple[Path, bool]], scraper_log: dict[Path, int]
    ) -> None:
        """Handle the results of the scraping operations."""
        for path, success in results:
            if not success:
                scraper_log[path] = util.get_datestamp()
                continue
            with suppress(KeyError):
                scraper_log.pop(path)
        util.save_simple_json(scraper_log, SCRAPER_LOG_RESOURCE)

    @staticmethod
    def scrape_images(rom_db: dict[str, RomDetail]) -> None:
        """Call this function to scrape images."""
        asyncio.run(ImageManager._scrape_missing_images(rom_db))
