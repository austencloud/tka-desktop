#!/usr/bin/env python3
"""
Option Picker Reactivity Test

Tests the automatic option picker switching behavior after enhancing signal flow
to prevent cascade refreshes.
"""

import sys
from pathlib import Path

# Add the source path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QTimer

from core.dependency_injection.di_container import DIContainer
from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget


class OptionPickerReactivityTest(QMainWindow):
    """Test automatic option picker reactivity with enhanced signal flow"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Option Picker Reactivity Test - Enhanced Signal Flow")
        self.setGeometry(100, 100, 1400, 800)

        # Create container
        self.container = DIContainer()

        # Setup UI
        self._setup_ui()

        # Setup timer for state monitoring
        self._setup_monitoring()

    def _setup_ui(self):
        """Setup test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Status label
        self.status_label = QLabel(
            "Testing Option Picker Reactivity - Enhanced Signal Flow"
        )
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        layout.addWidget(self.status_label)

        # Test buttons
        button_layout = QVBoxLayout()

        self.clear_button = QPushButton("Clear Sequence (Should → Start Pos Picker)")
        self.clear_button.clicked.connect(self._test_clear_sequence)
        button_layout.addWidget(self.clear_button)

        self.force_update_button = QPushButton("Force Picker Update")
        self.force_update_button.clicked.connect(self._test_force_update)
        button_layout.addWidget(self.force_update_button)

        layout.addLayout(button_layout)

        # Create construct tab widget
        try:
            self.construct_tab = ConstructTabWidget(self.container)
            layout.addWidget(self.construct_tab)
            self.status_label.setText("✅ Construct tab loaded! Test reactivity:")
            self.status_label.setStyleSheet("font-weight: bold; color: green;")
        except Exception as e:
            self.status_label.setText(f"❌ Error loading construct tab: {e}")
            self.status_label.setStyleSheet("font-weight: bold; color: red;")
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()

    def _setup_monitoring(self):
        """Setup monitoring for picker state changes"""
        self.refresh_count = 0
        self.last_refresh_time = 0

        # Monitor for excessive refreshes
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._check_refresh_rate)
        self.monitor_timer.start(1000)  # Check every second

    def _test_clear_sequence(self):
        """Test sequence clearing reactivity"""
        print("\n🧪 TESTING: Clear sequence reactivity")
        self.refresh_count = 0

        if hasattr(self.construct_tab, "clear_sequence"):
            self.construct_tab.clear_sequence()
            print("📋 Clear sequence triggered")

            # Check picker state after a short delay
            QTimer.singleShot(500, self._check_picker_state_after_clear)
        else:
            print("❌ Clear sequence method not available")

    def _test_force_update(self):
        """Test force picker update"""
        print("\n🧪 TESTING: Force picker update")
        self.refresh_count = 0

        if hasattr(self.construct_tab, "force_picker_update"):
            self.construct_tab.force_picker_update()
            print("📋 Force update triggered")
        else:
            print("❌ Force update method not available")

    def _check_picker_state_after_clear(self):
        """Check if picker switched to start position after clearing"""
        try:
            if hasattr(self.construct_tab, "layout_manager") and hasattr(
                self.construct_tab.layout_manager, "picker_stack"
            ):

                current_index = (
                    self.construct_tab.layout_manager.picker_stack.currentIndex()
                )

                if current_index == 0:
                    print(
                        "✅ SUCCESS: Picker correctly switched to start position picker (index 0)"
                    )
                    self.status_label.setText(
                        "✅ Clear test passed: Start position picker active"
                    )
                    self.status_label.setStyleSheet("font-weight: bold; color: green;")
                else:
                    print(
                        f"❌ FAILURE: Picker still on index {current_index} (should be 0)"
                    )
                    self.status_label.setText(
                        f"❌ Clear test failed: Picker index {current_index}"
                    )
                    self.status_label.setStyleSheet("font-weight: bold; color: red;")
            else:
                print("❌ Cannot access picker stack for testing")
        except Exception as e:
            print(f"❌ Error checking picker state: {e}")

    def _check_refresh_rate(self):
        """Monitor refresh rate to detect cascade issues"""
        if self.refresh_count > 3:
            print(
                f"⚠️ WARNING: Detected {self.refresh_count} refreshes in the last second (possible cascade)"
            )
            self.status_label.setText(
                f"⚠️ Warning: {self.refresh_count} refreshes detected"
            )
            self.status_label.setStyleSheet("font-weight: bold; color: orange;")

        self.refresh_count = 0


def main():
    print("🧪 Starting Option Picker Reactivity Test - Enhanced Signal Flow")
    print("=" * 60)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = OptionPickerReactivityTest()
    window.show()

    print("✅ Test window ready!")
    print("📋 Tests available:")
    print("   • Clear Sequence (should switch to start position picker)")
    print("   • Force Picker Update (manual state sync)")
    print("   • Monitor for cascade refreshes")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
