from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from base_widgets.pictograph.components.placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )


class SmallBilateralPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.ppm = beta_prop_positioner.prop_placement_manager
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        letter_handler = self.beta_prop_positioner.reposition_beta_by_letter_handler
        if self.pictograph.check.ends_with_layer3():
            for prop in self.pictograph.props.values():
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

        else:
            if self.pictograph.letter in ["G", "H"]:
                letter_handler.reposition_G_H()
            elif self.pictograph.letter == "I":
                letter_handler.reposition_I()
            elif self.pictograph.letter in ["J", "K", "L"]:
                letter_handler.reposition_J_K_L()
            elif self.pictograph.letter in ["Y", "Z"]:
                letter_handler.reposition_Y_Z()
            elif self.pictograph.letter == "β":
                letter_handler.reposition_β()
            elif self.pictograph.letter in ["Y-", "Z-"]:
                letter_handler.reposition_Y_dash_Z_dash()
            elif self.pictograph.letter == "Ψ":
                letter_handler.reposition_Ψ()
            elif self.pictograph.letter == "Ψ-":
                letter_handler.reposition_Ψ_dash()
