from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QWidget

from base_widgets.pytoggle import PyToggle

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_selector.lesson_selector import LessonSelector


class LessonModeToggleWidget(QWidget):
    """Widget for selecting quiz modes (Fixed Questions vs Countdown)."""

    def __init__(self, lesson_selector: "LessonSelector"):
        super().__init__(lesson_selector)
        self.lesson_selector = lesson_selector
        # Current mode: "Fixed Questions" by default
        self.current_mode = "fixed_question"

        # Layout setup
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Labels for each mode
        self.fixed_question_label = QLabel("30 Questions")
        self.countdown_label = QLabel("Countdown")

        # Align the labels
        self.fixed_question_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Toggle switch (PyToggle) in the middle
        self.toggle_switch = PyToggle()
        self.toggle_switch.stateChanged.connect(self.toggle_mode)

        # Horizontal spacers for even spacing between the labels and toggle
        fixed_to_toggle_spacer = QSpacerItem(
            20, 0, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )
        toggle_to_countdown_spacer = QSpacerItem(
            20, 0, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )

        # Add elements to the layout
        self.layout.addStretch(2)
        self.layout.addWidget(self.fixed_question_label, 1)
        self.layout.addItem(fixed_to_toggle_spacer)
        self.layout.addWidget(self.toggle_switch, 1)
        self.layout.addItem(toggle_to_countdown_spacer)
        self.layout.addWidget(self.countdown_label, 1)
        self.layout.addStretch(2)

        # Initial style update
        self.update_mode_label_styles()

        # add a black border

    def toggle_mode(self, state):
        """Toggle between the quiz modes when the PyToggle is clicked."""
        if state:
            self.current_mode = "countdown"
        else:
            self.current_mode = "fixed_question"
        self.update_mode_label_styles()

    def update_mode_label_styles(self):
        """Update the styles of the mode labels to indicate the selected mode."""
        global_settings = (
            self.lesson_selector.main_widget.settings_manager.global_settings
        )
        font_color_updater = self.lesson_selector.main_widget.font_color_updater
        if self.current_mode == "fixed_question":
            self.fixed_question_label.setStyleSheet(
                f"font-weight: bold; color: {font_color_updater.get_font_color(global_settings.get_background_type())};"
            )
            self.countdown_label.setStyleSheet("font-weight: normal; color: gray;")
        else:
            self.fixed_question_label.setStyleSheet("font-weight: normal; color: gray;")
            self.countdown_label.setStyleSheet(
                f"font-weight: bold; color: {font_color_updater.get_font_color(global_settings.get_background_type())};"
            )

    def get_selected_mode(self) -> str:
        """Return the currently selected mode."""
        return self.current_mode
