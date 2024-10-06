"""Defines constants."""

import os
import re
from pathlib import Path

from enums.cpu_governor import CPUGovernor
from model.cpu_profile import CPUProfile

APP_NAME = "aROMa"

TSP_LIBRARY_VAR = "LD_LIBRARY_PATH"
RUNNING_ON_TSP = TSP_LIBRARY_VAR in os.environ
APP_PATH = Path("." if RUNNING_ON_TSP else "./src/aroma")
APP_CONFIG_PATH = APP_PATH / "config.json"
RESOURCES = APP_PATH / "aroma" / "resources"
APP_LOGGING_CONFIG_PATH = RESOURCES / "config" / "logging.conf"
APP_TRANSLATION_PATH = APP_PATH / "translations"
DOWNLOADER_PATH = RESOURCES / "downloader"
ARCHIVE_AUTH_CONFIG = DOWNLOADER_PATH / "session.json"
SD_PATH = Path("/mnt/SDCARD" if RUNNING_ON_TSP else "G:\\")
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

SCRAPER_LOG_RESOURCE = RESOURCES / "scraping" / "scraper_log.json"
SCRAPER_MAX_WIDTH = 400
SCRAPER_MAX_HEIGHT = 580
SCRAPER_MEDIA_TYPES = [
    "box-2D",
    "box-3D",
    "mixrbv1",
    "mixrbv2",
    "screenmarqueesmall",
    "ss",
    "sstitle",
    "wheel",
]
SCRAPER_REGION_TREE = {
    "ae": ["ae", "mor", "wor", "us", "ame", "uk", "ss"],
    "afr": ["afr", "wor", "us", "ame", "uk", "ss"],
    "ame": ["ame", "wor", "us", "uk", "eu"],
    "asi": ["asi", "wor", "us", "ame", "uk", "eu", "ss"],
    "au": ["au", "oce", "wor", "us", "ame", "uk", "ss"],
    "bg": ["bg", "eu", "wor", "us", "ame", "uk", "ss"],
    "br": ["br", "ame", "wor", "pt", "eu", "us", "uk", "ss"],
    "ca": ["ca", "ame", "wor", "us", "uk", "eu", "ss"],
    "cl": ["cl", "ame", "wor", "us", "uk", "ss"],
    "cn": ["cn", "asi", "wor", "us", "ame", "uk", "ss"],
    "cz": ["cz", "eu", "wor", "us", "ame", "uk", "ss"],
    "de": ["de", "eu", "wor", "us", "ame", "uk", "ss"],
    "dk": ["dk", "eu", "wor", "us", "ame", "uk", "ss"],
    "eu": ["eu", "wor", "us", "ame", "uk", "ss"],
    "fi": ["fi", "eu", "wor", "us", "ame", "uk", "ss"],
    "fr": ["fr", "eu", "wor", "us", "ame", "uk", "ss"],
    "gr": ["gr", "eu", "wor", "us", "ame", "uk", "ss"],
    "hu": ["hu", "eu", "wor", "us", "ame", "uk", "ss"],
    "il": ["il", "mor", "wor", "us", "ame", "uk", "ss"],
    "it": ["it", "eu", "wor", "us", "ame", "uk", "ss"],
    "jp": ["jp", "asi", "wor", "us", "ame", "uk", "ss"],
    "kr": ["kr", "asi", "wor", "us", "ame", "uk", "ss"],
    "kw": ["kw", "mor", "wor", "us", "ame", "uk", "ss"],
    "mex": ["mex", "ame", "wor", "es", "eu", "us", "uk", "ss"],
    "mor": ["mor", "wor", "us", "ame", "uk", "ss"],
    "nl": ["nl", "eu", "wor", "us", "ame", "uk", "ss"],
    "no": ["no", "eu", "wor", "us", "ame", "uk", "ss"],
    "nz": ["nz", "oce", "wor", "us", "ame", "uk", "ss"],
    "oce": ["oce", "wor", "us", "ame", "uk", "ss"],
    "pe": ["pe", "ame", "wor", "us", "uk", "ss"],
    "pl": ["pl", "eu", "wor", "us", "ame", "uk", "ss"],
    "pt": ["pt", "eu", "wor", "br", "us", "ame", "uk", "ss"],
    "ru": ["ru", "wor", "us", "ame", "uk", "ss"],
    "se": ["se", "eu", "wor", "us", "ame", "uk", "ss"],
    "sk": ["sk", "eu", "wor", "us", "ame", "uk", "ss"],
    "sp": ["sp", "eu", "wor", "mex", "us", "ame", "uk", "ss"],
    "ss": ["ss", "wor", "us", "ame", "uk"],
    "tr": ["tr", "mor", "wor", "us", "ame", "uk", "ss"],
    "tw": ["tw", "asi", "wor", "us", "ame", "uk", "ss"],
    "uk": ["uk", "eu", "wor", "us", "ame", "ss"],
    "us": ["us", "ame", "wor", "uk", "eu", "ss"],
    "wor": ["wor", "us", "ame", "uk", "ss"],
    "za": ["za", "afr", "wor", "us", "ame", "uk", "ss"],
}
SCRAPER_SYSTEM_MAP = {
    "ADVMAME": "75",
    "AMIGA": "64",
    "AMIGACD": "134",
    "AMIGACDTV": "129",
    "ARCADE": "75",
    "ARDUBOY": "263",
    "ATARI2600": "26",
    "ATARIST": "42",
    "ATOMISWAVE": "53",
    "COLECO": "183",
    "COLSGM": "183",
    "C64": "66",
    "CPC": "65",
    "CPET": "240",
    "CPLUS4": "99",
    "CPS1": "6",
    "CPS2": "7",
    "CPS3": "8",
    "DAPHNE": "49",
    "DC": "23",
    "DOS": "135",
    "EASYRPG": "231",
    "EBK": "93",
    "ATARI800": "43",
    "CHANNELF": "80",
    "FBA2012": "75",
    "FBALPHA": "75",
    "FBNEO": "75",
    "FC": "3",
    "FDS": "106",
    "ATARI5200": "40",
    "GB": "9",
    "GBA": "12",
    "GBC": "10",
    "GG": "21",
    "GW": "52",
    "INTELLIVISION": "115",
    "JAGUAR": "27",
    "LOWRESNX": "244",
    "LUTRO": "206",
    "LYNX": "28",
    "MAME": "75",
    "MAME2003PLUS": "75",
    "MAME2010": "75",
    "MBA": "75",
    "MD": "1",
    "MDMSU": "1",
    "MEGADUCK": "90",
    "MS": "2",
    "MSX": "113",
    "MSX2": "116",
    "N64": "14",
    "N64DD": "122",
    "NAOMI": "56",
    "NDS": "15",
    "NEOCD": "70",
    "NEOGEO": "142",
    "NGP": "25",
    "NGC": "82",
    "ODYSSEY": "104",
    "OPENBOR": "214",
    "PALMOS": "219",
    "PANASONIC": "29",
    "PCE": "31",
    "PCECD": "114",
    "PC88": "221",
    "PCFX": "72",
    "PC98": "208",
    "PICO": "234",
    "POKEMINI": "211",
    "PORTS": "137",
    "PS": "57",
    "PSP": "61",
    "PSPMINIS": "172",
    "SATURN": "22",
    "SATELLAVIEW": "107",
    "SCUMMVM": "123",
    "SEGACD": "20",
    "SG1000": "109",
    "ATARI7800": "41",
    "SFC": "4",
    "SFCMSU": "4",
    "SGB": "127",
    "SFX": "105",
    "SUFAMI": "108",
    "SUPERVISION": "207",
    "SEGA32X": "19",
    "THOMSON": "141",
    "TIC": "222",
    "UZEBOX": "216",
    "VB": "11",
    "VECTREX": "102",
    "VIC20": "73",
    "VIDEOPAC": "104",
    "VMU": "23",
    "WS": "45",
    "X68000": "79",
    "X1": "220",
    "ZXEIGHTYONE": "77",
    "ZXS": "76",
}

NON_CONFIGURABLE_SYSTEM_PREFIX = ["PORTS", "_"]

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
INACTIVE_COLOR = (90, 90, 90)
INACTIVE_SEL = (150, 150, 150)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 14

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"

ROM_DB_IGNORE_EXT = {"srm", "sav", "db", "png"}
ROM_DB_IGNORE_WORDS = {"\u00b0"}
EMU_EXT_KEY = "extlist"


MAX_CPU_FREQ = 2010001
MIN_CPU_FREQ = 268000
CPU_FREQ_STEP = 67000


CPU_PROFILES = [
    CPUProfile("CUSTOM"),
    CPUProfile(
        "BALANCED",
        CPUGovernor.ON_DEMAND,
        402000,
        1608000,
    ),
    CPUProfile(
        "POWERSAVE",
        CPUGovernor.CONSERVATIVE,
        402000,
        1608000,
    ),
    CPUProfile(
        "PERFOMANCE",
        CPUGovernor.ON_DEMAND,
        603000,
        1809000,
    ),
]
