import os
import logging
from typing import TYPE_CHECKING
from PIL import Image, PngImagePlugin
from PyQt6.QtWidgets import QMessageBox
import json

from data.constants import (
    GRID_MODE,
    SEQUENCE_START_POSITION,
    END_POS,
    DIAMOND,
    BOX,  # Import grid mode constants
)
from main_window.main_widget.sequence_level_evaluator import SequenceLevelEvaluator
from main_window.main_widget.thumbnail_finder import ThumbnailFinder
from utils.path_helpers import get_data_path


class MetaDataExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_tags(self, file_path: str) -> list[str]:
        """Retrieve the list of tags from the metadata."""
        metadata = self.extract_metadata_from_file(file_path)
        if metadata:
            return metadata.get("tags", [])  # Default to an empty list if no tags exist
        return []

    def set_tags(self, file_path: str, tags: list[str]):
        """Set the list of tags in the metadata."""
        try:
            with Image.open(file_path) as img:
                metadata = self.extract_metadata_from_file(file_path) or {}
                metadata["tags"] = tags  # Update or create the tags field

                # Save the updated metadata back to the image
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("metadata", json.dumps(metadata))
                img.save(file_path, pnginfo=pnginfo)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Error saving tags to thumbnail: {e}",
            )

    def extract_metadata_from_file(self, file_path):
        # Check if a file exists at the path we're passing as "file_path"
        if not file_path:
            return None

        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
                else:
                    # Silent logging instead of annoying popup
                    self.logger.debug(
                        f"No sequence metadata found in thumbnail: {file_path}"
                    )
                    return None
        except Exception as e:
            # Keep critical errors as popups since these indicate real issues
            QMessageBox.critical(
                None,
                "Error",
                f"Error loading sequence from thumbnail: {e}",
            )
        return None

    def get_favorite_status(self, file_path: str) -> bool:
        metadata = self.extract_metadata_from_file(file_path)
        if metadata:
            return metadata.get("is_favorite", False)
        return False

    def set_favorite_status(self, file_path: str, is_favorite: bool):
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    metadata_dict = json.loads(metadata)
                else:
                    metadata_dict = {}

                metadata_dict["is_favorite"] = is_favorite

                # Save the image with updated metadata
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("metadata", json.dumps(metadata_dict))
                img.save(file_path, pnginfo=pnginfo)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Error saving favorite status to thumbnail: {e}",
            )

    def get_author(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return metadata["sequence"][0]["author"]
        return

    def get_level(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            if "level" in metadata["sequence"][0]:
                if metadata["sequence"][0]["level"] != 0:
                    return metadata["sequence"][0]["level"]
                else:

                    evaluator = SequenceLevelEvaluator()
                    level = evaluator.get_sequence_difficulty_level(
                        metadata["sequence"]
                    )
                    metadata["sequence"][0]["level"] = level

                    # Save the updated metadata back to the image
                    try:
                        with Image.open(file_path) as img:
                            pnginfo = PngImagePlugin.PngInfo()
                            pnginfo.add_text("metadata", json.dumps(metadata))
                            img.save(file_path, pnginfo=pnginfo)
                    except Exception as e:
                        QMessageBox.critical(
                            None,
                            "Error",
                            f"Error saving level to thumbnail: {e}",
                        )
                    return level
        return

    def get_length(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return len(metadata["sequence"]) - 2
        return 0  # Default to 0 if no valid sequence length is found

    def get_start_pos(self, file_path):
        """
        Get the start position type (alpha, beta, gamma) from the metadata.

        If the sequence_start_position field is missing, it attempts to derive it from the end_pos field of the start position entry.
        """
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata and len(metadata["sequence"]) > 1:
            start_pos_entry = metadata["sequence"][1]

            # First try to get the sequence_start_position directly
            if SEQUENCE_START_POSITION in start_pos_entry:
                return start_pos_entry[SEQUENCE_START_POSITION]

            # If not available, try to derive it from the end_pos
            if END_POS in start_pos_entry:
                end_pos = start_pos_entry[END_POS]
                if end_pos.startswith("alpha"):
                    return "alpha"
                elif end_pos.startswith("beta"):
                    return "beta"
                elif end_pos.startswith("gamma"):
                    return "gamma"

        return None

    def get_metadata_and_thumbnail_dict(self) -> list[dict[str, str]]:
        """Collect all sequences and their metadata along with the associated thumbnail paths."""
        dictionary_dir = get_data_path("dictionary")
        metadata_and_thumbnail_dict = []

        for word in os.listdir(dictionary_dir):
            word_dir = os.path.join(dictionary_dir, word)
            if os.path.isdir(word_dir) and "__pycache__" not in word:
                thumbnails = ThumbnailFinder().find_thumbnails(word_dir)
                for thumbnail in thumbnails:
                    metadata = self.extract_metadata_from_file(thumbnail)
                    if metadata:
                        metadata_and_thumbnail_dict.append(
                            {"metadata": metadata, "thumbnail": thumbnail}
                        )

        return metadata_and_thumbnail_dict

    def get_grid_mode(self, file_path):
        """
        Get the grid mode from the metadata.

        If the grid_mode field is missing, it defaults to 'diamond'.
        """
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            # Check if grid_mode exists in the metadata
            if GRID_MODE in metadata["sequence"][0]:
                return metadata["sequence"][0][GRID_MODE]
            else:
                # Default to 'diamond' if grid_mode is not specified
                return DIAMOND
        return DIAMOND  # Default to 'diamond' if no metadata is found

    def get_full_metadata(self, file_path: str) -> dict:
        """Extract all available metadata for a given file."""
        return self.extract_metadata_from_file(file_path) or {}

    def fix_start_position_in_metadata(self, file_path: str) -> bool:
        """
        Fix the start position in the metadata of an image file.

        This function checks if the sequence_start_position field is correctly set
        (alpha, beta, or gamma) and fixes it if necessary.

        Returns:
            bool: True if the metadata was fixed, False otherwise.
        """
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if not metadata:
                    return False

                metadata_dict = json.loads(metadata)
                if not metadata_dict or "sequence" not in metadata_dict:
                    return False

                sequence = metadata_dict["sequence"]
                if len(sequence) < 2:
                    return False

                # Get the second entry (index 1) which should be the start position
                start_pos_entry = sequence[1]

                # Check if the entry has an end_pos field (which it should if it's a start position)
                if END_POS not in start_pos_entry:
                    return False

                end_pos = start_pos_entry.get(END_POS, "")

                # Determine the correct start position
                correct_start_pos = None
                if end_pos.startswith("alpha"):
                    correct_start_pos = "alpha"
                elif end_pos.startswith("beta"):
                    correct_start_pos = "beta"
                elif end_pos.startswith("gamma"):
                    correct_start_pos = "gamma"

                if not correct_start_pos:
                    return False

                needs_update = False

                # If sequence_start_position is missing, add it
                if SEQUENCE_START_POSITION not in start_pos_entry:
                    start_pos_entry[SEQUENCE_START_POSITION] = correct_start_pos
                    needs_update = True
                # If sequence_start_position is incorrect, fix it
                elif start_pos_entry[SEQUENCE_START_POSITION] != correct_start_pos:
                    start_pos_entry[SEQUENCE_START_POSITION] = correct_start_pos
                    needs_update = True

                # Save the updated metadata back to the image if needed
                if needs_update:
                    pnginfo = PngImagePlugin.PngInfo()
                    pnginfo.add_text("metadata", json.dumps(metadata_dict))
                    img.save(file_path, pnginfo=pnginfo)
                    return True

                return False
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Error fixing start position in metadata: {e}",
            )
            return False
