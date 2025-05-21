from datetime import datetime
import json
import os
from PyQt6.QtGui import QImage
from typing import TYPE_CHECKING
from PIL import Image, PngImagePlugin
import numpy as np
from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
    TempBeatFrame,
)

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager.image_export_manager import (
    ImageExportManager,
)
from utils.path_helpers import (
    get_dictionary_path,
    get_sequence_card_image_exporter_path,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardImageExporter:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.main_widget = sequence_card_tab.main_widget
        self.temp_beat_frame = TempBeatFrame(sequence_card_tab)
        self.export_manager = ImageExportManager(
            self.temp_beat_frame, self.temp_beat_frame.__class__
        )
        # self.export_all_images()

    def export_all_images(self):
        """
        Dynamically renders sequences from the dictionary with consistent export settings.

        This method:
        1. Loads sequences directly from the dictionary
        2. Applies consistent export settings to all sequences
        3. Organizes sequences by word
        4. Renders them on-demand rather than pre-exporting
        """
        dictionary_path = get_dictionary_path()
        export_path = get_sequence_card_image_exporter_path()

        # Create the export directory if it doesn't exist
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        print(f"Loading sequences from dictionary: {dictionary_path}")

        # Get all word folders in the dictionary
        word_folders = []
        for item in os.listdir(dictionary_path):
            item_path = os.path.join(dictionary_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                word_folders.append(item)

        print(f"Found {len(word_folders)} word folders in dictionary")

        # Process each word folder
        total_sequences = 0
        processed_sequences = 0

        for word in word_folders:
            word_path = os.path.join(dictionary_path, word)

            # Get all PNG files in the word folder
            sequences = [
                f
                for f in os.listdir(word_path)
                if f.endswith(".png") and not f.startswith("__")
            ]

            total_sequences += len(sequences)

            # Create a word-specific folder in the export directory
            word_export_path = os.path.join(export_path, word)
            os.makedirs(word_export_path, exist_ok=True)

            # Process each sequence in the word folder
            for sequence_file in sequences:
                sequence_path = os.path.join(word_path, sequence_file)

                # Extract metadata
                metadata = MetaDataExtractor().extract_metadata_from_file(sequence_path)
                if metadata and "sequence" in metadata:
                    sequence = metadata["sequence"]

                    # Set export options with all required metadata visible
                    # Use consistent settings for all images
                    options = {
                        "add_word": True,  # Show the word
                        "add_user_info": True,  # Show author info
                        "add_difficulty_level": True,  # Show difficulty level
                        "add_date": True,  # Show date
                        "add_note": True,  # Show any notes
                        "add_beat_numbers": True,  # Show beat numbers
                        "add_reversal_symbols": True,  # Show reversal symbols
                        "combined_grids": False,  # Don't use combined grids
                        "include_start_position": False,  # Include start position
                    }

                    try:
                        # Generate the image with 50% size reduction
                        self.temp_beat_frame.populate_beat_frame_from_json(sequence)
                        qimage = (
                            self.export_manager.image_creator.create_sequence_image(
                                sequence,
                                options=options,
                                dictionary=False,
                                output_scale=0.5,
                            )
                        )

                        # Convert to PIL image and add metadata
                        pil_image = self.qimage_to_pil(qimage)

                        # Update the date if needed
                        if "date_added" not in metadata:
                            metadata["date_added"] = datetime.now().isoformat()

                        info = self._create_png_info(metadata)

                        # Save the image with the original filename in the word folder
                        output_path = os.path.join(word_export_path, sequence_file)
                        pil_image.save(output_path, "PNG", pnginfo=info)

                        processed_sequences += 1
                    except Exception as e:
                        print(f"Error processing {sequence_path}: {e}")

        print(
            f"Processed {processed_sequences} of {total_sequences} sequences from dictionary"
        )

    def get_all_images(self, path: str) -> list[str]:
        images = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root, file))
        return images

    def qimage_to_pil(self, qimage: QImage) -> Image.Image:
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, copy=False).reshape((height, width, 4))
        arr = arr[..., [2, 1, 0, 3]]  # Convert from ARGB to RGBA
        return Image.fromarray(arr, "RGBA")

    def _create_png_info(self, metadata: dict) -> PngImagePlugin.PngInfo:
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", json.dumps(metadata))
        return info
