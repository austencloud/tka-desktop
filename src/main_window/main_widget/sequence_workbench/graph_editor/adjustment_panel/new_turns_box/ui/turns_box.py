# === turns_box/ui/turns_box.py ===
from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, HEX_BLUE, HEX_RED
from ..managers.prop_rot_dir_manager import PropRotDirManager
from .turns_box_header import TurnsBoxHeader
from .turns_widget import TurnsWidget

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.beat_adjustment_panel import (
        BeatAdjustmentPanel,
    )


class TurnsBox(QFrame):
    """Main container for turns controls and management"""

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
        self.matching_motion = self.pictograph.managers.get.motion_by_color(self.color)

        # Set object name for CSS styling
        self.setObjectName(self.__class__.__name__)

        # Setup
        self._setup_widgets()
        self._setup_layout()

    # In turns_box.py, add this property to the TurnsBox class
    @property
    def prop_rot_dir_btn_state(self):
        """Compatibility property to access rotation state"""
        return self.prop_rot_dir_manager.state.current

    def _setup_widgets(self) -> None:
        """Initialize and connect widgets"""
        # Create header
        self.header = TurnsBoxHeader(self)

        # Create prop rotation manager
        self.prop_rot_dir_manager = PropRotDirManager(self)

        # Create turns widget
        self.turns_widget = TurnsWidget(self)

        # Connect turns widget to prop rotation manager
        self.turns_widget.adjustment_manager.connect_prop_rot_dir_manager(
            self.prop_rot_dir_manager
        )

    def _setup_layout(self) -> None:
        """Set up widget layout"""
        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.turns_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Calculate border width based on parent size
        border_width = self.graph_editor.sequence_workbench.width() // 200

        # Determine color based on turns box color
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

        # Create whitened color by blending with white
        whitened_r = min(255, r + (255 - r) // 2)
        whitened_g = min(255, g + (255 - g) // 2)
        whitened_b = min(255, b + (255 - b) // 2)
        whitened_color = f"rgb({whitened_r}, {whitened_g}, {whitened_b})"

        # Apply styles
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ "
            f"border: {border_width}px solid {color_hex}; "
            f"background-color: {whitened_color};}}"
        )

        # Propagate resize event
        self.turns_widget.resizeEvent(event)
        self.header.resizeEvent(event)
        super().resizeEvent(event)
