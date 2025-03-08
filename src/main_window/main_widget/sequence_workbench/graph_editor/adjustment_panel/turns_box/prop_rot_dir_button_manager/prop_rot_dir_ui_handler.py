# ==========================================
# File: prop_rot_dir_ui_handler.py
# ==========================================
from typing import TYPE_CHECKING
from utils.path_helpers import get_image_path
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from .prop_rot_dir_button import PropRotDirButton

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirUIHandler:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.buttons = []

    def setup_buttons(self) -> None:
        """Initialize rotation direction buttons."""
        self.buttons = [
            self._create_button(CLOCKWISE, "clockwise.png"),
            self._create_button(COUNTER_CLOCKWISE, "counter_clockwise.png")
        ]
        self._arrange_buttons()

    def _create_button(self, direction, icon_name) -> PropRotDirButton:
        """Factory method for creating buttons."""
        button = PropRotDirButton(
            self.turns_box,
            direction,
            get_image_path(f"{ICON_DIR}clock/{icon_name}")
        )
        button.clicked.connect(lambda _, d=direction: self.turns_box.prop_rot_dir_button_manager.handle_rotation_change(d))
        return button

    def sync_button_states(self) -> None:
        """Sync UI states with current rotation state."""
        current_dir = self.turns_box.prop_rot_dir_btn_state
        for btn in self.buttons:
            is_active = current_dir.get(btn.prop_rot_dir, False)
            btn.set_selected(is_active)
            btn.setVisible(is_active is not None)

    def handle_button_visibility(self, motion) -> None:
        """Control button visibility based on motion state."""
        if motion.state.turns == 0:
            self._hide_all_buttons()
        elif motion.state.turns == "fl":
            self._hide_all_buttons()
        else:
            self._show_all_buttons()

    def _hide_all_buttons(self) -> None:
        for button in self.buttons:
            button.hide()

    def _show_all_buttons(self) -> None:
        for button in self.buttons:
            button.show()

