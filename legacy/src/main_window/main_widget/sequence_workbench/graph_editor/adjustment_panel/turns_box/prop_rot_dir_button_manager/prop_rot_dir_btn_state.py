# === prop_rot_dir_button_manager/core.py ===
from PyQt6.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING, Dict

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE


class PropRotationState(QObject):
    """Manages the state machine for rotation directions"""

    state_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._state: Dict[str, bool] = {CLOCKWISE: False, COUNTER_CLOCKWISE: False}

    def update_state(self, direction: str, value: bool):
        """Atomic state update with validation"""
        if direction not in self._state:
            return
        self._state = {
            k: (v if k == direction else not v) for k, v in self._state.items()
        }
        self.state_changed.emit(self._state)

    @property
    def current(self):
        return self._state.copy()
