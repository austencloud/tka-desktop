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
        """Switch to the initial selection page in the stacked layout with layout preservation."""
        # Preserve browse tab layout ratios before stack switching
        self._preserve_browse_tab_layout()

        # Use fade stack switching with layout preservation
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

    def _preserve_browse_tab_layout(self):
        """Preserve the browse tab's 2:1 layout ratio during stack switching."""
        try:
            # Ensure browse tab layout ratios are preserved during stack switching
            if hasattr(self.main_widget, "content_layout"):
                # Set browse tab's 2:1 stretch ratio
                self.main_widget.content_layout.setStretch(0, 2)  # Left stack: 2 parts
                self.main_widget.content_layout.setStretch(1, 1)  # Right stack: 1 part

                # Clear any fixed width constraints that might interfere
                if hasattr(self.main_widget, "left_stack"):
                    self.main_widget.left_stack.setMaximumWidth(
                        16777215
                    )  # QWIDGETSIZE_MAX
                    self.main_widget.left_stack.setMinimumWidth(0)
                if hasattr(self.main_widget, "right_stack"):
                    self.main_widget.right_stack.setMaximumWidth(
                        16777215
                    )  # QWIDGETSIZE_MAX
                    self.main_widget.right_stack.setMinimumWidth(0)

        except Exception as e:
            # Log the error but don't fail the operation
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to preserve browse tab layout: {e}")
