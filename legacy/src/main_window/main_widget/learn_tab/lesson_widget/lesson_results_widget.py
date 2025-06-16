from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from main_window.main_widget.learn_tab.lesson_widget.lesson_results_label import (
    LessonResultLabel,
)
from main_window.main_widget.learn_tab.lesson_widget.lesson_start_over_button import (
    LessonStartOverButton,
)


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.learn_tab import LearnTab
    from main_window.main_widget.learn_tab.lesson_widget.lesson_widget import (
        LessonWidget,
    )


class LessonResultsWidget(QWidget):
    """Widget containing the result label and the 'Start Over' button."""

    def __init__(self, learn_tab: "LearnTab"):
        super().__init__(learn_tab)
        self.learn_tab = learn_tab
        self.main_widget = learn_tab.main_widget
        self.result_label = LessonResultLabel(self)

        self.setObjectName("ResultsWidget")

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("color: white; font-weight: bold;")
        self.result_section = QFrame(self)
        self.result_section.setObjectName("ResultSection")
        self.result_section.setStyleSheet(
            """
            QFrame#ResultSection {
                background-color: rgba(0, 0, 0, 150);  /* Semi-transparent dark background */
                border-radius: 15px;  /* Rounded corners */
                padding: 20px;  /* Padding around the text for better spacing */
            }
        """
        )

        result_section_layout = QVBoxLayout(self.result_section)
        result_section_layout.addWidget(self.result_label)
        result_section_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_over_button = LessonStartOverButton(self)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

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

    def _resize_result_label(self):
        result_label_font_size = self.main_widget.width() // 100
        font = self.result_label.font()
        font.setPointSize(result_label_font_size)
        self.result_label.setFont(font)
        self.result_label.adjustSize()

    def show_results(self, lesson_widget: "LessonWidget", incorrect_guesses):
        """Display the results after the quiz or countdown ends."""
        self.set_result_text(
            f"🎉 Well done!! 🎉\n\n"
            + f"You successfully completed {lesson_widget.current_question - 1} question"
            + f"{'s' if lesson_widget.current_question - 1 != 1 else ''}"
            + (
                f"!\nwithout making any mistakes! Great job!"
                if incorrect_guesses == 0
                else f" but you made {incorrect_guesses} mistake"
                f"{'s' if incorrect_guesses != 1 else ''}.\nKeep on practicing!"
            )
        )
        widgets_to_fade = [
            lesson_widget.question_widget,
            lesson_widget.answers_widget,
            lesson_widget.indicator_label,
            lesson_widget.progress_label,
            self,
        ]
        widget_fader = self.main_widget.fade_manager.widget_fader
        widget_fader.fade_and_update(
            widgets_to_fade, lambda: self._fade_to_results(lesson_widget)
        )

    def _fade_to_results(self, lesson_widget: "LessonWidget"):
        lesson_widget.learn_tab.stack.setCurrentWidget(self)
        lesson_widget.prepare_quiz_ui(lesson_widget.mode)
        stack_fader = self.main_widget.fade_manager.stack_fader

        self.start_over_button.clicked.connect(
            lambda: stack_fader.fade_stack(
                self.learn_tab.stack,
                self.learn_tab.stack.indexOf(lesson_widget),
                300,
                lambda: self.learn_tab.stack.setCurrentWidget(lesson_widget),
            )
        )
