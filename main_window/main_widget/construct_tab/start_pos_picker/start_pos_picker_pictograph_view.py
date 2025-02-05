from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView


if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker
    from base_widgets.base_pictograph.pictograph import Pictograph


class StartPosPickerPictographView(BorderedPictographView):
    def __init__(
        self, start_pos_picker: "StartPosPicker", pictograph: "Pictograph"
    ) -> None:
        super().__init__(pictograph)
        self.start_pos_picker = start_pos_picker
        self.pictograph = pictograph
        self.start_position_adder = (
            start_pos_picker.construct_tab.main_widget.sequence_workbench.beat_frame.start_position_adder
        )

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_position_adder.add_start_pos_to_sequence(self.pictograph)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        size = self.start_pos_picker.width() // 5
        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width
        self.pictograph.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
