"""
Start Position Selection Performance Test

Tests the real Modern application to measure delays when selecting a start position
for the first time and identifies performance bottlenecks.
"""

import time
import sys
from pathlib import Path
from typing import Dict, List, Optional
import threading
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QGuiApplication

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class StartPositionTestMonitor(QObject):
    """Monitors start position selection performance in real application."""

    test_completed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.start_time = None
        self.selection_time = None
        self.options_loaded_time = None
        self.test_results = {}

    def start_test(self, main_window):
        """Start monitoring the start position selection test."""
        self.main_window = main_window
        self.start_time = time.perf_counter()

        print("🧪 Starting start position selection test...")
        print("📍 Looking for construct tab and start position picker...")

        # Find the construct tab and start position picker
        self.find_and_test_start_position_picker()

    def find_and_test_start_position_picker(self):
        """Find the start position picker and test selection."""
        try:
            # Navigate to construct tab
            if hasattr(self.main_window, "tab_widget"):
                construct_tab = None
                for i in range(self.main_window.tab_widget.count()):
                    if "construct" in self.main_window.tab_widget.tabText(i).lower():
                        self.main_window.tab_widget.setCurrentIndex(i)
                        construct_tab = self.main_window.tab_widget.currentWidget()
                        break

                if construct_tab:
                    print("✅ Found construct tab")
                    self.test_start_position_selection(construct_tab)
                else:
                    print("❌ Could not find construct tab")
                    self.complete_test_with_error("Construct tab not found")
            else:
                print("❌ Main window has no tab_widget")
                self.complete_test_with_error("No tab widget found")

        except Exception as e:
            print(f"❌ Error finding construct tab: {e}")
            self.complete_test_with_error(str(e))

    def test_start_position_selection(self, construct_tab):
        """Test start position selection on the construct tab."""
        try:
            # Look for start position picker
            start_pos_picker = self.find_start_position_picker(construct_tab)

            if start_pos_picker:
                print("✅ Found start position picker")
                self.simulate_start_position_click(start_pos_picker)
            else:
                print("❌ Could not find start position picker")
                self.complete_test_with_error("Start position picker not found")

        except Exception as e:
            print(f"❌ Error testing start position selection: {e}")
            self.complete_test_with_error(str(e))

    def find_start_position_picker(self, construct_tab):
        """Find the start position picker widget."""
        # Look for start position picker in the construct tab
        for child in construct_tab.findChildren(QWidget):
            if hasattr(child, "objectName") and "start" in child.objectName().lower():
                return child
            if (
                hasattr(child, "__class__")
                and "StartPosition" in child.__class__.__name__
            ):
                return child

        # Alternative: look for layout manager
        if hasattr(construct_tab, "layout_manager"):
            layout_manager = construct_tab.layout_manager
            if hasattr(layout_manager, "start_position_picker"):
                return layout_manager.start_position_picker
            if hasattr(layout_manager, "picker_stack"):
                # Check if picker stack has start position picker
                for i in range(layout_manager.picker_stack.count()):
                    widget = layout_manager.picker_stack.widget(i)
                    if (
                        hasattr(widget, "__class__")
                        and "Start" in widget.__class__.__name__
                    ):
                        return widget

        return None

    def simulate_start_position_click(self, start_pos_picker):
        """Simulate clicking on a start position."""
        print("🎯 Simulating start position selection...")

        # Record selection start time
        self.selection_time = time.perf_counter()

        try:
            # Look for StartPositionOption widgets specifically
            start_position_options = []

            # Method 1: Look for StartPositionOption widgets
            for child in start_pos_picker.findChildren(QWidget):
                if (
                    hasattr(child, "__class__")
                    and "StartPositionOption" in child.__class__.__name__
                ):
                    start_position_options.append(child)
                    print(
                        f"📍 Found StartPositionOption: {child.position_key if hasattr(child, 'position_key') else 'unknown'}"
                    )

            # Method 2: Look for widgets with position_selected signal
            if not start_position_options:
                for child in start_pos_picker.findChildren(QWidget):
                    if hasattr(child, "position_selected"):
                        start_position_options.append(child)
                        print(
                            f"📍 Found widget with position_selected signal: {child.__class__.__name__}"
                        )

            # Method 3: Look for any clickable widgets in the picker
            if not start_position_options:
                for child in start_pos_picker.findChildren(QWidget):
                    if (
                        hasattr(child, "mousePressEvent")
                        and child.size().width() > 100
                        and child.size().height() > 100
                    ):  # Likely a position option
                        start_position_options.append(child)
                        print(
                            f"📍 Found large clickable widget: {child.__class__.__name__}"
                        )

            if start_position_options:
                print(f"✅ Found {len(start_position_options)} start position options")

                # Set up monitoring for option picker loading
                self.setup_option_picker_monitoring()

                # Click the first available option
                first_option = start_position_options[0]
                print(f"🖱️ Clicking start position: {first_option.__class__.__name__}")

                # Method 1: Try position_selected signal
                if hasattr(first_option, "position_selected"):
                    position_key = getattr(
                        first_option, "position_key", "alpha1_alpha1"
                    )
                    print(
                        f"   Emitting position_selected signal with key: {position_key}"
                    )
                    first_option.position_selected.emit(position_key)

                # Method 2: Try mouse press event
                else:
                    from PyQt6.QtGui import QMouseEvent
                    from PyQt6.QtCore import Qt, QPoint

                    print(f"   Simulating mouse press event")
                    press_event = QMouseEvent(
                        QMouseEvent.Type.MouseButtonPress,
                        QPoint(first_option.width() // 2, first_option.height() // 2),
                        Qt.MouseButton.LeftButton,
                        Qt.MouseButton.LeftButton,
                        Qt.KeyboardModifier.NoModifier,
                    )
                    first_option.mousePressEvent(press_event)

                print("✅ Start position clicked, monitoring for option picker...")

            else:
                print("❌ No start position options found")
                # Debug: Print all children to understand structure
                print("🔍 Debug: All children in start position picker:")
                for child in start_pos_picker.findChildren(QWidget):
                    print(f"   - {child.__class__.__name__}: {child.objectName()}")

                self.complete_test_with_error("No start position options found")

        except Exception as e:
            print(f"❌ Error simulating click: {e}")
            import traceback

            traceback.print_exc()
            self.complete_test_with_error(str(e))

    def setup_option_picker_monitoring(self):
        """Set up monitoring to detect when option picker loads."""
        # Use a timer to check for option picker loading
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_option_picker_loaded)
        self.monitor_timer.start(100)  # Check every 100ms

        # Set a timeout for the test
        self.timeout_timer = QTimer()
        self.timeout_timer.timeout.connect(self.test_timeout)
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.start(10000)  # 10 second timeout

    def check_option_picker_loaded(self):
        """Check if option picker has loaded with options."""
        try:
            # Look for option picker in the main window
            option_picker = self.find_option_picker()

            if option_picker:
                # Check if it has loaded options
                if self.has_loaded_options(option_picker):
                    self.options_loaded_time = time.perf_counter()
                    print("✅ Option picker loaded with options!")
                    self.complete_test_successfully()
                    return

            # Check if we're still on start position picker (no transition happened)
            elapsed = time.perf_counter() - self.selection_time
            if elapsed > 2.0:  # If more than 2 seconds, something might be wrong
                print(f"⚠️ Still waiting for options after {elapsed:.1f}s...")

        except Exception as e:
            print(f"❌ Error checking option picker: {e}")

    def find_option_picker(self):
        """Find the option picker widget."""
        # Look in the main window for option picker
        for child in self.main_window.findChildren(QWidget):
            if hasattr(child, "__class__") and "Option" in child.__class__.__name__:
                return child
        return None

    def has_loaded_options(self, option_picker):
        """Check if option picker has loaded options."""
        # Look for pictograph frames or option widgets
        option_widgets = option_picker.findChildren(QWidget)

        # Count visible widgets that might be options
        visible_options = 0
        for widget in option_widgets:
            if widget.isVisible() and hasattr(widget, "__class__"):
                class_name = widget.__class__.__name__.lower()
                if (
                    "pictograph" in class_name
                    or "option" in class_name
                    or "frame" in class_name
                ):
                    visible_options += 1

        return visible_options > 0

    def test_timeout(self):
        """Handle test timeout."""
        print("⏰ Test timed out - option picker did not load within 10 seconds")
        self.complete_test_with_error("Timeout - options did not load")

    def complete_test_successfully(self):
        """Complete the test with success."""
        self.cleanup_timers()

        total_time = self.options_loaded_time - self.start_time
        selection_to_load_time = self.options_loaded_time - self.selection_time

        self.test_results = {
            "success": True,
            "total_time": total_time,
            "selection_to_load_time": selection_to_load_time,
            "start_time": self.start_time,
            "selection_time": self.selection_time,
            "options_loaded_time": self.options_loaded_time,
        }

        print(f"🎉 Test completed successfully!")
        print(f"📊 Total time: {total_time:.3f}s")
        print(f"🎯 Selection to load time: {selection_to_load_time:.3f}s")

        self.test_completed.emit(self.test_results)

    def complete_test_with_error(self, error_message):
        """Complete the test with an error."""
        self.cleanup_timers()

        self.test_results = {
            "success": False,
            "error": error_message,
            "elapsed_time": (
                time.perf_counter() - self.start_time if self.start_time else 0
            ),
        }

        print(f"❌ Test failed: {error_message}")
        self.test_completed.emit(self.test_results)

    def cleanup_timers(self):
        """Clean up any running timers."""
        if hasattr(self, "monitor_timer"):
            self.monitor_timer.stop()
        if hasattr(self, "timeout_timer"):
            self.timeout_timer.stop()


