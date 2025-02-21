import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtGui import QImage
from PIL import Image, PngImagePlugin, ImageEnhance
import numpy as np
from datetime import datetime

if TYPE_CHECKING:
    from .add_to_dictionary_manager import AddToDictionaryManager


class ThumbnailGenerator:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.manager = add_to_dictionary_manager
        self.sequence_workbench = add_to_dictionary_manager.sequence_workbench

    def generate_and_save_thumbnail(
        self, sequence, structural_variation_number, directory
    ):
        """Generate and save thumbnail for a sequence variation."""
        beat_frame_image = self.sequence_workbench.sequence_beat_frame.image_export_manager.image_creator.create_sequence_image(
            sequence, include_start_pos=False
        )
        pil_image = self.qimage_to_pil(beat_frame_image)

        # Resize the image to 65% of the original size
        pil_image = self._resize_image(pil_image, 0.5)

        # Apply sharpening to improve clarity after resizing
        pil_image = self._sharpen_image(pil_image)

        metadata = {"sequence": sequence, "date_added": datetime.now().isoformat()}
        metadata_str = json.dumps(metadata)
        info = self._create_png_info(metadata_str)

        image_filename = self._create_image_filename(structural_variation_number)
        image_path = os.path.join(directory, image_filename)
        self._save_image(pil_image, image_path, info)
        return image_path

    def _resize_image(self, image: Image.Image, scale_factor: float) -> Image.Image:
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        return image.resize(new_size, Image.LANCZOS)

    def _sharpen_image(self, image: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(
            1.5
        )  # 1.0 is original sharpness; >1.0 increases sharpness

    def qimage_to_pil(self, qimage: QImage) -> Image.Image:
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, copy=False).reshape((height, width, 4))
        arr = arr[..., [2, 1, 0, 3]]  # Adjust for RGB
        return Image.fromarray(arr, "RGBA")

    def _create_png_info(self, metadata: str) -> PngImagePlugin.PngInfo:
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", metadata.encode("utf-8"))
        return info

    def _create_image_filename(self, structural_variation_number):
        base_word = (
            self.manager.sequence_workbench.sequence_beat_frame.get.current_word()
        )
        return f"{base_word}_ver{structural_variation_number}.png"

    def _save_image(
        self, pil_image: Image.Image, image_path: str, info: PngImagePlugin.PngInfo
    ):
        pil_image.save(image_path, "PNG", pnginfo=info)
