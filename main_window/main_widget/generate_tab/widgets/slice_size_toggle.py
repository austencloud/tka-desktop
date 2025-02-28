from typing import TYPE_CHECKING
from .labeled_toggle_base import LabeledToggleBase

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class SliceSizeToggle(LabeledToggleBase):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(
            generate_tab=generate_tab,
            left_text="Halved",
            right_text="Quartered",
        )

    def _handle_toggle_changed(self, state: bool):
        permutation_type = self.generate_tab.settings.get_setting("permutation_type")

        # Prevent quartered if permutation is mirrored
        if permutation_type == "mirrored":
            self.set_state(False)  # Force 'halved'
            return  # Prevent any further updates

        rot_type = "quartered" if state else "halved"
        self.generate_tab.settings.set_setting("rotation_type", rot_type)
        self.update_label_styles()
