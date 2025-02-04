from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWorkbench,
    )


class DifficultyLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWorkbench") -> None:
        super().__init__(sequence_widget)
        self.main_widget = sequence_widget.main_widget
        self.json_manager = self.main_widget.json_manager
        self.difficulty_level = 1
        self.setFont(QFont("Arial", sequence_widget.width() // 40))
        self.setToolTip("Difficulty Level")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_difficulty_level(self, level: Union[int, str]) -> None:
        if level == "":
            self.setText("")
            return
        self.difficulty_level = level
        self.setText(f"Level {self.difficulty_level}")
        self.update()

    def update_difficulty_label(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        difficulty_level = (
            self.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                sequence
            )
        )
        self.set_difficulty_level(difficulty_level)
