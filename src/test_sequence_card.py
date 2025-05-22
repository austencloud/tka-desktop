import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the sequence card tab
from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sequence Card Tab Test")
        self.resize(1200, 800)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout
        layout = QVBoxLayout(central_widget)

        # Create a mock main widget that inherits from QWidget
        class MockMainWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)

                # Create settings manager
                from settings_manager.settings_manager import SettingsManager

                self.settings_manager = SettingsManager()

                # Create other required components
                from main_window.main_widget.json_manager.json_manager import (
                    JsonManager,
                )

                self.json_manager = JsonManager()

                # Create a mock fade manager
                class MockFadeManager:
                    def __init__(self):
                        self.stack_fader = self
                        self.parallel_stack_fader = self

                    def fade_stack(self, stack, index):
                        pass

                    def fade_both_stacks(
                        self,
                        right_stack,
                        right_index,
                        left_stack,
                        left_index,
                        width_ratio,
                    ):
                        pass

                self.fade_manager = MockFadeManager()

                # Create mock stacks
                from PyQt6.QtWidgets import QStackedWidget

                self.left_stack = QStackedWidget()
                self.right_stack = QStackedWidget()

                # Create a mock pictograph dataset
                self.pictograph_dataset = {}

                # Create a mock size provider
                self.size = lambda: (1200, 800)

        # Create a mock main widget
        mock_main_widget = MockMainWidget(self)

        # Create the sequence card tab
        self.sequence_card_tab = SequenceCardTab(mock_main_widget)

        # Add the sequence card tab to the layout
        layout.addWidget(self.sequence_card_tab)

        # Show the window
        self.show()


def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
