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

APP_ROM_DB_PATH: Path = APP_PATH / "rom_db.json"

ARCADE_NAMES_TARGET_FILE: Path = \
    Path("/mnt/SDCARD/BIOS/arcade_lists/arcade-rom-names.txt")
ARCADE_LIBRARY_NAME = "libgamename.so"
CUSTOM_ARCADE_LIBRARY_CRC = "08a1cae0"
ARCADE_LIBRARY_APP_RESOURCE = \
    RESOURCES / "naming" / f"{ARCADE_LIBRARY_NAME}.zip"
NAMES_APP_RESOURCE = RESOURCES / "naming" / "names.zip"
NAMING_DISC_KEYWORDS = {"disc", "disk", "side", "tape", "set"}
NAMING_FORMAT_KEYWORDS = {"pal", "ntsc", "secam"}
ARCADE_ID_METHOD = "file_stem"
ARCADE_NAMING_SYSTEMS = [
    "MAME2003PLUS", "FBNEO", "CPS1", "CPS2", "CPS3", "NEOGEO", "ATOMISWAVE",
    "CANNONBALL", "NAOMI", "PGM", "MAME", "MAME2010", "DAPHNE"
]
NAMING_EXCLUDE_SYSTEMS = [
    "PS", "SEGACD", "PCECD", "NEOCD", "SATURN", "DC", "PANASONIC", "PCFX",
    "SFX", "PORTS"
]

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 12

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"

ROM_DB_IGNORE_EXT = {"srm", "sav", "db", 'png'}
ROM_DB_IGNORE_WORDS = {"\u00b0"}
EMU_EXT_KEY = "extlist"
