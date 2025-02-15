from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class BrowseTabSettings:
    DEFAULT_BROWSE_SETTINGS = {
        "sort_method": "sequence_length",
        "current_section": "starting_letter",
        "current_filter": {},
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  

    def get_sort_method(self) -> str:
        return self.settings.value(
            "browse/sort_method", self.DEFAULT_BROWSE_SETTINGS["sort_method"]
        )

    def set_sort_method(self, sort_method: str) -> None:
        self.settings.setValue("browse/sort_method", sort_method)

    def get_current_filter(self) -> dict:
        return self.settings.value(
            "browse/current_filter",
            self.DEFAULT_BROWSE_SETTINGS["current_filter"],
            type=dict,
        )

    def set_current_filter(self, current_filter: dict) -> None:
        self.settings.setValue("browse/current_filter", current_filter)

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
        """
        Return a small browse indicating which word was selected,
        which variation index, etc.
        For example: {"word": "Foobar", "variation_index": 2}
        """
        return self.settings.value("browse/selected_sequence", {}, type=dict)

    def set_selected_sequence(self, data: dict) -> None:
        self.settings.setValue("browse/selected_sequence", data)

    def get_browse_ratio(self) -> float:
        return self.settings.value("browse/browse_ratio", 0.6667, type=float)

    def set_browse_ratio(self, ratio: float) -> None:
        self.settings.setValue("browse/browse_ratio", ratio)
