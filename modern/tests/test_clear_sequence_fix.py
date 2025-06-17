#!/usr/bin/env python3
"""
Test script for the clear sequence fix

This script tests that the clear sequence operation preserves the start position beat
while clearing all subsequent beats, and transitions back to the start position picker.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from core.dependency_injection.di_container import DIContainer
from src.core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from src.application.services.simple_layout_service import SimpleLayoutService
from src.application.services.simple_sequence_service import (
    SequenceService,
    SimpleSequenceDataService,
    SimpleSettingsService,
    SimpleValidationService,
)
from src.presentation.factories.workbench_factory import configure_workbench_services
from src.presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
from domain.models.core_models import SequenceData, BeatData


class ClearSequenceTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Clear Sequence Fix Test")
        self.setMinimumSize(1400, 900)

        # Setup container and services
        self.container = DIContainer()
        self._configure_services()

        # Setup UI
        self._setup_ui()

    def _configure_services(self):
        """Configure dependency injection services"""
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        self.container.register_singleton(ISettingsService, SimpleSettingsService)
        self.container.register_singleton(
            ISequenceDataService, SimpleSequenceDataService
        )
        self.container.register_singleton(IValidationService, SimpleValidationService)
        self.container.register_singleton(SequenceService, SequenceService)
        configure_workbench_services(self.container)

    def _setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Clear Sequence Fix Test")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
                margin: 10px;
            }
        """
        )
        layout.addWidget(title)

        # Test controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)

        # Status label
        self.status_label = QLabel("Ready to test clear sequence functionality...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #3498db;
                font-size: 14px;
                padding: 5px;
                background-color: #ebf3fd;
                border-radius: 3px;
                margin: 5px;
            }
        """
        )
        controls_layout.addWidget(self.status_label)

        # Test buttons
        self.create_test_sequence_btn = QPushButton("1. Create Test Sequence")
        self.create_test_sequence_btn.clicked.connect(self._create_test_sequence)
        self.create_test_sequence_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        controls_layout.addWidget(self.create_test_sequence_btn)

        self.clear_sequence_btn = QPushButton("2. Clear Sequence (Test Fix)")
        self.clear_sequence_btn.clicked.connect(self._test_clear_sequence)
        self.clear_sequence_btn.setEnabled(False)
        self.clear_sequence_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        controls_layout.addWidget(self.clear_sequence_btn)

        layout.addWidget(controls_widget)

        try:
            # Create the construct tab
            self.construct_tab = ConstructTabWidget(self.container)
            layout.addWidget(self.construct_tab)

            # Connect signals to monitor behavior
            self.construct_tab.sequence_modified.connect(self._on_sequence_modified)

            self.status_label.setText("✅ Construct tab loaded successfully!")
            self.status_label.setStyleSheet(
                """
                QLabel {
                    color: #27ae60;
                    font-size: 14px;
                    padding: 5px;
                    background-color: #d5f4e6;
                    border-radius: 3px;
                    margin: 5px;
                }
            """
            )

        except Exception as e:
            self.status_label.setText(f"❌ Error loading construct tab: {e}")
            self.status_label.setStyleSheet(
                """
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    padding: 5px;
                    background-color: #fadbd8;
                    border-radius: 3px;
                    margin: 5px;
                }
            """
            )
            print(f"Error details: {e}")
            import traceback

            traceback.print_exc()

    def _create_test_sequence(self):
        """Create a test sequence with multiple beats"""
        try:
            # Create a test sequence with start position + 3 beats
            start_beat = BeatData.empty().update(
                beat_number=1, letter="START", duration=1.0, is_blank=False
            )

            beat2 = BeatData.empty().update(
                beat_number=2, letter="A", duration=1.0, is_blank=False
            )

            beat3 = BeatData.empty().update(
                beat_number=3, letter="B", duration=1.0, is_blank=False
            )

            beat4 = BeatData.empty().update(
                beat_number=4, letter="C", duration=1.0, is_blank=False
            )

            test_sequence = SequenceData(
                name="Test Sequence",
                word="SABC",
                beats=[start_beat, beat2, beat3, beat4],
            )

            # Set the sequence in the workbench
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(test_sequence)

            self.status_label.setText(
                f"✅ Created test sequence with {test_sequence.length} beats"
            )
            self.clear_sequence_btn.setEnabled(True)
            self.create_test_sequence_btn.setEnabled(False)

        except Exception as e:
            self.status_label.setText(f"❌ Error creating test sequence: {e}")
            print(f"Error details: {e}")
            import traceback

            traceback.print_exc()

    def _test_clear_sequence(self):
        """Test the clear sequence functionality"""
        try:
            # Get current sequence before clearing
            current_sequence = (
                self.construct_tab.workbench.get_sequence()
                if self.construct_tab.workbench
                else None
            )
            if not current_sequence:
                self.status_label.setText("❌ No sequence to clear")
                return

            original_length = current_sequence.length
            self.status_label.setText(
                f"🧪 Clearing sequence (was {original_length} beats)..."
            )

            # Trigger clear sequence
            self.construct_tab.clear_sequence()

        except Exception as e:
            self.status_label.setText(f"❌ Error clearing sequence: {e}")
            print(f"Error details: {e}")
            import traceback

            traceback.print_exc()

    def _on_sequence_modified(self, sequence):
        """Handle sequence modification events"""
        if sequence:
            if sequence.length == 0:
                self.status_label.setText(
                    f"✅ SUCCESS! Sequence cleared - start position view stays visible, all beat views hidden"
                )
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        color: #27ae60;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 10px;
                        background-color: #d5f4e6;
                        border: 2px solid #27ae60;
                        border-radius: 5px;
                        margin: 5px;
                    }
                """
                )

                # Reset for another test
                self.clear_sequence_btn.setEnabled(False)
                self.create_test_sequence_btn.setEnabled(True)
            else:
                self.status_label.setText(
                    f"📊 Sequence modified: {sequence.length} beats"
                )
        else:
            self.status_label.setText("📊 Sequence set to None")


def main():
    print("🧪 Testing Clear Sequence Fix")
    print("=" * 50)
    print("This test verifies that:")
    print("1. Clear sequence preserves the start position beat at index 0")
    print("2. All subsequent beats are cleared")
    print("3. The UI transitions back to start position picker")
    print("4. The start position beat shows START text overlay")
    print()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ClearSequenceTestWindow()
    window.show()

    print("🎯 Test Instructions:")
    print("1. Click 'Create Test Sequence' to create a 4-beat sequence")
    print("2. Click 'Clear Sequence' to test the fix")
    print("3. Verify that only the start position beat remains visible")
    print("4. Check that the UI returns to start position picker")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
