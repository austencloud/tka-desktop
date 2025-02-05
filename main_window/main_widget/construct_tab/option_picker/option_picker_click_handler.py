# option_picker_click_handler.py

from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.base_pictograph.pictograph import Pictograph


class OptionPickerClickHandler:
    def __init__(self, option_picker: "OptionPicker") -> None:
        self.option_picker = option_picker
        self.construct_tab = self.option_picker.construct_tab
        self.main_widget = self.construct_tab.main_widget
        self.beat_frame = self.main_widget.sequence_workbench.beat_frame
        self.sequence_workbench = self.main_widget.sequence_workbench
        self.add_to_sequence_manager = self.construct_tab.add_to_sequence_manager
        self.settings_manager = self.main_widget.settings_manager
        self.layout_settings = self.settings_manager.sequence_layout

    def get_click_handler(self, start_pos: "Pictograph") -> callable:
        return lambda event: self.handle_click(start_pos)

    def handle_click(self, clicked_option: "Pictograph") -> None:
        """Handle the logic when an option is clicked."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        new_beat = self.add_to_sequence_manager.create_new_beat(clicked_option)
        next_beat_number = self.beat_frame.beat_adder.calculate_next_beat_number()
        num_beats = int(self.layout_settings.get_layout_setting("num_beats"))

        if (
            next_beat_number > num_beats
        ) and not self.layout_settings.get_layout_setting("grow_sequence"):
            error_message = (
                f"Can't add the beat. Sequence length is set to "
                f"{next_beat_number - 1} beats."
            )
            self.sequence_workbench.indicator_label.show_message(error_message)
            return
        self.beat_frame.beat_adder.add_beat_to_sequence(new_beat)

        if new_beat.view:
            selection_manager = self.beat_frame.selection_overlay
            selection_manager.select_beat(new_beat.view)
            QApplication.processEvents()

            self.option_picker.update_option_picker()

            new_beat.view.is_filled = True
            self.option_picker.scroll_area.display_manager.order_and_display_pictographs()
            self.option_picker.choose_your_next_pictograph_label.set_default_text()

        QApplication.restoreOverrideCursor()
