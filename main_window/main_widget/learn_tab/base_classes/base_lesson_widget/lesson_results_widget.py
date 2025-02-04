from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_start_over_button import LessonStartOverButton

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class LessonResultsWidget(QWidget):
    """Widget containing the result label and the 'Start Over' button."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget

        # Set an object name for styling
        self.setObjectName("ResultsWidget")

        # Create result label and start over button
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("color: white; font-weight: bold;")

        # Create a frame to hold the result label (the semi-transparent section)
        self.result_section = QFrame(self)
        self.result_section.setObjectName("ResultSection")

        # Apply styling for the result section to give it a semi-transparent background
        self.result_section.setStyleSheet(
            """
            QFrame#ResultSection {
                background-color: rgba(0, 0, 0, 150);  /* Semi-transparent dark background */
                border-radius: 15px;  /* Rounded corners */
                padding: 20px;  /* Padding around the text for better spacing */
            }
        """
        )

        # Layout for the result section
        result_section_layout = QVBoxLayout(self.result_section)
        result_section_layout.addWidget(self.result_label)
        result_section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Start Over button
        self.start_over_button = LessonStartOverButton(self)

        # Layout setup
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(
            20, 20, 20, 20
        )  # Adjust margins for rounded edges
        self.layout.setSpacing(10)

        # Add the result section and the start over button to the main layout
        self.layout.addStretch(3)
        self.layout.addWidget(
            self.result_section, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.start_over_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addStretch(3)

        self.setLayout(self.layout)

        # Apply stylesheet for the entire widget for consistency
        self.setStyleSheet(
            """
            QWidget#ResultsWidget {
                background-color: rgba(255, 255, 255, 200);  /* Semi-transparent white */
                border-radius: 15px;
            }
        """
        )

    def set_result_text(self, text: str):
        """Set the result text for the result label."""
        self.result_label.setText(text)
        self.adjustSize()

    def resizeEvent(self, event):
        """Resize the result label and start-over button to fit the content."""
        self._resize_result_label()
        self._resize_start_over_button()

    def _resize_start_over_button(self):
        start_over_button_font_size = self.main_widget.width() // 60
        self.start_over_button.setStyleSheet(
            f"font-size: {start_over_button_font_size}px;"
        )
        self.start_over_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )

    def _resize_result_label(self):
        result_label_font_size = self.main_widget.width() // 100
        font = self.result_label.font()
        font.setPointSize(result_label_font_size)
        self.result_label.setFont(font)
        self.result_label.adjustSize()

    def show_results(self, incorrect_guesses):
        """Display the results after the quiz or countdown ends."""
        self.lesson_widget.central_layout.addWidget(self)

        self.set_result_text(
            f"🎉 Well done!! 🎉\n\n"
            + f"You successfully completed {self.lesson_widget.current_question - 1} question"
            + f"{'s' if self.lesson_widget.current_question - 1 != 1 else ''}"
            + (
                f"!\nwithout making any mistakes! Great job!"
                if incorrect_guesses == 0
                else f" but you made {incorrect_guesses} mistake"
                f"{'s' if incorrect_guesses != 1 else ''}.\nKeep on practicing!"
            )
        )
