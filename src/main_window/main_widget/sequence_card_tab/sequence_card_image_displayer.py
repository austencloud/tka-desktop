import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from main_window.main_widget.metadata_extractor import MetaDataExtractor

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
        self.max_images_per_row = (
            3  # Increased from 2 to 3 images per row for better space usage
        )

    def display_sequences(self, sequences: list[dict]):
        """
        Display sequence card images filtered by the selected length.

        Args:
            sequences: A list of dictionaries containing sequence information:
                - path: The path to the sequence file
                - word: The word associated with the sequence
                - metadata: The metadata extracted from the sequence file
        """
        self.pages = self.sequence_card_tab.pages
        self.pages_cache = self.sequence_card_tab.pages_cache


        # If no sequences are found, show a message
        if not sequences:
            print("No sequences found for the selected length.")
            self._show_no_sequences_message()
            return

        # Sort sequences by word and then by filename
        sorted_sequences = sorted(
            sequences, key=lambda seq: (seq["word"], os.path.basename(seq["path"]))
        )

        # Calculate the available width for two pages side by side
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        nav_sidebar_width = self.nav_sidebar.width()
        available_width = (
            scroll_area_width - nav_sidebar_width - 40
        )  # Account for margins

        # Set up page dimensions (A4 aspect ratio: 8.5:11)
        self.margin = 25  # Fixed margin between pages
        self.page_width = (available_width - self.margin) // 2
        self.page_height = int(self.page_width * 11 / 8.5)  # Maintain A4 aspect ratio
        self.image_card_margin = self.page_width // 40

        self.current_page_index = -1
        current_word = None

        # Group sequences by word
        for sequence in sorted_sequences:
            # If this is a new word, add a word header


            # Load the sequence image
            image_path = sequence["path"]
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                print(f"Error loading image: {image_path}")
                continue

            # Calculate scaling for smaller images (3 per row instead of 2)
            max_image_width = self.page_width // 3 - self.image_card_margin
            scale_factor = max_image_width / pixmap.width() if pixmap.width() > 0 else 1
            scaled_height = int(pixmap.height() * scale_factor)

            # Optimize for more rows per page
            if (
                scaled_height + self.margin * 2 > self.page_height // 4
            ):  # Increased from 3 to 4 divisions
                num_rows = self.get_num_rows_based_on_sequence_length(
                    self.nav_sidebar.selected_length
                )
                # Increase number of rows by 25% to fit more images
                num_rows = int(num_rows * 1.25)
                scaled_height = int(self.page_height // num_rows - self.margin)
                scale_factor = (
                    scaled_height / pixmap.height() if pixmap.height() > 0 else 1
                )
                max_image_width = int(
                    pixmap.width() * scale_factor - self.image_card_margin
                )

            # Scale the image
            scaled_pixmap = pixmap.scaled(
                max_image_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Create a label to display the image
            label = QLabel(self.sequence_card_tab)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add tooltip with sequence information
            if "metadata" in sequence and "sequence" in sequence["metadata"]:
                seq_data = sequence["metadata"]["sequence"][0]
                tooltip = f"Word: {seq_data.get('word', 'Unknown')}\n"
                tooltip += f"Author: {seq_data.get('author', 'Unknown')}\n"
                tooltip += f"Level: {seq_data.get('level', 'Unknown')}\n"

                if "date_added" in sequence["metadata"]:
                    tooltip += (
                        f"Date: {sequence['metadata']['date_added'].split('T')[0]}\n"
                    )

                label.setToolTip(tooltip)

            # Add the image to the page with 3 columns instead of 2
            self.add_image_to_page(
                label,
                self.nav_sidebar.selected_length,
                scaled_pixmap,
                max_images_per_row=3,  # Increased from 2 to 3
            )

        # Cache the pages for future use
        self.pages_cache[self.nav_sidebar.selected_length] = self.pages.copy()



    def _show_no_sequences_message(self):
        """Show a message when no sequences are found."""
        # Initialize margin if not already set
        if not hasattr(self, "margin"):
            self.margin = 20
            self.page_width = 800
            self.page_height = 600
            self.image_card_margin = 10

        # Clear any existing pages
        self.sequence_card_tab.pages.clear()
        self.current_page_index = -1

        # Create a new page
        self.create_new_page()

        # Get the current page layout
        if self.current_page_index >= 0 and self.current_page_index < len(
            self.sequence_card_tab.pages
        ):
            page_layout = self.sequence_card_tab.pages[self.current_page_index].layout()

            # Create a message label with transparent background
            message = QLabel("No sequences found for the selected length.")
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            message.setStyleSheet(
                """
                font-size: 16px;
                color: #333333;
                background-color: transparent;
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 20px;
                margin: 20px;
            """
            )

            # Add the message to the page (span 3 columns instead of 2)
            page_layout.addWidget(message, 1, 0, 1, 3)

            # Cache the page
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
        """Create a new page and add it to the pages list."""
        self.current_page_index += 1
        new_page = self.sequence_card_tab.page_factory.create_page()

        # Apply enhanced styling with shadow effect
        new_page.setStyleSheet(
            """
            background-color: white;
            border: 1px solid #aaaaaa;
            border-radius: 4px;
            margin: 5px;
        """
        )

        # Add the page to the list
        self.sequence_card_tab.pages.append(new_page)
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
        top_spacer = QLabel(self.sequence_card_tab)
        top_spacer.setFixedHeight(self.margin // 3)
        top_spacer.setStyleSheet("background-color: transparent;")
        page_layout.addWidget(top_spacer, 0, 0, 1, self.max_images_per_row)

    def add_bottom_spacer(self, page_layout: QGridLayout, pixmap_height: int):
        """Adds a bottom spacer row to ensure the last row of images aligns with the top."""
        # Calculate the remaining space
        total_height = self.sequence_card_tab.image_displayer.page_height

        # Calculate used height without relying on top_spacer
        # Use a fixed value for the top margin instead
        top_margin = self.margin // 3
        used_height = self.current_row * pixmap_height + top_margin

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
        """
        This method is no longer used as we now load sequences directly from the dictionary.
        It's kept as a stub for backward compatibility.
        """
        print(
            "Sample image generation is disabled. Loading sequences directly from dictionary."
        )
