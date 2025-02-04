from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class BrowseTabSettings:
    DEFAULT_DICTIONARY_SETTINGS = {
        "sort_method": "sequence_length",
        "current_section": "starting_letter",
        "current_filter": {},
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_sort_method(self) -> str:
        # Retrieve the sort method or use the default
        return self.settings.value(
            "dictionary/sort_method", self.DEFAULT_DICTIONARY_SETTINGS["sort_method"]
        )

    def set_sort_method(self, sort_method: str) -> None:
        # Update the sort method in QSettings
        self.settings.setValue("dictionary/sort_method", sort_method)

    def get_current_filter(self) -> dict:
        # Retrieve the current filter or use the default empty dict
        return self.settings.value(
            "dictionary/current_filter",
            self.DEFAULT_DICTIONARY_SETTINGS["current_filter"],
            type=dict,
        )

    def set_current_filter(self, current_filter: dict) -> None:
        # Update the current filter in QSettings
        self.settings.setValue("dictionary/current_filter", current_filter)

    def get_current_section(self) -> str:
        # Retrieve the current section or use the default
        return self.settings.value(
            "dictionary/current_section",
            self.DEFAULT_DICTIONARY_SETTINGS["current_section"],
        )

    def set_current_section(self, section: str) -> None:
        # Update the current section in QSettings
        self.settings.setValue("dictionary/current_section", section)
