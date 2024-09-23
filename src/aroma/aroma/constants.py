"""Defines constants."""

import os
import re
from pathlib import Path

APP_NAME = "aROMa"

TSP_LIBRARY_VAR = "LD_LIBRARY_PATH"
RUNNING_ON_TSP = TSP_LIBRARY_VAR in os.environ
APP_PATH = Path("." if RUNNING_ON_TSP else "./src/aROMa")
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

ARCADE_NAMES_TARGET_FILE = (
    SD_PATH / "BIOS" / "arcade_lists" / "arcade-rom-names.txt"
)
ARCADE_LIBRARY_NAME = "libgamename.so"
CUSTOM_ARCADE_LIBRARY_CRC = "08a1cae0"
ARCADE_LIBRARY_APP_RESOURCE = (
    RESOURCES / "naming" / f"{ARCADE_LIBRARY_NAME}.zip"
)
NAMES_APP_RESOURCE = RESOURCES / "naming" / "names.zip"
ARCADE_NAMES_DB = RESOURCES / "naming" / "arcade.db"
CONSOLE_NAMES_DB = RESOURCES / "naming" / "console.db"
ARCADE_ID_METHOD = "file_stem"
CONSOLE_ID_METHOD = "db_crc"
FILE_ID_METHOD = "file_crc"
ARCADE_NAMING_SYSTEMS = [
    "MAME2003PLUS",
    "FBNEO",
    "CPS1",
    "CPS2",
    "CPS3",
    "NEOGEO",
    "ATOMISWAVE",
    "CANNONBALL",
    "NAOMI",
    "PGM",
    "MAME",
    "MAME2010",
    "DAPHNE",
]
NAMING_EXCLUDE_SYSTEMS = [
    "PS",
    "SEGACD",
    "PCECD",
    "NEOCD",
    "SATURN",
    "DC",
    "PANASONIC",
    "PCFX",
    "SFX",
    "PORTS",
]
NAMING_REGION_RESOURCE = RESOURCES / "naming" / "regions.json"
NAMING_FORMATS_RESOURCE = RESOURCES / "naming" / "formats.json"
NAMING_DISC_PATTERN = re.compile(
    r"\b(side|disk|disc|tape|set)[ \-](\w|\d{1,})\b",
    re.IGNORECASE,
)
NAMING_FORMAT_PATTERN = re.compile(r"\b(pal|ntsc|secam)\b", re.IGNORECASE)
NAMING_SEARCH_PATTERN = re.compile(r"\((.*?)\)")
NAMING_YEAR_PATTERN = re.compile(r"\b(\d{2}[0-9x]{2})\b", re.IGNORECASE)
NAMING_REMOVE_PATTERN = re.compile(r"{[^{}]*}|\[[^][]*]|\([^()]*\)")
NAMING_VERSION_PATTERN = re.compile(
    r"\b(?!(?:\d{4}\.\d{2}\.\d{2})\b)(rev\s?\d+|v\d+[\.\d+]+)\b",
    re.IGNORECASE,
)
NAMING_TITLE_ID = "$t"
NAMING_NAME_ID = "$n"
NAMING_REGION_ID = "$r"
NAMING_DISC_ID = "$d"
NAMING_FORMAT_ID = "$f"
NAMING_HACK_ID = "$h"
NAMING_VERSION_ID = "$v"
NAMING_YEAR_ID = "$y"
NAMING_ADDITIONAL_ID = "$a"
TSP_CACHE_DB_SUFFIX = "_cache7.db"

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 12

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"

ROM_DB_IGNORE_EXT = {"srm", "sav", "db", "png"}
ROM_DB_IGNORE_WORDS = {"\u00b0"}
EMU_EXT_KEY = "extlist"
