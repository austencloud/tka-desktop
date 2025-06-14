# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont

from interfaces.settings_manager_interface import ISettingsManager


class PagePreviewColumnSelector(QFrame):
    column_count_changed = pyqtSignal(int)

    def __init__(self, settings_manager, sidebar_width: int = 200):
        super().__init__()
        self.settings_manager:"ISettingsManager" = settings_manager
        self.sidebar_width = sidebar_width
        self.setObjectName("columnFrame")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(8)

        self.create_label()
        self.create_dropdown()

        layout.addWidget(self.column_label)
        layout.addWidget(self.column_dropdown)

    def create_label(self):
        self.column_label = QLabel("Preview Columns")
        self.column_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.column_label.setWordWrap(True)
        self.column_label.setToolTip(
            "Controls ONLY how many page previews appear side-by-side in the UI"
        )

        label_font_size = min(max(11, int(self.sidebar_width / 18)), 13)
        label_font = QFont()
        label_font.setPointSize(label_font_size)
        label_font.setWeight(QFont.Weight.Medium)
        self.column_label.setFont(label_font)
        self.column_label.setObjectName("columnLabel")

    def create_dropdown(self):
        self.column_dropdown = QComboBox()
        self.column_dropdown.addItems(["2", "3", "4", "5", "6"])
        self.column_dropdown.setObjectName("columnDropdown")
        self.column_dropdown.setFixedHeight(32)
        self.column_dropdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        current_count = int(
            self.settings_manager.get_setting("sequence_card_tab", "column_count", 3)
        )
        index = self.column_dropdown.findText(str(current_count))
        if index >= 0:
            self.column_dropdown.setCurrentIndex(index)

        self.column_dropdown.currentIndexChanged.connect(
            lambda: self.column_count_changed.emit(
                int(self.column_dropdown.currentText())
            )
        )

    def get_current_count(self) -> int:
        return int(self.column_dropdown.currentText())
