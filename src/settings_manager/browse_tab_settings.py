import json
from typing import TYPE_CHECKING, Union

from main_window.main_widget.browse_tab.browse_tab_filter_controller import datetime

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class BrowseTabSettings:
    DEFAULT_BROWSE_SETTINGS = {
        "sort_method": "sequence_length",
        "current_section": "starting_letter",
        "current_filter": {},
        # Cache settings
        "cache_mode": "High Performance",  # "High Performance", "Balanced", "Storage Efficient"
        "cache_max_size_mb": 5000,  # Default cache size in MB
        "cache_location": "",  # Empty means use default AppData location
        "preload_thumbnails": True,  # Preload thumbnails on startup
        "enable_disk_cache": True,  # Enable persistent disk caching
        "cache_quality_mode": "two_stage",  # "fast_only", "two_stage", "smooth_only"
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_sort_method(self) -> str:
        return self.settings.value(
            "browse/sort_method", self.DEFAULT_BROWSE_SETTINGS["sort_method"]
        )

    def get_date_sub_sort_method(self) -> str:
        """Returns 'year', 'month', 'day', or 'full'."""
        return self.settings.value("browse/date_sub_sort_method", "full")

    def set_date_sub_sort_method(self, sub_method: str) -> None:
        """Stores the user's sub-sorting choice for date-based sorts."""
        # sub_method should be one of: 'year', 'month', 'day', 'full'
        self.settings.setValue("browse/date_sub_sort_method", sub_method)

    def set_sort_method(self, sort_method: str) -> None:
        self.settings.setValue("browse/sort_method", sort_method)

    def get_current_filter(self) -> Union[str, dict, datetime]:
        json_string = self.settings.value("browse/current_filter", "")
        if not json_string:
            return {}
        try:
            data = json.loads(json_string)
        except (ValueError, TypeError):
            return {}

        if (
            isinstance(data, dict)
            and "__string__" in data
            and isinstance(data["__string__"], str)
        ):
            return data["__string__"]
        elif (
            isinstance(data, dict)
            and "__datetime__" in data
            and isinstance(data["__datetime__"], str)
        ):
            try:
                return datetime.fromisoformat(data["__datetime__"])
            except ValueError:
                return data
        return data

    def set_current_filter(self, filter_criteria: Union[str, dict, datetime]) -> None:
        def default_serializer(obj):
            if isinstance(obj, datetime):
                return {"__datetime__": obj.isoformat()}
            raise TypeError(f"Type {type(obj)} not serializable")

        if isinstance(filter_criteria, str):
            data = {"__string__": filter_criteria}
        elif isinstance(filter_criteria, datetime):
            data = {"__datetime__": filter_criteria.isoformat()}
        else:
            data = filter_criteria
        json_string = json.dumps(data, default=default_serializer)
        self.settings.setValue("browse/current_filter", json_string)

    def get_current_section(self) -> str:
        return self.settings.value(
            "browse/current_section",
            self.DEFAULT_BROWSE_SETTINGS["current_section"],
        )

    def set_current_section(self, section: str) -> None:
        self.settings.setValue("browse/current_section", section)

    def get_browse_left_stack_index(self) -> int:
        return self.settings.value("browse/browse_left_stack_index", 4, type=int)

    def set_browse_left_stack_index(self, index: int) -> None:
        self.settings.setValue("browse/browse_left_stack_index", index)

    def get_browse_right_stack_index(self) -> int:
        return self.settings.value("browse/browse_right_stack_index", 6, type=int)

    def set_browse_right_stack_index(self, index: int) -> None:
        self.settings.setValue("browse/browse_right_stack_index", index)

    def get_selected_sequence(self) -> dict:
        json_string = self.settings.value("browse/selected_sequence", "{}")
        try:
            data = json.loads(json_string)
        except (ValueError, TypeError):
            return {}
        return data

    def set_selected_sequence(self, data: dict) -> None:
        json_string = json.dumps(data, ensure_ascii=False).encode("utf8").decode()
        self.settings.setValue("browse/selected_sequence", json_string)

    def get_browse_ratio(self) -> float:
        return self.settings.value("browse/browse_ratio", 0.6667, type=float)

    def set_browse_ratio(self, ratio: float) -> None:
        self.settings.setValue("browse/browse_ratio", ratio)

    # Cache settings getters and setters
    def get_cache_mode(self) -> str:
        """Get cache mode: 'High Performance', 'Balanced', or 'Storage Efficient'."""
        return self.settings.value(
            "browse/cache_mode", self.DEFAULT_BROWSE_SETTINGS["cache_mode"]
        )

    def set_cache_mode(self, mode: str):
        """Set cache mode and update cache size accordingly."""
        self.settings.setValue("browse/cache_mode", mode)
        # Update cache size based on mode
        size_map = {"High Performance": 1000, "Balanced": 500, "Storage Efficient": 100}
        if mode in size_map:
            self.set_cache_max_size_mb(size_map[mode])

    def get_cache_max_size_mb(self) -> int:
        """Get maximum cache size in MB."""
        return int(
            self.settings.value(
                "browse/cache_max_size_mb",
                self.DEFAULT_BROWSE_SETTINGS["cache_max_size_mb"],
            )
        )

    def set_cache_max_size_mb(self, size_mb: int):
        """Set maximum cache size in MB."""
        self.settings.setValue("browse/cache_max_size_mb", size_mb)

    def get_cache_location(self) -> str:
        """Get cache directory location. Empty string means use default."""
        return self.settings.value(
            "browse/cache_location", self.DEFAULT_BROWSE_SETTINGS["cache_location"]
        )

    def set_cache_location(self, location: str):
        """Set cache directory location."""
        self.settings.setValue("browse/cache_location", location)

    def get_preload_thumbnails(self) -> bool:
        """Get whether to preload thumbnails on startup."""
        return self.settings.value(
            "browse/preload_thumbnails",
            self.DEFAULT_BROWSE_SETTINGS["preload_thumbnails"],
            type=bool,
        )

    def set_preload_thumbnails(self, enabled: bool):
        """Set whether to preload thumbnails on startup."""
        self.settings.setValue("browse/preload_thumbnails", enabled)

    def get_enable_disk_cache(self) -> bool:
        """Get whether disk caching is enabled."""
        return self.settings.value(
            "browse/enable_disk_cache",
            self.DEFAULT_BROWSE_SETTINGS["enable_disk_cache"],
            type=bool,
        )

    def set_enable_disk_cache(self, enabled: bool):
        """Set whether disk caching is enabled."""
        self.settings.setValue("browse/enable_disk_cache", enabled)

    def get_cache_quality_mode(self) -> str:
        """Get cache quality mode: 'fast_only', 'two_stage', or 'smooth_only'."""
        return self.settings.value(
            "browse/cache_quality_mode",
            self.DEFAULT_BROWSE_SETTINGS["cache_quality_mode"],
        )

    def set_cache_quality_mode(self, mode: str):
        """Set cache quality mode."""
        self.settings.setValue("browse/cache_quality_mode", mode)

    def get_thumbnail_processing_settings(self) -> dict:
        """Get thumbnail processing settings for ultra-high quality rendering."""
        return {
            "scaling_algorithm": "smooth",  # smooth, fast, or ultra
            "multi_step_scaling": True,
            "intermediate_scale_factor": 0.7,
            "sharpening_enabled": self.get_sharpening_enabled(),  # Use actual user setting
            "enhancement_enabled": self.get_enhancement_enabled(),  # Use actual user setting
            "ultra_quality_enabled": self.get_ultra_quality_enabled(),  # Use actual user setting
            "quality_priority": "high",  # high, balanced, or fast
            "cache_high_quality": True,
            "cache_quality_mode": self.get_cache_quality_mode(),  # Use actual user setting
            "enable_disk_cache": self.get_enable_disk_cache(),  # Use actual user setting
            "max_source_resolution": 4096,  # Maximum source image resolution
            "target_dpi": 96,  # Target DPI for display
        }

    # In browse_tab_settings.py

    def get_ultra_quality_enabled(self) -> bool:
        return self.settings.value("browse/ultra_quality_enabled", True, type=bool)

    def set_ultra_quality_enabled(self, enabled: bool) -> None:
        self.settings.setValue("browse/ultra_quality_enabled", enabled)

    def get_sharpening_enabled(self) -> bool:
        return self.settings.value("browse/sharpening_enabled", True, type=bool)

    def set_sharpening_enabled(self, enabled: bool) -> None:
        self.settings.setValue("browse/sharpening_enabled", enabled)

    def get_enhancement_enabled(self) -> bool:
        return self.settings.value("browse/enhancement_enabled", True, type=bool)

    def set_enhancement_enabled(self, enabled: bool) -> None:
        self.settings.setValue("browse/enhancement_enabled", enabled)
