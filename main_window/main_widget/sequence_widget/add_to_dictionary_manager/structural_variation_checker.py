import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .add_to_dictionary_manager import AddToDictionaryManager


class StructuralVariationChecker:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.add_to_dictionary_manager = add_to_dictionary_manager
        self.dictionary_dir = add_to_dictionary_manager.dictionary_dir
        self.metadata_extractor = (
            add_to_dictionary_manager.sequence_widget.main_widget.metadata_extractor
        )

    def check_for_structural_variation(self, current_sequence, base_word):
        base_path = os.path.join(self.dictionary_dir, base_word)
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, filename)
                    existing_sequence = (
                        self.metadata_extractor.extract_metadata_from_file(file_path)
                    )
                    if existing_sequence and self.are_structural_variations_identical(
                        current_sequence, existing_sequence
                    ):
                        return True  # Structural variation exists
        return False  # No matching structural variation found

    def are_structural_variations_identical(self, seq1, seq2):
        def structural_variation_matches(b1, b2):
            ignored_keys = ["turns", "end_ori", "start_ori"]
            for key in b1.keys():
                if key not in ignored_keys and b1[key] != b2[key]:
                    return False
            return True

        if len(seq1) != len(seq2):
            return False

        for beat1, beat2 in zip(seq1, seq2):
            for color in ["blue_attributes", "red_attributes"]:
                if color in beat1 and color in beat2:
                    if not structural_variation_matches(beat1[color], beat2[color]):
                        return False
        return True
