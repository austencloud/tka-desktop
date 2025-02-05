from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy


from ..GE_pictograph_view import GE_PictographView, GE_Pictograph

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.beat_frame.beat import Beat
    from ..graph_editor import GraphEditor


class GraphEditorPictographContainer(QWidget):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setup_pictograph()

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.GE_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def setup_pictograph(self):
        self.GE_pictograph = GE_Pictograph(self)
        self.GE_view = GE_PictographView(self, self.GE_pictograph)

    def update_pictograph(self, reference_beat: "Beat" = None) -> None:
        selected_beat_view = (
            self.graph_editor.sequence_workbench.beat_frame.get.currently_selected_beat_view()
        )
        if not selected_beat_view:
            return
        if not reference_beat:
            reference_beat = selected_beat_view.beat

        view = self.GE_view
        pictograph = view.pictograph

        pictograph.is_blank = False
        view.reference_beat = reference_beat
        view.is_start_pos = reference_beat.view.is_start_pos
        pictograph.blue_reversal = reference_beat.blue_reversal
        pictograph.red_reversal = reference_beat.red_reversal

        pictograph.updater.update_pictograph(reference_beat.pictograph_data)

        beat_number_text = reference_beat.beat_number_item.beat_number_int
        if beat_number_text:
            pictograph.beat_number_item.update_beat_number(beat_number_text)
        else:
            pictograph.start_text_item.add_start_text()

    def resizeEvent(self, event):
        size = self.graph_editor.height()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
