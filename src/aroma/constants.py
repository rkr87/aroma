"""
Defines constants.
"""
import os
from pathlib import Path

APP_NAME: str = "aROMa"

TSP_LIBRARY_VAR: str = "LD_LIBRARY_PATH"
RUNNING_ON_TSP: bool = TSP_LIBRARY_VAR in os.environ
APP_PATH: Path = Path("." if RUNNING_ON_TSP else "./src")
APP_CONFIG_PATH: Path = APP_PATH / "config.json"
RESOURCES: Path = APP_PATH / "aroma" / "resources"
APP_LOGGING_CONFIG_PATH: Path = RESOURCES / "config" / "logging.conf"
APP_TRANSLATION_PATH: Path = APP_PATH / "translations"
SD_PATH: Path = Path("/mnt/SDCARD" if RUNNING_ON_TSP else "G:")
ROM_PATH: Path = SD_PATH / "Roms"
IMG_PATH: Path = SD_PATH / "Imgs"
EMU_PATH: Path = SD_PATH / "Emus"
COLLECTION_PATH: Path = SD_PATH / "Best"
TSP_USER_LIBRARY_PATH: Path = Path("/usr/trimui/lib")
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720

APP_ROM_DB_PATH: Path = APP_PATH / "test.json"

ARCADE_NAMES_TARGET_FILE: Path = \
    Path("/mnt/SDCARD/BIOS/arcade_lists/arcade-rom-names.txt")
ARCADE_LIBRARY_NAME = "libgamename.so"
CUSTOM_ARCADE_LIBRARY_CRC = "0x8a1cae0"
ARCADE_LIBRARY_APP_RESOURCE = \
    RESOURCES / "naming" / f"{ARCADE_LIBRARY_NAME}.zip"
ARCADE_NAMES_APP_RESOURCE = RESOURCES / "naming" / "names.zip"


PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 12

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"

IGNORE_EXT = {"srm", "sav", "db"}
IGNORE_WORDS = {"\u00b0"}
EMU_EXT_KEY = "extlist"
