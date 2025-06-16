from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QMouseEvent, QKeyEvent, QCursor
from PyQt6.QtWidgets import QApplication
from base_widgets.pictograph.elements.views.base_pictograph_view import (
    BasePictographView,
)
from data.constants import GOLD
from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.hotkey_graph_adjuster import (
    HotkeyGraphAdjuster,
)
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph_view_mouse_event_handler import (
    GE_PictographViewMouseEventHandler,
)
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_view_key_event_handler import (
    GraphEditorViewKeyEventHandler,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import (
    GE_Pictograph,
)

if TYPE_CHECKING:
    from .....main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.legacy_GE_pictograph_container import (
        LegacyGraphEditorPictographContainer,
    )


class GE_PictographView(BasePictographView):
    reference_beat: "Beat" = None
    is_start_pos = False

    def __init__(
        self,
        container: "LegacyGraphEditorPictographContainer",
        pictograph: "GE_Pictograph",
    ) -> None:
        super().__init__(pictograph)
        self.graph_editor = container.graph_editor
        self.pictograph = pictograph
        self.main_widget = self.graph_editor.main_widget
        self.setScene(pictograph)
        self.setFrameShape(BasePictographView.Shape.Box)
        self.mouse_event_handler = GE_PictographViewMouseEventHandler(self)
        self.key_event_handler = GraphEditorViewKeyEventHandler(self)
        self.graph_editor.selection_manager.selection_changed.connect(
            self.on_selection_changed
        )
        self.hotkey_graph_adjuster = HotkeyGraphAdjuster(self)

    def on_selection_changed(self):
        self.scene().update()

    def set_to_blank_grid(self) -> None:
        self.pictograph = GE_Pictograph(self)
        self.setScene(self.pictograph)
        self.pictograph.elements.view = self

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.key_event_handler.handle_key_press(event):
            super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_event_handler.handle_mouse_press(event)
        QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        from legacy.src.main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.legacy_GE_pictograph_container import (
            LegacyGraphEditorPictographContainer,
        )

        if isinstance(self.parent(), LegacyGraphEditorPictographContainer):
            if self.mouse_event_handler.is_arrow_under_cursor(event):
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        pen = QPen(Qt.GlobalColor.black, 0)
        painter.setPen(pen)

        right_edge = self.viewport().width() - 1
        painter.drawLine(right_edge, 0, right_edge, self.viewport().height())
        overlay_color = QColor(GOLD)
        overlay_pen = QPen(overlay_color, 4)
        overlay_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(overlay_pen)

        overlay_rect = (
            self.viewport()
            .rect()
            .adjusted(
                overlay_pen.width() // 2,
                overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
            )
        )
        painter.drawRect(overlay_rect)
        painter.end()

    def resizeEvent(self, event) -> None:
        self.setFixedSize(self.graph_editor.height(), self.graph_editor.height())

        scene_size = self.scene().sceneRect().size()
        view_size = self.viewport().size()
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )
        self.resetTransform()
        self.scale(scale_factor, scale_factor)
