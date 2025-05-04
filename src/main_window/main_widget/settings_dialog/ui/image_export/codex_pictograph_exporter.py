import os
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Any, Optional
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import Qt

from base_widgets.pictograph.pictograph import Pictograph
from data.constants import GRID_MODE, PROP_TYPE, COLOR, RED, BLUE
from utils.path_helpers import get_my_photos_path, get_image_path
from main_window.main_widget.grid_mode_checker import GridModeChecker
from objects.prop.prop import Prop
from objects.prop.prop_factory import PropFactory
from svg_manager.svg_manager import SvgManager
from svg_manager.prop_svg_manager import PropSvgManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class CustomPropSvgManager(PropSvgManager):
    """
    Custom PropSvgManager that uses simple_staff.svg instead of staff.svg
    """

    def _get_prop_image_file(self, prop: "Prop") -> str:
        """Override to use simple_staff.svg for Staff props"""
        if prop.prop_type_str == "Staff":
            return "props/simple_staff.svg"
        elif prop.prop_type_str == "Hand":
            return self._get_hand_svg_file(prop)
        elif prop.prop_type_str == "Chicken":
            return f"props/chicken.png"
        else:
            return f"props/{prop.prop_type_str}.svg"


class CustomSvgManager(SvgManager):
    """
    Custom SvgManager that uses the CustomPropSvgManager
    """

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__(pictograph)
        # Replace the prop_manager with our custom one
        self.prop_manager = CustomPropSvgManager(self)


