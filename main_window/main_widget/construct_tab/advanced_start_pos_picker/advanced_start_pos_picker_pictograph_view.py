from typing import TYPE_CHECKING

from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph
    from .advanced_start_pos_picker import AdvancedStartPosPicker


class AdvancedStartPosPickerPictographView(BorderedPictographView):
    def __init__(
        self,
        advanced_start_pos_picker: "AdvancedStartPosPicker",
        pictograph: "Pictograph",
    ):
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.construct_tab = advanced_start_pos_picker.construct_tab
        self.picker = advanced_start_pos_picker

    def resizeEvent(self, event):
        view_width = self.construct_tab.main_widget.right_stack.width() // 6
        self.setFixedSize(view_width, view_width)
        self.view_scale = view_width / self.picker.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        super().resizeEvent(event)
