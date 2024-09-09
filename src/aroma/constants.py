"""
Defines constants.
"""
import os

TSP_LIBRARY_VAR: str = "LD_LIBRARY_PATH"
PATH_PREFIX: str = "." if TSP_LIBRARY_VAR in os.environ else "./src"
RESOURCES: str = f"{PATH_PREFIX}/aroma/resources"
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720

PRIMARY_COLOR = (217, 217, 217)
SECONDARY_COLOR = (23, 147, 209)
BG_COLOR = (16, 16, 16)
