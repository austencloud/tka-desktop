from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_widget.generate_tab.freeform.freeform_sequence_generator_frame import (
        FreeformSequenceGeneratorFrame,
    )
    from main_window.main_widget.generate_tab.circular.circular_sequence_generator_frame import (
        CircularSequenceGeneratorFrame,
    )


class GenerateTabFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        sequence_generator = self.main_widget.generate_tab
        # Gather freeform labels
        freeform_labels = self._get_freeform_builder_labels(
            sequence_generator.freeform_generator_frame
        )
        # Gather circular labels
        circular_labels = self._get_circular_builder_labels(
            sequence_generator.circular_generator_frame
        )

        self._apply_font_colors(freeform_labels + circular_labels)

        # Update toggles
        sequence_generator.freeform_generator_frame.continuous_rotation_toggle.update_mode_label_styles()
        sequence_generator.circular_generator_frame.continuous_rotation_toggle.update_mode_label_styles()
        sequence_generator.overwrite_checkbox.set_label_color(self.font_color)

    def _get_freeform_builder_labels(
        self, freeform_generator_frame: "FreeformSequenceGeneratorFrame"
    ) -> list[QWidget]:
        return [
            freeform_generator_frame.level_selector.level_label,
            freeform_generator_frame.length_adjuster.length_label,
            freeform_generator_frame.length_adjuster.length_value_label,
            freeform_generator_frame.turn_intensity_adjuster.intensity_label,
            freeform_generator_frame.turn_intensity_adjuster.intensity_value_label,
            freeform_generator_frame.letter_type_picker.filter_label,
        ]

    def _get_circular_builder_labels(
        self, circular_generator_frame: "CircularSequenceGeneratorFrame"
    ) -> list[QWidget]:
        return [
            circular_generator_frame.level_selector.level_label,
            circular_generator_frame.length_adjuster.length_label,
            circular_generator_frame.length_adjuster.length_value_label,
            circular_generator_frame.turn_intensity_adjuster.intensity_label,
            circular_generator_frame.turn_intensity_adjuster.intensity_value_label,
        ]
