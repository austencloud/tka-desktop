from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class ConstructTabSettings:
    DEFAULT_SETTINGS = {
        "filters": {
            "continuous": False,
            "one_reversal": False,
            "two_reversals": False,
        }
    }

    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_filters(self) -> dict:
        # Attempt to load filters setting as a dictionary
        filters = self.settings.value("builder/construct_tab/filters", None)

        # Check if filters loaded successfully; otherwise, use defaults
        if isinstance(filters, dict):
            return filters
        else:
            # Return default filters if conversion fails
            return self.DEFAULT_SETTINGS["filters"]

    def set_filters(self, filters: dict):
        self.settings.setValue("builder/construct_tab/filters", filters)
