from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .generate_tab import GenerateTab

class GenerateSequenceButton(QPushButton):
    def __init__(self, sequence_generator_widget: "GenerateTab"):
        super().__init__(sequence_generator_widget)
        sequence_generator_widget = sequence_generator_widget
        self.main_widget = sequence_generator_widget.main_widget
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("font-size: 16px; padding: 8px;")
        self.setText("Generate Sequence")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        """Resize the button based on the main widget's width."""
        width = self.main_widget.width()
        font_size = width // 75
        self.setStyleSheet(f"font-size: {font_size}px;")
        self.updateGeometry()
        self.repaint()
        self.setFixedWidth(self.main_widget.width() // 4)
        self.setFixedHeight(self.main_widget.height() // 14)
