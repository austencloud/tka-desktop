# graph_editor_state.py
from typing import Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal
from enums.letter.letter import Letter
from data.constants import BLUE, RED
from base_widgets.pictograph.pictograph import Pictograph
from objects.arrow.arrow import Arrow

class GraphEditorState(QObject):
    """Centralized state manager for the Graph Editor."""

    # Define signals for state changes
    turns_changed = pyqtSignal(str, object)  # color, new_value
    orientation_changed = pyqtSignal(str, str)  # color, new_orientation
    prop_rot_dir_changed = pyqtSignal(str, str)  # color, new_direction
    motion_type_changed = pyqtSignal(str, str)  # color, new_type
    letter_changed = pyqtSignal(Letter)  # new_letter
    selected_arrow_changed = pyqtSignal(object)  # arrow

    def __init__(self):
        super().__init__()
        self._state = {
            "blue": {
                "turns": 0,
                "orientation": "in",
                "prop_rot_dir": "clockwise",
                "motion_type": "standard",
            },
            "red": {
                "turns": 0,
                "orientation": "in",
                "prop_rot_dir": "clockwise",
                "motion_type": "standard",
            },
            "letter": None,
            "selected_arrow": None,
            "currently_editing_pictograph": None,
        }

    # Getter methods
    def get_turns(self, color: str) -> object:
        return self._state[color]["turns"]

    def get_orientation(self, color: str) -> str:
        return self._state[color]["orientation"]

    def get_prop_rot_dir(self, color: str) -> str:
        return self._state[color]["prop_rot_dir"]

    def get_motion_type(self, color: str) -> str:
        return self._state[color]["motion_type"]

    def get_letter(self) -> Optional[Letter]:
        return self._state["letter"]

    def get_selected_arrow(self) -> Optional[Arrow]:
        return self._state["selected_arrow"]

    def get_pictograph(self) -> Optional[Pictograph]:
        return self._state["currently_editing_pictograph"]

    # Setter methods with signals
    def set_turns(self, color: str, value: object) -> None:
        if self._state[color]["turns"] != value:
            self._state[color]["turns"] = value
            self.turns_changed.emit(color, value)

    def set_orientation(self, color: str, orientation: str) -> None:
        if self._state[color]["orientation"] != orientation:
            self._state[color]["orientation"] = orientation
            self.orientation_changed.emit(color, orientation)

    def set_prop_rot_dir(self, color: str, direction: str) -> None:
        if self._state[color]["prop_rot_dir"] != direction:
            self._state[color]["prop_rot_dir"] = direction
            self.prop_rot_dir_changed.emit(color, direction)

    def set_motion_type(self, color: str, motion_type: str) -> None:
        if self._state[color]["motion_type"] != motion_type:
            self._state[color]["motion_type"] = motion_type
            self.motion_type_changed.emit(color, motion_type)

    def set_letter(self, letter: Letter) -> None:
        if not letter:
            return
        if self._state["letter"] != letter:
            self._state["letter"] = letter
            self.letter_changed.emit(letter)

    def set_selected_arrow(self, arrow: Optional[object]) -> None:
        if self._state["selected_arrow"] != arrow:
            self._state["selected_arrow"] = arrow
            self.selected_arrow_changed.emit(arrow)

    def set_pictograph(self, pictograph: Optional[object]) -> None:
        self._state["currently_editing_pictograph"] = pictograph

    # Update entire color state at once
    def update_color_state(self, color: str, state_dict: Dict[str, Any]) -> None:
        for key, value in state_dict.items():
            if key == "turns" and self._state[color]["turns"] != value:
                self._state[color]["turns"] = value
                self.turns_changed.emit(color, value)
            elif key == "orientation" and self._state[color]["orientation"] != value:
                self._state[color]["orientation"] = value
                self.orientation_changed.emit(color, value)
            elif key == "prop_rot_dir" and self._state[color]["prop_rot_dir"] != value:
                self._state[color]["prop_rot_dir"] = value
                self.prop_rot_dir_changed.emit(color, value)
            elif key == "motion_type" and self._state[color]["motion_type"] != value:
                self._state[color]["motion_type"] = value
                self.motion_type_changed.emit(color, value)

    # Sync state from pictograph
    def sync_from_pictograph(self, pictograph: "Pictograph") -> None:
        """Update state from pictograph data"""
        self.set_pictograph(pictograph)
        self.set_letter(pictograph.state.letter)

        blue_motion = pictograph.elements.blue_motion
        red_motion = pictograph.elements.red_motion

        self.update_color_state(
            BLUE,
            {
                "turns": blue_motion.state.turns,
                "orientation": blue_motion.state.end_ori,
                "prop_rot_dir": blue_motion.state.prop_rot_dir,
                "motion_type": blue_motion.state.motion_type,
            },
        )

        self.update_color_state(
            RED,
            {
                "turns": red_motion.state.turns,
                "orientation": red_motion.state.end_ori,
                "prop_rot_dir": red_motion.state.prop_rot_dir,
                "motion_type": red_motion.state.motion_type,
            },
        )
