import os
import re
from typing import List, Dict, Union

from .structural_variation_checker import StructuralVariationChecker
from .thumbnail_generator import ThumbnailGenerator
from utilities.path_helpers import get_images_and_data_path


class DictionaryService:
    """
    Handles back-end dictionary logic for storing new sequence variations,
    checking for duplicates, generating thumbnails, etc.
    It does *not* talk to UI widgets or show pop-ups.
    """

    def __init__(
        self,
        create_sequence_image_callback: callable = None,
        get_current_word_callback: callable = None,
    ):
        self.dictionary_dir = get_images_and_data_path("dictionary")
        self.structural_checker = StructuralVariationChecker()
        self.thumbnail_generator = ThumbnailGenerator(
            create_sequence_image_callback, get_current_word_callback
        )

    def add_variation(
        self, sequence_data: List[dict], base_word: str
    ) -> Dict[str, Union[str, int]]:
        """
        Attempt to add a new variation for the given sequence_data under base_word.

        Returns a dict describing the result:
          - {'status': 'ok', 'variation_number': int}
          - {'status': 'duplicate'}
          - {'status': 'invalid'}

        'invalid' means the sequence is empty or invalid for dictionary logic.
        'duplicate' means a structural match was found, so we won't create a new variation.
        'ok' means we successfully wrote a new variation to disk.
        """

        # Basic sanity check:
        if len(sequence_data) <= 1:
            return {"status": "invalid"}

        base_path = os.path.join(self.dictionary_dir, base_word)
        os.makedirs(base_path, exist_ok=True)

        # Check for structural duplication:
        if self.structural_checker.check_for_structural_variation(
            sequence_data, base_word
        ):
            return {"status": "duplicate"}

        # If not a duplicate, figure out next version #:
        variation_number = self.get_next_variation_number(base_word)

        # Actually save files (thumbnail, etc.)
        self.save_variation(sequence_data, base_word, variation_number)

        return {"status": "ok", "variation_number": variation_number}

    def get_next_variation_number(self, base_word: str) -> int:
        """Gets the next available version number for a word in the root dictionary folder."""
        base_path = os.path.join(self.dictionary_dir, base_word)
        existing_versions = []
        for file in os.listdir(base_path):
            match = re.search(r"_ver(\d+)", file)
            if match:
                existing_versions.append(int(match.group(1)))
        return max(existing_versions, default=0) + 1

    def save_variation(
        self, sequence: List[dict], base_word: str, variation_number: int
    ) -> None:
        """
        Saves the new variation: generate a thumbnail, store it in the base_word folder.
        You could also write out extra JSON, if desired.
        """
        base_path = os.path.join(self.dictionary_dir, base_word)
        self.thumbnail_generator.generate_and_save_thumbnail(
            sequence, variation_number, base_path
        )

    def collect_thumbnails(self, base_word: str) -> List[str]:
        """Return a list of all thumbnail file paths for the given word."""
        base_path = os.path.join(self.dictionary_dir, base_word)
        thumbnails = []
        if os.path.exists(base_path):
            for filename in os.listdir(base_path):
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(base_path, filename))
        return thumbnails
