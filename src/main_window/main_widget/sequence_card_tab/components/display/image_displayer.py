# src/main_window/main_widget/sequence_card_tab/components/display/image_displayer.py
import os
import gc
from typing import TYPE_CHECKING, Dict, Set
from PyQt6.QtWidgets import QLabel, QApplication, QProgressDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class SequenceCardImageDisplayer:
    """Optimized image displayer that works with existing architecture."""

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.main_widget = sequence_card_tab.main_widget
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.settings_manager = sequence_card_tab.settings_manager

        # Initialize variables from original
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0

        # Optimized caching
        self.image_cache: Dict[str, QPixmap] = {}
        self.loaded_images: Set[str] = set()

        # Quality settings
        self.quality_settings = {
            "target_dpi": 150,  # Higher DPI for better quality
            "use_smooth_scaling": True,
            "max_cache_size_mb": 300,
        }

        # Get column count
        self.max_images_per_row = (
            self.settings_manager.sequence_card_tab.get_column_count()
        )

    def display_sequences(self, sequences: list[dict]):
        """Display sequences with optimized image loading."""
        # Clear caches
        self._clear_cache()

        # Store references
        self.pages = self.sequence_card_tab.pages
        self.pages_cache = self.sequence_card_tab.pages_cache

        # Show progress
        self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
        self.sequence_card_tab.description_label.setText(
            "Loading high-quality images..."
        )
        QApplication.processEvents()

        if not sequences:
            self._show_no_sequences_message()
            self._cleanup_loading()
            return

        # Sort sequences
        sorted_sequences = sorted(
            sequences, key=lambda seq: (seq["word"], os.path.basename(seq["path"]))
        )

        # Calculate layout
        self._calculate_layout()

        # Reset counters
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0

        # Process images with progress
        self._process_images_optimized(sorted_sequences)

        # Cache pages
        if hasattr(self.nav_sidebar, "selected_length"):
            self.pages_cache[self.nav_sidebar.selected_length] = self.pages.copy()

        self._cleanup_loading()

    def _calculate_layout(self):
        """Calculate optimal layout dimensions for high quality display."""
        scroll_area_width = self.sequence_card_tab.scroll_area.width()
        nav_sidebar_width = self.nav_sidebar.width()
        available_width = scroll_area_width - nav_sidebar_width - 60  # More margin

        # A4 aspect ratio with better proportions
        self.margin = 30
        self.page_width = (available_width - self.margin) // 2
        self.page_height = int(self.page_width * 11 / 8.5)
        self.image_card_margin = max(10, self.page_width // 30)  # Proportional margin

    def _process_images_optimized(self, sequences: list[dict]):
        """Process images with optimized quality and caching."""
        total_sequences = len(sequences)

        # Create progress dialog
        progress = QProgressDialog(
            "Loading high-quality images...",
            "Cancel",
            0,
            total_sequences,
            self.sequence_card_tab,
        )
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(500)

        try:
            for i, sequence in enumerate(sequences):
                if progress.wasCanceled():
                    break

                progress.setValue(i)
                progress.setLabelText(
                    f"Processing {sequence.get('word', 'Unknown')} ({i+1}/{total_sequences})"
                )

                # Load and process image
                try:
                    image_path = sequence.get("path", "")
                    if image_path and os.path.exists(image_path):
                        # Load high-quality image
                        pixmap = self._load_high_quality_image(image_path)

                        if not pixmap.isNull():
                            # Create label and add to page
                            label = self._create_image_label(sequence, pixmap)
                            self._add_image_to_page(label, pixmap)

                            # Cache the image
                            self.image_cache[image_path] = pixmap
                            self.loaded_images.add(image_path)

                except Exception as e:
                    print(f"Error processing {sequence.get('path', 'unknown')}: {e}")

                # Keep UI responsive
                if i % 5 == 0:
                    QApplication.processEvents()
                    self._manage_memory()

        finally:
            progress.close()

    def _load_high_quality_image(self, image_path: str) -> QPixmap:
        """Load image with high quality settings."""
        # Check cache first
        if image_path in self.image_cache:
            return self.image_cache[image_path]

        try:
            # Load original image
            image = QImage(image_path)
            if image.isNull():
                return QPixmap()

            # Calculate target size based on layout and quality settings
            target_width = (self.page_width // self.max_images_per_row) - (
                self.image_card_margin * 2
            )

            # Scale for higher DPI
            dpi_scale = self.quality_settings["target_dpi"] / 96.0  # 96 DPI is standard
            target_width = int(target_width * dpi_scale)

            # Calculate proportional height
            aspect_ratio = image.height() / image.width()
            target_height = int(target_width * aspect_ratio)

            # Use high-quality scaling
            if self.quality_settings["use_smooth_scaling"]:
                scaled_image = image.scaled(
                    target_width,
                    target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                scaled_image = image.scaled(
                    target_width,
                    target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.FastTransformation,
                )

            # Convert to pixmap
            pixmap = QPixmap.fromImage(scaled_image)

            # Scale back down to display size (maintains quality)
            display_width = (self.page_width // self.max_images_per_row) - (
                self.image_card_margin * 2
            )
            display_height = int(display_width * aspect_ratio)

            final_pixmap = pixmap.scaled(
                display_width,
                display_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            return final_pixmap

        except Exception as e:
            print(f"Error loading high-quality image {image_path}: {e}")
            return QPixmap()

    def _create_image_label(self, sequence: dict, pixmap: QPixmap) -> QLabel:
        """Create an image label with tooltip."""
        label = QLabel(self.sequence_card_tab)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add detailed tooltip
        if "metadata" in sequence and "sequence" in sequence["metadata"]:
            try:
                seq_data = sequence["metadata"]["sequence"][0]
                tooltip = f"Word: {seq_data.get('word', 'Unknown')}\n"
                tooltip += f"Author: {seq_data.get('author', 'Unknown')}\n"
                tooltip += f"Level: {seq_data.get('level', 'Unknown')}\n"

                if "date_added" in sequence["metadata"]:
                    date_str = sequence["metadata"]["date_added"].split("T")[0]
                    tooltip += f"Date Added: {date_str}\n"

                label.setToolTip(tooltip)
            except Exception:
                pass

        return label

    def _add_image_to_page(self, label: QLabel, pixmap: QPixmap):
        """Add image to page using existing logic."""
        selected_length = getattr(self.nav_sidebar, "selected_length", 4)

        if self.current_page_index == -1 or self._is_current_page_full(
            selected_length, pixmap.height()
        ):
            self._create_new_page()

        page_layout = self.sequence_card_tab.pages[self.current_page_index].layout()

        # Add top spacer for first image
        if self.current_row == 0 and self.current_col == 0:
            self._add_top_spacer(page_layout)

        page_layout.addWidget(label, self.current_row + 1, self.current_col)
        self.current_col += 1

        if self.current_col >= self.max_images_per_row:
            self.current_col = 0
            self.current_row += 1

        if self._is_last_image_in_page(selected_length):
            self._add_bottom_spacer(page_layout, pixmap.height())

    def _create_new_page(self):
        """Create new page using existing factory."""
        self.current_page_index += 1
        new_page = self.sequence_card_tab.page_factory.create_page()
        self.sequence_card_tab.pages.append(new_page)
        self.current_row = 0
        self.current_col = 0

    def _is_current_page_full(self, selected_length: int, image_height: int) -> bool:
        """Check if current page is full."""
        if self.current_page_index == -1:
            return True

        num_rows = self._get_num_rows_for_length(selected_length)
        return self.current_row >= num_rows

    def _is_last_image_in_page(self, selected_length: int) -> bool:
        """Check if this is the last image in the page."""
        num_rows = self._get_num_rows_for_length(selected_length)
        return self.current_row >= num_rows - 1

    def _get_num_rows_for_length(self, selected_length: int) -> int:
        """Get number of rows based on sequence length."""
        return {
            0: 5,  # Show all
            2: 6,  # Short sequences
            3: 6,
            4: 5,
            5: 5,
            6: 4,
            8: 4,
            10: 3,
            12: 3,
            16: 2,  # Long sequences
        }.get(selected_length, 4)

    def _add_top_spacer(self, page_layout):
        """Add top spacer."""
        top_spacer = QLabel(self.sequence_card_tab)
        top_spacer.setFixedHeight(self.margin // 3)
        top_spacer.setStyleSheet("background-color: transparent;")
        page_layout.addWidget(top_spacer, 0, 0, 1, self.max_images_per_row)

    def _add_bottom_spacer(self, page_layout, image_height: int):
        """Add bottom spacer."""
        remaining_height = max(
            0, self.page_height - (self.current_row * image_height) - self.margin
        )

        if remaining_height > 10:
            spacer = QLabel(self.sequence_card_tab)
            spacer.setFixedHeight(remaining_height)
            spacer.setStyleSheet("background-color: transparent;")
            page_layout.addWidget(
                spacer, self.current_row + 1, 0, 1, self.max_images_per_row
            )

    def _manage_memory(self):
        """Manage memory usage during processing."""
        try:
            import psutil

            process = psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)

            if memory_mb > self.quality_settings["max_cache_size_mb"]:
                # Clear oldest entries from cache
                if len(self.image_cache) > 20:
                    # Keep only the 20 most recent images
                    keys_to_remove = list(self.image_cache.keys())[:-20]
                    for key in keys_to_remove:
                        if key in self.image_cache:
                            del self.image_cache[key]

                gc.collect()
        except ImportError:
            pass  # psutil not available

    def _clear_cache(self):
        """Clear image cache."""
        self.image_cache.clear()
        self.loaded_images.clear()
        gc.collect()

    def _show_no_sequences_message(self):
        """Show message when no sequences found."""
        # Create a message label
        message_label = QLabel("No sequences found for the selected length")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet(
            """
            color: #7f8c8d;
            font-size: 16px;
            font-style: italic;
            padding: 20px;
        """
        )

        # Create a new page
        self._create_new_page()

        # Add message to page
        page_layout = self.sequence_card_tab.pages[self.current_page_index].layout()
        page_layout.addWidget(message_label, 1, 0, 1, self.max_images_per_row)

    def _cleanup_loading(self):
        """Clean up after loading."""
        self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

        # Update description based on selected length
        selected_length = getattr(self.nav_sidebar, "selected_length", 0)
        if selected_length == 0:
            description = "Viewing all sequences"
        else:
            description = f"Viewing sequences with length {selected_length}"

        self.sequence_card_tab.description_label.setText(description)
        QApplication.processEvents()

    def cleanup(self):
        """Clean up resources."""
        self._clear_cache()
