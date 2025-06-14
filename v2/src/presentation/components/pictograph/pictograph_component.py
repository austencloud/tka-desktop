"""
Direct pictograph view for Kinetic Constructor v2 - matches v1 container hierarchy.
"""

from typing import Optional
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter

from domain.models.core_models import BeatData

from .pictograph_scene import PictographScene


class PictographComponent(QGraphicsView):
    pictograph_updated = pyqtSignal(object)

    def __init__(self, parent: Optional[QGraphicsView] = None):
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError:
                print(f"❌ Parent widget deleted, cannot create PictographComponent")
                raise RuntimeError("Parent widget has been deleted")

        super().__init__(parent)

        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[PictographScene] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        try:
            self.scene = PictographScene(parent=self)
            self.setScene(self.scene)

            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setFrameStyle(0)

            self.setContentsMargins(0, 0, 0, 0)
            viewport = self.viewport()
            if viewport:
                viewport.setContentsMargins(0, 0, 0, 0)
            self.setViewportMargins(0, 0, 0, 0)
            self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            self._fit_view()
        except RuntimeError as e:
            print(f"❌ Failed to setup PictographComponent UI: {e}")

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
        try:
            if self.scene:
                self.scene.clear()
                self.scene.setParent(None)
                self.scene = None
        except RuntimeError:
            pass

    def _fit_view(self) -> None:
        if self.scene:
            try:
                self.resetTransform()

                scene_size = (950, 950)
                view_size = self.size()

                view_scale = min(
                    view_size.width() / scene_size[0],
                    view_size.height() / scene_size[1],
                )

                self.scale(view_scale, view_scale)
                self.centerOn(self.scene.CENTER_X, self.scene.CENTER_Y)
            except RuntimeError:
                pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._fit_view()
