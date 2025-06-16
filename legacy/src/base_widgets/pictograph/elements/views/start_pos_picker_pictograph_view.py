from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QSize
from typing import Callable

from base_widgets.pictograph.elements.views.bordered_pictograph_view import (
    BorderedPictographView,
)


if TYPE_CHECKING:
    from .....main_window.main_widget.construct_tab.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class StartPosPickerPictographView(BorderedPictographView):
    def __init__(
        self,
        start_pos_picker: "StartPosPicker",
        pictograph: "LegacyPictograph",
        size_provider: Callable[[], QSize],
    ) -> None:
        super().__init__(pictograph)
        self.start_pos_picker = start_pos_picker
        self.pictograph = pictograph
        self.start_position_adder = start_pos_picker.beat_frame.start_position_adder
        self.size_provider = size_provider

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_position_adder.add_start_pos_to_sequence(self.pictograph)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        size = self.size_provider().width() // 10
        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width
        self.pictograph.elements.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
