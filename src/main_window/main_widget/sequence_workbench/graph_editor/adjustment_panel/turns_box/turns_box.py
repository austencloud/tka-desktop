from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED, OPP, SAME
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
        self.state = self.graph_editor.state  # Reference to centralized state

        self.matching_motion = self.pictograph.managers.get.motion_by_color(self.color)
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self.setObjectName(self.__class__.__name__)

        self._setup_widgets()
        self._setup_layout()
        self._connect_state_signals()

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

    def _connect_state_signals(self) -> None:
        """Connect to the centralized state signals"""
        self.state.turns_changed.connect(self._handle_turns_changed)
        self.state.prop_rot_dir_changed.connect(self._handle_prop_rot_dir_changed)
        self.state.motion_type_changed.connect(self._handle_motion_type_changed)

    def _handle_turns_changed(self, color, value):
        """Handle turns changes from central state"""
        if color == self.color:
            self.turns_widget.display_frame.update_turns_display(
                self.matching_motion, value
            )

    def _handle_prop_rot_dir_changed(self, color, direction):
        """Handle prop rotation direction changes from central state"""
        if color == self.color:
            self.prop_rot_dir_button_manager.update_buttons_for_prop_rot_dir(direction)

    def _handle_motion_type_changed(self, color, motion_type):
        """Handle motion type changes from central state"""
        if color == self.color:
            self.turns_widget.motion_type_label.update_display(motion_type)

    # Update method to push changes to the centralized state
    def update_turns(self, value):
        """Update turns in the centralized state"""
        self.state.set_turns(self.color, value)

    def update_prop_rot_dir(self, direction):
        """Update prop rotation direction in the centralized state"""
        self.state.set_prop_rot_dir(self.color, direction)

    def update_motion_type(self, motion_type):
        """Update motion type in the centralized state"""
        self.state.set_motion_type(self.color, motion_type)

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
