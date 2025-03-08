# ==========================================
# File: prop_rot_dir_button.py
# ==========================================
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QSize
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_box import TurnsBox


class PropRotDirButton(StyledButton):
    def __init__(self, turns_box: "TurnsBox", prop_rot_dir: str, icon_path: str) -> None:
        super().__init__(label="", icon_path=icon_path)
        self.turns_box = turns_box
        self.prop_rot_dir = prop_rot_dir
        self._setup_button()

    def _setup_button(self) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Set {self.prop_rot_dir.replace('_', ' ').title()} Rotation")

    def update_state_dict(self, state_dict: dict, value: bool) -> None:
        state_dict[self.prop_rot_dir] = value

    def update_appearance(self) -> None:
        """Update visual state based on current selection."""
        is_active = self.turns_box.prop_rot_dir_btn_state[self.prop_rot_dir]
        self.setProperty("active", str(is_active).lower())
        self.style().polish(self)

    def resizeEvent(self, event) -> None:
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        icon_size = int(button_size * 0.8)
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)

