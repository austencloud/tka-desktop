from typing import TYPE_CHECKING

from Enums.letters import LetterType
from .letter_type_picker_widget import LetterTypePickerWidget
from main_window.main_widget.generate_tab.freeform.freeform_sequence_generator import (
    FreeFormSequenceGenerator,
)
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class FreeformSequenceGeneratorFrame(BaseSequenceGeneratorFrame):

    def __init__(self, generate_tab: "GenerateTab") -> None:
        super().__init__(generate_tab, "freeform")

        self.letter_type_picker = LetterTypePickerWidget(self)
        self.layout.addWidget(self.letter_type_picker)

        self.builder = FreeFormSequenceGenerator(self)
        self.letter_type_picker.apply_settings()
        self.beat_deleter = (
            self.tab.main_widget.sequence_workbench.beat_frame.sequence_workbench.beat_deleter
        )

    def on_create_sequence(self, overwrite_sequence: bool):
        if overwrite_sequence:
            self.beat_deleter.reset_widgets(False)

        settings_keys = [
            ("sequence_length", int),
            ("max_turn_intensity", float),
            ("sequence_level", int),
            ("continuous_rotation", lambda x: x),
        ]

        settings = [
            setting_type(
                self.generate_tab_settings.get_sequence_generator_setting(
                    key, self.generator_type
                )
            )
            for key, setting_type in settings_keys
        ]

        self.builder.build_sequence(*settings)

    def get_selected_letter_types(self) -> list[LetterType]:
        return self.letter_type_picker.get_selected_letter_types()
