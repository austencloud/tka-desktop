# src/main_window/main_widget/sequence_workbench/graph_editor/adjustment_panel/new_turns_adjustment_manager/turns_state.py
from PyQt6.QtCore import QObject, pyqtSignal
from .turns_value import TurnsValue


class TurnsState(QObject):
    turns_changed = pyqtSignal(TurnsValue)
    validation_error = pyqtSignal(str)

    def __init__(self, initial_value: TurnsValue):
        super().__init__()
        self._current_turns = initial_value

    @property
    def current(self) -> TurnsValue:
        return self._current_turns

    @current.setter
    def current(self, value: TurnsValue):
        try:
            if self._current_turns != value:
                self._validate_transition(value)
                self._current_turns = value
                self.turns_changed.emit(value)
        except ValueError as e:
            self.validation_error.emit(str(e))

    def _validate_transition(self, new_value: TurnsValue):
        """Ensure valid state transitions"""
        current = self._current_turns.raw_value
        new = new_value.raw_value

        if current == "fl" and new == 0:
            return  # Valid float to zero transition
        if current == 0 and new == "fl":
            return  # Valid zero to float transition
        if isinstance(new, (int, float)) and not (0 <= new <= 3):
            raise ValueError("Turns must be between 0 and 3")
