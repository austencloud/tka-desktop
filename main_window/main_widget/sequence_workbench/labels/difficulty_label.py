from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class DifficultyLabel(QLabel):
    def __init__(self, sequence_workbench: "SequenceWorkbench") -> None:
        super().__init__(sequence_workbench)
        self.main_widget = sequence_workbench.main_widget
        self.difficulty_level = 1
        self.setFont(QFont("Arial", sequence_workbench.width() // 40))
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
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()
        difficulty_level = (
            self.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                sequence
            )
        )
        self.set_difficulty_level(difficulty_level)
