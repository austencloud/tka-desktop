import os
from datetime import datetime
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import Qt

from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import LETTER, START_POS, END_POS, BLUE, RED, MOTION_TYPE
from utils.path_helpers import get_my_photos_path

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class PictographExporter:
    """
    Class for exporting all pictographs in the program as individual images.
    """

    def __init__(self, image_export_tab: "ImageExportTab"):
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget

    def export_all_pictographs(self):
        """
        Export all pictographs in the program as individual images.
        """
        # Ask the user for a directory to save the images
        directory = self._get_export_directory()
        if not directory:
            return  # User canceled

        # Collect all pictographs
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Filter out blank pictographs and duplicates
        valid_pictographs = self._filter_pictographs(pictographs)

        if not valid_pictographs:
            QMessageBox.information(
                self.image_export_tab,
                "No Pictographs",
                "No valid pictographs found to export.",
            )
            return

        # Create a progress message
        self.main_widget.sequence_workbench.indicator_label.show_message(
            f"Exporting {len(valid_pictographs)} pictographs..."
        )

        # Export each pictograph
        exported_count = self._export_pictographs(valid_pictographs, directory)

        # Show completion message
        self.main_widget.sequence_workbench.indicator_label.show_message(
            f"Successfully exported {exported_count} pictographs to {directory}"
        )

        # Open the directory
        os.startfile(directory)

    def _get_export_directory(self) -> str:
        """
        Get the directory where pictographs will be exported.

        Returns:
            The selected directory path or empty string if canceled.
        """
        # Use the default photos directory as the starting point
        default_dir = get_my_photos_path("pictograph_exports")
        os.makedirs(default_dir, exist_ok=True)

        # Show directory selection dialog
        directory = QFileDialog.getExistingDirectory(
            self.image_export_tab, "Select Directory to Save Pictographs", default_dir
        )

        return directory

    def _filter_pictographs(
        self, pictographs: List[LegacyPictograph]
    ) -> List[LegacyPictograph]:
        """
        Filter out blank pictographs and duplicates.

        Args:
            pictographs: List of pictographs to filter

        Returns:
            Filtered list of valid pictographs
        """
        valid_pictographs = []
        seen_keys = set()

        for pictograph in pictographs:
            # Skip blank pictographs
            if pictograph.is_blank or not pictograph.state.pictograph_data:
                continue

            # Create a unique key for the pictograph to avoid duplicates
            data = pictograph.state.pictograph_data
            letter = data.get(LETTER, "unknown")
            start_pos = data.get(START_POS, "unknown")
            end_pos = data.get(END_POS, "unknown")
            blue_motion = data.get(f"{BLUE}_{MOTION_TYPE}", "unknown")
            red_motion = data.get(f"{RED}_{MOTION_TYPE}", "unknown")

            key = f"{letter}_{start_pos}_{end_pos}_{blue_motion}_{red_motion}"

            if key not in seen_keys:
                seen_keys.add(key)
                valid_pictographs.append(pictograph)

        return valid_pictographs

    def _export_pictographs(
        self, pictographs: List[LegacyPictograph], directory: str
    ) -> int:
        """
        Export pictographs as individual images.

        Args:
            pictographs: List of pictographs to export
            directory: Directory to save the images

        Returns:
            Number of successfully exported pictographs
        """
        exported_count = 0
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for i, pictograph in enumerate(pictographs):
            try:
                # Get pictograph data for filename
                data = pictograph.state.pictograph_data
                letter = data.get(LETTER, "unknown")
                start_pos = data.get(START_POS, "unknown")
                end_pos = data.get(END_POS, "unknown")

                # Create filename
                filename = (
                    f"pictograph_{letter}_{start_pos}_{end_pos}_{timestamp}_{i+1}.png"
                )
                filepath = os.path.join(directory, filename)

                # Create image from pictograph
                image = self._create_pictograph_image(pictograph)

                # Save image
                if image.save(filepath, "PNG"):
                    exported_count += 1

            except Exception as e:
                print(f"Error exporting pictograph: {e}")

        return exported_count

    def _create_pictograph_image(self, pictograph: LegacyPictograph) -> QImage:
        """
        Create a QImage from a pictograph.

        Args:
            pictograph: The pictograph to convert to an image

        Returns:
            QImage of the pictograph
        """
        # Create image with the same size as the pictograph
        size = 950  # Standard pictograph size
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        # Draw the pictograph onto the image
        painter = QPainter(image)
        pictograph.render(painter)
        painter.end()

        return image
