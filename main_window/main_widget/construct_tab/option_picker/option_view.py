from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OptionView(BorderedPictographView):
    def __init__(
        self, option_picker: "OptionPicker", pictograph: "BasePictograph"
    ) -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.option_picker = option_picker
        self.click_handler = option_picker.click_handler

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_handler.handle_click(self.pictograph)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        spacing = self.option_picker.scroll_area.spacing

        calculated_width = (self.option_picker.width() // 8) - spacing
        size = min(calculated_width, self.option_picker.height() // 8)

        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width + spacing
        self.pictograph.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
