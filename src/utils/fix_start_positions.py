"""
Utility script to fix start positions in all images in the dictionary.

This script scans all images in the dictionary and fixes any incorrect start position metadata.
"""

import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.thumbnail_finder import ThumbnailFinder
from utils.path_helpers import get_data_path


def fix_start_positions_in_dictionary():
    """
    Fix start positions in all images in the dictionary.

    Returns:
        tuple: (total_images, fixed_images, failed_images, missing_start_pos)
    """
    dictionary_dir = get_data_path("dictionary")
    metadata_extractor = MetaDataExtractor()
    total_images = 0
    fixed_images = 0
    failed_images = 0
    missing_start_pos = 0
    problem_files = []

    print("Scanning dictionary for images with incorrect start positions...")

    for word in os.listdir(dictionary_dir):
        word_dir = os.path.join(dictionary_dir, word)
        if os.path.isdir(word_dir) and "__pycache__" not in word:
            thumbnails = ThumbnailFinder().find_thumbnails(word_dir)
            for thumbnail in thumbnails:
                total_images += 1
                try:
                    # Extract metadata to check if it has a sequence with a start position
                    metadata = metadata_extractor.extract_metadata_from_file(thumbnail)
                    if (
                        not metadata
                        or "sequence" not in metadata
                        or len(metadata["sequence"]) < 2
                    ):
                        missing_start_pos += 1
                        print(
                            f"Warning: No valid sequence or start position in {thumbnail}"
                        )
                        continue

                    # Try to fix the start position
                    if metadata_extractor.fix_start_position_in_metadata(thumbnail):
                        fixed_images += 1
                        print(f"Fixed start position in {thumbnail}")
                except Exception as e:
                    failed_images += 1
                    problem_files.append((thumbnail, str(e)))
                    print(f"Failed to fix start position in {thumbnail}: {e}")

    print("\nSummary:")
    print(f"Total images processed: {total_images}")
    print(f"Images fixed: {fixed_images}")
    print(f"Images with missing start positions: {missing_start_pos}")
    print(f"Images that failed to process: {failed_images}")

    if problem_files:
        print("\nProblem files:")
        for file, error in problem_files:
            print(f"- {file}: {error}")

    return total_images, fixed_images, failed_images, missing_start_pos


if __name__ == "__main__":
    app = QApplication([])

    total, fixed, failed, missing = fix_start_positions_in_dictionary()

    message = f"Start position fix complete!\n\n"
    message += f"Total images processed: {total}\n"
    message += f"Images fixed: {fixed}\n"
    message += f"Images with missing start positions: {missing}\n"
    message += f"Images failed: {failed}\n"

    if fixed > 0:
        message += (
            f"\nSuccessfully fixed {fixed} images with incorrect start positions."
        )

    if missing > 0:
        message += f"\n\nWarning: {missing} images have no valid start position data."
        message += f"\nThese may be older sequences or have other issues."

    QMessageBox.information(None, "Start Position Fix Complete", message)
