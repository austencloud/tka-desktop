import os
from typing import TYPE_CHECKING, Dict, Any
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import Qt

from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import (
    START_POS,
    END_POS,
    BLUE_ATTRS,
    RED_ATTRS,
    MOTION_TYPE,
    GRID_MODE,
)
from utils.path_helpers import get_my_photos_path
from main_window.main_widget.grid_mode_checker import GridModeChecker

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class PictographDatasetExporter:
    """
    Class for exporting all pictographs from the pictograph dataset as individual images.
    """

    def __init__(self, image_export_tab: "ImageExportTab"):
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget

    def export_all_pictographs(self):
        """
        Export all pictographs from the dataset as individual images.
        """
        # Ask the user for a directory to save the images
        directory = self._get_export_directory()
        if not directory:
            return  # User canceled

        # Get the pictograph dataset
        pictograph_dataset = self.main_widget.pictograph_dataset

        if not pictograph_dataset:
            QMessageBox.information(
                self.image_export_tab,
                "No Pictographs",
                "No pictographs found in the dataset.",
            )
            return

        # Count total pictographs
        total_count = sum(
            len(pictographs) for pictographs in pictograph_dataset.values()
        )

        # Create a progress dialog
        progress = QProgressDialog(
            "Exporting pictographs...", "Cancel", 0, total_count, self.image_export_tab
        )
        progress.setWindowTitle("Exporting Pictographs")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()

        # Export each pictograph
        exported_count = 0
        try:
            for letter_enum, pictograph_dicts in pictograph_dataset.items():
                letter = letter_enum.value

                # We'll create subdirectories later based on grid mode

                for i, pictograph_data in enumerate(pictograph_dicts):
                    if progress.wasCanceled():
                        break

                    try:
                        # Determine the correct grid mode for this pictograph
                        grid_mode = GridModeChecker.get_grid_mode(pictograph_data)

                        # Skip if grid mode is None or skewed
                        if not grid_mode or grid_mode == "skewed":
                            print(
                                f"Skipping pictograph with invalid grid mode: {grid_mode}"
                            )
                            continue

                        # Create a temporary pictograph with the data
                        pictograph = self._create_pictograph_from_data(
                            pictograph_data, grid_mode
                        )

                        # Create a filename
                        start_pos = pictograph_data.get(START_POS, "unknown")
                        end_pos = pictograph_data.get(END_POS, "unknown")
                        blue_motion = pictograph_data.get(BLUE_ATTRS, {}).get(
                            MOTION_TYPE, "unknown"
                        )
                        red_motion = pictograph_data.get(RED_ATTRS, {}).get(
                            MOTION_TYPE, "unknown"
                        )

                        # Create subdirectories: first by grid mode, then by letter
                        grid_dir = os.path.join(directory, grid_mode)
                        letter_dir = os.path.join(grid_dir, letter)
                        os.makedirs(letter_dir, exist_ok=True)

                        filename = f"{letter}_{start_pos}_{end_pos}_{blue_motion}_{red_motion}.png"
                        filepath = os.path.join(letter_dir, filename)

                        # Create image from pictograph
                        image = self._create_pictograph_image(pictograph)

                        # Save image
                        image.save(filepath, "PNG")
                        exported_count += 1

                    except Exception as e:
                        print(f"Error exporting pictograph {letter}_{i}: {e}")

                    # Update progress
                    progress.setValue(exported_count)

        finally:
            progress.close()

        # Show completion message
        if exported_count > 0:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                f"Successfully exported {exported_count} pictographs to {directory} (organized by grid mode and letter)"
            )

            # Open the directory
            os.startfile(directory)
        else:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "No pictographs were exported."
            )

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

    def _create_pictograph_from_data(
        self, pictograph_data: Dict[str, Any], grid_mode: str
    ) -> LegacyPictograph:
        """
        Create a pictograph instance from pictograph data.

        Args:
            pictograph_data: The pictograph data dictionary
            grid_mode: The grid mode to use (box or diamond)

        Returns:
            A pictograph instance with the data applied
        """
        # Create a new pictograph
        pictograph = LegacyPictograph()

        # Add grid mode to the data
        data_copy = pictograph_data.copy()
        data_copy[GRID_MODE] = grid_mode

        # Update the pictograph with the data
        pictograph.managers.updater.update_pictograph(data_copy)

        return pictograph

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
