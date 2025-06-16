import json
import os
from PIL import Image

from data.constants import BLUE_ATTRS, RED_ATTRS, TURNS, START_ORI, END_ORI
from utils.path_helpers import get_data_path


class TurnPatternVariationChecker:
    def __init__(self):
        self.directory = get_data_path("dictionary")

    def check_for_turn_pattern_variation(self, sequence):
        # Iterate recursively through all files in the directory and subdirectories
        for root, dirs, files in os.walk(self.directory):
            for file_name in files:
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file_name)
                    if self.are_turns_patterns_identical(sequence, file_path):
                        return True
        return False

    def are_turns_patterns_identical(self, seq1, image_path):
        try:
            with Image.open(image_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    seq2 = json.loads(metadata)
                    return self.compare_turns_patterns(seq1, seq2)
        except IOError as e:
            # raise an error
            raise e
        return False

    def compare_turns_patterns(self, seq1, seq2):
        # Compare specific attributes within each sequence
        if len(seq1) != len(seq2):
            return False

        keys_to_compare = [TURNS, START_ORI, END_ORI]
        for beat1, beat2 in zip(seq1, seq2):
            for attr in [BLUE_ATTRS, RED_ATTRS]:
                if not self.compare_attributes(
                    beat1.get(attr, {}), beat2.get(attr, {}), keys_to_compare
                ):
                    return False
        return True

    def compare_attributes(self, attr1, attr2, keys):
        for key in keys:
            if attr1.get(key) != attr2.get(key):
                return False
        return True
