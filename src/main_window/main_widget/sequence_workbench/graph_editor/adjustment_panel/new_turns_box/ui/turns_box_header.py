# === turns_box/ui/turns_box_header.py ===
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR, NO_ROT
from utils.path_helpers import get_image_path
from .buttons.prop_rot_dir_button import PropRotDirButton

if TYPE_CHECKING:
    from .turns_box import TurnsBox
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.base_adjustment_box_header_widget import (
        BaseAdjustmentBoxHeaderWidget,
    )


class TurnsBoxHeader(QFrame):  # Replace with actual base class
    """Header widget for the turns box"""

    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget

        # Setup
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        """Initialize widgets"""
        # Create header label
        self.header_label = self._create_header_label("Rotation Direction")

        # Create rotation direction buttons
        self.cw_button = PropRotDirButton(
            self.turns_box, CLOCKWISE, get_image_path(f"{ICON_DIR}clock/clockwise.png")
        )

        self.ccw_button = PropRotDirButton(
            self.turns_box,
            COUNTER_CLOCKWISE,
            get_image_path(f"{ICON_DIR}clock/counter_clockwise.png"),
        )

        # Create separator
        self.separator = self._create_separator()

    def _create_header_label(self, text: str):
        """Create styled header label"""
        from PyQt6.QtWidgets import QLabel
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont("Cambria", 12, QFont.Weight.Bold)
        font.setUnderline(True)
        label.setFont(font)

        return label

    def _create_separator(self):
        """Create separator line"""
        from PyQt6.QtWidgets import QFrame

        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        return separator

    def _setup_layout(self) -> None:
        """Set up widget layout"""
        # Create layout for header content
        self.top_hbox = QHBoxLayout()
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.ccw_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.cw_button)
        self.top_hbox.addStretch(1)

        # Create layout for separator
        self.separator_hbox = QHBoxLayout()
        self.separator_hbox.addWidget(self.separator)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.top_hbox)
        main_layout.addLayout(self.separator_hbox)
        main_layout.setContentsMargins(5, 5, 5, 0)
        main_layout.setSpacing(2)

        self.setLayout(main_layout)

    def update_turns_box_header(self) -> None:
        """Update the header based on current rotation state"""
        # Get pictograph and motion
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
        motion = pictograph.managers.get.motion_by_color(self.turns_box.color)

        # Skip if no motion
        if not motion:
            self.hide_prop_rot_dir_buttons()
            return

        # Update based on prop rotation direction

        if motion.state.prop_rot_dir == NO_ROT:
            self.hide_prop_rot_dir_buttons()
        else:
            self.show_prop_rot_dir_buttons()

        if motion.state.prop_rot_dir == CLOCKWISE:
            self.cw_button.set_selected(True)
            self.ccw_button.set_selected(False)
        elif motion.state.prop_rot_dir == COUNTER_CLOCKWISE:
            self.cw_button.set_selected(False)  # Currently uses incorrect True value
            self.ccw_button.set_selected(True)  # Currently uses incorrect False value

    def show_prop_rot_dir_buttons(self) -> None:
        """Show rotation direction buttons"""
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        """Hide rotation direction buttons"""
        self.cw_button.hide()
        self.ccw_button.hide()

    def unpress_prop_rot_dir_buttons(self) -> None:
        # Should set both to False, not True
        self.cw_button.set_selected(False)
        self.ccw_button.set_selected(False)

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        # Update font size based on parent dimensions
        font_size = self.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.header_label.setFont(font)

        # Propagate resize event
        self.cw_button.resizeEvent(event)
        self.ccw_button.resizeEvent(event)
        super().resizeEvent(event)
