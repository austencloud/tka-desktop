from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QKeyEvent
from PyQt6.QtWidgets import QLineEdit
from main_window.main_widget.write_tab.editable_label_manager import (
    EditableLabelManager,
)

if TYPE_CHECKING:
    from .timestamp import Timestamp


class TimestampLineEdit(QLineEdit):
    def __init__(self, timestamp: "Timestamp", initial_text="0:00"):
        super().__init__(initial_text)
        self.timestamp = timestamp

        # Regular expression to validate only X:XX format
        self.timestamp_regex = QRegularExpression(r"^\d{1,2}:\d{2}$")
        self.validator = QRegularExpressionValidator(self.timestamp_regex)
        self.setValidator(None)  # Temporarily bypass validator for formatting
        self.setMaxLength(5)  # Max length for "X:XX" format

        # Styling to match `EditableLabel`
        self.setStyleSheet(
            "background-color: #FFFFFF; border: 1px solid gray; padding: 5px;"
        )
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Track for initial clear on first input
        self.first_keypress = True

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events to auto-format input as a timestamp."""
        key = event.key()

        # Clear initial text on the first keypress
        if self.first_keypress:
            self.clear()
            self.first_keypress = False

        # Allow Backspace and Delete without blocking
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            super().keyPressEvent(event)
            self._apply_temporary_format()  # Update format after deletion
            return

        # Handle numeric input only and restrict to exactly 3 digits
        if event.text().isdigit():
            current_text = self.text().replace(":", "")
            new_text = current_text + event.text()

            # Prevent invalid seconds values by checking the second digit for tens of seconds
            if len(new_text) == 2 and int(new_text[1]) > 5:
                return  # Reject if tens of seconds > 5

            # Apply custom formatting based on number of digits
            formatted_text = ""
            if len(new_text) == 1:
                formatted_text = f"{new_text}:"
            elif len(new_text) == 2:
                formatted_text = f"{new_text[0]}:{new_text[1]}"
            elif len(new_text) == 3:
                formatted_text = f"{new_text[0]}:{new_text[1:]}"
                self.setText(formatted_text)
                self._auto_accept()  # Accept automatically once in X:XX format
                return

            self.setText(formatted_text)
            self.setCursorPosition(len(self.text()))  # Move cursor to end

        event.accept()

    def _apply_temporary_format(self):
        """Apply temporary format to text for visual feedback."""
        current_text = self.text().replace(":", "")
        formatted_text = ""
        if len(current_text) == 1:
            formatted_text = f"{current_text}:"
        elif len(current_text) == 2:
            formatted_text = f"{current_text[0]}:{current_text[1]}"
        elif len(current_text) == 3:
            formatted_text = f"{current_text[0]}:{current_text[1:]}"

        self.setText(formatted_text)
        self.setCursorPosition(len(self.text()))

    def _auto_accept(self):
        """Automatically accept the timestamp once in X:XX format."""
        self.setValidator(self.validator)
        self.clearFocus()
        self.setValidator(None)  # Disable to allow edits again later
        self._hide_edit()  # Hide the edit field

    def _hide_edit(self) -> None:
        """Hide the edit field and update the timestamp display."""
        text = self.text()
        self.timestamp.label.setText(text)
        self.timestamp.layout.setCurrentWidget(self.timestamp.label)
        EditableLabelManager.clear_active()
