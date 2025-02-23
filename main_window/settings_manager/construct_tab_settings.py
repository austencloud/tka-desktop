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

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings

    def get_filters(self) -> dict:
        default_filters = self.DEFAULT_SETTINGS["filters"].copy()
        result = {}

        for key, default_value in default_filters.items():
            raw_val = self.settings.value(f"construct_tab/filters/{key}", str(default_value))
            if raw_val.lower() == "true":
                result[key] = True
            elif raw_val.lower() == "false":
                result[key] = False
            else:
                result[key] = raw_val

        return result


    def set_filters(self, filter: str):
        if filter == None:
            return
        self.settings.setValue(f"construct_tab/filters/{filter}", True)
        for key in self.DEFAULT_SETTINGS["filters"]:
            if key != filter:
                self.settings.setValue(f"construct_tab/filters/{key}", False)
