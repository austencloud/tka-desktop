"""
Generate all checkbox component for the codex exporter.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from .turn_config_style_provider import TurnConfigStyleProvider


class GenerateAllCheckbox(QWidget):
    """Checkbox for generating all turn combinations."""

    # Signal emitted when the checkbox state changes
    state_changed = pyqtSignal(bool)

    def __init__(self, parent=None, style_provider=None, initial_state=False):
        """Initialize the generate all checkbox.

        Args:
            parent: The parent widget
            style_provider: The style provider for consistent styling
            initial_state: The initial state of the checkbox
        """
        super().__init__(parent)
        self.style_provider = style_provider or TurnConfigStyleProvider(self)
        self.initial_state = initial_state
        self._setup_ui()

    def _setup_ui(self):
        """Set up the generate all checkbox UI."""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create checkbox
        self.checkbox = QCheckBox("Generate all turn combinations (0-3 turns)", self)
        self.checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.checkbox.setChecked(self.initial_state)
        self.checkbox.setStyleSheet(self.style_provider.get_checkbox_style())
        self.checkbox.stateChanged.connect(self._on_state_changed)

        # Add to layout
        layout.addWidget(self.checkbox)

    def _on_state_changed(self, state):
        """Handle checkbox state changes.

        Args:
            state: The new checkbox state
        """
        self.state_changed.emit(bool(state))

    def is_checked(self):
        """Get the current checkbox state.

        Returns:
            bool: Whether the checkbox is checked
        """
        return self.checkbox.isChecked()

    def set_checked(self, checked):
        """Set the checkbox state.

        Args:
            checked: The new checkbox state
        """
        self.checkbox.setChecked(checked)
