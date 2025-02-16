from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from .prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from .turns_box_header import TurnsBoxHeader
from .turns_widget.turns_widget import TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from ..beat_adjustment_panel import BeatAdjustmentPanel
    from base_widgets.pictograph.pictograph import Pictograph


class TurnsBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "BeatAdjustmentPanel",
        pictograph: "Pictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.adjustment_panel.graph_editor
        self.matching_motion = self.pictograph.get.motion_by_color(self.color)
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.prop_rot_dir_button_manager = PropRotDirButtonManager(self)
        self.header = TurnsBoxHeader(self)
        self.turns_widget = TurnsWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.turns_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.border_width = self.graph_editor.sequence_workbench.width() // 200
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {self.border_width}px solid "
            f"{self.color}; background-color: white;}}"
        )
        self.turns_widget.resizeEvent(event)
        self.header.resizeEvent(event)
        super().resizeEvent(event)
