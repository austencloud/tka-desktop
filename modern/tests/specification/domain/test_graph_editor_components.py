import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt

from core.dependency_injection.di_container import DIContainer
from src.application.services.graph_editor_service import GraphEditorService
from presentation.components.workbench.graph_editor.graph_editor import (
    GraphEditor,
)
from src.domain.models.core_models import SequenceData, BeatData


class GraphEditorTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Editor Test")
        self.setGeometry(100, 100, 800, 600)

        # Setup service
        self.graph_service = GraphEditorService()

        # Setup UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Test buttons
        btn_layout = QVBoxLayout()

        toggle_btn = QPushButton("Toggle Graph Editor")
        toggle_btn.clicked.connect(self.toggle_graph_editor)
        btn_layout.addWidget(toggle_btn)

        load_beat_btn = QPushButton("Load Test Beat")
        load_beat_btn.clicked.connect(self.load_test_beat)
        btn_layout.addWidget(load_beat_btn)

        test_arrow_btn = QPushButton("Test Arrow Selection")
        test_arrow_btn.clicked.connect(self.test_arrow_selection)
        btn_layout.addWidget(test_arrow_btn)

        layout.addLayout(btn_layout)

        # Create graph editor
        self.graph_editor = GraphEditor(
            graph_service=self.graph_service, parent=central_widget
        )

        # Connect signals for testing
        self.graph_editor.visibility_changed.connect(self.on_visibility_changed)
        self.graph_editor.arrow_selected.connect(self.on_arrow_selected)
        self.graph_editor.beat_modified.connect(self.on_beat_modified)

        layout.addWidget(self.graph_editor)
        layout.addStretch()

        # Set dark theme
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #666;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """
        )

    def toggle_graph_editor(self):
        print("Toggling graph editor visibility...")
        self.graph_editor.toggle_visibility()

    def load_test_beat(self):
        print("Loading test beat...")
        # Create mock beat data
        test_beat = BeatData(
            beat=1,
            sequence_start_position="beta",
            blue_motion_type="pro",
            red_motion_type="anti",
        )

        self.graph_editor.set_selected_beat(test_beat, 1)

    def test_arrow_selection(self):
        print("Testing arrow selection...")
        # Simulate arrow selection
        if self.graph_editor._pictograph_container:
            self.graph_editor._pictograph_container._on_arrow_clicked("test_arrow_1")

    def on_visibility_changed(self, visible: bool):
        print(f"Graph editor visibility changed: {visible}")

    def on_arrow_selected(self, arrow_id: str):
        print(f"Arrow selected: {arrow_id}")

    def on_beat_modified(self, beat_data: BeatData):
        print(f"Beat modified: {beat_data}")


def main():
    app = QApplication(sys.argv)

    window = GraphEditorTestWindow()
    window.show()

    print("Graph Editor Test Started")
    print("Use buttons to test functionality:")
    print("- Toggle Graph Editor: Show/hide the editor")
    print("- Load Test Beat: Load sample beat data")
    print("- Test Arrow Selection: Simulate arrow click")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
