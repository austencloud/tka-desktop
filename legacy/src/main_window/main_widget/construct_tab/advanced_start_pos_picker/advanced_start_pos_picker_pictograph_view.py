from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize
from typing import Callable

from base_widgets.pictograph.elements.views.bordered_pictograph_view import (
    BorderedPictographView,
)


if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class AdvancedStartPosPickerPictographView(BorderedPictographView):
    def __init__(
        self,
        advanced_start_pos_picker: "AdvancedStartPosPicker",
        pictograph: "LegacyPictograph",
        size_provider: Callable[[], QSize],
    ):
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.picker = advanced_start_pos_picker
        self.pictograph = pictograph
        self.start_position_adder = (
            advanced_start_pos_picker.beat_frame.start_position_adder
        )
        self.size_provider = size_provider

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        size = self.size_provider().width() // 12
        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width
        self.pictograph.elements.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
