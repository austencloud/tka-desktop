# learn_tab/base_classes/base_lesson_widget/lesson_layout_manager.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonLayoutManager:
    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.lesson_widget = lesson_widget
        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setup_layout(self):
        self.refresh_central_layout()

        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        back_layout.addWidget(self.lesson_widget.go_back_button)

        indicator_label_layout = QHBoxLayout()
        indicator_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        indicator_label_layout.addWidget(self.lesson_widget.indicator_label)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(back_layout, 1)
        main_layout.addLayout(self.central_layout, 10)
        main_layout.addLayout(indicator_label_layout, 2)
        self.lesson_widget.setLayout(main_layout)

    def refresh_central_layout(self):
        self._clear_stretches(self.central_layout)
        for widget in [
            self.lesson_widget.progress_label,
            self.lesson_widget.question_widget,
            self.lesson_widget.answers_widget,
        ]:
            self.central_layout.addWidget(widget)
            self.central_layout.addStretch(1)

    def _clear_stretches(self, layout: QVBoxLayout) -> None:
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.spacerItem():
                layout.takeAt(i)
