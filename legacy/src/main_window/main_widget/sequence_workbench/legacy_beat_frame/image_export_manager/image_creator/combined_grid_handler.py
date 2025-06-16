from typing import TYPE_CHECKING
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtCore import Qt
from data.constants import BOX, DIAMOND
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.beat_view import LegacyBeatView
    from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_creator.image_creator import (
        ImageCreator,
    )


class CombinedGridHandler:
    """
    Handles the creation and rendering of combined diamond and box grids for image export.
    """

    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.beat_frame = image_creator.beat_frame
        self.diamond_grid_path = get_image_path(f"grid/{DIAMOND}_grid.svg")
        self.box_grid_path = get_image_path(f"grid/{BOX}_grid.svg")

    def process_beat_for_combined_grids(
        self, beat_view: "LegacyBeatView", beat_size: int
    ) -> QPixmap:
        """
        Process a beat view to show both diamond and box grids.

        Args:
            beat_view: The beat view to process
            beat_size: The size of the beat in pixels

        Returns:
            A QPixmap with both grids visible
        """
        # Create a copy of the beat with both grids visible
        beat_pixmap = self._grab_pixmap_with_combined_grids(beat_view, beat_size)

        return beat_pixmap

    def _grab_pixmap_with_combined_grids(
        self, beat_view: "LegacyBeatView", beat_size: int
    ) -> QPixmap:
        """
        Grab a pixmap of the beat with both diamond and box grids visible.

        Args:
            beat_view: The beat view to grab
            beat_size: The size of the beat in pixels

        Returns:
            A QPixmap with both grids visible
        """
        # First grab the normal beat pixmap
        normal_pixmap = beat_view.beat.grabber.grab().scaled(
            beat_size,
            beat_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Create a new image to draw on
        combined_image = QImage(
            normal_pixmap.width(), normal_pixmap.height(), QImage.Format.Format_ARGB32
        )
        combined_image.fill(Qt.GlobalColor.transparent)

        # Draw the normal beat pixmap
        painter = QPainter(combined_image)
        painter.drawPixmap(0, 0, normal_pixmap)

        # Get the current grid mode
        current_grid_mode = beat_view.beat.state.grid_mode

        # Draw the other grid on top with some transparency
        if current_grid_mode == DIAMOND:
            # Add the box grid
            self._draw_grid_with_transparency(painter, self.box_grid_path, beat_size)
        elif current_grid_mode == BOX:
            # Add the diamond grid
            self._draw_grid_with_transparency(
                painter, self.diamond_grid_path, beat_size
            )

        painter.end()

        return QPixmap.fromImage(combined_image)

    def _draw_grid_with_transparency(
        self, painter: QPainter, grid_path: str, size: int
    ) -> None:
        """
        Draw a grid with transparency on the painter.

        Args:
            painter: The QPainter to draw on
            grid_path: The path to the grid SVG
            size: The size to draw the grid
        """
        from PyQt6.QtSvg import QSvgRenderer

        # Create a temporary image for the grid
        grid_image = QImage(size, size, QImage.Format.Format_ARGB32)
        grid_image.fill(Qt.GlobalColor.transparent)

        # Draw the SVG onto the image
        grid_painter = QPainter(grid_image)
        renderer = QSvgRenderer(grid_path)
        renderer.render(grid_painter)
        grid_painter.end()

        # Set opacity for the grid to full opacity (no transparency)
        painter.setOpacity(1.0)  # 100% opacity

        # Draw the grid image onto the main image
        painter.drawImage(0, 0, grid_image)
