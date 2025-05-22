# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt




class SidebarHeader(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("headerFrame")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        title_label = QLabel("Filter by Length")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("headerTitle")

        subtitle_label = QLabel("Select sequence length")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("headerSubtitle")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
