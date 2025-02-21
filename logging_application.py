

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication

class LoggingApplication(QApplication):
    def notify(self, receiver, event):

        return super().notify(receiver, event)
