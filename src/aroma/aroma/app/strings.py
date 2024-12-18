# pylint: disable=too-many-arguments
"""Module for handling string translation."""

from dataclasses import dataclass, field

from shared.classes.json_dataclass import JsonDataClass
from shared.constants import (
    NAMING_ADDITIONAL_ID,
    NAMING_DISC_ID,
    NAMING_FORMAT_ID,
    NAMING_HACK_ID,
    NAMING_NAME_ID,
    NAMING_REGION_ID,
    NAMING_TITLE_ID,
    NAMING_VERSION_ID,
    NAMING_YEAR_ID,
)


@dataclass
class Strings(JsonDataClass):  # pylint: disable=too-many-instance-attributes
    """Singleton class for managing various string translation."""

    yes: str = ""
    no: str = ""
    stock: str = ""
    custom: str = ""
    rom_naming: str = ""
    rom_naming_desc: list[str] = field(default_factory=list)
    downloader: str = ""
    downloader_desc: str = ""
    archive_user: str = ""
    archive_user_desc: list[str] = field(default_factory=list)
    archive_user_prompt: str = ""
    archive_password: str = ""
    archive_password_desc: list[str] = field(default_factory=list)
    archive_password_prompt: str = ""
    refresh_roms: str = ""
    refresh_roms_desc: list[str] = field(default_factory=list)
    console_naming: str = ""
    console_naming_desc: list[str] = field(default_factory=list)
    naming_title_desc: str = ""
    naming_name_desc: str = ""
    naming_region_desc: str = ""
    naming_disc_desc: str = ""
    naming_format_desc: str = ""
    naming_hack_desc: str = ""
    naming_version_desc: str = ""
    naming_year_desc: str = ""
    naming_additional_desc: str = ""
    name_format: str = ""
    name_format_desc: list[str] = field(default_factory=list)
    name_format_prompt: str = ""
    options: str = ""
    options_desc: list[str] = field(default_factory=list)
    logging_level: str = ""
    logging_desc: list[str] = field(default_factory=list)
    logging_debug: str = ""
    logging_info: str = ""
    logging_warning: str = ""
    logging_error: str = ""
    language: str = ""
    language_desc: list[str] = field(default_factory=list)
    image_management: str = ""
    image_management_desc: list[str] = field(default_factory=list)
    remove_broken: str = ""
    remove_broken_desc: list[str] = field(default_factory=list)
    remove_broken_refresh: str = ""
    remove_broken_refresh_desc: list[str] = field(default_factory=list)
    scrape_missing: str = ""
    scrape_missing_desc: list[str] = field(default_factory=list)
    scrape_missing_refresh: str = ""
    scrape_missing_refresh_desc: list[str] = field(default_factory=list)
    scrape_days_to_retry: str = ""
    scrape_days_to_retry_desc: list[str] = field(default_factory=list)
    scrape_days_to_retry_never: str = ""
    scrape_days_to_retry_always: str = ""
    scrape_days_to_retry_days: str = ""
    scrape_media_type: str = ""
    scrape_media_type_desc: list[str] = field(default_factory=list)
    scrape_max_cpu_threads: str = ""
    scrape_max_cpu_threads_desc: list[str] = field(default_factory=list)
    scrape_user: str = ""
    scrape_user_desc: list[str] = field(default_factory=list)
    scrape_user_prompt: str = ""
    scrape_password: str = ""
    scrape_password_desc: list[str] = field(default_factory=list)
    scrape_password_prompt: str = ""
    scrape_preferred_region: str = ""
    scrape_preferred_region_desc: list[str] = field(default_factory=list)
    scrape_region_ae: str = ""
    scrape_region_afr: str = ""
    scrape_region_ame: str = ""
    scrape_region_asi: str = ""
    scrape_region_au: str = ""
    scrape_region_bg: str = ""
    scrape_region_br: str = ""
    scrape_region_ca: str = ""
    scrape_region_cl: str = ""
    scrape_region_cn: str = ""
    scrape_region_cz: str = ""
    scrape_region_de: str = ""
    scrape_region_dk: str = ""
    scrape_region_eu: str = ""
    scrape_region_fi: str = ""
    scrape_region_fr: str = ""
    scrape_region_gr: str = ""
    scrape_region_hu: str = ""
    scrape_region_il: str = ""
    scrape_region_it: str = ""
    scrape_region_jp: str = ""
    scrape_region_kr: str = ""
    scrape_region_kw: str = ""
    scrape_region_mex: str = ""
    scrape_region_mor: str = ""
    scrape_region_nl: str = ""
    scrape_region_no: str = ""
    scrape_region_nz: str = ""
    scrape_region_oce: str = ""
    scrape_region_pe: str = ""
    scrape_region_pl: str = ""
    scrape_region_pt: str = ""
    scrape_region_ru: str = ""
    scrape_region_se: str = ""
    scrape_region_sk: str = ""
    scrape_region_sp: str = ""
    scrape_region_ss: str = ""
    scrape_region_tr: str = ""
    scrape_region_tw: str = ""
    scrape_region_uk: str = ""
    scrape_region_us: str = ""
    scrape_region_wor: str = ""
    scrape_region_za: str = ""
    emu_management: str = ""
    emu_management_desc: list[str] = field(default_factory=list)
    clean_emus: str = ""
    clean_emus_desc: list[str] = field(default_factory=list)
    add_launch_menus: str = ""
    add_launch_menus_desc: list[str] = field(default_factory=list)
    remove_launch_menus: str = ""
    remove_launch_menus_desc: list[str] = field(default_factory=list)
    restore_launch_scripts: str = ""
    restore_launch_scripts_desc: list[str] = field(default_factory=list)
    clean_emus_refresh: str = ""
    clean_emus_refresh_desc: list[str] = field(default_factory=list)
    default_emu: str = ""
    default_emu_desc: list[str] = field(default_factory=list)
    cpu_governor_on_demand: str = ""
    cpu_governor_performance: str = ""
    cpu_governor_conservative: str = ""
    cpu_governor_powersave: str = ""
    cpu_governor_userspace: str = ""
    cpu_governor_schedutil: str = ""
    cpu_governor_interactive: str = ""
    cpu_governor: str = ""
    cpu_governor_desc: list[str] = field(default_factory=list)
    cpu_min_frequency: str = ""
    cpu_min_frequency_desc: list[str] = field(default_factory=list)
    cpu_max_frequency: str = ""
    cpu_max_frequency_desc: list[str] = field(default_factory=list)
    cpu_cores: str = ""
    cpu_cores_desc: list[str] = field(default_factory=list)
    cpu_profile: str = ""
    cpu_profile_desc: list[str] = field(default_factory=list)
    cpu_profile_balanced: str = ""
    cpu_profile_powersave: str = ""
    cpu_profile_performance: str = ""
    none_set: str = ""
    current: str = ""
    formatted: str = ""
    downloading_file: str = ""
    cleaning_emus: str = ""
    scraping_imgs: str = ""
    removing_broken_imgs: str = ""
    refreshing_roms: str = ""
    launch_rom: str = ""
    rom: str = ""
    emu: str = ""
    keyboard_input_history: str = ""
    keyboard_help_info: str = ""

    @property
    def _format_mapping(self) -> dict[str, str]:
        """TODO."""
        return {
            NAMING_TITLE_ID: self.naming_title_desc,
            NAMING_NAME_ID: self.naming_name_desc,
            NAMING_REGION_ID: self.naming_region_desc,
            NAMING_DISC_ID: self.naming_disc_desc,
            NAMING_FORMAT_ID: self.naming_format_desc,
            NAMING_HACK_ID: self.naming_hack_desc,
            NAMING_VERSION_ID: self.naming_version_desc,
            NAMING_YEAR_ID: self.naming_year_desc,
            NAMING_ADDITIONAL_ID: self.naming_additional_desc,
        }

    def get_format_mapping(self, join_str: str = "=") -> list[str]:
        """TODO."""
        return [join_str.join(pair) for pair in self._format_mapping.items()]

    def get_mapped_name_format(
        self, unformatted: str, *, include_prefix: bool = False
    ) -> str:
        """TODO."""
        formatted = unformatted.lower()
        for k, v in self._format_mapping.items():
            formatted = formatted.replace(k, v)
        return (
            f"{self.formatted}: {formatted}" if include_prefix else formatted
        )
