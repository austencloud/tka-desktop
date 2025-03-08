# ==========================================
# File: prop_rot_dir_button_manager.py
# ==========================================
from typing import TYPE_CHECKING
from .prop_rot_dir_logic_handler import PropRotDirLogicHandler
from .prop_rot_dir_ui_handler import PropRotDirUIHandler

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


from .prop_rot_dir_btn_state import PropRotationState

class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.state = PropRotationState()
        self.ui_handler = PropRotDirUIHandler(turns_box)
        self.logic_handler = PropRotDirLogicHandler(turns_box, self.ui_handler, self.state)

        self.state.state_changed.connect(self.ui_handler.sync_button_states)
        
        # Setup initial button states
        self.ui_handler.setup_buttons()
        self.ui_handler.sync_button_states()


    def handle_rotation_change(self, prop_rot_dir: str) -> None:
        """Main entry point for rotation direction changes."""
        if self.logic_handler.validate_rotation_change(prop_rot_dir):
            self.logic_handler.update_rotation_states(prop_rot_dir)
            self.ui_handler.sync_button_states()
            self.logic_handler.update_related_components()

    def update_for_motion_change(self, motion) -> None:
        """Update buttons based on motion state changes."""
        self.logic_handler.current_motion = motion
        self.ui_handler.handle_button_visibility(motion)
        self.ui_handler.sync_button_states()

    @property
    def buttons(self):
        return self.ui_handler.buttons

