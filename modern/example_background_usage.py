# Example usage of the modern background system

from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.presentation.components.backgrounds.background_widget import BackgroundWidget


class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Background System Demo")
        self.setGeometry(100, 100, 800, 600)

        # Create background widget
        self.background_widget = BackgroundWidget("Aurora", self)
        self.background_widget.setGeometry(self.rect())

        # Example of switching backgrounds
        self.show_background_types()

    def show_background_types(self):
        from src.presentation.components.backgrounds.background_factory import (
            BackgroundFactory,
        )

        print("Available backgrounds:", BackgroundFactory.get_available_backgrounds())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background_widget"):
            self.background_widget.setGeometry(self.rect())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())
