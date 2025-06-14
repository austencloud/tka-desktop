from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

class MainWidgetDimmer(QWidget):
    def __init__(self, main_widget: QWidget):
        super().__init__(main_widget)
        self.main_widget = main_widget
        # Set up the dimming overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )  # Allow interaction with other widgets
        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5);"
        )  # Semi-transparent dark overlay
        self.setGeometry(main_widget.window().rect())  # Cover the entire main window

    def show(self):
        """Show the dimmer and ensure it covers the main window."""
        self.setGeometry(self.main_widget.window().rect())  # Cover the main window
        super().show()

    def resizeEvent(self, event):
        """Ensure the dimmer resizes with the main window."""
        self.setGeometry(self.main_widget.window().rect())
        super().resizeEvent(event)
