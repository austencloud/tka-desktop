from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab


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
        self.pages = self.sequence_card_tab.pages
        self.pages_cache = self.sequence_card_tab.pages_cache
        filtered_images = [
            img_path
            for img_path in images
            if self.get_sequence_length(img_path) == self.nav_sidebar.selected_length
        ]
        sorted_images = sorted(
            filtered_images, key=lambda img_path: self.get_sequence_length(img_path)
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
        return self.main_widget.metadata_extractor.get_sequence_length(image_path)

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
