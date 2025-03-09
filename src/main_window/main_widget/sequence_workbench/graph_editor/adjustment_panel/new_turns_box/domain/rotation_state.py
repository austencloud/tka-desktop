# === turns_box/domain/rotation_state.py ===
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional
from PyQt6.QtCore import QObject, pyqtSignal

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT


class RotationState(QObject):
    """State manager for rotation directions"""

    state_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._state: Dict[str, bool] = {CLOCKWISE: False, COUNTER_CLOCKWISE: False}

    def update_state(self, direction: str, value: bool) -> None:
        if direction not in self._state and direction != NO_ROT:
            return

        if direction == NO_ROT:
            self._state = {k: False for k in self._state}
        else:
            # Use old code's approach that was working
            self._state = {
                k: (value if k == direction else not v) for k, v in self._state.items()
            }

        self.state_changed.emit(self._state)

    @property
    def current(self) -> Dict[str, bool]:
        """Get a copy of the current state"""
        return self._state.copy()

    @property
    def active_direction(self) -> Optional[str]:
        """Get the currently active direction, or None if none is active"""
        for direction, is_active in self._state.items():
            if is_active:
                return direction
        return NO_ROT
