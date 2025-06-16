from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional

from data.constants import GOLD
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)


from base_widgets.pictograph.elements.views.beat_view import LegacyBeatView

if TYPE_CHECKING:
    from .legacy_beat_frame import LegacyBeatFrame


class BeatSelectionOverlay(QWidget):
    def __init__(self, beat_frame: "LegacyBeatFrame"):
        super().__init__(beat_frame)
        self.selected_beat: Optional[LegacyBeatView | StartPositionBeatView] = None
        self.border_color = QColor(GOLD)
        self.border_width = 4
        self.beat_frame = beat_frame
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat_view(self, beat_view: LegacyBeatView, toggle_animation=True):
        if not beat_view:
            return
        if self.selected_beat == beat_view:
            return

        if self.selected_beat:
            self.deselect_beat()

        self.selected_beat = beat_view
        self.selected_beat.is_selected = True

        self.update_overlay_position()

        self.show()

        self._update_graph_editor(toggle_animation)

        beat_view.setCursor(Qt.CursorShape.ArrowCursor)

    def _safe_show(self):
        """Safely show the widget without interrupting animations."""
        if not self.isVisible():
            self.show()

    def _update_graph_editor(self, toggle_animation: bool = False):
        """Update graph editor components."""
        # Get sequence workbench through the new widget manager system
        main_widget = self.selected_beat.beat_frame.main_widget
        try:
            sequence_workbench = main_widget.widget_manager.get_widget(
                "sequence_workbench"
            )
            if sequence_workbench:
                graph_editor = sequence_workbench.graph_editor
            else:
                # Fallback: try direct access for backward compatibility
                if hasattr(main_widget, "sequence_workbench"):
                    graph_editor = main_widget.sequence_workbench.graph_editor
                else:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(
                        "sequence_workbench not available in BeatSelectionOverlay"
                    )
                    return
        except AttributeError:
            # Fallback: try direct access for backward compatibility
            if hasattr(main_widget, "sequence_workbench"):
                graph_editor = main_widget.sequence_workbench.graph_editor
            else:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "sequence_workbench not available in BeatSelectionOverlay"
                )
                return
        graph_editor.pictograph_container.update_pictograph(self.selected_beat.beat)
        graph_editor.adjustment_panel.update_turns_panel()
        graph_editor.adjustment_panel.update_adjustment_panel()

        if toggle_animation and not graph_editor.is_toggled:
            graph_editor.animator.toggle()

    def deselect_beat(self):
        if self.selected_beat:
            self.selected_beat.is_selected = False
            self.selected_beat.setCursor(Qt.CursorShape.PointingHandCursor)
            self.selected_beat.update()

        self.selected_beat = None

        self.hide()

    def update_overlay_position(self):
        if self.selected_beat:
            self.setGeometry(self.selected_beat.geometry())
            self.raise_()
            self.update()

    def get_selected_beat(self) -> Optional[LegacyBeatView]:
        return self.selected_beat

    def paintEvent(self, event):
        if not self.selected_beat:
            return

        painter = QPainter(self)
        pen = QPen(self.border_color, self.border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        rect = self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2,
        )
        painter.drawRect(rect)
        painter.end()
