from typing import TYPE_CHECKING

from PyQt6.QtCore import QSettings


class ConstructTabSettings:
    DEFAULT_SETTINGS = {
        "filters": {
            "continuous": False,
            "one_reversal": False,
            "two_reversals": False,
        }
    }

    def __init__(self, settings: QSettings) -> None:
        self.settings = settings

    def get_filters(self) -> dict:
        filters = {}
        for key, default_value in self.DEFAULT_SETTINGS["filters"].items():
            raw_val = self.settings.value(
                f"construct_tab/filters/{key}", str(default_value)
            ).lower()
            filters[key] = (
                raw_val == "true" if raw_val in ("true", "false") else raw_val
            )
        return filters

    def set_filters(self, filter: str):
        if not filter:
            return
        for key in self.DEFAULT_SETTINGS["filters"]:
            self.settings.setValue(f"construct_tab/filters/{key}", key == filter)
