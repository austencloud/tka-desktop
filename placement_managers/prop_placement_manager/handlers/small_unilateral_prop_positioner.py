from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SmallUnilateralPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.prop_placement_manager = beta_prop_positioner.prop_placement_manager
        self.pictograph = beta_prop_positioner.pictograph
        self.dir_calculator = self.prop_placement_manager.dir_calculator
        self.blue_prop = self.pictograph.elements.blue_prop
        self.red_prop = self.pictograph.elements.red_prop
        self.red_motion = self.pictograph.elements.red_motion
        self.blue_motion = self.pictograph.elements.blue_motion
        self.default_positioner = self.prop_placement_manager.default_positioner
        self.classifier = self.beta_prop_positioner.classifier