class CodexPictographExporter:
    """
    Class for exporting the default codex pictographs as individual images.
    """

    def __init__(self, image_export_tab: "ImageExportTab"):
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget

    def export_codex_pictographs(self):
        """
        Export the default codex pictographs as individual images.
        """
        # Ask the user for a directory to save the images
        directory = self._get_export_directory()
        if not directory:
            return  # User canceled

        # Get the codex data manager
        codex = self.main_widget.codex
        codex_data_manager = codex.data_manager
        pictograph_data = codex_data_manager.get_pictograph_data()

        if not pictograph_data:
            QMessageBox.information(
                self.image_export_tab,
                "No Pictographs",
                "No codex pictographs found to export.",
            )
            return

        # Count total pictographs
        total_count = sum(1 for data in pictograph_data.values() if data is not None)

        # Create a progress dialog
        progress = QProgressDialog(
            "Exporting codex pictographs...",
            "Cancel",
            0,
            total_count,
            self.image_export_tab,
        )
        progress.setWindowTitle("Exporting Codex Pictographs")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()

        # Export each pictograph
        exported_count = 0
        try:
            for letter, data in pictograph_data.items():
                if progress.wasCanceled():
                    break

                if data is None:
                    continue

                try:
                    # Determine the correct grid mode for this pictograph
                    grid_mode = GridModeChecker.get_grid_mode(data)

                    # Skip if grid mode is None or skewed
                    if not grid_mode or grid_mode == "skewed":
                        print(
                            f"Skipping pictograph with invalid grid mode: {grid_mode}"
                        )
                        continue

                    # Create a temporary pictograph with the data
                    pictograph = self._create_pictograph_from_data(data, grid_mode)

                    # Export to a single flat folder

                    # Create a simple filename with just the letter
                    filename = f"{letter}.png"

                    # Check if the file already exists (for letters with multiple pictographs)
                    filepath = os.path.join(directory, filename)
                    if os.path.exists(filepath):
                        # If the file exists, add the grid mode to differentiate
                        filename = f"{letter}-{grid_mode}.png"
                        filepath = os.path.join(directory, filename)

                    # Create image from pictograph
                    # Only add border if this is a single pictograph (total_count == 1)
                    image = self._create_pictograph_image(pictograph, total_count == 1)

                    # Save image with specific quality settings to ensure border is visible
                    image.save(filepath, "PNG", 100)  # Use maximum quality
                    exported_count += 1

                    # Verify the image was saved correctly
                    print(f"Saved pictograph to {filepath}")

                except Exception as e:
                    print(f"Error exporting codex pictograph {letter}: {e}")

                # Update progress
                progress.setValue(exported_count)

        finally:
            progress.close()

        # Show completion message
        if exported_count > 0:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                f"Successfully exported {exported_count} codex pictographs to {directory} with simple letter-based filenames"
            )

            # Open the directory
            os.startfile(directory)
        else:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "No codex pictographs were exported."
            )

    def _get_export_directory(self) -> str:
        """
        Get the directory where pictographs will be exported.

        Returns:
            The selected directory path or empty string if canceled.
        """
        # Use the default photos directory as the starting point
        default_dir = get_my_photos_path("codex_pictograph_exports")
        os.makedirs(default_dir, exist_ok=True)

        # Show directory selection dialog
        directory = QFileDialog.getExistingDirectory(
            self.image_export_tab,
            "Select Directory to Save Codex Pictographs",
            default_dir,
        )

        return directory

    def _create_pictograph_from_data(
        self, pictograph_data: Dict[str, Any], grid_mode: str
    ) -> Pictograph:
        """
        Create a pictograph instance from pictograph data.

        Args:
            pictograph_data: The pictograph data dictionary
            grid_mode: The grid mode to use (box or diamond)

        Returns:
            A pictograph instance with the data applied
        """
        # Create a new pictograph
        pictograph = Pictograph()

        # Replace the default SvgManager with our custom one that uses simple_staff.svg
        pictograph.managers.svg_manager = CustomSvgManager(pictograph)

        # Add grid mode to the data
        data_copy = pictograph_data.copy()
        data_copy[GRID_MODE] = grid_mode

        # Update the pictograph with the data
        pictograph.managers.updater.update_pictograph(data_copy)

        # Disable the default border by setting a flag
        pictograph.state.disable_borders = True

        # Create a custom view without borders
        from base_widgets.pictograph.elements.views.base_pictograph_view import (
            BasePictographView,
        )

        view = BasePictographView(pictograph)
        view.setStyleSheet("border: none;")
        pictograph.elements.view = view

        return pictograph

    def _create_pictograph_image(
        self, pictograph: Pictograph, add_border: bool = False
    ) -> QImage:
        """
        Create a QImage from a pictograph, optionally with a black border.

        Args:
            pictograph: The pictograph to convert to an image
            add_border: Whether to add a 1-pixel black border (default: False)

        Returns:
            QImage of the pictograph, with a border if requested
        """
        # Define border width
        border_width = 1 if add_border else 0  # 1-pixel border when add_border is True

        # Standard pictograph size
        standard_size = 950

        # Create the image with appropriate size
        image_size = (
            standard_size if not add_border else standard_size + (border_width * 2)
        )
        image = QImage(image_size, image_size, QImage.Format.Format_RGB32)

        # Fill with white (or black if we're adding a border)
        image.fill(Qt.GlobalColor.black if add_border else Qt.GlobalColor.white)

        # Create painter for the image
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if add_border:
            # Draw white rectangle inside the border
            painter.fillRect(
                border_width,
                border_width,
                standard_size,
                standard_size,
                Qt.GlobalColor.white,
            )

        # Calculate the rect where the pictograph should be drawn
        target_rect = image.rect()
        if add_border:
            # Adjust the target rect to account for the border
            target_rect = target_rect.adjusted(
                border_width, border_width, -border_width, -border_width
            )

        # Use the view to render the pictograph
        if hasattr(pictograph.elements, "view") and pictograph.elements.view:
            # Save the painter state before transforming
            painter.save()

            # Move to the target rect's top-left corner
            painter.translate(target_rect.topLeft())

            # Scale to fit the target rect
            scale_factor = target_rect.width() / standard_size
            painter.scale(scale_factor, scale_factor)

            # Render the pictograph
            pictograph.elements.view.render(painter)

            # Restore the painter state
            painter.restore()
        else:
            # Render directly to the target rect
            pictograph.render(painter, target_rect)

        painter.end()
        return image
