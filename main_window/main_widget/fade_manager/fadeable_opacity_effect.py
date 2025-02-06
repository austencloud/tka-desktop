from PyQt6.QtWidgets import QGraphicsOpacityEffect


class FadableOpacityEffect(QGraphicsOpacityEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.in_animation = False
