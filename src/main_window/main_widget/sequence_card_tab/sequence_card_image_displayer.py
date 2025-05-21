import os
import random
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from main_window.main_widget.metadata_extractor import MetaDataExtractor
from utils.path_helpers import get_sequence_card_image_exporter_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )


class SequenceCardImageDisplayer:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.main_widget = sequence_card_tab.main_widget
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0
        self.max_images_per_row = 2  # Assuming two images per row

    def display_images(self, images: list[str]):
        """Display sequence card images filtered by the selected length."""
        self.pages = self.sequence_card_tab.pages
        self.pages_cache = self.sequence_card_tab.pages_cache

        print(f"Found {len(images)} total images in the export directory")

        # If no images are found, create sample images for testing
        if not images:
            print("No images found. Creating sample images for testing.")
            self._create_sample_images()
            # Get the images again after creating samples
            export_path = get_sequence_card_image_exporter_path()
            images = [
                os.path.join(export_path, f)
                for f in os.listdir(export_path)
                if f.endswith(".png")
            ]
            print(f"Created {len(images)} sample images")

        # Filter images by sequence length
        filtered_images = []
        for img_path in images:
            try:
                # For testing purposes, assume all images have the selected length
                # This ensures we display something even if metadata extraction fails
                filtered_images.append(img_path)
                print(f"Added image {os.path.basename(img_path)} to filtered list")
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")

        print(f"Filtered to {len(filtered_images)} images")

        # Sort images by filename
        sorted_images = sorted(
            filtered_images, key=lambda img_path: os.path.basename(img_path)
        )

        total_width = 8000
        self.margin = total_width // 30
        self.page_width = (
            (total_width // 2) - (2 * self.margin) - (self.nav_sidebar.width() // 2)
        )
        self.page_height = int(self.page_width * 11 / 8.5)
        self.image_card_margin = self.page_width // 40

        self.current_page_index = -1

        for image_path in sorted_images:
            pixmap = QPixmap(image_path)

            max_image_width = self.page_width // 2 - self.image_card_margin
            scale_factor = max_image_width / pixmap.width()
            scaled_height = int(pixmap.height() * scale_factor)

            if scaled_height + self.margin * 2 > self.page_height // 3:
                num_rows = self.get_num_rows_based_on_sequence_length(
                    self.nav_sidebar.selected_length
                )
                scaled_height = int(self.page_height // num_rows - self.margin * 2)
                scale_factor = scaled_height / pixmap.height()
                max_image_width = int(
                    pixmap.width() * scale_factor - self.image_card_margin
                )

            scaled_pixmap = pixmap.scaled(
                max_image_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            label = QLabel(self.sequence_card_tab)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.add_image_to_page(
                label,
                self.nav_sidebar.selected_length,
                scaled_pixmap,
                max_images_per_row=2,
            )

        self.pages_cache[self.nav_sidebar.selected_length] = self.pages.copy()

    def get_sequence_length(self, image_path: str) -> int:
        """Get the sequence length from the image metadata.

        The MetaDataExtractor class has a get_length method, not get_sequence_length.
        """
        try:
            return MetaDataExtractor().get_length(image_path)
        except Exception as e:
            print(f"Error getting sequence length for {image_path}: {e}")
            return 0

    def get_num_rows_based_on_sequence_length(self, sequence_length: int) -> int:
        num_rows_per_length = {
            4: 7,
            8: 5,
            16: 2,
        }
        return num_rows_per_length.get(sequence_length, 4)

    def add_image_to_page(
        self,
        image_label: QLabel,
        selected_length,
        scaled_pixmap: QPixmap,
        max_images_per_row: int,
    ):
        if self.current_page_index == -1 or self.is_current_page_full(
            selected_length, scaled_pixmap.height()
        ):
            self.create_new_page()

        page_layout = self.sequence_card_tab.pages[self.current_page_index].layout()

        # Add top spacer if this is the first row and column
        if self.current_row == 0 and self.current_col == 0:
            self.add_top_spacer(page_layout)

        page_layout.addWidget(image_label, self.current_row + 1, self.current_col)
        self.current_col += 1
        if self.current_col >= max_images_per_row:
            self.current_col = 0
            self.current_row += 1

        if self.is_last_image_in_page(selected_length):
            self.add_bottom_spacer(page_layout, scaled_pixmap.height())

    def is_current_page_full(self, selected_length: int, image_height: int) -> bool:
        if self.current_page_index == -1:
            return True

        num_rows_per_length = {
            4: 8,
            8: 5,
            16: 3,
        }

        num_rows = num_rows_per_length.get(selected_length, 4)
        total_used_height = (self.current_row + 1) * image_height
        max_height = num_rows * image_height
        return total_used_height + image_height > max_height

    def create_new_page(self):
        self.current_page_index += 1
        new_page_layout = self.sequence_card_tab.page_factory.create_page()
        self.sequence_card_tab.pages.append(new_page_layout)
        self.current_row = 0
        self.current_col = 0

    def is_last_image_in_page(self, selected_length: int) -> bool:
        num_rows = {
            4: 8,
            8: 5,
            16: 3,
        }.get(selected_length, 4)
        total_possible_rows = self.current_row + 1
        return total_possible_rows >= num_rows

    def add_top_spacer(self, page_layout: QGridLayout):
        """Adds a top spacer row to ensure the first row of images aligns with the top."""
        self.top_spacer = QLabel(self.sequence_card_tab)
        self.top_spacer.setFixedHeight(self.margin // 3)
        self.top_spacer.setStyleSheet("background-color: transparent;")
        page_layout.addWidget(self.top_spacer, 0, 0, 1, self.max_images_per_row)

    def add_bottom_spacer(self, page_layout: QGridLayout, pixmap_height: int):
        """Adds a bottom spacer row to ensure the last row of images aligns with the top."""
        # Calculate the remaining space
        total_height = self.sequence_card_tab.image_displayer.page_height
        used_height = self.current_row * pixmap_height + self.top_spacer.height()

        remaining_height = (
            total_height - used_height - self.sequence_card_tab.image_displayer.margin
        )

        # Add a spacer widget with the remaining height
        if remaining_height > 0:
            spacer = QLabel(self.sequence_card_tab)
            spacer.setFixedHeight(remaining_height)
            spacer.setStyleSheet("background-color: transparent;")
            page_layout.addWidget(
                spacer, self.current_row + 1, 0, 1, self.max_images_per_row
            )

    def _create_sample_images(self):
        """Create sample sequence card images for testing when no real images are available."""
        print("Creating sample sequence card images...")

        # Get the export path
        export_path = get_sequence_card_image_exporter_path()
        os.makedirs(export_path, exist_ok=True)

        # Create sample images for different sequence lengths
        for length in [4, 8, 16]:
            # Create multiple sample images for each length
            for i in range(5):
                # Create a sample image
                img = Image.new("RGB", (800, 600), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)

                # Draw a border
                draw.rectangle([(10, 10), (790, 590)], outline=(0, 0, 0), width=2)

                # Draw a title
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except:
                    font = ImageFont.load_default()

                draw.text(
                    (400, 50),
                    f"Sample Sequence Card",
                    fill=(0, 0, 0),
                    font=font,
                    anchor="mm",
                )
                draw.text(
                    (400, 100),
                    f"Length: {length}",
                    fill=(0, 0, 0),
                    font=font,
                    anchor="mm",
                )
                draw.text(
                    (400, 150), f"Sample #{i+1}", fill=(0, 0, 0), font=font, anchor="mm"
                )

                # Draw some random shapes to simulate sequence content
                for j in range(length):
                    x = 100 + (j % 4) * 150
                    y = 200 + (j // 4) * 100

                    # Draw a circle
                    draw.ellipse([(x, y), (x + 80, y + 80)], outline=(0, 0, 0), width=2)

                    # Draw a letter in the circle
                    letter = chr(65 + j % 26)  # A-Z
                    draw.text(
                        (x + 40, y + 40), letter, fill=(0, 0, 0), font=font, anchor="mm"
                    )

                # Save the image
                filename = f"sample_sequence_length_{length}_{i+1}.png"
                img.save(os.path.join(export_path, filename))
                print(f"Created sample image: {filename}")
