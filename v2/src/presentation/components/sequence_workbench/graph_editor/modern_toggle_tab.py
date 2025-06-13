from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QFont


class ModernToggleTab(QWidget):
    toggle_requested = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self._graph_editor = parent

        self._setup_ui()
        self._position_tab()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._toggle_btn = QPushButton("Graph Editor ▲")
        self._toggle_btn.clicked.connect(self.toggle_requested.emit)
        self._toggle_btn.setFont(QFont("Arial", 9))

        self._toggle_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(80, 80, 80, 200),
                    stop: 0.3 rgba(160, 160, 160, 200),
                    stop: 0.6 rgba(120, 120, 120, 200),
                    stop: 1 rgba(40, 40, 40, 200)
                );
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px 8px 0px 0px;
                color: white;
                padding: 4px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(100, 100, 100, 220),
                    stop: 0.3 rgba(180, 180, 180, 220),
                    stop: 0.6 rgba(140, 140, 140, 220),
                    stop: 1 rgba(60, 60, 60, 220)
                );
            }
        """
        )

        layout.addWidget(self._toggle_btn)
        self.setFixedSize(self._toggle_btn.sizeHint())

    def _position_tab(self):
        if not self._graph_editor._parent_workbench:
            return

        parent = self._graph_editor._parent_workbench
        self.setParent(parent)

        x = 0
        y = parent.height() - self.height()
        self.move(x, y)
        self.raise_()

    def update_position(self):
        if not self._graph_editor._parent_workbench:
            return

        parent = self._graph_editor._parent_workbench
        x = 0

        if self._graph_editor.is_visible():
            # Position above the visible graph editor
            y = parent.height() - self._graph_editor.height() - self.height()
            self._toggle_btn.setText("Graph Editor ▼")
        else:
            # Position at bottom when graph editor is hidden
            y = parent.height() - self.height()
            self._toggle_btn.setText("Graph Editor ▲")

        self.move(x, y)
        self.raise_()
