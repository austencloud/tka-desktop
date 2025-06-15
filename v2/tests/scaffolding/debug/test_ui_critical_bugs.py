#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: UI-focused critical bug reproduction and testing
DELETE_AFTER: 2025-07-15
CREATED: 2025-06-14
AUTHOR: @austencloud
RELATED_ISSUE: UI component critical bugs testing
"""

"""
UI Critical Bug Tests for TKA V2
================================

Tests that actually run the UI to reproduce the critical bugs:
1. Program crashes when clearing sequence
2. Option selection doesn't work after start position selection
"""

import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QTimer, pyqtSignal

# Add v2 to path
v2_path = Path(__file__).parent
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))

try:
    from core.dependency_injection.di_container import SimpleContainer
    from src.core.interfaces.core_services import ILayoutService
    from src.application.services.simple_layout_service import SimpleLayoutService
    from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
    from src.domain.models.core_models import SequenceData, BeatData
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure you're running from the v2 directory")
    sys.exit(1)


class UIBugTestWindow(QMainWindow):
    """Test window for reproducing UI bugs in V2."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐛 V2 UI Critical Bug Tests")
        self.setGeometry(100, 100, 1400, 900)

        # Test state
        self.test_results = []
        self.current_test_step = 0

        self.setup_ui()

        # Schedule test sequence
        QTimer.singleShot(2000, self.start_test_sequence)

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Status label
        self.status_label = QLabel("🔄 Initializing test environment...")
        layout.addWidget(self.status_label)

        # Test control buttons
        self.test_clear_btn = QPushButton("🗑️ Test Clear Sequence")
        self.test_clear_btn.clicked.connect(self.test_clear_sequence)
        layout.addWidget(self.test_clear_btn)

        self.test_option_btn = QPushButton("🎯 Test Option Selection")
        self.test_option_btn.clicked.connect(self.test_option_selection)
        layout.addWidget(self.test_option_btn)

        self.run_sequence_btn = QPushButton("🚀 Run Full Test Sequence")
        self.run_sequence_btn.clicked.connect(self.start_test_sequence)
        layout.addWidget(self.run_sequence_btn)

        # Results area
        self.results_label = QLabel("📊 Test results will appear here...")
        layout.addWidget(self.results_label)

        # Create the construct tab widget for testing
        try:
            container = SimpleContainer()
            container.register_singleton(ILayoutService, SimpleLayoutService)

            self.construct_tab = ConstructTabWidget(container, parent=self)
            layout.addWidget(self.construct_tab)

            self.status_label.setText("✅ Construct tab created successfully")
            print("✅ Construct tab created successfully")

        except Exception as e:
            self.status_label.setText(f"❌ Failed to create construct tab: {e}")
            print(f"❌ Failed to create construct tab: {e}")
            traceback.print_exc()
            self.construct_tab = None

    def start_test_sequence(self):
        """Start the automated test sequence."""
        self.status_label.setText("🚀 Starting automated test sequence...")
        self.test_results = []
        self.current_test_step = 0

        # Test sequence with delays
        QTimer.singleShot(500, self.test_step_1_select_start_position)

    def test_step_1_select_start_position(self):
        """Test Step 1: Select start position."""
        self.status_label.setText("🎯 Step 1: Selecting start position...")

        if not self.construct_tab:
            self.add_test_result("❌ Step 1 Failed: No construct tab available")
            return

        try:
            # Select start position
            self.construct_tab._handle_start_position_selected("alpha1_alpha1")
            self.add_test_result("✅ Step 1: Start position selected successfully")

            # Check if workbench has start position
            if self.construct_tab.workbench:
                start_pos = self.construct_tab.workbench.get_start_position()
                if start_pos:
                    self.add_test_result(f"✅ Start position set: {start_pos.letter}")
                else:
                    self.add_test_result("⚠️ Start position not found in workbench")

            # Continue to next step
            QTimer.singleShot(1000, self.test_step_2_option_selection)

        except Exception as e:
            self.add_test_result(f"❌ Step 1 Failed: {e}")
            traceback.print_exc()

    def test_step_2_option_selection(self):
        """Test Step 2: Try option selection."""
        self.status_label.setText("🎯 Step 2: Testing option selection...")

        try:
            # Get initial sequence state
            workbench = self.construct_tab.workbench
            if not workbench:
                self.add_test_result("❌ Step 2 Failed: No workbench available")
                return

            initial_sequence = workbench.get_sequence()
            initial_length = initial_sequence.length if initial_sequence else 0

            self.add_test_result(f"📊 Initial sequence length: {initial_length}")

            # Try to select an option
            self.construct_tab._handle_option_selected("test_option_beta5")

            # Check if sequence was updated
            final_sequence = workbench.get_sequence()
            final_length = final_sequence.length if final_sequence else 0

            self.add_test_result(f"📊 Final sequence length: {final_length}")

            if final_length > initial_length:
                self.add_test_result(
                    "✅ Step 2: Option selection added beat to sequence"
                )
            else:
                self.add_test_result("❌ Step 2: Option selection did not add beat")

            # Continue to next step
            QTimer.singleShot(1000, self.test_step_3_clear_sequence)

        except Exception as e:
            self.add_test_result(f"❌ Step 2 Failed: {e}")
            traceback.print_exc()

    def test_step_3_clear_sequence(self):
        """Test Step 3: Clear sequence (this might crash)."""
        self.status_label.setText("🎯 Step 3: Testing clear sequence...")

        try:
            workbench = self.construct_tab.workbench
            if not workbench:
                self.add_test_result("❌ Step 3 Failed: No workbench available")
                return

            # Get sequence before clear
            before_sequence = workbench.get_sequence()
            before_length = before_sequence.length if before_sequence else 0

            self.add_test_result(f"📊 Sequence length before clear: {before_length}")

            # Try to clear sequence (this is where crashes might happen)
            workbench._handle_clear()

            # Check sequence after clear
            after_sequence = workbench.get_sequence()
            after_length = after_sequence.length if after_sequence else 0

            self.add_test_result(f"📊 Sequence length after clear: {after_length}")

            if after_length == 0:
                self.add_test_result("✅ Step 3: Clear sequence worked correctly")
            else:
                self.add_test_result(
                    "❌ Step 3: Clear sequence did not clear all beats"
                )

            # Also test construct tab clear
            self.construct_tab.clear_sequence()
            self.add_test_result("✅ Step 3: Construct tab clear also worked")

            # Finish test sequence
            QTimer.singleShot(1000, self.finish_test_sequence)

        except Exception as e:
            self.add_test_result(f"❌ Step 3 CRASHED: {e}")
            traceback.print_exc()
            QTimer.singleShot(1000, self.finish_test_sequence)

    def test_clear_sequence(self):
        """Manual test for clear sequence."""
        self.status_label.setText("🗑️ Testing clear sequence manually...")

        if not self.construct_tab or not self.construct_tab.workbench:
            self.add_test_result("❌ Manual Clear Test: No workbench available")
            return

        try:
            workbench = self.construct_tab.workbench

            # Get current state
            current_sequence = workbench.get_sequence()
            current_length = current_sequence.length if current_sequence else 0

            self.add_test_result(f"📊 Current sequence length: {current_length}")

            # Clear sequence
            workbench._handle_clear()

            # Check result
            cleared_sequence = workbench.get_sequence()
            cleared_length = cleared_sequence.length if cleared_sequence else 0

            if cleared_length == 0:
                self.add_test_result("✅ Manual Clear: Sequence cleared successfully")
            else:
                self.add_test_result(
                    f"❌ Manual Clear: Still has {cleared_length} beats"
                )

        except Exception as e:
            self.add_test_result(f"❌ Manual Clear CRASHED: {e}")
            traceback.print_exc()

    def test_option_selection(self):
        """Manual test for option selection."""
        self.status_label.setText("🎯 Testing option selection manually...")

        if not self.construct_tab:
            self.add_test_result("❌ Manual Option Test: No construct tab available")
            return

        try:
            # First ensure we have a start position
            self.construct_tab._handle_start_position_selected("alpha1_alpha1")
            self.add_test_result("✅ Manual Option: Start position set")

            # Get initial sequence
            workbench = self.construct_tab.workbench
            if workbench:
                initial_sequence = workbench.get_sequence()
                initial_length = initial_sequence.length if initial_sequence else 0

                # Try option selection
                self.construct_tab._handle_option_selected("manual_test_option")

                # Check result
                final_sequence = workbench.get_sequence()
                final_length = final_sequence.length if final_sequence else 0

                if final_length > initial_length:
                    self.add_test_result("✅ Manual Option: Beat added to sequence")
                else:
                    self.add_test_result("❌ Manual Option: No beat added")
            else:
                self.add_test_result("❌ Manual Option: No workbench available")

        except Exception as e:
            self.add_test_result(f"❌ Manual Option FAILED: {e}")
            traceback.print_exc()

    def add_test_result(self, message: str):
        """Add a test result message."""
        self.test_results.append(message)
        print(message)

        # Update results display
        results_text = "\n".join(self.test_results[-10:])  # Show last 10 results
        self.results_label.setText(results_text)

    def finish_test_sequence(self):
        """Finish the test sequence and show summary."""
        self.status_label.setText("📊 Test sequence completed!")

        # Count results
        total_tests = len([r for r in self.test_results if "Step" in r])
        passed_tests = len([r for r in self.test_results if "✅" in r and "Step" in r])
        failed_tests = len([r for r in self.test_results if "❌" in r and "Step" in r])

        summary = f"\n📊 SUMMARY: {passed_tests}/{total_tests} tests passed"
        if failed_tests > 0:
            summary += f"\n🚨 {failed_tests} tests failed - bugs detected!"
        else:
            summary += "\n🎉 All tests passed - no bugs detected!"

        self.add_test_result(summary)


def main():
    """Main test function."""
    print("🐛 Starting V2 UI Critical Bug Tests...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    test_window = UIBugTestWindow()
    test_window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
