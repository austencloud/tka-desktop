"""
Turn slider component for the codex exporter.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from .turn_config_style_provider import TurnConfigStyleProvider


class TurnSlider(QWidget):
    """Reusable component for configuring turn values."""

    # Signal emitted when the turn value changes
    value_changed = pyqtSignal(float)

    def __init__(
        self,
        label_text,
        accent_color,
        parent=None,
        style_provider=None,
        initial_value=0.0,
    ):
        """Initialize the turn slider.

        Args:
            label_text: The label text for the slider
            accent_color: The accent color for the slider
            parent: The parent widget
            style_provider: The style provider for consistent styling
            initial_value: The initial value for the slider
        """
        super().__init__(parent)
        self.label_text = label_text
        self.accent_color = accent_color
        self.style_provider = style_provider or TurnConfigStyleProvider(self)
        self.initial_value = initial_value
        self._setup_ui()

    def _setup_ui(self):
        """Set up the turn slider UI."""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style_provider.slider_spacing)

        # Create header layout
        header_layout = QHBoxLayout()

        # Create label
        self.turn_label = QLabel(self.label_text, self)
        self.turn_label.setStyleSheet(
            self.style_provider.get_turn_label_style(self.accent_color)
        )

        # Create value label
        self.value_label = QLabel(f"{self.initial_value:.1f}", self)
        self.value_label.setStyleSheet(
            self.style_provider.get_turn_value_label_style(self.accent_color)
        )
        self.value_label.setMinimumWidth(self.style_provider.value_min_width)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # Add to header layout
        header_layout.addWidget(self.turn_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.value_label)

        # Create slider
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.slider.setRange(0, 6)  # 0 to 3 in 0.5 increments
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setValue(int(self.initial_value * 2))  # Convert to slider value
        self.slider.valueChanged.connect(self._update_value_label)
        self.slider.setStyleSheet(
            self.style_provider.get_slider_style(self.accent_color)
        )

        # Make the slider taller
        self.slider.setMinimumHeight(40)  # Adjust this value as needed
        self.slider.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        # Add to layout with more spacing
        layout.addLayout(header_layout)
        layout.addSpacing(10)  # Add some space between the header and the slider
        layout.addWidget(self.slider)
        layout.addSpacing(10)  # Add some space at the bottom

    def _update_value_label(self, value):
        """Update the value label when the slider value changes.

        Args:
            value: The new slider value
        """
        turn_value = value / 2.0
        self.value_label.setText(f"{turn_value:.1f}")
        self.value_changed.emit(turn_value)

    def set_value(self, value):
        """Set the slider value.

        Args:
            value: The new value (0.0 to 3.0)
        """
        self.slider.setValue(int(value * 2))

    def get_value(self):
        """Get the current slider value.

        Returns:
            float: The current value (0.0 to 3.0)
        """
        return self.slider.value() / 2.0

    def set_enabled(self, enabled):
        """Enable or disable the slider.

        Args:
            enabled: Whether the slider should be enabled
        """
        self.slider.setEnabled(enabled)
        self.value_label.setEnabled(enabled)

        # Update styling based on enabled state
        if enabled:
            self.slider.setStyleSheet(
                self.style_provider.get_slider_style(self.accent_color)
            )
            self.value_label.setStyleSheet(
                self.style_provider.get_turn_value_label_style(self.accent_color)
            )
        else:
            self.slider.setStyleSheet(
                self.style_provider.get_slider_style(self.accent_color, False)
            )
            self.value_label.setStyleSheet(
                self.style_provider.get_turn_value_label_style(self.accent_color, False)
            )
