from typing import TYPE_CHECKING

from styles.styled_button import StyledButton


if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.lesson_widget.lesson_widget import (
        LessonWidget,
    )


class LessonGoBackButton(StyledButton):
    def __init__(self, lesson_widget: "LessonWidget"):
        super().__init__("Back")
        self.lesson_widget = lesson_widget
        self.main_widget = self.lesson_widget.main_widget
        learn_tab = self.lesson_widget.learn_tab
        stack_fader = learn_tab.main_widget.fade_manager.stack_fader
        self.clicked.connect(lambda: stack_fader.fade_stack(learn_tab.stack, 0))
