from typing import TYPE_CHECKING

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )


class LessonIndicatorLabel(BaseIndicatorLabel):
    def __init__(self, lesson_widget: "BaseLessonWidget") -> None:
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.setStyleSheet(
            """
            LessonIndicatorLabel {
            background-color: rgba(255, 255, 255, 128); /* semi-transparent white */
            border-radius: 10px; /* rounded edges */
            }
            """
        )

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.lesson_widget.height() // 16)
        # get the width from font metrics - 
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self.text())
        self.setFixedWidth(text_width + 20)  # add some padding
        font = self.font()
        font.setPointSize(self.lesson_widget.learn_tab.main_widget.width() // 60)
        self.setFont(font)
        super().resizeEvent(event)
