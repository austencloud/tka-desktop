from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class WriteTabSettings:
    DEFAULT_act_tab_SETTINGS = {
        "act_title": "Untitled Act",
        "last_saved_act": None,
    }

    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def save_act_title(self, title: str) -> None:
        """Save the current act's title."""
        self.settings.setValue("act_sheet/act_title", title)

    def get_act_title(self) -> str:
        """Retrieve the saved act title with a default fallback."""
        return self.settings.value(
            "act_sheet/act_title", self.DEFAULT_act_tab_SETTINGS["act_title"]
        )

    def save_last_act(self, act_data: dict) -> None:
        """Save the most recent act data."""
        self.settings.setValue("act_tab/last_saved_act", act_data)

    def load_last_act(self) -> dict:
        """Load the most recent act data with None as the default."""
        return self.settings.value("act_tab/last_saved_act", None, type=dict)
