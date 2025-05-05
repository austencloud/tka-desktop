from typing import TYPE_CHECKING, Dict, Any, Optional
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import Qt

from base_widgets.pictograph.pictograph import Pictograph
from data.constants import GRID_MODE
from main_window.main_widget.grid_mode_checker import GridModeChecker
from main_window.main_widget.settings_dialog.ui.image_export.codex_pictograph_exporter import (
    CodexPictographExporter,
    CustomSvgManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class FixedCodexPictographExporter:
    """
    A modified version of the CodexPictographExporter with a fixed image creation method
    to avoid zooming issues.
    """

    def __init__(self, image_export_tab: "ImageExportTab"):
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget
        self.original_exporter = CodexPictographExporter(image_export_tab)

    def _create_pictograph_from_data(self, pictograph_data: Dict[str, Any], grid_mode: str) -> Pictograph:
        """
        Create a pictograph instance from pictograph data.
        Delegates to the original exporter.
        """
        return self.original_exporter._create_pictograph_from_data(pictograph_data, grid_mode)

    def _get_export_directory(self):
        """
        Ask the user for a directory to save the exported images.
        Delegates to the original exporter.
        """
        return self.original_exporter._get_export_directory()

    def _create_pictograph_image(self, pictograph: Pictograph, add_border: bool = False) -> QImage:
        """
        Create a QImage from a pictograph, optionally with a black border.
        This is a fixed version to avoid zooming issues.

        Args:
            pictograph: The pictograph to convert to an image
            add_border: Whether to add a border (default: False)

        Returns:
            QImage of the pictograph, with a border if requested
        """
        # Define border width
        border_width = 2 if add_border else 0  # 2-pixel border when add_border is True

        # Standard pictograph size - using a smaller size to avoid zooming
        standard_size = 800

        # Create the image with appropriate size
        image_size = standard_size + (border_width * 2)
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

            # Scale to fit the target rect - using a smaller scale factor
            scale_factor = target_rect.width() / 950  # Standard pictograph size is 950
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
