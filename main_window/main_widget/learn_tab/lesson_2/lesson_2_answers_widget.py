# lesson_2_answers_widget.py
from main_window.main_widget.learn_tab.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.generic_answers_widget import (
    GenericAnswersWidget,
)
from main_window.main_widget.learn_tab.base_classes.pictograph_answers_renderer import (
    PictographAnswersRenderer,
)


class Lesson2AnswersWidget(BaseAnswersWidget):
    def __init__(self, lesson_2_widget):
        super().__init__(lesson_2_widget)
        self.renderer = PictographAnswersRenderer(columns=2, spacing=30)
        self.generic_widget = GenericAnswersWidget(lesson_2_widget, self.renderer)
        self.setLayout(self.generic_widget.layout())

    def create_answer_buttons(
        self, pictograph_data_list, correct_pictograph, check_answer_callback
    ) -> None:
        self.generic_widget.create_answer_options(
            pictograph_data_list, correct_pictograph, check_answer_callback
        )

    def update_answer_buttons(
        self, pictograph_data_list, correct_pictograph, check_answer_callback
    ) -> None:
        self.generic_widget.update_answer_options(
            pictograph_data_list, correct_pictograph, check_answer_callback
        )

    def disable_answer(self, answer) -> None:
        self.generic_widget.disable_answer(answer)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        size = int(self.main_widget.height() // 4)
        for view in self.renderer.pictograph_views.values():
            view.setFixedSize(size, size)
