from typing import Dict, Any, Tuple
from src.core.interfaces.tab_settings_interfaces import IImageExportService
from src.core.interfaces.core_services import IUIStateManagementService


class ImageExportService(IImageExportService):
    """Service for managing image export settings"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        self._supported_formats = ["PNG", "JPEG", "BMP", "TIFF"]
        self._quality_presets = {"Low": 25, "Medium": 50, "High": 75, "Maximum": 95}

        # Default export options
        self._default_export_options = {
            "include_start_position": False,
            "add_user_info": True,
            "add_word": True,
            "add_difficulty_level": True,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "use_last_save_directory": False,
            "combined_grids": False,
        }

    def get_export_format(self) -> str:
        """Get the current export format"""
        return self.ui_state_service.get_setting("export_format", "PNG")

    def set_export_format(self, format_name: str) -> bool:
        """Set the export format"""
        if format_name not in self._supported_formats:
            return False

        self.ui_state_service.set_setting("export_format", format_name)
        return True

    def get_supported_formats(self) -> list:
        """Get list of supported export formats"""
        return self._supported_formats.copy()

    def get_export_quality(self) -> int:
        """Get export quality (0-100)"""
        return self.ui_state_service.get_setting("export_quality", 85)

    def set_export_quality(self, quality: int) -> bool:
        """Set export quality (0-100)"""
        if not 0 <= quality <= 100:
            return False

        self.ui_state_service.set_setting("export_quality", quality)
        return True

    def get_export_dimensions(self) -> Tuple[int, int]:
        """Get export dimensions (width, height)"""
        width = self.ui_state_service.get_setting("export_width", 1920)
        height = self.ui_state_service.get_setting("export_height", 1080)
        return (width, height)

    def set_export_dimensions(self, width: int, height: int) -> bool:
        """Set export dimensions"""
        if width <= 0 or height <= 0:
            return False

        self.ui_state_service.set_setting("export_width", width)
        self.ui_state_service.set_setting("export_height", height)
        return True

    def get_include_background(self) -> bool:
        """Get whether to include background in export"""
        return self.ui_state_service.get_setting("export_include_background", True)

    def set_include_background(self, include: bool) -> None:
        """Set whether to include background in export"""
        self.ui_state_service.set_setting("export_include_background", include)

    def get_scale_factor(self) -> float:
        """Get the scale factor for export"""
        return self.ui_state_service.get_setting("export_scale_factor", 1.0)

    def set_scale_factor(self, scale: float) -> bool:
        """Set the scale factor for export"""
        if scale <= 0:
            return False

        self.ui_state_service.set_setting("export_scale_factor", scale)
        return True

    def get_quality_presets(self) -> Dict[str, int]:
        """Get available quality presets"""
        return self._quality_presets.copy()

    def apply_quality_preset(self, preset_name: str) -> bool:
        """Apply a quality preset"""
        if preset_name not in self._quality_presets:
            return False

        quality = self._quality_presets[preset_name]
        return self.set_export_quality(quality)

    def get_export_path(self) -> str:
        """Get the default export path"""
        import os

        default_path = os.path.join(os.path.expanduser("~"), "TKA_Exports")
        return self.ui_state_service.get_setting("export_path", default_path)

    def set_export_path(self, path: str) -> bool:
        """Set the default export path"""
        if not path:
            return False

        self.ui_state_service.set_setting("export_path", path)
        return True

    def get_auto_filename(self) -> bool:
        """Get whether to auto-generate filenames"""
        return self.ui_state_service.get_setting("export_auto_filename", True)

    def set_auto_filename(self, auto: bool) -> None:
        """Set whether to auto-generate filenames"""
        self.ui_state_service.set_setting("export_auto_filename", auto)

    def get_filename_template(self) -> str:
        """Get the filename template for auto-generation"""
        return self.ui_state_service.get_setting(
            "export_filename_template", "sequence_{timestamp}"
        )

    def set_filename_template(self, template: str) -> None:
        """Set the filename template for auto-generation"""
        self.ui_state_service.set_setting("export_filename_template", template)

    def get_all_export_settings(self) -> Dict[str, Any]:
        """Get all export settings as a dictionary"""
        width, height = self.get_export_dimensions()

        return {
            "format": self.get_export_format(),
            "quality": self.get_export_quality(),
            "width": width,
            "height": height,
            "include_background": self.get_include_background(),
            "scale_factor": self.get_scale_factor(),
            "export_path": self.get_export_path(),
            "auto_filename": self.get_auto_filename(),
            "filename_template": self.get_filename_template(),
        }

    def get_export_option(self, option: str) -> Any:
        """Get a specific export option"""
        default_value = self._default_export_options.get(option, False)
        return self.ui_state_service.get_setting(
            f"image_export/{option}", default_value
        )

    def set_export_option(self, option: str, value: Any) -> None:
        """Set a specific export option"""
        self.ui_state_service.set_setting(f"image_export/{option}", value)

    def get_all_export_options(self) -> Dict[str, Any]:
        """Get all export options as a dictionary"""
        return {
            key: self.get_export_option(key)
            for key in self._default_export_options.keys()
        }
