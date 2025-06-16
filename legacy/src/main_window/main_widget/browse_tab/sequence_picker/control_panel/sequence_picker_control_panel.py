from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.browse_tab.sequence_picker.control_panel.sequence_picker_go_back_button import (
    SequencePickerGoBackButton,
)

from .currently_displaying_label import (
    CurrentlyDisplayingLabel,
)
from .sequence_picker_count_label import SequencePickerCountLabel
from .sort_widget.sequence_picker_sort_widget import SequencePickerSortWidget

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.sequence_picker import (
        SequencePicker,
    )


class SequencePickerControlPanel(QWidget):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker

        # Debug control panel creation
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🏗️ Creating SequencePickerControlPanel")
        logger.info(f"Control panel parent: {sequence_picker}")

        self._setup_ui()

        logger.info("✅ SequencePickerControlPanel created successfully")

    def _setup_ui(self):
        import logging

        logger = logging.getLogger(__name__)

        logger.info("🔧 Setting up control panel UI")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        logger.info("🔘 Creating go back button...")
        self.go_back_button = SequencePickerGoBackButton(self.sequence_picker)
        logger.info(f"✅ Go back button created: {self.go_back_button}")

        logger.info("🏷️ Creating other control panel widgets...")
        self.currently_displaying_label = CurrentlyDisplayingLabel(self.sequence_picker)
        self.count_label = SequencePickerCountLabel(self.sequence_picker)
        self.sort_widget = SequencePickerSortWidget(self.sequence_picker)

        logger.info("📦 Adding widgets to layout...")
        self.main_layout.addWidget(self.go_back_button)
        self.main_layout.addWidget(self.currently_displaying_label)
        self.main_layout.addWidget(self.count_label)
        self.main_layout.addWidget(self.sort_widget)

        self.setLayout(self.main_layout)
        logger.info("✅ Control panel UI setup completed")

        # Debug: Check if this control panel is actually visible
        logger.info(f"Control panel visible: {self.isVisible()}")
        logger.info(f"Control panel size: {self.size()}")
        logger.info(f"Control panel parent: {self.parent()}")

        # Check if the sequence picker (parent) is in the left stack
        if hasattr(self.sequence_picker.main_widget, "left_stack"):
            left_stack = self.sequence_picker.main_widget.left_stack
            current_index = left_stack.currentIndex()
            logger.info(f"Left stack current index: {current_index}")
            logger.info(f"Left stack widget count: {left_stack.count()}")

            # Check if sequence picker is the current widget
            current_widget = left_stack.currentWidget()
            logger.info(f"Current left stack widget: {current_widget}")
            logger.info(f"Sequence picker widget: {self.sequence_picker}")
            logger.info(
                f"Is sequence picker current? {current_widget == self.sequence_picker}"
            )

            # Check all widgets in the stack
            for i in range(left_stack.count()):
                widget = left_stack.widget(i)
                logger.info(f"Left stack index {i}: {widget}")
        else:
            logger.warning("Main widget has no left_stack attribute")
