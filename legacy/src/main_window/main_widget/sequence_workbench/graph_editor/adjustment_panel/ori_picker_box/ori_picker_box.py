from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from .ori_picker_widget.ori_picker_widget import OriPickerWidget
from .ori_picker_header import OriPickerHeader
from .color_utils import ColorUtils

if TYPE_CHECKING:
    from ..legacy_adjustment_panel import LegacyAdjustmentPanel
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class OriPickerBox(QFrame):
    vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
    prop_rot_dir_btn_state: dict[str, bool] = {
        CLOCKWISE: False,
        COUNTER_CLOCKWISE: False,
    }

    def __init__(
        self,
        adjustment_panel: "LegacyAdjustmentPanel",
        start_pos: "LegacyPictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.start_pos = start_pos
        self.graph_editor = self.adjustment_panel.graph_editor
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header = OriPickerHeader(self)
        self.ori_picker_widget = OriPickerWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.ori_picker_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        border_width = self.graph_editor.sequence_workbench.width() // 200
        color_hex = (
            HEX_RED
            if self.color == "red"
            else HEX_BLUE if self.color == "blue" else self.color
        )
        whitened_color = ColorUtils.lighten_color(color_hex)
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {border_width}px solid "
            f"{color_hex}; background-color: {whitened_color};}}"
        )
        self.ori_picker_widget.resizeEvent(event)
        super().resizeEvent(event)
