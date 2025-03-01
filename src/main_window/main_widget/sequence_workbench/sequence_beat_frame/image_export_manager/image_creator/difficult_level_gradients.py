from PyQt6.QtGui import QLinearGradient, QColor
from PyQt6.QtCore import QPointF, QRect, Qt


class DifficultyLevelGradients:
    def __init__(self):
        self.gradients = {
            1: [
                (0, QColor(245, 245, 245)),
            ],
            2: [
                (0, QColor(170, 170, 170)),
                (0.15, QColor(230, 230, 230)),
                (0.3, QColor(180, 180, 180)),
                (0.4, QColor(220, 220, 220)),
                (0.55, QColor(190, 190, 190)),
                (0.75, QColor(130, 130, 130)),
                (1, QColor(110, 110, 110)),
            ],
            3: [
                (0, QColor(255, 235, 153)),
                (0.2, QColor(255, 223, 77)),
                (0.4, QColor(255, 215, 0)),
                (0.5, QColor(255, 223, 77)),
                (0.6, QColor(238, 201, 0)),
                (0.8, QColor(204, 164, 0)),
                (1, QColor(153, 101, 21)),
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
        }

    def get_gradient(self, rect: QRect, difficulty_level: int) -> QLinearGradient:
        gradient = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.bottomRight()))

        if difficulty_level in self.gradients:
            for pos, color in self.gradients[difficulty_level]:
                gradient.setColorAt(pos, color)
        else:
            gradient.setColorAt(0, Qt.GlobalColor.white)
            gradient.setColorAt(1, Qt.GlobalColor.white)

        return gradient
