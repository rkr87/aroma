"""TODO."""

from dataclasses import dataclass, field
from typing import TypeVar, cast

_T = TypeVar("_T", str, bool, list[str], int)


@dataclass
class CollectionConfig:  # pylint: disable = too-many-instance-attributes
    """TODO."""

    label: str
    directory: str
    is_aroma_collection: bool
    icon: str = "icon.png"
    iconsel: str = "icon_selected.png"
    background: str = "bg.png"
    themecolor: str = "1793d1"
    launch: str = "launch.sh"
    rompath: str = "./Roms"
    imgpath: str = "./Imgs"
    useswap: int = 0
    shortname: int = 0
    hidebios: int = 1
    extlist: str = "txt"
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    systems_separated: bool = True
    override_group_method: bool = False
    custom_group_method: str = ""

    @property
    def format_label(self) -> str:
        """TODO."""
        label = (
            self.label
            if self.is_aroma_collection
            else f"{self.label} (NON-AROMA)"
        )
        return label.upper()

    @staticmethod
    def from_dict(
        obj: dict[str, str | bool | list[str]], directory: str
    ) -> "CollectionConfig":
        """TODO."""

        def get_value(
            key: str,
            expected_type: type,
            default: _T,
        ) -> _T:
            """Fetch and validate a value from the dictionary."""
            if isinstance(value := obj.get(key), expected_type):
                return cast(_T, value)
            return default

        return CollectionConfig(
            label=get_value("label", str, "UNKNOWN"),
            directory=directory,
            is_aroma_collection=get_value(
                "is_aroma_collection", bool, default=False
            ),
            icon=get_value("icon", str, "icon.png"),
            iconsel=get_value("iconsel", str, "icon_selected.png"),
            background=get_value("background", str, "bg.png"),
            themecolor=get_value("themecolor", str, "1793d1"),
            include=get_value("include", list, []),
            exclude=get_value("exclude", list, []),
            imgpath=get_value("imgpath", str, "./Imgs"),
            useswap=get_value("useswap", int, 0),
            shortname=get_value("shortname", int, 0),
            hidebios=get_value("hidebios", int, 1),
            systems_separated=get_value(
                "systems_separated", bool, default=True
            ),
            override_group_method=get_value(
                "override_group_method", bool, default=False
            ),
            custom_group_method=get_value(
                "custom_group_method", str, default="$n"
            ),
        )
