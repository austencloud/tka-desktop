from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..models.pictograph import PictographData
from ..determination_result import DeterminationResult

if TYPE_CHECKING:
    from ..services.motion_comparator import MotionComparator
    from ..services.attribute_manager import AttributeManager

class BaseDeterminationStrategy(ABC):
    def __init__(
        self, comparator: "MotionComparator", attribute_manager: "AttributeManager"
    ):
        self.comparator = comparator
        self.attribute_manager = attribute_manager

    @abstractmethod
    def execute(self, pictograph: PictographData, swap_prop_rot_dir: bool = False) -> DeterminationResult:
        pass

    def applies_to(self, pictograph: PictographData) -> bool:
        """Determine if this strategy is applicable based on pictograph motion types."""
        return False  # To be overridden in subclasses
