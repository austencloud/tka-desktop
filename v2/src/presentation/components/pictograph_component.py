"""
Unified pictograph component for Kinetic Constructor v2.
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

from src.presentation.components.pictograph_scene import PictographScene
from ...domain.models.core_models import BeatData


class PictographComponent(QWidget):
    pictograph_updated = pyqtSignal(object)

    def __init__(self, parent: Optional[QWidget] = None):
        # Validate parent before proceeding
        if parent is not None:
            try:
                # Test if parent is still valid
                _ = parent.isVisible()
            except RuntimeError:
                print(f"❌ Parent widget deleted, cannot create PictographComponent")
                raise RuntimeError("Parent widget has been deleted")

        super().__init__(parent)

        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[PictographScene] = None
        self.view: Optional[QGraphicsView] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)

            # Create scene with explicit parent to improve lifecycle management
            self.scene = PictographScene(parent=self)
            self.view = QGraphicsView(self.scene, parent=self)
            self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.view.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )
            self.view.setFrameStyle(0)

            layout.addWidget(self.view)
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.setMinimumSize(100, 100)
            self._fit_view()
        except RuntimeError as e:
            print(f"❌ Failed to setup PictographComponent UI: {e}")
            # Create minimal fallback UI
            from PyQt6.QtWidgets import QLabel

            layout = QVBoxLayout(self)
            fallback_label = QLabel("Pictograph Error")
            layout.addWidget(fallback_label)

    def update_from_beat(self, beat_data: BeatData) -> None:
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

    def cleanup(self) -> None:
        """Cleanup resources to prevent memory leaks"""
        try:
            if self.scene:
                self.scene.clear()
                self.scene.setParent(None)
                self.scene = None
            if self.view:
                self.view.setParent(None)
                self.view = None
        except RuntimeError:
            # Objects already deleted
            pass

    def _fit_view(self) -> None:
        if self.view and self.scene:
            try:
                self.view.resetTransform()
                container_size = min(self.view.width(), self.view.height())
                scene_size = self.scene.SCENE_SIZE
                target_scale = (container_size * 0.9) / scene_size
                self.view.scale(target_scale, target_scale)
                self.view.centerOn(self.scene.CENTER_X, self.scene.CENTER_Y)
            except RuntimeError:
                # View or scene has been deleted
                pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._fit_view()
