from typing import TYPE_CHECKING
from PyQt6.QtGui import QFontMetrics
from main_window.main_widget.tab_indices import LeftStackIndex
from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerGoBackButton(StyledButton):
    """A go-back button that returns to the initial filter selection."""

    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__("Go Back")
        self.sequence_picker = sequence_picker
        self.browse_tab = self.sequence_picker.browse_tab
        self.main_widget = self.sequence_picker.main_widget
        self.clicked.connect(self.switch_to_initial_filter_selection)

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        self.main_widget.fade_manager.stack_fader.fade_stack(
            self.main_widget.left_stack, LeftStackIndex.FILTER_SELECTOR, 300
        )
        self.browse_tab.browse_settings.set_browse_left_stack_index(
            LeftStackIndex.FILTER_SELECTOR.value
        )
        self.browse_tab.browse_settings.set_current_section("filter_selector")
        self.browse_tab.browse_settings.set_current_filter(None)

    def resizeEvent(self, event) -> None:
        """Handle resizing to update styles dynamically."""
        self._border_radius = min(self.height(), self.width()) // 2
        self.update_appearance()
        self.setFixedWidth(int(self.sequence_picker.main_widget.width() // 15))
        self.setFixedHeight(int(self.sequence_picker.main_widget.height() // 16))

        # Set the font size programmatically according to the button width
        font = self.font()
        font_size = QFontMetrics(font).horizontalAdvance(self.text()) // len(
            self.text()
        )
        # Increase the font size by a factor to make it larger
        font.setPointSize(int(font_size * 3))
        self.setFont(font)

        super().resizeEvent(event)
