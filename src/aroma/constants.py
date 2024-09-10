"""
Defines constants.
"""
import os

APP_NAME: str = "aROMa"

TSP_LIBRARY_VAR: str = "LD_LIBRARY_PATH"
RUNNING_ON_TSP: bool = TSP_LIBRARY_VAR in os.environ
PATH_PREFIX: str = "." if RUNNING_ON_TSP else "./src"
RESOURCES: str = f"{PATH_PREFIX}/aroma/resources"
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
