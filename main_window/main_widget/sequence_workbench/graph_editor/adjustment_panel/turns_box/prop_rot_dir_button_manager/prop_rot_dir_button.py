from typing import TYPE_CHECKING
from base_widgets.base_rot_dir_button import BaseRotDirButton
from PyQt6.QtCore import Qt, QSize

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_box import (
        TurnsBox,
    )


class PropRotDirButton(BaseRotDirButton):
    def __init__(self, turns_box: "TurnsBox", prop_rot_dir: str) -> None:
        super().__init__(prop_rot_dir)
        self.turns_box = turns_box
        self.prop_rot_dir = prop_rot_dir

    def get_button_style(self, pressed: bool) -> str:
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        border_radius = str(button_size // 2) + "px"  # Set border-radius to half the button size
        if pressed:
            return f"""
                QPushButton {{
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                    border-radius: {border_radius};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: white;
                    border: 1px solid black;
                    border-radius: {border_radius};
                }}
                QPushButton:hover {{
                    background-color: #e6f0ff;
                }}
            """

    def update_state_dict(self, state_dict: dict, value: bool) -> None:
        state_dict[self.prop_rot_dir] = value

    def press(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=True))

    def unpress(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=False))

    def is_pressed(self) -> bool:
        return self.styleSheet() == self.get_button_style(pressed=True)

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
