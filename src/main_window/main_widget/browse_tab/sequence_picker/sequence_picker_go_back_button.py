from typing import TYPE_CHECKING

from base_widgets.base_go_back_button import (
    BaseGoBackButton,
)
from main_window.main_widget.tab_indices import LeftStackIndex


if TYPE_CHECKING:
    from .sequence_picker import SequencePicker


class SequencePickerGoBackButton(BaseGoBackButton):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker.main_widget)
        self.sequence_picker = sequence_picker
        self.browse_tab = self.sequence_picker.browse_tab
        self.main_widget = self.sequence_picker.main_widget
        self.clicked.connect(lambda: self.switch_to_initial_filter_selection())

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        sequence_viewer = self.browse_tab.sequence_viewer
        widgets = [
            sequence_viewer.image_label,
            sequence_viewer.placeholder_label,
            sequence_viewer.word_label,
            sequence_viewer.variation_number_label,
            sequence_viewer.nav_buttons_widget,
            sequence_viewer.action_button_panel,
        ]

        self.main_widget.fade_manager.widget_and_stack_fader.fade_widgets_and_stack(
            widgets,
            self.main_widget.left_stack,
            LeftStackIndex.FILTER_SELECTOR,
            300,
            self.browse_tab.sequence_viewer.clear,
        )
        self.browse_tab.browse_settings.set_browse_left_stack_index(
            LeftStackIndex.FILTER_SELECTOR.value
        )
        self.browse_tab.browse_settings.set_current_section("filter_selector")
        self.browse_tab.browse_settings.set_current_filter(None)
        # self.sequence_picker.filter_stack.show_section("filter_selector")
