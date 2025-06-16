from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor, QPolygon
from PyQt6.QtCore import QSize, Qt, QPoint
from src.legacy_settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class CircularSequenceIndicator(QToolButton):
    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        """Indicator that shows when a sequence is circular (ends at its start position)."""
        super().__init__(sequence_workbench)
        self.main_widget = sequence_workbench.main_widget
        self.sequence_workbench = sequence_workbench
        self.setToolTip("Circular Sequence: Ends at start position")
        self.setCheckable(False)
        self.setStyleSheet("border: none; background: transparent;")  # Clean look

        self.is_circular = False
        self.update_indicator()
        self.hide()  # Initially hidden until we know if sequence is circular

    def update_indicator(self):
        """Updates the indicator based on whether the sequence is circular."""
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()

        # Check if sequence has enough beats to be circular
        if len(sequence) < 3:  # Metadata + start position + at least one beat
            self.hide()
            return

        # Check if sequence is circular using the same logic as in SequencePropertiesManager
        if len(sequence) > 2:
            if sequence[-1].get("is_placeholder", False) and len(sequence) > 3:
                self.is_circular = sequence[-2].get("end_pos") == sequence[1].get(
                    "end_pos"
                )
            else:
                self.is_circular = sequence[-1].get("end_pos") == sequence[1].get(
                    "end_pos"
                )

            if self.is_circular:
                self.show()
                self.update_icon()
            else:
                self.hide()
        else:
            self.hide()

    def update_icon(self):
        """Creates and updates the circular indicator icon."""
        size = max(
            24, self.sequence_workbench.width() // 24
        )  # Slightly smaller than difficulty icon

        # Create a circular icon
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a circle with an arrow that loops back to itself
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(60, 145, 230))  # Blue color for the circle

        # Draw the main circle
        painter.drawEllipse(2, 2, size - 4, size - 4)

        # Draw the arrow (circular arrow symbol)
        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QColor(255, 255, 255))

        # Draw a simple circular arrow using a small circle with a gap
        painter.drawArc(5, 5, size - 10, size - 10, 45 * 16, 270 * 16)

        # Draw arrowhead
        arrow_size = size // 5
        points = QPolygon(
            [
                QPoint(size - 7, size // 2 - arrow_size // 2),
                QPoint(size - 7 + arrow_size, size // 2),
                QPoint(size - 7, size // 2 + arrow_size // 2),
            ]
        )
        painter.drawPolygon(points)

        painter.end()

        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)

    def resizeEvent(self, event):
        """Handles resize events to keep the icon properly sized."""
        super().resizeEvent(event)
        if self.is_circular:
            self.update_icon()
