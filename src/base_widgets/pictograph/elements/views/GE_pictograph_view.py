# GE_pictograph_view.py (modifications)
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QPen, QColor, QCursor

from data.constants import GOLD
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph_view_mouse_event_handler import (
    GE_PictographViewMouseEventHandler,
)
from main_window.main_widget.sequence_workbench.graph_editor.graph_editor_view_key_event_handler import (
    GraphEditorViewKeyEventHandler,
)
from main_window.main_widget.hotkey_graph_adjuster.hotkey_graph_adjuster import (
    HotkeyGraphAdjuster,
)
from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph import (
    GE_Pictograph,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_pictograph_container import (
        GraphEditorPictographContainer,
    )
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat


class GE_PictographView(QGraphicsView):
    """GraphicsView for GE_Pictograph in the Graph Editor."""

    def __init__(
        self,
        pictograph_container: "GraphEditorPictographContainer",
        pictograph: "GE_Pictograph",
    ) -> None:
        super().__init__(pictograph_container)
        self.pictograph_container = pictograph_container
        self.pictograph = pictograph
        self.graph_editor = pictograph_container.graph_editor
        self.main_widget = self.graph_editor.main_widget
        self.reference_beat: Optional["Beat"] = None
        self.is_start_pos = False

        # Connect to state signals
        self.state = self.graph_editor.state
        self._connect_state_signals()

        # Set up event handlers
        self.mouse_event_handler = GE_PictographViewMouseEventHandler(self)
        self.key_event_handler = GraphEditorViewKeyEventHandler(self)
        self.hotkey_graph_adjuster = HotkeyGraphAdjuster(self)

        # Set up view properties
        self.setScene(pictograph)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

    def _connect_state_signals(self) -> None:
        """Connect to centralized state signals."""
        self.state.selected_arrow_changed.connect(self._handle_arrow_selection_changed)

    def set_to_blank_grid(self) -> None:
        self.pictograph = GE_Pictograph(self)
        self.setScene(self.pictograph)
        self.pictograph.elements.view = self

    def _handle_arrow_selection_changed(self, arrow) -> None:
        self.update()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events."""
        self.mouse_event_handler.handle_mouse_press(event)
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:
        """Handle key press events."""
        if not self.key_event_handler.handle_key_press(event):
            super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_event_handler.handle_mouse_press(event)
        QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        from main_window.main_widget.sequence_workbench.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
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
