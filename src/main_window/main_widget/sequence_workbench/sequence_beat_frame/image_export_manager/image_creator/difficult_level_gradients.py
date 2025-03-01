# /f:/CODE/the-kinetic-constructor-desktop/main_window/main_widget/sequence_workbench/sequence_beat_frame/image_export_manager/image_creator/difficulty_level_gradients.py
from PyQt6.QtGui import QLinearGradient, QColor
from PyQt6.QtCore import QPointF, QRect, Qt


class DifficultyLevelGradients:
    def __init__(self):
        self.gradients = {
            1: [(0, Qt.GlobalColor.white), (1, Qt.GlobalColor.white)],
            2: [
                (0, QColor(220, 220, 220)),
                (0.4, QColor(190, 190, 190)),
                (0.7, QColor(170, 170, 170)),
                (1, QColor(200, 200, 200)),
            ],
            3: [
                (0, QColor(255, 235, 153)),
                (0.4, QColor(255, 223, 77)),
                (0.8, QColor(238, 201, 0)),
                (1, QColor(204, 164, 0)),
            ],
            4: [
                (0, QColor(200, 162, 200)),
                (0.3, QColor(170, 132, 170)),
                (0.6, QColor(148, 0, 211)),
                (1, QColor(100, 0, 150)),
            ],
            5: [
                (0, QColor(255, 69, 0)),
                (0.4, QColor(255, 0, 0)),
                (0.8, QColor(139, 0, 0)),
                (1, QColor(100, 0, 0)),
            ],
        }  # I hope you appreciate this dictionary. It's a work of art, if I do say so myself.

    def get_gradient(self, rect: QRect, difficulty_level: int) -> QLinearGradient:
        gradient = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.bottomRight()))

        if difficulty_level in self.gradients:
            for pos, color in self.gradients[difficulty_level]:
                gradient.setColorAt(pos, color)
        else:
            # Default gradient if difficulty level is not found. Because we handle errors with grace.
            gradient.setColorAt(0, Qt.GlobalColor.white)
            gradient.setColorAt(1, Qt.GlobalColor.white)
        return gradient
