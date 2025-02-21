from typing import TYPE_CHECKING, Callable
from PyQt6.QtCore import Qt, QSize

from base_widgets.pictograph.bordered_pictograph_view import BorderedPictographView


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph_scene import PictographScene
    from .option_picker import OptionPicker


class OptionView(BorderedPictographView):

    def __init__(
        self,
        option_picker: "OptionPicker",
        pictograph: "PictographScene",
        mw_size_provider: Callable[[], QSize],
    ):
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.option_picker = option_picker
        self.click_handler = option_picker.option_click_handler
        self.mw_size_provider = mw_size_provider

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_handler.handle_click(self.pictograph)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resize_option_view()

    def resize_option_view(self):
        spacing = self.option_picker.option_scroll.spacing

        size = max(
            self.mw_size_provider().width() // 16,
            self.option_picker.width() // 8,
        )
        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width + spacing
        self.pictograph.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
