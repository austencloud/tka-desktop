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
        """Exports all images with headers and footers to a temporary directory."""
        dictionary_path = get_dictionary_path()
        export_path = get_sequence_card_image_exporter_path()

        # Create the export directory if it doesn't exist
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        print(f"Exporting sequence card images to: {export_path}")
        print(f"Loading images from dictionary: {dictionary_path}")

        # Count total images for progress reporting
        images = self.get_all_images(dictionary_path)
        total_images = len(images)
        processed_images = 0
        exported_images = 0

        print(f"Found {total_images} images to process")

        for image_path in images:
            processed_images += 1
            if processed_images % 10 == 0:
                print(f"Processing image {processed_images} of {total_images}")

            # Extract metadata and create a temporary beat frame
            metadata = MetaDataExtractor().extract_metadata_from_file(image_path)
            if metadata and "sequence" in metadata:
                sequence = metadata["sequence"]

                # Get sequence length for organization
                sequence_length = len(sequence) - 1  # Subtract 1 for metadata entry

                # Set export options
                options = {
                    "add_word": True,
                    "add_user_info": True,
                    "add_difficulty_level": True,
                }

                try:
                    # Generate the image
                    self.temp_beat_frame.populate_beat_frame_from_json(sequence)
                    qimage = self.export_manager.image_creator.create_sequence_image(
                        sequence, include_start_pos=False, options=options
                    )

                    # Convert to PIL image and add metadata
                    pil_image = self.qimage_to_pil(qimage)
                    metadata["date_added"] = datetime.now().isoformat()
                    info = self._create_png_info(metadata)

                    # Save the image with the original filename
                    image_filename = os.path.basename(image_path)
                    output_path = os.path.join(export_path, image_filename)
                    pil_image.save(output_path, "PNG", pnginfo=info)

                    exported_images += 1
                except Exception as e:
                    print(f"Error exporting {image_path}: {e}")

        print(
            f"Export complete. Processed {processed_images} images, exported {exported_images} images."
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
