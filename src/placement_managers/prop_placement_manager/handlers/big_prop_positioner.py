from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class BigPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.ppm = beta_prop_positioner.prop_placement_manager
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        letter_handler = self.beta_prop_positioner.reposition_beta_by_letter_handler
        ends_with_layer3 = self.pictograph.managers.check.ends_with_layer3()
        ends_with_in_out_ori = self.pictograph.managers.check.ends_with_in_out_ori()
        ends_with_clock_counter_ori = (
            self.pictograph.managers.check.ends_with_clock_counter_ori()
        )
        small_uni_len = len(self.beta_prop_positioner.classifier.small_uni)
        big_uni_len = len(self.beta_prop_positioner.classifier.big_uni)
        letter = self.pictograph.state.letter.value

        if ends_with_layer3:
            for prop in self.pictograph.elements.props.values():
                self.beta_prop_positioner.prop_placement_manager.default_positioner.set_prop_to_default_loc(
                    prop
                )
        if (ends_with_in_out_ori or ends_with_clock_counter_ori) and (
            small_uni_len == 2 or big_uni_len == 2
        ):
            return

        letter_actions = {
            "G": letter_handler.reposition_G_H,
            "H": letter_handler.reposition_G_H,
            "I": letter_handler.reposition_I,
            "J": letter_handler.reposition_J_K_L,
            "K": letter_handler.reposition_J_K_L,
            "L": letter_handler.reposition_J_K_L,
            "Y": letter_handler.reposition_Y_Z,
            "Z": letter_handler.reposition_Y_Z,
            "β": letter_handler.reposition_beta,
            "Y-": letter_handler.reposition_Y_dash_Z_dash,
            "Z-": letter_handler.reposition_Y_dash_Z_dash,
            "Ψ": letter_handler.reposition_psi,
            "Ψ-": letter_handler.reposition_psi_dash,
        }

        if letter in letter_actions:
            letter_actions[letter]()
