from typing import TYPE_CHECKING

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.lesson_widget import (
        LessonWidget,
    )


class LessonIndicatorLabel(BaseIndicatorLabel):
    def __init__(self, lesson_widget: "LessonWidget") -> None:
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget

    def get_styleSheet(self):
        border_radius = min(self.width(), self.height()) // 2
        return f"""
            LessonIndicatorLabel {{
                background-color: rgba(255, 255, 255, 128); /* semi-transparent white */
                border-radius: {border_radius}px; /* rounded edges */
            }}
            """

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.lesson_widget.height() // 16)
        self.setFixedWidth(self.lesson_widget.width() // 2)
        font = self.font()
        font.setPointSize(self.lesson_widget.learn_tab.main_widget.width() // 60)
        self.setFont(font)
        super().resizeEvent(event)
