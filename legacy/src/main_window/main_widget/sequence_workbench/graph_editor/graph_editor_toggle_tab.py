# graph_editor_toggle_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.graph_editor.legacy_graph_editor import (
        LegacyGraphEditor,
    )

# Define transparency value for easy modification
OPACITY = 0.7

# Define common gradients as constants for readability
BLUESTEEL_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #1e3c72,
        stop: 0.3 #6c9ce9,
        stop: 0.6 #4a77d4,
        stop: 1 #2a52be
    )
"""

SILVER_GRADIENT = f"""
    qlineargradient(
        spread: pad,
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(80, 80, 80, {OPACITY}),
        stop: 0.3 rgba(160, 160, 160, {OPACITY}),
        stop: 0.6 rgba(120, 120, 120, {OPACITY}),
        stop: 1 rgba(40, 40, 40, {OPACITY})
    )
"""


class GraphEditorToggleTab(QWidget):
    """Toggle tab widget to expand/collapse the GraphEditor."""

    def __init__(self, graph_editor: "LegacyGraphEditor") -> None:
        super().__init__(graph_editor.sequence_workbench)
        self.graph_editor = graph_editor
        self.sequence_workbench = graph_editor.sequence_workbench
        self._setup_layout()
        self._setup_components()
        self.move(0, self.sequence_workbench.height() - self.height())
        self.raise_()

    def _setup_components(self):
        self.label = QLabel("Editor", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.label)
        self.label.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                font-weight: bold;
                border-radius: 10px;
                background: {SILVER_GRADIENT};
            }}
            QLabel:hover {{
                color: white;
                font-weight: bold;
                background: {BLUESTEEL_GRADIENT};
                border-radius: 10px;
                border: 1px solid white;
            }}
        """
        )

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def mousePressEvent(self, event) -> None:
        toggler = self.graph_editor.animator
        if toggler:
            toggler.toggle()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setFixedHeight(self.sequence_workbench.main_widget.height() // 20)
        self.setFixedWidth(self.sequence_workbench.width() // 8)
        font_size = self.height() // 3
        font = QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        family = "Georgia"
        self.label.setFont(QFont(family, font_size))
        self.setStyleSheet("background-color: white")

    def reposition_toggle_tab(self):
        sequence_workbench_height = self.sequence_workbench.height()
        graph_editor_height = (
            self.sequence_workbench.height()
            - self.sequence_workbench.graph_editor.get_graph_editor_height()
        )
        if self.graph_editor.is_toggled:
            self.move(0, graph_editor_height - self.height())
        else:
            self.move(0, sequence_workbench_height - self.height())
