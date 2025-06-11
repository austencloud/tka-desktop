#!/usr/bin/env python3
"""
Standalone Beat Renderer - Renders beats onto images.

This module handles the rendering of beat data onto QImage objects,
creating visual representations of sequence beats without dependencies
on the main application's beat view system.
"""

from typing import Dict, List, Optional
from PyQt6.QtGui import QImage, QPainter, QPixmap, QFont, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QRect


class StandaloneBeatRenderer:
    """
    Renderer for drawing beats onto images.

    This class creates visual representations of beats using simplified
    rendering logic that doesn't depend on the main application's components.
    """

    def __init__(self):
        """Initialize the beat renderer."""
        pass

    def render_beats(
        self,
        image: QImage,
        beat_data_list: List[Dict],
        columns: int,
        rows: int,
        beat_size: int,
        include_start_position: bool = False,
        start_pos_data: Optional[Dict] = None,
        additional_height_top: int = 0,
        add_beat_numbers: bool = True,
        add_reversal_symbols: bool = True,
    ) -> None:
        """
        Render all beats onto the image.

        Args:
            image: QImage to render onto
            beat_data_list: List of beat data dictionaries
            columns: Number of columns in layout
            rows: Number of rows in layout
            beat_size: Size of each beat in pixels
            include_start_position: Whether to include start position
            start_pos_data: Start position data dictionary
            additional_height_top: Additional height at top for overlays
            add_beat_numbers: Whether to add beat numbers
            add_reversal_symbols: Whether to add reversal symbols
        """
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        try:
            # Render start position if included
            if include_start_position and start_pos_data:
                self._render_start_position(
                    painter, start_pos_data, beat_size, additional_height_top
                )

            # Render each beat
            for i, beat_data in enumerate(beat_data_list):
                self._render_single_beat(
                    painter=painter,
                    beat_data=beat_data,
                    beat_index=i,
                    columns=columns,
                    beat_size=beat_size,
                    include_start_position=include_start_position,
                    additional_height_top=additional_height_top,
                    add_beat_numbers=add_beat_numbers,
                    add_reversal_symbols=add_reversal_symbols,
                )

        finally:
            painter.end()

    def _render_start_position(
        self,
        painter: QPainter,
        start_pos_data: Dict,
        beat_size: int,
        additional_height_top: int,
    ) -> None:
        """
        Render the start position.

        Args:
            painter: QPainter instance
            start_pos_data: Start position data
            beat_size: Size of the beat area
            additional_height_top: Top margin
        """
        x, y = 0, additional_height_top
        rect = QRect(x, y, beat_size, beat_size)

        # Draw start position background
        painter.fillRect(rect, QColor(240, 248, 255))  # Light blue background

        # Draw border
        painter.setPen(QPen(QColor(100, 149, 237), 3))  # Cornflower blue border
        painter.drawRect(rect)

        # Draw start position label
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))

        start_pos = start_pos_data.get("start_pos", "START")
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"START\n{start_pos}")

    def _render_single_beat(
        self,
        painter: QPainter,
        beat_data: Dict,
        beat_index: int,
        columns: int,
        beat_size: int,
        include_start_position: bool,
        additional_height_top: int,
        add_beat_numbers: bool,
        add_reversal_symbols: bool,
    ) -> None:
        """
        Render a single beat.

        Args:
            painter: QPainter instance
            beat_data: Beat data dictionary
            beat_index: Index of the beat
            columns: Number of columns
            beat_size: Size of each beat
            include_start_position: Whether start position is included
            additional_height_top: Top margin
            add_beat_numbers: Whether to add beat numbers
            add_reversal_symbols: Whether to add reversal symbols
        """
        # Calculate position
        position_index = beat_index
        if include_start_position:
            position_index += 1

        col = position_index % columns
        row = position_index // columns

        x = col * beat_size
        y = row * beat_size + additional_height_top

        rect = QRect(x, y, beat_size, beat_size)

        # Draw beat background
        painter.fillRect(rect, Qt.GlobalColor.white)

        # Draw border
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawRect(rect)

        # Draw beat content
        self._draw_beat_content(painter, rect, beat_data)

        # Add beat number if requested
        if add_beat_numbers:
            self._draw_beat_number(painter, rect, beat_data.get("beat_number", 0))

        # Add reversal symbols if requested
        if add_reversal_symbols:
            self._draw_reversal_symbols(painter, rect, beat_data)

    def _draw_beat_content(
        self, painter: QPainter, rect: QRect, beat_data: Dict
    ) -> None:
        """
        Draw the main content of a beat.

        Args:
            painter: QPainter instance
            rect: Rectangle to draw in
            beat_data: Beat data dictionary
        """
        # Draw letter in center
        letter = beat_data.get("letter", "?")
        font = QFont("Arial", 72, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))

        # Center the letter
        letter_rect = QRect(
            rect.x(), rect.y() + rect.height() // 3, rect.width(), rect.height() // 3
        )
        painter.drawText(letter_rect, Qt.AlignmentFlag.AlignCenter, letter)

        # Draw position information
        start_pos = beat_data.get("start_pos", "")
        end_pos = beat_data.get("end_pos", "")

        font = QFont("Arial", 16)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.darkBlue))

        # Draw start position (top)
        start_rect = QRect(rect.x() + 10, rect.y() + 10, rect.width() - 20, 30)
        painter.drawText(
            start_rect, Qt.AlignmentFlag.AlignCenter, f"Start: {start_pos}"
        )

        # Draw end position (bottom)
        end_rect = QRect(
            rect.x() + 10, rect.y() + rect.height() - 40, rect.width() - 20, 30
        )
        painter.drawText(end_rect, Qt.AlignmentFlag.AlignCenter, f"End: {end_pos}")

        # Draw motion type
        motion_type = beat_data.get("motion_type", "static")
        motion_rect = QRect(
            rect.x() + 10, rect.y() + rect.height() - 70, rect.width() - 20, 30
        )
        painter.drawText(motion_rect, Qt.AlignmentFlag.AlignCenter, motion_type.title())

    def _draw_beat_number(
        self, painter: QPainter, rect: QRect, beat_number: int
    ) -> None:
        """
        Draw beat number in the top-left corner.

        Args:
            painter: QPainter instance
            rect: Rectangle to draw in
            beat_number: Beat number to display
        """
        # Draw background circle
        circle_size = 40
        circle_rect = QRect(rect.x() + 10, rect.y() + 10, circle_size, circle_size)

        painter.setBrush(QBrush(QColor(255, 215, 0)))  # Gold background
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(circle_rect)

        # Draw number
        font = QFont("Arial", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.drawText(circle_rect, Qt.AlignmentFlag.AlignCenter, str(beat_number))

    def _draw_reversal_symbols(
        self, painter: QPainter, rect: QRect, beat_data: Dict
    ) -> None:
        """
        Draw reversal symbols if applicable.

        Args:
            painter: QPainter instance
            rect: Rectangle to draw in
            beat_data: Beat data dictionary
        """
        # Check for reversals in blue and red attributes
        blue_attrs = beat_data.get("blue_attributes", {})
        red_attrs = beat_data.get("red_attributes", {})

        # Simple reversal detection (this would be more complex in the real system)
        blue_reversal = blue_attrs.get("prop_rot_dir") != beat_data.get("prop_rot_dir")
        red_reversal = red_attrs.get("prop_rot_dir") != beat_data.get("prop_rot_dir")

        if blue_reversal or red_reversal:
            # Draw reversal indicator
            symbol_rect = QRect(rect.x() + rect.width() - 50, rect.y() + 10, 40, 40)
            painter.setBrush(QBrush(QColor(255, 100, 100)))  # Red background
            painter.setPen(QPen(Qt.GlobalColor.darkRed, 2))
            painter.drawEllipse(symbol_rect)

            # Draw "R" for reversal
            font = QFont("Arial", 20, QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QPen(Qt.GlobalColor.white))
            painter.drawText(symbol_rect, Qt.AlignmentFlag.AlignCenter, "R")

    def create_placeholder_beat(self, beat_size: int) -> QPixmap:
        """
        Create a placeholder beat pixmap.

        Args:
            beat_size: Size of the beat

        Returns:
            QPixmap with placeholder content
        """
        pixmap = QPixmap(beat_size, beat_size)
        pixmap.fill(Qt.GlobalColor.lightGray)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw placeholder content
        painter.setPen(QPen(Qt.GlobalColor.darkGray, 2))
        painter.drawRect(0, 0, beat_size, beat_size)

        font = QFont("Arial", 48)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.darkGray))
        painter.drawText(0, 0, beat_size, beat_size, Qt.AlignmentFlag.AlignCenter, "?")

        painter.end()
        return pixmap
