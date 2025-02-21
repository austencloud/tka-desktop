from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QColor

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateSequenceButton(QPushButton):
    def __init__(
        self, sequence_generator_widget: "GenerateTab", text: str, overwrite: bool
    ):
        super().__init__(sequence_generator_widget)
        self.clicked.connect(
            lambda: sequence_generator_widget.controller.handle_generate_sequence(
                overwrite=overwrite
            )
        )

        self.sequence_generator_widget = sequence_generator_widget
        self.main_widget = sequence_generator_widget.main_widget

        # Initialize button properties
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)

        # Setup animations
        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(100)

        # Connect press and release events
        self.pressed.connect(self._handle_press)
        self.released.connect(self._handle_release)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.main_widget.width()
        font_size = width // 75
        button_height = self.main_widget.height() // 14
        border_radius = button_height // 4

        self.setStyleSheet(
            f"""
            QPushButton {{
                font-size: {font_size}px;
                padding: 8px;
                border-radius: {border_radius}px;
                background-color: #2196F3;
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """
        )

        self.setFixedWidth(self.main_widget.width() // 6)
        self.setFixedHeight(button_height)

    def _handle_press(self):
        # Create press animation
        self.click_animation.setStartValue(self.geometry())
        compressed = self.geometry()
        compressed.setHeight(int(compressed.height() * 0.95))
        compressed.setWidth(int(compressed.width() * 0.95))

        self.click_animation.setEndValue(compressed)
        self.click_animation.start()

    def _handle_release(self):
        # Create release animation
        self.click_animation.setStartValue(self.geometry())
        self.click_animation.setEndValue(self.geometry())
        self.click_animation.start()

    def disconnect(self):
        self.clicked.disconnect()
        self.pressed.disconnect()
        self.released.disconnect()
