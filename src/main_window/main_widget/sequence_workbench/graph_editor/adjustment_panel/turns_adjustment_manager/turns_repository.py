# Abstract repository
from abc import ABC, abstractmethod

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.turns_value import (
    TurnsValue,
)


class TurnsRepository(ABC):
    @abstractmethod
    def save(self, value: TurnsValue):
        pass

    @abstractmethod
    def load(self) -> TurnsValue:
        pass
