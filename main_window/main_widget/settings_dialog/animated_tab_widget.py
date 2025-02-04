from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QTabWidget

class AnimatedTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentChanged.connect(self._animate_transition)

    def _animate_transition(self, index):
        current_widget = self.widget(index)
        if current_widget:
            animation = QPropertyAnimation(current_widget, b"windowOpacity")
            animation.setDuration(300)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.start()
