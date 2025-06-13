from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent, QPainter

from src.domain.models.core_models import BeatData


class ModernPictographContainer(QWidget):
    arrow_selected = pyqtSignal(str)
    beat_modified = pyqtSignal(BeatData)

    def __init__(self, parent):
        super().__init__(parent)
        self._graph_editor = parent
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self._pictograph_view = ModernPictographView(self)
        self._pictograph_view.arrow_clicked.connect(self._on_arrow_clicked)

        layout.addWidget(self._pictograph_view)

        self.setFixedSize(300, 300)
        self.setStyleSheet(
            """
            ModernPictographContainer {
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background-color: rgba(0, 0, 0, 0.1);
            }
        """
        )

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data
        self._pictograph_view.set_beat(beat_data)

    def _on_arrow_clicked(self, arrow_id: str):
        self._selected_arrow_id = arrow_id
        self.arrow_selected.emit(arrow_id)


class ModernPictographView(QGraphicsView):
    arrow_clicked = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self._container = parent
        self._current_beat: Optional[BeatData] = None

        self._setup_view()

    def _setup_view(self):
        self.setScene(QGraphicsScene())
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFrameStyle(0)
        self.setStyleSheet("background: transparent;")

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data
        self._render_beat()

    def _render_beat(self):
        if not self._current_beat:
            self.scene().clear()
            return

        # Placeholder rendering - will integrate with V1 pictograph system
        self.scene().clear()
        self.scene().addText(f"Beat: {self._current_beat}", color=Qt.GlobalColor.white)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Placeholder arrow detection - will integrate with V1 arrow system
            mock_arrow_id = "arrow_1"
            self.arrow_clicked.emit(mock_arrow_id)
        super().mousePressEvent(event)
