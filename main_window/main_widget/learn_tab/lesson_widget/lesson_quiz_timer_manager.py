# quiz_timer_manager.py

from PyQt6.QtCore import QTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lesson_widget import LessonWidget


class QuizTimerManager:
    """Handles timer logic for the quiz."""

    def __init__(self, lesson: "LessonWidget"):
        self.lesson = lesson
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self, duration):
        """Start the quiz timer."""
        self.lesson.quiz_time = duration

        # Update the timer label immediately
        minutes, seconds = divmod(self.lesson.quiz_time, 60)
        self.lesson.progress_label.setText(f"Time Remaining: {minutes}:{seconds:02d}")

        self.timer.start(1000)

    def update_timer(self):
        """Update the quiz timer each second."""

        # Decrement the quiz_time first
        self.lesson.quiz_time -= 1

        if self.lesson.quiz_time >= 0:
            minutes, seconds = divmod(self.lesson.quiz_time, 60)
            self.lesson.progress_label.setText(
                f"Time Remaining: {minutes}:{seconds:02d}"
            )
        else:
            self.timer.stop()
            self.lesson.learn_tab.results_widget.show_results(
                self, self.lesson.incorrect_guesses
            )

    def stop_timer(self):
        """Stop the quiz timer."""
        if self.timer.isActive():
            self.timer.stop()
