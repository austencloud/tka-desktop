from typing import Dict, List, Any
from src.core.interfaces.tab_settings_interfaces import (
    IUserProfileService,
    IPropTypeService,
    IVisibilityService,
    IBeatLayoutService,
    IImageExportService,
    PropType,
)
from src.core.interfaces.settings_interfaces import ISettingsService


class UserProfileService(IUserProfileService):
    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_current_user(self) -> str:
        return self.settings.get_setting("user_profile/current_user", "Default User")

    def set_current_user(self, user: str) -> None:
        self.settings.set_setting("user_profile/current_user", user)

    def get_all_users(self) -> List[str]:
        users = self.settings.get_setting("user_profile/all_users", ["Default User"])
        return users if isinstance(users, list) else ["Default User"]


class PropTypeService(IPropTypeService):
    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_current_prop_type(self) -> PropType:
        prop_str = self.settings.get_setting("prop_type/current", "STAFF")
        try:
            return PropType(prop_str)
        except ValueError:
            return PropType.STAFF

    def set_prop_type(self, prop_type: PropType) -> None:
        self.settings.set_setting("prop_type/current", prop_type.value)

    def get_available_prop_types(self) -> List[PropType]:
        return list(PropType)


class VisibilityService(IVisibilityService):
    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service
        self._default_glyphs = {
            "TKA": True,
            "Reversals": True,
            "VTG": True,
            "Elemental": True,
            "Positions": True,
            "Non-radial_points": True,
        }

    def get_glyph_visibility(self, glyph_name: str) -> bool:
        default = self._default_glyphs.get(glyph_name, True)
        return self.settings.get_setting(f"visibility/glyph_{glyph_name}", default)

    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        self.settings.set_setting(f"visibility/glyph_{glyph_name}", visible)

    def get_motion_visibility(self, color: str) -> bool:
        return self.settings.get_setting(f"visibility/motion_{color}", True)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        self.settings.set_setting(f"visibility/motion_{color}", visible)


class BeatLayoutService(IBeatLayoutService):
    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service
        self._default_layouts = {4: (2, 2), 8: (2, 4), 16: (4, 4), 32: (8, 4)}

    def get_layout_for_length(self, length: int) -> tuple[int, int]:
        saved = self.settings.get_setting(f"beat_layout/length_{length}")
        if saved and isinstance(saved, (list, tuple)) and len(saved) == 2:
            return tuple(saved)
        return self._default_layouts.get(length, (4, 4))

    def set_layout_for_length(self, length: int, rows: int, cols: int) -> None:
        self.settings.set_setting(f"beat_layout/length_{length}", [rows, cols])


class ImageExportService(IImageExportService):
    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service
        self._default_options = {
            "include_start_position": True,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "add_user_info": True,
            "add_word": True,
            "add_difficulty_level": True,
            "combined_grids": False,
            "use_last_save_directory": True,
        }

    def get_export_option(self, option: str) -> Any:
        default = self._default_options.get(option, False)
        return self.settings.get_setting(f"image_export/{option}", default)

    def set_export_option(self, option: str, value: Any) -> None:
        self.settings.set_setting(f"image_export/{option}", value)

    def get_all_export_options(self) -> Dict[str, Any]:
        return {key: self.get_export_option(key) for key in self._default_options}
