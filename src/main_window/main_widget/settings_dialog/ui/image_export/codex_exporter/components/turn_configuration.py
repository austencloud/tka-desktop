"""
Turn configuration component for the codex exporter dialog.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QButtonGroup,
    QSlider,
)
from PyQt6.QtCore import Qt
from settings_manager.settings_manager import SettingsManager
from ..widgets import ModernCard, ModernSlider, ModernRadioButton


class TurnConfigurationComponent(QWidget):
    """Component for configuring turns."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the turn configuration UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create the card
        turn_card = ModernCard(self, "Turn Configuration")
        turn_layout = QVBoxLayout()

        # Grid mode selection
        grid_mode_layout = QHBoxLayout()
        grid_mode_label = QLabel("Grid Mode:")
        grid_mode_label.setStyleSheet(
            "font-weight: bold; color: palette(windowtext); background-color: transparent;"
        )

        self.grid_mode_group = QButtonGroup(self)
        self.diamond_radio = ModernRadioButton("Diamond", self)
        self.box_radio = ModernRadioButton("Box", self)

        # Set default based on settings
        grid_mode = self.settings_manager.codex_exporter.get_grid_mode()
        if grid_mode == "box":
            self.box_radio.setChecked(True)
        else:
            self.diamond_radio.setChecked(True)

        self.grid_mode_group.addButton(self.diamond_radio)
        self.grid_mode_group.addButton(self.box_radio)

        grid_mode_layout.addWidget(grid_mode_label)
        grid_mode_layout.addWidget(self.diamond_radio)
        grid_mode_layout.addWidget(self.box_radio)
        grid_mode_layout.addStretch()

        turn_layout.addLayout(grid_mode_layout)

        # Turn sliders
        turn_selection_layout = QVBoxLayout()

        # First turn slider (red hand)
        first_turn_layout = QHBoxLayout()
        first_turn_label = QLabel("Red Hand Turns:")
        first_turn_label.setStyleSheet(
            "color: #e74c3c; font-weight: bold; background-color: transparent;"
        )

        self.first_turn_slider = ModernSlider(Qt.Orientation.Horizontal, self)
        self.first_turn_slider.setRange(0, 6)  # 0 to 3 turns in 0.5 increments
        self.first_turn_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.first_turn_slider.setTickInterval(1)

        # Set default from settings
        last_red_turns = self.settings_manager.codex_exporter.get_last_red_turns()
        self.first_turn_slider.setValue(int(last_red_turns * 2))

        self.first_turn_value_label = QLabel(f"{last_red_turns:.1f}")
        self.first_turn_value_label.setStyleSheet(
            "color: #e74c3c; font-weight: bold; background-color: transparent;"
        )
        self.first_turn_slider.valueChanged.connect(self._update_first_turn_label)

        first_turn_layout.addWidget(first_turn_label)
        first_turn_layout.addWidget(self.first_turn_slider)
        first_turn_layout.addWidget(self.first_turn_value_label)

        # Second turn slider (blue hand)
        second_turn_layout = QHBoxLayout()
        second_turn_label = QLabel("Blue Hand Turns:")
        second_turn_label.setStyleSheet(
            "color: #3498db; font-weight: bold; background-color: transparent;"
        )

        self.second_turn_slider = ModernSlider(Qt.Orientation.Horizontal, self)
        self.second_turn_slider.setRange(0, 6)  # 0 to 3 turns in 0.5 increments
        self.second_turn_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.second_turn_slider.setTickInterval(1)

        # Set default from settings
        last_blue_turns = self.settings_manager.codex_exporter.get_last_blue_turns()
        self.second_turn_slider.setValue(int(last_blue_turns * 2))

        self.second_turn_value_label = QLabel(f"{last_blue_turns:.1f}")
        self.second_turn_value_label.setStyleSheet(
            "color: #3498db; font-weight: bold; background-color: transparent;"
        )
        self.second_turn_slider.valueChanged.connect(self._update_second_turn_label)

        second_turn_layout.addWidget(second_turn_label)
        second_turn_layout.addWidget(self.second_turn_slider)
        second_turn_layout.addWidget(self.second_turn_value_label)

        turn_selection_layout.addLayout(first_turn_layout)
        turn_selection_layout.addLayout(second_turn_layout)

        # Generate all checkbox
        self.generate_all_checkbox = QCheckBox(
            "Generate All Turn Combinations (0-3 turns)"
        )
        self.generate_all_checkbox.setChecked(False)
        self.generate_all_checkbox.setStyleSheet("color: palette(windowtext);")
        self.generate_all_checkbox.stateChanged.connect(self._update_sliders_state)

        # Add info label
        info_label = QLabel(
            "Note: Hybrid pictographs (C, F, I, L, O, R, S, T, U, V) "
            "will generate multiple images with different turn combinations."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet(
            "color: palette(windowtext); font-style: italic; background-color: transparent;"
        )

        # Add the controls to the turn layout
        turn_layout.addLayout(turn_selection_layout)
        turn_layout.addWidget(self.generate_all_checkbox)
        turn_layout.addWidget(info_label)

        turn_card.layout.addLayout(turn_layout)
        layout.addWidget(turn_card)

    def _update_first_turn_label(self, value):
        """Update the first turn value label."""
        turn_value = value / 2.0
        self.first_turn_value_label.setText(f"{turn_value:.1f}")

    def _update_second_turn_label(self, value):
        """Update the second turn value label."""
        turn_value = value / 2.0
        self.second_turn_value_label.setText(f"{turn_value:.1f}")

    def _update_sliders_state(self, state):
        """Update the state of the sliders based on the generate all checkbox."""
        enabled = not bool(state)
        self.first_turn_slider.setEnabled(enabled)
        self.second_turn_slider.setEnabled(enabled)
        self.first_turn_value_label.setEnabled(enabled)
        self.second_turn_value_label.setEnabled(enabled)

    def get_turn_values(self):
        """Get the selected turn values."""
        red_turns = self.first_turn_slider.value() / 2.0
        blue_turns = self.second_turn_slider.value() / 2.0
        generate_all = self.generate_all_checkbox.isChecked()
        grid_mode = "box" if self.box_radio.isChecked() else "diamond"

        return {
            "red_turns": red_turns,
            "blue_turns": blue_turns,
            "generate_all": generate_all,
            "grid_mode": grid_mode,
        }
