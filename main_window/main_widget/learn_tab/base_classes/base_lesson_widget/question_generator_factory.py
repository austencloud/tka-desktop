from main_window.main_widget.learn_tab.base_classes.base_question_generator import (
    BaseQuestionGenerator,
)
from main_window.main_widget.learn_tab.lesson_1.lesson_1_question_generator import Lesson1QuestionGenerator
from main_window.main_widget.learn_tab.lesson_2.lesson_2_question_generator import Lesson2QuestionGenerator
from main_window.main_widget.learn_tab.lesson_3.lesson_3_question_generator import Lesson3QuestionGenerator


class QuestionGeneratorFactory:
    """
    Factory to create the correct question generator based on lesson type.
    """

    LESSON_GENERATORS = {
        "Lesson1": Lesson1QuestionGenerator,
        "Lesson2": Lesson2QuestionGenerator,
        "Lesson3": Lesson3QuestionGenerator,
    }

    @staticmethod
    def create_generator(lesson_type: str, lesson_widget) -> BaseQuestionGenerator:
        generator_class = QuestionGeneratorFactory.LESSON_GENERATORS.get(lesson_type)
        if not generator_class:
            raise ValueError(f"Unknown lesson type: {lesson_type}")
        return generator_class(lesson_widget)