def run_start_position_test():
    """Run the start position selection test on the real application."""
    print("🚀 Starting Real Application Start Position Test")
    print("=" * 60)

    try:
        # Create QApplication
        app = QApplication([])

        # Import and create the main window
        from main import KineticConstructorModern
        from PyQt6.QtGui import QGuiApplication

        screen = QGuiApplication.primaryScreen()

        print("📱 Creating main window...")
        main_window = KineticConstructorModern(
            target_screen=screen,
            parallel_mode=False,
            parallel_geometry=None,
            enable_api=False,
        )

        print("✅ Main window created, showing application...")
        main_window.show()

        # Create test monitor
        monitor = StartPositionTestMonitor()

        # Set up test completion handler
        def on_test_completed(results):
            print("\n" + "=" * 60)
            print("TEST RESULTS")
            print("=" * 60)

            if results["success"]:
                print(f"✅ SUCCESS: Start position selection test passed")
                print(f"📊 Performance Metrics:")
                print(f"   - Total time: {results['total_time']:.3f}s")
                print(
                    f"   - Selection to load: {results['selection_to_load_time']:.3f}s"
                )

                if results["selection_to_load_time"] > 1.0:
                    print(
                        f"⚠️ PERFORMANCE ISSUE: Selection to load time is {results['selection_to_load_time']:.3f}s"
                    )
                    print(f"   This is longer than expected (should be < 1.0s)")
                else:
                    print(f"✅ GOOD PERFORMANCE: Selection to load time is acceptable")
            else:
                print(f"❌ FAILED: {results['error']}")
                print(f"⏱️ Elapsed time: {results.get('elapsed_time', 0):.3f}s")

            # Quit the application
            QTimer.singleShot(1000, app.quit)

        monitor.test_completed.connect(on_test_completed)

        # Start the test after a short delay to let the UI settle
        QTimer.singleShot(2000, lambda: monitor.start_test(main_window))

        # Run the application
        return app.exec()

    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_start_position_test())
