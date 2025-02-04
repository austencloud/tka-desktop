from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout, QFrame
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)

from .beat_view import BeatView


if TYPE_CHECKING:
    from .layout_options_dialog import LayoutOptionsDialog


class LayoutOptionsBeatFrame(QFrame):
    """This class is responsible for displaying a preview of the selected layout options inside the layout options dialog."""

    def __init__(self, dialog: "LayoutOptionsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self.sequence_widget = dialog.sequence_widget
        self.main_widget = self.sequence_widget.main_widget
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview(self):
        # Clear the layout first
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        if not self.dialog.panel.sequence_growth_checkbox.isChecked():
            num_beats = int(self.dialog.panel.beats_combo_box.currentText())
            selected_layout = self.dialog.panel.layout_combo_box.currentText()

            if selected_layout:
                cols, rows = map(int, selected_layout.split(" x "))

                cols_with_start_pos = cols + 1
                rows_with_start_pos = rows + 1
                beat_size = min(
                    self.dialog.width() // cols_with_start_pos,
                    int(self.dialog.height() * 0.75) // rows_with_start_pos,
                )

                if self.layout.count() == 0:
                    start_pos_view = StartPositionBeatView(self)
                    start_pos_view.setParent(self)  # Ensure proper parenting
                    self.layout.addWidget(start_pos_view, 0, 0)
                    start_pos_view.start_pos.initializer.set_nonradial_points_visibility(
                        False
                    )
                    start_pos_view.setFixedSize(beat_size, beat_size)

                    beat_index = 0
                    for row in range(rows):
                        for col in range(1, cols + 1):
                            if beat_index < num_beats:
                                beat_view = BeatView(self, beat_index + 1)
                                beat_view.setParent(self)  # Ensure proper parenting
                                self.layout.addWidget(beat_view, row, col)
                                beat_view.setFixedSize(beat_size, beat_size)
                                beat_index += 1
                                beat_view.blank_beat.initializer.set_nonradial_points_visibility(
                                    False
                                )
