"""
Legacy Settings Adapter

Adapts the existing legacy settings structure to work with V2's interface-based approach.
"""

from typing import Any, Dict, Optional
from src.core.interfaces.settings_interfaces import ISettingsService
from src.core.interfaces.tab_settings_interfaces import (
    IUserProfileService,
    IPropTypeService,
    IVisibilityService,
    IBeatLayoutService,
    IImageExportService,
)


class LegacySettingsAdapter(ISettingsService):
    """Adapts legacy settings to the V2 ISettingsService interface"""

    def __init__(self):
        # Import and initialize the legacy settings manager
        try:
            import sys
            from pathlib import Path

            # Add legacy path to Python path
            legacy_path = (
                Path(__file__).parent.parent.parent.parent.parent / "legacy" / "src"
            )
            if str(legacy_path) not in sys.path:
                sys.path.insert(0, str(legacy_path))

            from legacy.src.legacy_settings_manager.legacy_settings_manager import (
                LegacySettingsManager,
            )

            self.legacy_settings = LegacySettingsManager()

        except Exception as e:
            print(f"Warning: Could not initialize legacy settings: {e}")
            self.legacy_settings = None

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value using the legacy settings manager"""
        if not self.legacy_settings:
            return default

        try:
            # Parse key format: "section/key"
            if "/" in key:
                section, setting_key = key.split("/", 1)
                return self.legacy_settings.get_setting(section, setting_key, default)
            else:
                # Try common settings locations
                return self.legacy_settings.settings.value(key, default)
        except Exception:
            return default

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value using the legacy settings manager"""
        if not self.legacy_settings:
            return

        try:
            if "/" in key:
                section, setting_key = key.split("/", 1)
                self.legacy_settings.set_setting(section, setting_key, value)
            else:
                self.legacy_settings.settings.setValue(key, value)
        except Exception as e:
            print(f"Warning: Could not set setting {key}: {e}")

    def save_settings(self) -> None:
        """Save settings to persistent storage"""
        if self.legacy_settings:
            self.legacy_settings.settings.sync()


class LegacyUserProfileService(IUserProfileService):
    """Adapts legacy user profile settings to V2 interface"""

    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_current_user(self) -> str:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.users.get_current_user()
        return self.settings.get_setting("user_profile/current_user", "")

    def set_current_user(self, username: str) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.users.set_current_user(username)
        else:
            self.settings.set_setting("user_profile/current_user", username)

    def get_user_profiles(self) -> Dict[str, Dict[str, Any]]:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.users.get_user_profiles()
        return {}

    def create_user_profile(self, username: str, data: Dict[str, Any]) -> bool:
        # For now, just set as current user
        self.set_current_user(username)
        return True

    def delete_user_profile(self, username: str) -> bool:
        # Simplified implementation
        return True


class LegacyPropTypeService(IPropTypeService):
    """Adapts legacy prop type settings to V2 interface"""

    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_prop_type(self) -> str:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            prop_type = self.settings.legacy_settings.global_settings.get_prop_type()
            return prop_type.name if hasattr(prop_type, "name") else str(prop_type)
        return self.settings.get_setting("global/prop_type", "Staff")

    def set_prop_type(self, prop_type: str) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            # Convert string to PropType enum if needed
            try:
                from enums.prop_type import PropType

                prop_enum = PropType[prop_type]
                self.settings.legacy_settings.global_settings.set_prop_type(
                    prop_enum, []
                )
            except:
                self.settings.set_setting("global/prop_type", prop_type)
        else:
            self.settings.set_setting("global/prop_type", prop_type)

    def get_available_prop_types(self) -> list[str]:
        try:
            from enums.prop_type import PropType

            return [prop.name for prop in PropType]
        except:
            return ["Staff", "Club", "Buugeng", "Fractals", "Triad", "BigBallz"]


class LegacyVisibilityService(IVisibilityService):
    """Adapts legacy visibility settings to V2 interface"""

    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.visibility.get_glyph_visibility(
                glyph_type
            )
        return self.settings.get_setting(f"visibility/{glyph_type}", True)

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.visibility.set_glyph_visibility(
                glyph_type, visible
            )
        else:
            self.settings.set_setting(f"visibility/{glyph_type}", visible)

    def get_motion_visibility(self, color: str) -> bool:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.visibility.get_motion_visibility(color)
        return self.settings.get_setting(f"visibility/{color}_motion", True)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.visibility.set_motion_visibility(
                color, visible
            )
        else:
            self.settings.set_setting(f"visibility/{color}_motion", visible)


class LegacyBeatLayoutService(IBeatLayoutService):
    """Adapts legacy beat layout settings to V2 interface"""

    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_beat_layout(self, sequence_length: int) -> tuple[int, int]:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            layout = self.settings.legacy_settings.sequence_layout.get_layout_setting(
                str(sequence_length)
            )
            return tuple(layout) if len(layout) >= 2 else (1, sequence_length)
        return (1, sequence_length)

    def set_beat_layout(self, sequence_length: int, rows: int, cols: int) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.sequence_layout.set_layout_setting(
                str(sequence_length), [rows, cols]
            )
        else:
            self.settings.set_setting(
                f"sequence_layout/{sequence_length}", f"{rows},{cols}"
            )

    def get_sequence_length(self) -> int:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.sequence_layout.get_num_beats()
        return self.settings.get_setting("sequence_layout/num_beats", 8)

    def set_sequence_length(self, length: int) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.sequence_layout.set_num_beats(length)
        else:
            self.settings.set_setting("sequence_layout/num_beats", length)


class LegacyImageExportService(IImageExportService):
    """Adapts legacy image export settings to V2 interface"""

    def __init__(self, settings_service: ISettingsService):
        self.settings = settings_service

    def get_export_option(self, option: str) -> bool:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.image_export.get_image_export_setting(
                option
            )
        return self.settings.get_setting(f"image_export/{option}", False)

    def set_export_option(self, option: str, value: bool) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.image_export.set_image_export_setting(
                option, value
            )
        else:
            self.settings.set_setting(f"image_export/{option}", value)

    def get_all_export_options(self) -> Dict[str, bool]:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return (
                self.settings.legacy_settings.image_export.get_all_image_export_options()
            )

        # Default options based on legacy
        defaults = {
            "include_start_position": False,
            "add_user_info": True,
            "add_word": True,
            "add_difficulty_level": True,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "use_last_save_directory": False,
            "combined_grids": False,
        }

        return {key: self.get_export_option(key) for key in defaults.keys()}

    def get_custom_note(self) -> str:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            return self.settings.legacy_settings.image_export.get_custom_note()
        return self.settings.get_setting("image_export/custom_note", "")

    def set_custom_note(self, note: str) -> None:
        if hasattr(self.settings, "legacy_settings") and self.settings.legacy_settings:
            self.settings.legacy_settings.image_export.set_custom_note(note)
        else:
            self.settings.set_setting("image_export/custom_note", note)
