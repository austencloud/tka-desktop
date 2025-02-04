from typing import TYPE_CHECKING
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame
from ..widgets.permutation_type_toggle import PermutationTypeToggle
from ..widgets.rotation_type_toggle import RotationTypeToggle
from .circular_sequence_generator import CircularSequenceGenerator

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class CircularSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "GenerateTab") -> None:
        super().__init__(sequence_generator_tab, "circular")
        self.builder = CircularSequenceGenerator(self)

        self.rotation_type_toggle = RotationTypeToggle(self)
        self.permutation_type_toggle = PermutationTypeToggle(self)

        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addStretch(1)

        self.apply_settings()
        self.beat_deleter = (
            self.tab.main_widget.sequence_widget.beat_frame.sequence_widget.beat_deleter
        )

    def apply_settings(self):
        super().apply_settings()

        rotation_type = self.generate_tab_settings.get_sequence_generator_setting(
            "rotation_type", self.generator_type
        )
        permutation_type = self.generate_tab_settings.get_sequence_generator_setting(
            "permutation_type", self.generator_type
        )

        self.rotation_type_toggle.set_state(rotation_type == "quartered")
        self.permutation_type_toggle.set_state(permutation_type == "rotated")

    def _update_rotation_type(self, rotation_type: str):
        self.generate_tab_settings.set_sequence_generator_setting(
            "rotation_type", rotation_type, self.generator_type
        )

    def _update_permutation_type(self, permutation_type: str):
        self.generate_tab_settings.set_sequence_generator_setting(
            "permutation_type", permutation_type, self.generator_type
        )
        if permutation_type == "mirrored":
            self.rotation_type_toggle.hide()
            self.length_adjuster.limit_length(False)
        else:
            self.rotation_type_toggle.show()
            self.length_adjuster.limit_length(True)

    def on_create_sequence(self, overwrite_sequence: bool):
        if overwrite_sequence:
            self.beat_deleter.reset_widgets(False)

        settings_keys = [
            ("sequence_length", int),
            ("max_turn_intensity", float),
            ("sequence_level", int),
            ("rotation_type", str),
            ("permutation_type", str),
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
