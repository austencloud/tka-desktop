from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )


class JsonLetterUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_letter_in_json_at_index(self, index: int, letter: str) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index]["letter"] = letter
        self.json_manager.loader_saver.save_current_sequence(sequence)
