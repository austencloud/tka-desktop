# graph_editor_toggle_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorToggleTab(QWidget):
    """Toggle tab widget to expand/collapse the GraphEditor."""

    toggled = pyqtSignal()

    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.sequence_widget)
        self.graph_editor = graph_editor
        self.sequence_widget = graph_editor.sequence_widget
        self._setup_layout()
        self._setup_components()
        self.move(0, self.sequence_widget.height() - self.height())
        self.raise_()

    def _setup_components(self):
        self.label = QLabel("Editor", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.label)

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
        self.setFixedHeight(self.sequence_widget.main_widget.height() // 20)
        font_size = self.height() // 3
        font = QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        family = "Georgia"
        self.label.setFont(QFont(family, font_size))
        self.setStyleSheet("background-color: white")

    def reposition_toggle_tab(self):
        sequence_widget_height = self.sequence_widget.height()
        graph_editor_height = (
            self.sequence_widget.height()
            - self.sequence_widget.graph_editor.get_graph_editor_height()
        )
        if self.graph_editor.is_toggled:
            self.move(0, graph_editor_height - self.height())
        else:
            self.move(0, sequence_widget_height - self.height())

    def enterEvent(self, event) -> None:
        self.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setStyleSheet("background-color: white; border: none;")
        super().leaveEvent(event)
