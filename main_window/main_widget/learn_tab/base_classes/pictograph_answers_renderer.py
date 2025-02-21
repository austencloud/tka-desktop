from typing import Any, List, Callable
from PyQt6.QtWidgets import QGridLayout, QWidget
from PyQt6.QtCore import Qt
from base_widgets.pictograph.pictograph_view import PictographView
from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.learn_tab.base_classes.base_answers_renderer import (
    BaseAnswersRenderer,
)
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)
from main_window.main_widget.pictograph_key_generator import PictographKeyGenerator


class PictographAnswersRenderer(BaseAnswersRenderer):
    def __init__(self, columns: int = 2, spacing: int = 30):
        """
        :param key_generator: a function or object that can generate a unique, hashable key from the pictograph dict.
        :param columns: number of columns in the grid
        :param spacing: spacing between grid cells
        """
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.columns = columns
        self.key_generator = PictographKeyGenerator()

        # We'll store view widgets keyed by the generated string (or tuple).
        self.pictograph_views: dict[str, LessonPictographView] = {}

    def get_layout(self):
        return self.layout

    def create_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],  # each answer is a dict describing a pictograph
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        # Clear the grid layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.pictograph_views.clear()

        for i, answer in enumerate(answers):
            # Generate a stable, hashable key from the pictograph data
            answer_key = self.key_generator.generate_pictograph_key(answer)

            # Create the pictograph scene and view
            scene = PictographScene()
            view = LessonPictographView(scene)
            scene.elements.view = view

            # Update the scene with the pictograph data
            scene.managers.updater.update_pictograph(answer)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)

            # Capture the current answer in the mouse event
            view.mousePressEvent = lambda event, a=answer: check_callback(
                a, correct_answer
            )

            # Place the view in the grid
            row, col = divmod(i, self.columns)
            self.layout.addWidget(view, row, col)

            # Store in our dictionary keyed by the stable key
            self.pictograph_views[answer_key] = view

    def update_answer_options(
        self,
        parent: QWidget,
        answers: List[Any],
        check_callback: Callable[[Any, Any], None],
        correct_answer: Any,
    ) -> None:
        """
        If the number of answers differs from what's stored, we recreate everything.
        Otherwise, we just update each existing view in place.
        """
        # If the number of new answers doesn't match existing, just recreate.
        if len(self.pictograph_views) != len(answers):
            self.create_answer_options(parent, answers, check_callback, correct_answer)
            return

        # Clear the old dictionary so we can rebuild it with new keys
        self.pictograph_views.clear()

        # Update each item in-place
        for i, answer in enumerate(answers):
            item = self.layout.itemAt(i)
            view: LessonPictographView = item.widget()
            scene = view.pictograph

            scene.managers.updater.update_pictograph(answer)
            scene.elements.view.update_borders()
            scene.state.quiz_mode = True
            scene.elements.tka_glyph.setVisible(False)

            # Reassign the mousePressEvent
            view.mousePressEvent = lambda event, a=answer: check_callback(
                a, correct_answer
            )

            # Generate a stable key again
            answer_key = self.key_generator.generate_pictograph_key(answer)
            self.pictograph_views[answer_key] = view

    def disable_answer_option(self, answer: Any) -> None:
        """
        'answer' is a dict, so we convert it to a stable key
        and look up the corresponding view to disable it.
        """
        answer_key = self.key_generator.generate_pictograph_key(answer)
        if answer_key in self.pictograph_views:
            view: LessonPictographView = self.pictograph_views[answer_key]
            view.setEnabled(False)
            view.set_overlay_color("red")
