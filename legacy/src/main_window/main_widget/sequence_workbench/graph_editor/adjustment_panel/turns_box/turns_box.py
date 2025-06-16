from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
from .prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from .turns_box_header import TurnsBoxHeader
from .turns_widget.turns_widget import TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from ..legacy_adjustment_panel import LegacyAdjustmentPanel
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class TurnsBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "LegacyAdjustmentPanel",
        pictograph: "LegacyPictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.adjustment_panel.graph_editor
        self.matching_motion = self.pictograph.managers.get.motion_by_color(self.color)
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header = TurnsBoxHeader(self)
        self.prop_rot_dir_button_manager = PropRotDirButtonManager(self)
        self.turns_widget = TurnsWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.turns_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        border_width = self.graph_editor.sequence_workbench.width() // 200
        # Convert named colors to hex
        color_hex = (
            HEX_RED
            if self.color == "red"
            else HEX_BLUE if self.color == "blue" else self.color
        )
        # Convert hex to RGB
        r, g, b = (
            int(color_hex[1:3], 16),
            int(color_hex[3:5], 16),
            int(color_hex[5:7], 16),
        )
        # Whiten the color by blending with white (255, 255, 255)
        whitened_r = min(255, r + (255 - r) // 2)
        whitened_g = min(255, g + (255 - g) // 2)
        whitened_b = min(255, b + (255 - b) // 2)
        whitened_color = f"rgb({whitened_r}, {whitened_g}, {whitened_b})"
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {border_width}px solid "
            f"{color_hex}; background-color: {whitened_color};}}"
        )
        self.turns_widget.resizeEvent(event)
        self.header.resizeEvent(event)
        super().resizeEvent(event)
