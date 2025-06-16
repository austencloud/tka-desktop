from typing import TYPE_CHECKING
from objects.prop.prop import Prop
from placement_managers.prop_placement_manager.handlers.beta_prop_direction_calculator import (
    BetaPropDirectionCalculator,
)
from placement_managers.prop_placement_manager.handlers.hand_positioner import (
    HandPositioner,
)
from placement_managers.prop_placement_manager.handlers.beta_offset_calculator import (
    BetaOffsetCalculator,
)
from .big_prop_positioner import BigPropPositioner
from .prop_classifier import PropClassifier
from .reposition_beta_props_by_letter_manager import RepositionBetaByLetterHandler
from .small_prop_positioner import SmallPropPositioner
from .swap_beta_handler import SwapBetaHandler

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

    from ..prop_placement_manager import PropPlacementManager


class BetaPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph: "LegacyPictograph" = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager

        self.classifier = PropClassifier(self.pictograph)
        self.hand_positioner = HandPositioner(self)
        self.small_prop_positioner = SmallPropPositioner(self)
        self.big_prop_positioner = BigPropPositioner(self)
        self.dir_calculator = BetaPropDirectionCalculator()
        self.reposition_beta_by_letter_handler = RepositionBetaByLetterHandler(self)
        self.swap_beta_handler = SwapBetaHandler(self)
        self.beta_offset_calculator = BetaOffsetCalculator(self)

    def reposition_beta_props(self) -> None:
        self.classifier.classify_props()
        match (
            bool(self.classifier.big_props),
            bool(self.classifier.small_props),
            bool(self.classifier.hands),
        ):
            case (True, _, _):
                if len(self.classifier.big_props) == 2:
                    self.big_prop_positioner.reposition()
            case (_, True, _):
                if len(self.classifier.small_props) == 2:
                    self.small_prop_positioner.reposition()
                    self.swap_beta_handler.swap_beta_if_needed()
            case (_, _, True):
                self.hand_positioner.reposition_beta_hands()
                self.swap_beta_handler.swap_beta_if_needed()

    def move_prop(self, prop: Prop, direction: str) -> None:
        offset_calculator = self.beta_offset_calculator
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
