from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.add_to_dictionary_manager.dictionary_service import (
        DictionaryService,
    )
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class AddToDictionaryUI:
    """
    Front-end class: ties DictionaryService results to your SequenceWorkbench UI.
    Shows pop-ups or updates the thumbnail widget.
    """

    def __init__(
        self,
        sequence_workbench: "SequenceWorkbench",
        dictionary_service: "DictionaryService",
    ):
        self.sequence_workbench = sequence_workbench
        self.dictionary_service = dictionary_service

    def add_to_dictionary(self):
        # 1. Grab the current sequence from your existing JSON manager:
        current_sequence = (
            self.sequence_workbench.main_widget.json_manager.loader_saver.load_current_sequence()
        )

        # 2. Check if it’s valid to add:
        if self.is_sequence_invalid(current_sequence):
            self.display_message(
                "You must build a sequence to add it to your dictionary."
            )
            return

        # 3. Identify the base word:
        base_word = self.sequence_workbench.sequence_beat_frame.get.current_word()

        # 4. Call the dictionary service:
        result = self.dictionary_service.add_variation(current_sequence, base_word)

        # 5. Handle the returned “status” codes:
        if result["status"] == "invalid":
            self.display_message("Invalid sequence. Please build it first.")
        elif result["status"] == "duplicate":
            self.display_message(
                f"This exact structural variation for '{base_word}' already exists."
            )
        elif result["status"] == "ok":
            version = result["variation_number"]
            self.display_message(
                f"New variation added to '{base_word}' as version {version}."
            )
            # Optionally refresh the UI “thumbnail box” for this word:
            self.update_thumbnail_box(base_word)
        else:
            self.display_message(
                "Unknown error adding to dictionary (unexpected status)."
            )

    def is_sequence_invalid(self, sequence_data: List[dict]) -> bool:
        # For example, you consider it invalid if it’s length <= 1:
        return len(sequence_data) <= 1

    def display_message(self, message: str) -> None:
        """
        Show a message in the existing 'indicator_label' or
        any other label / message box you prefer.
        """
        self.sequence_workbench.indicator_label.show_message(message)

    def update_thumbnail_box(self, base_word: str):
        """
        Re-collect thumbnails from the dictionary folder
        and refresh that UI component (thumbnail box).
        """
        thumbnails = self.dictionary_service.collect_thumbnails(base_word)
        thumbnail_box = self.find_thumbnail_box(base_word)
        if thumbnail_box is not None:
            thumbnail_box.update_thumbnails(thumbnails)

    def find_thumbnail_box(self, base_word: str):
        # Hook into your existing UI code:
        main_widget = self.sequence_workbench.main_widget
        return main_widget.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.get(
            base_word
        )
