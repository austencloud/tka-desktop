# src/main_window/main_widget/sequence_card_tab/tab.py

from interfaces.settings_manager_interface import ISettingsManager


from typing import TYPE_CHECKING


class SequenceCardSettingsHandler:
    def __init__(self, settings_manager: ISettingsManager):
        self.settings_manager = settings_manager
        self.saved_column_count = 3
        self.saved_length = 16
        self._load_settings()

    def _load_settings(self):
        if self.settings_manager:
            self.saved_column_count = int(
                self.settings_manager.get_setting(
                    "sequence_card_tab", "column_count", 3
                )
            )
            self.saved_length = int(
                self.settings_manager.get_setting(
                    "sequence_card_tab", "last_length", 16
                )
            )

        self.saved_column_count = int(self.saved_column_count)
        self.saved_length = int(self.saved_length)

    def save_length(self, length: int):
        if self.settings_manager:
            self.settings_manager.set_setting(
                "sequence_card_tab", "last_length", length
            )
        self.saved_length = length

    def save_column_count(self, column_count: int):
        if self.settings_manager:
            self.settings_manager.set_setting(
                "sequence_card_tab", "column_count", column_count
            )
        self.saved_column_count = column_count
