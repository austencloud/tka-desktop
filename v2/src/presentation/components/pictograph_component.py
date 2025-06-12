"""
Simple pictograph component for Kinetic Constructor v2.

This component renders pictographs using V2 SVG assets with modern modular architecture.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QGraphicsView,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter

from ...domain.models.core_models import BeatData
from .pictograph_scene import PictographScene


class PictographComponent(QWidget):
    """Simple pictograph component using V2 assets and modern modular architecture."""

    pictograph_updated = pyqtSignal(object)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[PictographScene] = None
        self.view: Optional[QGraphicsView] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the UI components with proper scaling to fit container."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scene = PictographScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setFrameStyle(0)

        layout.addWidget(self.view)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setMinimumSize(100, 100)
        self.resize(200, 200)

        self._fit_view()

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update the pictograph from beat data."""
        self.current_beat = beat_data
        if self.scene:
            self.scene.update_beat(beat_data)
            self._fit_view()
        self.pictograph_updated.emit(beat_data)

    def get_current_beat(self) -> Optional[BeatData]:
        return self.current_beat

    def clear_pictograph(self) -> None:
        self.current_beat = None
        if self.scene:
            self.scene.clear()

    def _fit_view(self) -> None:
        """Fit the view to properly scale and center the pictograph in container."""
        if self.view and self.scene:
            self.view.resetTransform()

            container_size = min(self.view.width(), self.view.height())

            scene_size = self.scene.SCENE_SIZE
            target_scale = (container_size * 0.9) / scene_size

            self.view.scale(target_scale, target_scale)

            self.view.centerOn(self.scene.CENTER_X, self.scene.CENTER_Y)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._fit_view()
