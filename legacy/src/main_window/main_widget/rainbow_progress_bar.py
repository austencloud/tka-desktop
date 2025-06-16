from typing import LiteralString
from PyQt6.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt


class RainbowProgressBar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_components()
        self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.loading_label)
        layout.addStretch(1)
        layout.addWidget(self.percentage_label)
        layout.addStretch(1)
        layout.addWidget(self.progress_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

    def _setup_components(self) -> None:
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(self._get_stylesheet())

        self.loading_label = QLabel("Loading...", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.percentage_label = QLabel("0%", self)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_value(self, value) -> None:
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")

    def _get_stylesheet(self) -> LiteralString:
        stylesheet = """
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background-color: #E0E0E0;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0, 
                    stop:0 red, 
                    stop:0.16 orange, 
                    stop:0.33 yellow, 
                    stop:0.49 green, 
                    stop:0.66 blue, 
                    stop:0.82 indigo, 
                    stop:1 violet
                );
            }
        """
        return stylesheet
