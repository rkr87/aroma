"""
Defines constants.
"""
import os
import re
from pathlib import Path

APP_NAME = "aROMa"

TSP_LIBRARY_VAR = "LD_LIBRARY_PATH"
RUNNING_ON_TSP = TSP_LIBRARY_VAR in os.environ
APP_PATH = Path("." if RUNNING_ON_TSP else "./src")
APP_CONFIG_PATH = APP_PATH / "config.json"
RESOURCES = APP_PATH / "aroma" / "resources"
APP_LOGGING_CONFIG_PATH = RESOURCES / "config" / "logging.conf"
APP_TRANSLATION_PATH = APP_PATH / "translations"
SD_PATH = Path("/mnt/SDCARD" if RUNNING_ON_TSP else "G:")
ROM_PATH = SD_PATH / "Roms"
IMG_PATH = SD_PATH / "Imgs"
EMU_PATH = SD_PATH / "Emus"
COLLECTION_PATH = SD_PATH / "Best"
TSP_USER_LIBRARY_PATH = Path("/usr/trimui/lib")
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

APP_ROM_DB_PATH = APP_PATH / "rom_db.json"

ARCADE_NAMES_TARGET_FILE = \
    SD_PATH / "BIOS" / "arcade_lists" / "arcade-rom-names.txt"
ARCADE_LIBRARY_NAME = "libgamename.so"
CUSTOM_ARCADE_LIBRARY_CRC = "08a1cae0"
ARCADE_LIBRARY_APP_RESOURCE = \
    RESOURCES / "naming" / f"{ARCADE_LIBRARY_NAME}.zip"
NAMES_APP_RESOURCE = RESOURCES / "naming" / "names.zip"
ARCADE_ID_METHOD = "file_stem"
ARCADE_NAMING_SYSTEMS = [
    "MAME2003PLUS", "FBNEO", "CPS1", "CPS2", "CPS3", "NEOGEO", "ATOMISWAVE",
    "CANNONBALL", "NAOMI", "PGM", "MAME", "MAME2010", "DAPHNE"
]
NAMING_EXCLUDE_SYSTEMS = [
    "PS", "SEGACD", "PCECD", "NEOCD", "SATURN", "DC", "PANASONIC", "PCFX",
    "SFX", "PORTS"
]
NAMING_REGION_RESOURCE = RESOURCES / "naming" / "regions.json"
NAMING_DISC_PATTERN = \
    re.compile(r'\b(side|disk|disc|tape|set)[ \-](\w|\d{1,})\b', re.IGNORECASE)
NAMING_FORMAT_PATTERN = \
    re.compile(r'\b(pal|ntsc|secam)\b', re.IGNORECASE)
NAMING_SEARCH_PATTERN = re.compile(r'\((.*?)\)')
NAMING_REMOVE_PATTERN = re.compile(r'{[^{}]*}|\[[^][]*]|\([^()]*\)')

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 12

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"

ROM_DB_IGNORE_EXT = {"srm", "sav", "db", 'png'}
ROM_DB_IGNORE_WORDS = {"\u00b0"}
EMU_EXT_KEY = "extlist"
