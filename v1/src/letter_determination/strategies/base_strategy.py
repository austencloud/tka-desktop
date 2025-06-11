from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from enums.letter.letter import Letter

if TYPE_CHECKING:
    from ..services.motion_comparator import MotionComparator
    from ..services.attribute_manager import AttributeManager


class LetterDeterminationStrategy(ABC):
    def __init__(
        self, comparator: "MotionComparator", attribute_manager: "AttributeManager"
    ):
        self.comparator = comparator
        self.attribute_manager = attribute_manager

    @abstractmethod
    def execute(self, pictograph_data: dict, swap_prop_rot_dir: bool = False) -> Letter:
        pass

    def applies_to(self, pictograph: dict) -> bool:
        """Determine if this strategy is applicable based on pictograph motion types."""
        return False  # To be overridden in subclasses
