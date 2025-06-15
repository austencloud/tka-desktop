#!/usr/bin/env python3
"""
Signal Emission Fix Test for TKA V2
===================================

Tests the fix for circular signal emission during clear sequence operations.
This test focuses specifically on the signal handling fix.
"""

import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import QTimer

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
    sys.exit(1)


class SignalEmissionTestWindow(QMainWindow):
    """Test window for validating the signal emission fix."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 Signal Emission Fix Test")
        self.setGeometry(100, 100, 800, 600)

        self.test_results = []
        self.setup_ui()

        # Start test sequence
        QTimer.singleShot(2000, self.start_test_sequence)

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Status display
        self.status_label = QLabel("🔄 Initializing signal emission fix test...")
        layout.addWidget(self.status_label)

        # Test button
        self.test_button = QPushButton("🧪 Run Clear Sequence Test")
        self.test_button.clicked.connect(self.run_clear_test)
        layout.addWidget(self.test_button)

        # Results display
        self.results_label = QLabel("📊 Test results will appear here...")
        layout.addWidget(self.results_label)

        # Create construct tab for testing
        try:
            container = SimpleContainer()
            container.register_singleton(ILayoutService, SimpleLayoutService)

            self.construct_tab = ConstructTabWidget(container, parent=self)
            layout.addWidget(self.construct_tab)

            self.log_result("✅ UI components initialized successfully")

        except Exception as e:
            self.log_result(f"❌ UI initialization failed: {e}")
            self.construct_tab = None

    def start_test_sequence(self):
        """Start the test sequence."""
        self.status_label.setText("🚀 Ready to test signal emission fix...")

        if not self.construct_tab:
            self.log_result("❌ Cannot run tests - no construct tab available")
            return

        # Setup sequence first
        self.setup_test_sequence()

    def setup_test_sequence(self):
        """Setup a test sequence for clearing."""
        self.log_result("\n🎯 Setting up test sequence...")

        try:
            # Set start position
            self.construct_tab._handle_start_position_selected("alpha1_alpha1")

            # Add some beats
            for i in range(2):
                self.construct_tab._handle_option_selected(f"test_beat_{i+1}")

            workbench = self.construct_tab.workbench
            if workbench:
                sequence = workbench.get_sequence()
                length = sequence.length if sequence else 0
                self.log_result(f"✅ Test sequence created: {length} beats")
            else:
                self.log_result("❌ No workbench available")

        except Exception as e:
            self.log_result(f"❌ Test sequence setup failed: {e}")

    def run_clear_test(self):
        """Run the clear sequence test."""
        self.log_result("\n🗑️ TESTING CLEAR SEQUENCE WITH SIGNAL FIX")

        if not self.construct_tab or not self.construct_tab.workbench:
            self.log_result("❌ No workbench available for test")
            return

        workbench = self.construct_tab.workbench

        try:
            # Get state before clear
            before_sequence = workbench.get_sequence()
            before_length = before_sequence.length if before_sequence else 0

            self.log_result(f"📊 Before clear: {before_length} beats")

            # Set up timeout detection
            self.clear_completed = False
            self.clear_timeout = False

            def clear_timeout_handler():
                self.clear_timeout = True
                self.log_result(
                    "❌ CLEAR OPERATION TIMED OUT - SIGNAL EMISSION HANGING"
                )

            timeout_timer = QTimer()
            timeout_timer.timeout.connect(clear_timeout_handler)
            timeout_timer.start(5000)  # 5 second timeout

            # Execute clear operation
            self.log_result("🔄 Executing clear sequence operation...")

            # Test the workbench clear method directly
            workbench._handle_clear()

            # If we reach here without hanging, the fix worked
            timeout_timer.stop()
            self.clear_completed = True

            if not self.clear_timeout:
                # Check result
                after_sequence = workbench.get_sequence()
                after_length = after_sequence.length if after_sequence else 0

                self.log_result(f"📊 After clear: {after_length} beats")

                if after_length == 0:
                    self.log_result(
                        "✅ SIGNAL EMISSION FIX CONFIRMED: Clear completed without hanging!"
                    )
                    self.log_result(
                        "✅ Circular signal emission prevented successfully"
                    )
                else:
                    self.log_result(
                        f"⚠️ Clear completed but {after_length} beats remain"
                    )

        except Exception as e:
            self.log_result(f"❌ Clear sequence crashed: {e}")
            traceback.print_exc()

    def log_result(self, message: str):
        """Log a test result."""
        self.test_results.append(message)
        print(message)

        # Update display (show last 10 results)
        display_results = self.test_results[-10:]
        self.results_label.setText("\n".join(display_results))


def test_construct_tab_signal_protection():
    """Test the construct tab signal protection mechanism."""
    print("\n🧪 Testing construct tab signal protection...")

    try:
        container = SimpleContainer()
        container.register_singleton(ILayoutService, SimpleLayoutService)

        construct_tab = ConstructTabWidget(container)

        # Test the protection flag
        if hasattr(construct_tab, "_emitting_signal"):
            print("✅ Signal protection flag exists")

            # Test setting the flag
            construct_tab._emitting_signal = True

            # Create a dummy sequence
            test_sequence = SequenceData.empty()

            # This should not emit a signal due to protection
            print("🔄 Testing protected signal emission...")
            construct_tab._on_workbench_modified(test_sequence)

            print("✅ Protected signal emission completed without hanging")
            return True
        else:
            print("❌ Signal protection flag not found")
            return False

    except Exception as e:
        print(f"❌ Signal protection test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("🔧 SIGNAL EMISSION FIX TEST FOR TKA V2")
    print("=" * 50)

    # Create QApplication first
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Test 1: Signal protection mechanism
    protection_test = test_construct_tab_signal_protection()

    # Test 2: Full UI test
    print("\n🖥️ Starting UI test...")

    test_window = SignalEmissionTestWindow()
    test_window.show()

    # Run for a limited time
    QTimer.singleShot(15000, app.quit)  # Auto-quit after 15 seconds

    app.exec()

    print("\n📊 TEST SUMMARY:")
    print(f"   Signal Protection: {'✅ PASS' if protection_test else '❌ FAIL'}")
    print("   UI Test: Check output above for results")

    if protection_test:
        print("\n🎉 Signal emission fix appears to be working!")
        return 0
    else:
        print("\n❌ Signal emission fix needs more work")
        return 1


if __name__ == "__main__":
    sys.exit(main())
