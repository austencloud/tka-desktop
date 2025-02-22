from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.add_to_dictionary_manager.dictionary_service import (
        DictionaryService,
    )
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class AddToDictionaryUI:
    def __init__(
        self,
        sequence_workbench: "SequenceWorkbench",
        dictionary_service: "DictionaryService",
    ):
        self.sequence_workbench = sequence_workbench
        self.dictionary_service = dictionary_service

    def add_to_dictionary(self):
        seq = self.sequence_workbench.main_widget.json_manager.loader_saver.load_current_sequence()
        if self.is_sequence_invalid(seq):
            self.display_message("You must build a sequence.")
            return

        word = self.sequence_workbench.sequence_beat_frame.get.current_word()
        result = self.dictionary_service.add_variation(seq, word)

        status = result["status"]
        if status == "invalid":
            self.display_message("Invalid sequence.")
        elif status == "duplicate":
            self.display_message(f"Variation exists for '{word}'.")
        elif status == "ok":
            version = result["variation_number"]
            self.display_message(f"Variation added to '{word}' as v{version}.")
            self.update_thumbnail_box(word)
        else:
            self.display_message("Unknown error.")

    def is_sequence_invalid(self, sequence_data: List[dict]) -> bool:
        return len(sequence_data) <= 1

    def display_message(self, message: str) -> None:
        self.sequence_workbench.indicator_label.show_message(message)

    def update_thumbnail_box(self, base_word: str):
        thumbs = self.dictionary_service.collect_thumbnails(base_word)
        box = self.find_thumbnail_box(base_word)
        if box:
            box.update_thumbnails(thumbs)

    def find_thumbnail_box(self, base_word: str):
        main_widget = self.sequence_workbench.main_widget
        return main_widget.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.get(
            base_word
        )

