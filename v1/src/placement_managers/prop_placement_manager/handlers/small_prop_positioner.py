from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SmallPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        letter_handler = self.beta_prop_positioner.reposition_beta_by_letter_handler
        if self.pictograph.managers.check.ends_with_layer3():
            for prop in self.pictograph.elements.props.values():
                self.beta_prop_positioner.prop_placement_manager.default_positioner.set_prop_to_default_loc(
                    prop
                )
        if (
            (
                self.pictograph.managers.check.ends_with_in_out_ori()
                or self.pictograph.managers.check.ends_with_clock_counter_ori()
            )
            and len(self.beta_prop_positioner.classifier.small_uni) == 2
        ) or self.pictograph.managers.check.ends_with_layer3():
            return

        else:
            if self.pictograph.state.letter.value in ["G", "H"]:
                letter_handler.reposition_G_H()
            elif self.pictograph.state.letter.value == "I":
                letter_handler.reposition_I()
            elif self.pictograph.state.letter.value in ["J", "K", "L"]:
                letter_handler.reposition_J_K_L()
            elif self.pictograph.state.letter.value in ["Y", "Z"]:
                letter_handler.reposition_Y_Z()
            elif self.pictograph.state.letter.value == "β":
                letter_handler.reposition_beta()
            elif self.pictograph.state.letter.value in ["Y-", "Z-"]:
                letter_handler.reposition_Y_dash_Z_dash()
            elif self.pictograph.state.letter.value == "Ψ":
                letter_handler.reposition_psi()
            elif self.pictograph.state.letter.value == "Ψ-":
                letter_handler.reposition_psi_dash()
