from typing import TYPE_CHECKING
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.base_rot_dir_button import (
    BaseRotDirButton,
)
from PyQt6.QtCore import Qt, QSize

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_box import (
        TurnsBox,
    )


class PropRotDirButton(StyledButton):
    def __init__(
        self, turns_box: "TurnsBox", prop_rot_dir: str, icon_path: str
    ) -> None:
        super().__init__(label="", icon_path=icon_path)
        self.turns_box = turns_box
        self.prop_rot_dir = prop_rot_dir

    def update_state_dict(self, state_dict: dict, value: bool) -> None:
        state_dict[self.prop_rot_dir] = value

    def enterEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def resizeEvent(self, event) -> None:
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        icon_size = int(button_size * 0.8)
        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)
