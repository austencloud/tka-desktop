import os
import json
from PIL import Image, PngImagePlugin

from main_window.main_widget.sequence_properties_manager.mirrored_color_swapped_permutation_checker import (
    MirroredColorSwappedPermutationChecker,
)
from main_window.main_widget.sequence_properties_manager.rotated_color_swapped_permutation_checker import (
    RotatedColorSwappedPermutationChecker,
)
from main_window.main_widget.sequence_properties_manager.strictly_color_swapped_permutation_checker import (
    StrictlyColorSwappedPermutationChecker,
)
from main_window.main_widget.sequence_properties_manager.strictly_mirrored_permutation_checker import (
    StrictlyMirroredPermutationChecker,
)
from main_window.main_widget.sequence_properties_manager.strictly_rotated_permutation_checker import (
    StrictlyRotatedPermutationChecker,
)
from utilities.word_simplifier import WordSimplifier
from main_window.main_widget.sequence_level_evaluator import SequenceLevelEvaluator

"""This module is responsible for updating the metadata of the images in the dictionary folder.
We are still making updates to the permutation checkers as of 8/26/2024 so please keep this around until we are done.
After finishing the permutation checkers, we will be able to update the metadata of the images in the dictionary folder correctly."""


class SequencePropertiesCheckerStandalone:

    def __init__(self, sequence):
        self.sequence = sequence[1:] if sequence else []

        # Default properties
        self.ends_at_start_pos = False
        self.is_permutable = False
        self.is_strictly_rotated_permutation = False
        self.is_strictly_mirrored_permutation = False
        self.is_strictly_colorswapped_permutation = False
        self.is_mirrored_color_swapped_permutation = False
        self.is_rotated_colorswapped_permutation = False

        # Instantiate the individual checkers
        self.rotated_checker = StrictlyRotatedPermutationChecker(self)
        self.mirrored_checker = StrictlyMirroredPermutationChecker(self)
        self.color_swapped_checker = StrictlyColorSwappedPermutationChecker(self)
        self.mirrored_color_swapped_checker = MirroredColorSwappedPermutationChecker(
            self
        )
        self.rotated_color_swapped_checker = RotatedColorSwappedPermutationChecker(self)

    def calculate_word(self) -> str:
        word = "".join(entry["letter"] for entry in self.sequence[1:])
        simplified_word = WordSimplifier.simplify_repeated_word(word)
        return simplified_word

    def check_all_properties(self):
        if not self.sequence:
            return self._default_properties()

        self.ends_at_start_pos = self._check_ends_at_start_pos()
        self.is_permutable = self._check_is_permutable()

        # Check for strictly rotated permutation first
        self.is_strictly_rotated_permutation = self.rotated_checker.check()

        if not self.is_strictly_rotated_permutation:
            # If not rotated, check for strictly mirrored permutation
            self.is_strictly_mirrored_permutation = self.mirrored_checker.check()

            if not self.is_strictly_mirrored_permutation:
                # If not mirrored, check for strictly color swapped permutation
                self.is_strictly_colorswapped_permutation = (
                    self.color_swapped_checker.check()
                )

                if not self.is_strictly_colorswapped_permutation:
                    # If not strictly color swapped, check for mirrored color swapped permutation
                    self.is_mirrored_color_swapped_permutation = (
                        self.mirrored_color_swapped_checker.check()
                    )

                    if not self.is_mirrored_color_swapped_permutation:
                        # If not mirrored color swapped, check for rotated color swapped permutation
                        self.is_rotated_colorswapped_permutation = (
                            self.rotated_color_swapped_checker.check()
                        )
                    else:
                        self.is_rotated_colorswapped_permutation = False
                else:
                    self.is_mirrored_color_swapped_permutation = False
                    self.is_rotated_colorswapped_permutation = False
            else:
                self.is_strictly_colorswapped_permutation = False
                self.is_mirrored_color_swapped_permutation = False
                self.is_rotated_colorswapped_permutation = False
        else:
            # If it's strictly rotated, all other permutations are false
            self.is_strictly_mirrored_permutation = False
            self.is_strictly_colorswapped_permutation = False
            self.is_mirrored_color_swapped_permutation = False
            self.is_rotated_colorswapped_permutation = False

        return {
            "word": self.calculate_word(),
            "author": "Austen Cloud",  # Default author or fetch from elsewhere
            "level": SequenceLevelEvaluator().get_sequence_difficulty_level(
                self.sequence
            ),
            "is_circular": self.ends_at_start_pos,
            "is_permutable": self.is_permutable,
            "is_strictly_rotated_permutation": self.is_strictly_rotated_permutation,
            "is_strictly_mirrored_permutation": self.is_strictly_mirrored_permutation,
            "is_strictly_colorswapped_permutation": self.is_strictly_colorswapped_permutation,
            "is_mirrored_color_swapped_permutation": self.is_mirrored_color_swapped_permutation,
            "is_rotated_colorswapped_permutation": self.is_rotated_colorswapped_permutation,
        }

    def _default_properties(self):
        return {
            "word": "",
            "author": "Austen Cloud",
            "level": 0,
            "is_circular": False,
            "is_permutable": False,
            "is_strictly_rotated_permutation": False,
            "is_strictly_mirrored_permutation": False,
            "is_strictly_colorswapped_permutation": False,
            "is_mirrored_color_swapped_permutation": False,
            "is_rotated_colorswapped_permutation": False,
        }

    def _check_ends_at_start_pos(self) -> bool:
        start_position = self.sequence[0]["end_pos"]
        current_position = self.sequence[-1]["end_pos"]
        return current_position == start_position

    def _check_is_permutable(self) -> bool:
        start_position = self.sequence[0]["end_pos"].rstrip("0123456789")
        current_position = self.sequence[-1]["end_pos"].rstrip("0123456789")
        return current_position == start_position


