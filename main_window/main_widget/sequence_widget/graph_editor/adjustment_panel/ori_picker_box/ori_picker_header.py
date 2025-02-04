from typing import TYPE_CHECKING
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget

if TYPE_CHECKING:
    from .ori_picker_box import OriPickerBox


class OriPickerHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self._add_widgets()

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)
