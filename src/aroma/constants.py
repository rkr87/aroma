"""
Defines constants.
"""
import os

APP_NAME: str = "aROMa"

TSP_LIBRARY_VAR: str = "LD_LIBRARY_PATH"
RUNNING_ON_TSP: bool = TSP_LIBRARY_VAR in os.environ
APP_PATH: str = "." if RUNNING_ON_TSP else "./src"
RESOURCES: str = f"{APP_PATH}/aroma/resources"
SD_PATH: str = "/" if RUNNING_ON_TSP else "E:/emulation/Games/"
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
MAX_ITEMS_PER_PAGE = 12

STOCK_STR = "STOCK"
CUSTOM_STR = "CUSTOM"
