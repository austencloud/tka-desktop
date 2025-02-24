# strategies/placement_strategy.py
from abc import ABC, abstractmethod
from PyQt6.QtCore import QPointF

from ...arrow_placement_manager.arrow_placement_context import ArrowPlacementContext


class PlacementStrategy(ABC):
    @abstractmethod
    def compute_adjustment(self, context: ArrowPlacementContext) -> QPointF:
        pass
