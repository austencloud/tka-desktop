# src/main_window/main_widget/sequence_card_tab/tab.py
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QProgressBar,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab


class SequenceCardHeader(QFrame):
    def __init__(self, parent: "SequenceCardTab"):
        super().__init__(parent)
        self.sequence_car_tab = parent
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName("sequenceCardHeader")
        self.setStyleSheet(
            """
            #sequenceCardHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 1px solid #4a5568;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        self.title_label = self._create_title()
        self.description_label = self._create_description()
        self.progress_container = self._create_progress()
        self.button_layout = self._create_buttons()

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.progress_container)
        layout.addLayout(self.button_layout)

    def _create_title(self):
        title_label = QLabel("Sequence Card Manager")
        title_label.setObjectName("sequenceCardTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #ffffff; letter-spacing: 0.5px;")
        return title_label

    def _create_description(self):
        description_label = QLabel("Select a sequence length to view cards")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet(
            """
            color: #bdc3c7;
            font-size: 13px;
            font-style: italic;
        """
        )
        return description_label

    def _create_progress(self):
        progress_container = QFrame()
        progress_container.setFixedHeight(20)
        progress_container.setStyleSheet("background: transparent;")
        progress_container_layout = QVBoxLayout(progress_container)
        progress_container_layout.setContentsMargins(0, 0, 0, 0)
        progress_container_layout.setSpacing(0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% (%v/%m)")
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: none;
                border-radius: 6px;
                text-align: center;
                background-color: rgba(0, 0, 0, 0.15);
                color: rgba(255, 255, 255, 0.9);
                font-size: 10px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 6px;
            }
            """
        )

        progress_container_layout.addWidget(self.progress_bar)
        self.progress_bar.hide()
        progress_container.setVisible(False)
        return progress_container

    def _create_buttons(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.export_button = self._create_action_button(
            "Export Pages", self.sequence_car_tab.page_exporter.export_all_pages_as_images
        )
        self.refresh_button = self._create_action_button(
            "Refresh", self.sequence_car_tab.load_sequences
        )
        self.regenerate_button = self._create_action_button(
            "Regenerate Images", self.sequence_car_tab.regenerate_all_images
        )

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.addStretch()

        return button_layout

    def _create_action_button(self, text: str, callback) -> QPushButton:
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 1px solid #5dade2;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                border: 1px solid #85c1e9;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
                border: 1px solid #3498db;
            }
        """
        )
        return button
