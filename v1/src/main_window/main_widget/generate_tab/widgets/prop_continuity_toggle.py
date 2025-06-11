from typing import TYPE_CHECKING
from .labeled_toggle_base import LabeledToggleBase

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class PropContinuityToggle(LabeledToggleBase):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(
            generate_tab=generate_tab,
            left_text="Random",
            right_text="Continuous",
        )

    def _handle_toggle_changed(self, state: bool):
        new_val = "continuous" if state else "random"
        self.generate_tab.settings.set_setting("prop_continuity", new_val)
        self.update_label_styles()