class MetadataUpdater:
    def __init__(self, dictionary_path, default_author="Austen Cloud"):
        self.dictionary_path = dictionary_path
        self.default_author = default_author

    def update_all_metadata(self):
        # Traverse through all files in the dictionary path
        for root, dirs, files in os.walk(self.dictionary_path):
            for file_name in files:
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file_name)
                    self.update_metadata_for_file(file_path)

    def update_metadata_for_file(self, file_path):
        # Extract existing metadata from the image
        metadata = self.extract_metadata_from_file(file_path)

        if metadata:
            sequence = metadata.get("sequence", [])
            # Use the SequencePropertiesCheckerStandalone to determine sequence properties
            sequence_checker = SequencePropertiesCheckerStandalone(sequence)
            sequence_properties = sequence_checker.check_all_properties()

            # Replace the existing metadata with the new one
            new_metadata = {
                "sequence": [
                    {
                        "word": sequence_properties["word"],
                        "author": self.default_author,
                        "level": sequence_properties["level"],
                        "prop_type": metadata.get("prop_type", "unknown"),
                        "is_circular": sequence_properties["is_circular"],
                        "is_permutable": sequence_properties["is_permutable"],
                        "is_strictly_rotated_permutation": sequence_properties[
                            "is_strictly_rotated_permutation"
                        ],
                        "is_strictly_mirrored_permutation": sequence_properties[
                            "is_strictly_mirrored_permutation"
                        ],
                        "is_strictly_colorswapped_permutation": sequence_properties[
                            "is_strictly_colorswapped_permutation"
                        ],
                        "is_mirrored_color_swapped_permutation": sequence_properties[
                            "is_mirrored_color_swapped_permutation"
                        ],
                        "is_rotated_colorswapped_permutation": sequence_properties[
                            "is_rotated_colorswapped_permutation"
                        ],
                    }
                ]
                + sequence[1:]  # Keep the rest of the sequence data as it is
            }

            metadata["sequence"] = new_metadata["sequence"]
        else:
            # If no metadata exists, create a new one
            metadata = {
                "sequence": [
                    {
                        "word": "",
                        "author": self.default_author,
                        "level": 0,
                        "prop_type": "unknown",
                        "is_circular": False,
                        "is_permutable": False,
                        "is_strictly_rotated_permutation": False,
                        "is_strictly_mirrored_permutation": False,
                        "is_strictly_colorswapped_permutation": False,
                        "is_mirrored_color_swapped_permutation": False,
                        "is_rotated_colorswapped_permutation": False,
                    }
                ]
            }

        # Save the updated metadata back to the image
        self.save_metadata_to_image(file_path, metadata)

    def extract_metadata_from_file(self, file_path):
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
        except Exception as e:
            print(f"Error loading sequence from thumbnail: {e}")
        return None

    def save_metadata_to_image(self, file_path, metadata):
        try:
            with Image.open(file_path) as img:
                # Prepare the metadata to be saved
                meta = PngImagePlugin.PngInfo()
                meta.add_text("metadata", json.dumps(metadata))

                img.save(file_path, "PNG", pnginfo=meta)
            print(f"Saved metadata to {file_path}")
        except Exception as e:
            print(f"Failed to save metadata to {file_path}: {e}")


# To execute the metadata update process
if __name__ == "__main__":
    dictionary_path = "F:/CODE/tka-sequence-constructor/dictionary"
    updater = MetadataUpdater(dictionary_path)
    updater.update_all_metadata()
