from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class WriteTabSettings:
    DEFAULT_WRITE_TAB_SETTINGS = {
        "act_title": "Untitled Act",
        "last_saved_act": None,
    }

    def __init__(self):
        self.settings = SettingsManager()

    def save_act_title(self, title: str) -> None:
        self.settings.set_value("act_sheet/act_title", title)

    def get_act_title(self) -> str:
        return self.settings.get_value(
            "act_sheet/act_title", self.DEFAULT_WRITE_TAB_SETTINGS["act_title"]
        )

    def save_last_act(self, act_data: dict) -> None:
        self.settings.set_value("act_tab/last_saved_act", act_data)

    def load_last_act(self) -> dict:
        return self.settings.get_value("act_tab/last_saved_act", None)
