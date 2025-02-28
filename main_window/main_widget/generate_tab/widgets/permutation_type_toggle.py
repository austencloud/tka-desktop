from typing import TYPE_CHECKING
from .labeled_toggle_base import LabeledToggleBase

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab

class PermutationTypeToggle(LabeledToggleBase):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(
            generate_tab=generate_tab,
            left_text="Mirrored",
            right_text="Rotated",
        )
        self.slice_size_toggle = self.generate_tab.slice_size_toggle  # Reference to rotation type toggle

    def _handle_toggle_changed(self, state: bool):
        permutation_type = "rotated" if state else "mirrored"
        self.generate_tab.settings.set_setting("permutation_type", permutation_type)

        # If mirrored is selected, force rotation_type to halved
        if permutation_type == "mirrored":
            self.slice_size_toggle.set_state(False)  # Force 'halved'
            self.generate_tab.settings.set_setting("rotation_type", "halved")

        self.update_label_styles()
