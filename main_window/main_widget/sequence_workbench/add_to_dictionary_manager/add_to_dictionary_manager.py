import os
import re

from typing import TYPE_CHECKING

from main_window.settings_manager.global_settings.app_context import AppContext
from .structural_variation_checker import StructuralVariationChecker
from .thumbnail_generator import ThumbnailGenerator
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class AddToDictionaryManager:
    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        self.sequence_workbench = sequence_workbench
        self.dictionary_dir = get_images_and_data_path("dictionary")
        self.structural_checker = StructuralVariationChecker(self)
        self.thumbnail_generator = ThumbnailGenerator(self)

    def add_to_dictionary(self):
        current_sequence = (
            AppContext.json_manager().loader_saver.load_current_sequence()
        )
        if self.is_sequence_invalid(current_sequence):
            self.display_message(
                "You must build a sequence to add it to your dictionary."
            )
            return
        self.process_sequence(current_sequence)

    def process_sequence(self, current_sequence):
        base_word = self.sequence_workbench.sequence_beat_frame.get.current_word()
        base_path = os.path.join(self.dictionary_dir, base_word)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if self.structural_checker.check_for_structural_variation(
            current_sequence, base_word
        ):
            self.display_message(
                f"This exact structural variation for {base_word} already exists."
            )
        else:
            variation_number = self.get_next_variation_number(base_word)
            self.save_variation(current_sequence, base_word, variation_number)
            self.display_message(
                f"New variation added to '{base_word}' as version {variation_number}."
            )

    def get_next_variation_number(self, base_word):
        """Gets the next available version number for a word in the root directory."""
        base_path = os.path.join(self.dictionary_dir, base_word)
        existing_versions = []
        for file in os.listdir(base_path):
            match = re.search(r"_ver(\d+)", file)
            if match:
                existing_versions.append(int(match.group(1)))
        return max(existing_versions, default=0) + 1

    def save_variation(self, sequence, base_word, variation_number):
        """Save the new variation in the root directory for the word."""
        base_path = os.path.join(self.dictionary_dir, base_word)

        self.thumbnail_generator.generate_and_save_thumbnail(
            sequence, variation_number, base_path, dictionary= True
        )

        self.display_message(
            f"Saved new variation for '{base_word}' as version {variation_number}."
        )

        thumbnails = self.collect_thumbnails(base_word)
        thumbnail_box = self.find_thumbnail_box(base_word)
        if thumbnail_box:
            thumbnail_box.update_thumbnails(thumbnails)

    def collect_thumbnails(self, base_word):
        """Collect all thumbnails for a word in the root directory."""
        base_path = os.path.join(self.dictionary_dir, base_word)
        thumbnails = []
        for filename in os.listdir(base_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                thumbnails.append(os.path.join(base_path, filename))
        return thumbnails

    def find_thumbnail_box(self, base_word):
        return self.sequence_workbench.main_widget.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.get(
            base_word
        )

    def display_message(self, message):
        self.sequence_workbench.indicator_label.show_message(message)

    def is_sequence_invalid(self, sequence):
        return len(sequence) <= 1
