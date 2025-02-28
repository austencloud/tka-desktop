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
        # Prevent changing the state if it's hidden (when mirrored is selected)
        if not self.isVisible():
            return

        rot_type = "quartered" if state else "halved"
        self.generate_tab.settings.set_setting("rotation_type", rot_type)
        self.update_label_styles()
