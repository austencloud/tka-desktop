# Abstract command
from abc import ABC, abstractmethod

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_state import (
    TurnsState,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)


class TurnsCommand(ABC):
    def __init__(self, state: TurnsState, color: str):  # ✅ Add color
        self._state = state
        self._color = color  # ✅ Store color

    @abstractmethod
    def execute(self):
        pass


class AdjustTurnsCommand(TurnsCommand):
    def __init__(self, state: TurnsState, delta: float, color: str):  # ✅ Pass color
        super().__init__(state, color)
        self._delta = delta

    def execute(self):
        new_value = self._state.current.adjust(self._delta)
        self._state.current = new_value


class SetTurnsCommand(TurnsCommand):
    def __init__(
        self, state: TurnsState, value: TurnsValue, color: str
    ):  # ✅ Pass color
        super().__init__(state, color)
        self._value = value

    def execute(self):
        self._state.current = self._value
