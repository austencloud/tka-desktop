# ==========================================
# File: prop_rot_dir_logic_handler.py
# ==========================================
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal
from utils.reversal_detector import ReversalDetector

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class PropRotDirLogicHandler(QObject):
    rotation_updated = pyqtSignal(dict)

    def __init__(self, turns_box: "TurnsBox", ui_handler) -> None:
        super().__init__()
        self.turns_box = turns_box
        self.ui_handler = ui_handler
        self.current_motion = None

    def validate_rotation_change(self, new_direction: str) -> bool:
        """Check if rotation change is valid."""
        return (
            not self.turns_box.prop_rot_dir_btn_state[new_direction]
            and self.current_motion is not None
        )

    def update_rotation_states(self, new_direction: str) -> None:
        """Update all related states for rotation change."""
        self._update_button_states(new_direction)
        self._update_motion_properties(new_direction)
        self._update_pictograph_data()
        self._detect_reversals()

    def _update_motion_properties(self, direction: str) -> None:
        """Update motion objects with new rotation direction."""
        for pictograph in self._get_affected_pictographs():
            for motion in pictograph.get(self.turns_box.color):
                motion.state.prop_rot_dir = direction
                motion.state.motion_type = self._determine_motion_type(motion)

        # Update pictographs & JSON
        self.turns_box.graph_editor.sequence_workbench.beat_frame.updater.update_beats_from_current_sequence_json()
        self.turns_box.graph_editor.main_widget.json_manager.ori_validation_engine.run(
            is_current_sequence=True
        )

    def _update_pictograph_data(self) -> None:
        """Update pictograph data with new direction state."""
        pass  # JSON updates would be handled here

    def _detect_reversals(self) -> None:
        """Handle reversal detection and update UI."""
        pass  # Implement reversal detection logic

    def _update_button_states(self, direction: str) -> None:
        """Update button states after a rotation change."""
        for button in self.ui_handler.buttons:
            button.set_selected(button.prop_rot_dir == direction)

    def _get_affected_pictographs(self) -> list:
        """Retrieve pictographs that need updating."""
        return []

    def _determine_motion_type(self, motion) -> str:
        """Determine new motion type based on rotation."""
        return motion.state.motion_type
