from typing import TYPE_CHECKING
from .labeled_toggle_base import LabeledToggleBase

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class GeneratorTypeToggle(LabeledToggleBase):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(
            generate_tab=generate_tab,
            left_text="Freeform",
            right_text="Circular",
        )

    def _handle_toggle_changed(self, state: bool):
        self.mode = "circular" if state else "freeform"
        self.generate_tab.controller.on_mode_changed(self.mode)
        self.update_label_styles()

    def current_mode(self) -> str:
        return self.mode
