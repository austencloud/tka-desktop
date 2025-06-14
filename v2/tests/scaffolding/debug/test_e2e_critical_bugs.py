#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: End-to-end critical bug reproduction with complete user workflow simulation
DELETE_AFTER: 2025-07-15
CREATED: 2025-06-14
AUTHOR: @austencloud
RELATED_ISSUE: Critical bugs - sequence clear crash and option selection workflow
"""

import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtTest import QTest

# Add v2/src to path
v2_src_path = Path(__file__).parent / "src"
if str(v2_src_path) not in sys.path:
    sys.path.insert(0, str(v2_src_path))

try:
    from src.core.dependency_injection.simple_container import SimpleContainer
    from src.core.interfaces.core_services import ILayoutService
    from src.application.services.simple_layout_service import SimpleLayoutService
    from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
    from src.domain.models.core_models import SequenceData, BeatData
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying alternative import paths...")
    try:
        import sys

        sys.path.insert(0, str(Path(__file__).parent))
        from src.core.dependency_injection.simple_container import SimpleContainer
        from src.core.interfaces.core_services import ILayoutService
        from src.application.services.simple_layout_service import SimpleLayoutService
        from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
        from src.domain.models.core_models import SequenceData, BeatData
    except ImportError as e2:
        print(f"❌ Alternative import also failed: {e2}")
        sys.exit(1)


class CriticalBugTestWindow(QMainWindow):
    """Test window for reproducing critical bugs in V2."""

    test_completed = pyqtSignal(str, bool, str)  # test_name, success, message

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐛 V2 Critical Bug E2E Tests")
        self.setGeometry(100, 100, 1400, 900)

        # Test results
        self.test_results = {}
        self.current_test = None

        # Create container and services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)

        self.setup_ui()

        # Schedule tests to run after UI is ready
        QTimer.singleShot(1000, self.run_all_tests)

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Test control buttons
        self.test_clear_btn = QPushButton("🗑️ Test Clear Sequence Bug")
        self.test_clear_btn.clicked.connect(self.test_clear_sequence_bug)
        layout.addWidget(self.test_clear_btn)

        self.test_option_btn = QPushButton("🎯 Test Option Selection Bug")
        self.test_option_btn.clicked.connect(self.test_option_selection_bug)
        layout.addWidget(self.test_option_btn)

        self.run_all_btn = QPushButton("🚀 Run All Tests")
        self.run_all_btn.clicked.connect(self.run_all_tests)
        layout.addWidget(self.run_all_btn)

        # Create the construct tab widget for testing
        try:
            self.construct_tab = ConstructTabWidget(self.container, parent=self)
            layout.addWidget(self.construct_tab)
            print("✅ Construct tab created successfully")
        except Exception as e:
            print(f"❌ Failed to create construct tab: {e}")
            traceback.print_exc()
            self.construct_tab = None

        # Connect to test completion signal
        self.test_completed.connect(self.on_test_completed)

    def run_all_tests(self):
        """Run all critical bug tests in sequence."""
        print("\n🚀 STARTING CRITICAL BUG E2E TESTS")
        print("=" * 60)

        # Reset test results
        self.test_results = {}

        # Run tests in sequence with delays
        QTimer.singleShot(500, self.test_clear_sequence_bug)
        QTimer.singleShot(2000, self.test_option_selection_bug)
        QTimer.singleShot(4000, self.generate_test_report)

    def test_clear_sequence_bug(self):
        """Test Bug #1: Program crashes when clearing sequence."""
        self.current_test = "clear_sequence_crash"
        print("\n🐛 TEST 1: Clear Sequence Crash Bug")
        print("-" * 40)

        if not self.construct_tab:
            self.test_completed.emit(
                "clear_sequence_crash", False, "Construct tab not available"
            )
            return

        try:
            # Step 1: Select a start position
            print("   Step 1: Selecting start position...")
            self.construct_tab._handle_start_position_selected("alpha1_alpha1")
            print("   ✅ Start position selected")

            # Step 2: Get workbench reference
            workbench = self.construct_tab.workbench
            if not workbench:
                self.test_completed.emit(
                    "clear_sequence_crash", False, "Workbench not available"
                )
                return

            # Step 3: Check initial state
            initial_sequence = workbench.get_sequence()
            initial_start_pos = workbench.get_start_position()
            print(
                f"   Initial sequence: {initial_sequence.length if initial_sequence else 0} beats"
            )
            print(
                f"   Initial start pos: {initial_start_pos.letter if initial_start_pos else 'None'}"
            )

            # Step 4: Try to clear sequence (this should NOT crash)
            print("   Step 2: Attempting to clear sequence...")

            # Test both clear methods
            try:
                # Method 1: Direct workbench clear
                workbench._handle_clear()
                print("   ✅ Workbench clear method succeeded")

                # Method 2: Construct tab clear
                self.construct_tab.clear_sequence()
                print("   ✅ Construct tab clear method succeeded")

                # Step 5: Verify state after clear
                final_sequence = workbench.get_sequence()
                final_start_pos = workbench.get_start_position()

                print(
                    f"   Final sequence: {final_sequence.length if final_sequence else 0} beats"
                )
                print(
                    f"   Final start pos: {final_start_pos.letter if final_start_pos else 'None'}"
                )

                # Verify expected behavior
                if final_sequence and final_sequence.length == 0:
                    print("   ✅ Sequence properly cleared")
                    success = True
                    message = "Clear sequence works correctly"
                else:
                    print("   ❌ Sequence not properly cleared")
                    success = False
                    message = f"Sequence still has {final_sequence.length if final_sequence else 'unknown'} beats"

            except Exception as clear_error:
                print(f"   ❌ Clear sequence failed: {clear_error}")
                traceback.print_exc()
                success = False
                message = f"Clear sequence crashed: {clear_error}"

            self.test_completed.emit("clear_sequence_crash", success, message)

        except Exception as e:
            print(f"   ❌ Test setup failed: {e}")
            traceback.print_exc()
            self.test_completed.emit(
                "clear_sequence_crash", False, f"Test setup failed: {e}"
            )

    def test_option_selection_bug(self):
        """Test Bug #2: Option selection doesn't work after start position selection."""
        self.current_test = "option_selection_broken"
        print("\n🐛 TEST 2: Option Selection After Start Position Bug")
        print("-" * 40)

        if not self.construct_tab:
            self.test_completed.emit(
                "option_selection_broken", False, "Construct tab not available"
            )
            return

        try:
            # Step 1: Clear any existing state
            print("   Step 1: Clearing existing state...")
            if self.construct_tab.workbench:
                try:
                    self.construct_tab.workbench._handle_clear()
                except:
                    pass  # Ignore errors during cleanup

            # Step 2: Select start position
            print("   Step 2: Selecting start position...")
            self.construct_tab._handle_start_position_selected("alpha1_alpha1")

            # Step 3: Verify start position was set
            workbench = self.construct_tab.workbench
            if not workbench:
                self.test_completed.emit(
                    "option_selection_broken", False, "Workbench not available"
                )
                return

            start_pos = workbench.get_start_position()
            print(f"   Start position set: {start_pos.letter if start_pos else 'None'}")

            # Step 4: Check if option picker is populated
            option_picker = self.construct_tab.option_picker
            if not option_picker:
                self.test_completed.emit(
                    "option_selection_broken", False, "Option picker not available"
                )
                return

            print("   Step 3: Checking option picker state...")

            # Step 5: Try to get available options
            try:
                # Check if option picker has beat options
                if hasattr(option_picker, "_beat_loader"):
                    beat_options = option_picker._beat_loader.get_beat_options()
                    print(
                        f"   Available beat options: {len(beat_options) if beat_options else 0}"
                    )

                    if beat_options and len(beat_options) > 0:
                        print("   ✅ Option picker has beat options")

                        # Step 6: Try to select an option
                        print("   Step 4: Attempting to select first option...")

                        # Simulate option selection
                        test_option_id = "test_option_1"
                        initial_sequence = workbench.get_sequence()
                        initial_length = (
                            initial_sequence.length if initial_sequence else 0
                        )

                        # Call option selection handler
                        self.construct_tab._handle_option_selected(test_option_id)

                        # Check if sequence was updated
                        final_sequence = workbench.get_sequence()
                        final_length = final_sequence.length if final_sequence else 0

                        print(f"   Sequence length before: {initial_length}")
                        print(f"   Sequence length after: {final_length}")

                        if final_length > initial_length:
                            print("   ✅ Option selection added beat to sequence")
                            success = True
                            message = "Option selection works correctly"
                        else:
                            print("   ❌ Option selection did not add beat to sequence")
                            success = False
                            message = "Option selection does not update sequence"
                    else:
                        print("   ❌ Option picker has no beat options")
                        success = False
                        message = (
                            "Option picker not populated after start position selection"
                        )
                else:
                    print("   ❌ Option picker missing beat loader")
                    success = False
                    message = "Option picker not properly initialized"

            except Exception as option_error:
                print(f"   ❌ Option selection test failed: {option_error}")
                traceback.print_exc()
                success = False
                message = f"Option selection error: {option_error}"

            self.test_completed.emit("option_selection_broken", success, message)

        except Exception as e:
            print(f"   ❌ Test setup failed: {e}")
            traceback.print_exc()
            self.test_completed.emit(
                "option_selection_broken", False, f"Test setup failed: {e}"
            )

    def on_test_completed(self, test_name: str, success: bool, message: str):
        """Handle test completion."""
        self.test_results[test_name] = {"success": success, "message": message}

        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status}: {test_name}")
        print(f"   Result: {message}")

    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n📊 CRITICAL BUG TEST REPORT")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(
            1 for result in self.test_results.values() if result["success"]
        )
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print()

        # Detailed results
        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            print(f"{status}: {test_name}")
            print(f"   {result['message']}")
            print()

        # Recommendations
        if failed_tests > 0:
            print("🔧 RECOMMENDED FIXES:")
            print("-" * 30)

            if not self.test_results.get("clear_sequence_crash", {}).get(
                "success", True
            ):
                print("1. Clear Sequence Bug:")
                print("   - Check SequenceData.empty() implementation")
                print("   - Verify beat frame update logic")
                print("   - Add proper error handling in clear methods")
                print()

            if not self.test_results.get("option_selection_broken", {}).get(
                "success", True
            ):
                print("2. Option Selection Bug:")
                print("   - Verify option picker population after start position")
                print("   - Check beat data loader initialization")
                print("   - Ensure proper signal connections")
                print("   - Verify sequence update logic in option selection")
                print()
        else:
            print("🎉 ALL TESTS PASSED!")
            print("   No critical bugs detected in current implementation.")


def main():
    """Main test function."""
    print("🐛 Starting V2 Critical Bug E2E Tests...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    test_window = CriticalBugTestWindow()
    test_window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
