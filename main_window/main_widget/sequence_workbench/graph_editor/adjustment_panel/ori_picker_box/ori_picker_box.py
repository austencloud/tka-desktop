from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from .ori_picker_widget.ori_picker_widget import OriPickerWidget
from .ori_picker_header import OriPickerHeader

if TYPE_CHECKING:
    from ..beat_adjustment_panel import BeatAdjustmentPanel
    from base_widgets.pictograph.pictograph_scene import PictographScene


class OriPickerBox(QFrame):
    vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
    prop_rot_dir_btn_state: dict[str, bool] = {
        CLOCKWISE: False,
        COUNTER_CLOCKWISE: False,
    }

    def __init__(
        self,
        adjustment_panel: "BeatAdjustmentPanel",
        start_pos: "PictographScene",
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
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ "
            f"border: {border_width}px solid {self.color}; "
            f"background-color: white; "
            f"}}"
        )
        self.ori_picker_widget.resizeEvent(event)
        super().resizeEvent(event)
