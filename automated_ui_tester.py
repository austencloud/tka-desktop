#!/usr/bin/env python3
"""
TKA Automated UI Testing Framework
==================================

Fully automated testing system that programmatically interacts with Legacy and V2
applications to test specific functionality issues without manual intervention.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Automated Legacy/V2 functional equivalence validation
"""

import asyncio
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

# Add both Legacy and V2 source paths
legacy_src_path = Path(__file__).parent / "legacy" / "src"
v2_src_path = Path(__file__).parent / "v2" / "src"

if str(legacy_src_path) not in sys.path:
    sys.path.insert(0, str(legacy_src_path))
if str(v2_src_path) not in sys.path:
    sys.path.insert(0, str(v2_src_path))


class UIElementFinder:
    """Utility class to find UI elements in TKA applications."""

    @staticmethod
    def find_widget_by_name(parent: QWidget, name: str) -> Optional[QWidget]:
        """Find a widget by its object name."""
        return parent.findChild(QWidget, name)

    @staticmethod
    def find_button_by_text(parent: QWidget, text: str) -> Optional[QPushButton]:
        """Find a button by its text content."""
        buttons = parent.findChildren(QPushButton)
        for button in buttons:
            if text.lower() in button.text().lower():
                return button
        return None

    @staticmethod
    def find_all_buttons(parent: QWidget) -> List[QPushButton]:
        """Find all buttons in a widget."""
        return parent.findChildren(QPushButton)

    @staticmethod
    def get_widget_hierarchy(widget: QWidget, level: int = 0) -> str:
        """Get a string representation of widget hierarchy for debugging."""
        indent = "  " * level
        result = f"{indent}{widget.__class__.__name__}"
        if hasattr(widget, "objectName") and widget.objectName():
            result += f" (name: {widget.objectName()})"
        if hasattr(widget, "text") and widget.text():
            result += f" (text: {widget.text()})"
        result += "\n"

        for child in widget.children():
            if isinstance(child, QWidget):
                result += UIElementFinder.get_widget_hierarchy(child, level + 1)

        return result


class LegacyApplicationController:
    """Controller for automated Legacy application interaction."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.sequence_workbench = None
        self.option_picker = None
        self.beat_frame = None
        self._discover_components()

    def _discover_components(self):
        """Discover Legacy application components."""
        try:
            # Find sequence workbench
            self.sequence_workbench = UIElementFinder.find_widget_by_name(
                self.main_window, "sequence_workbench"
            )

            if not self.sequence_workbench:
                # Try alternative discovery methods
                workbenches = self.main_window.findChildren(QWidget)
                for widget in workbenches:
                    if "workbench" in widget.__class__.__name__.lower():
                        self.sequence_workbench = widget
                        break

            print(f"🔍 Legacy sequence_workbench: {self.sequence_workbench}")

            if self.sequence_workbench:
                # Find option picker and beat frame within workbench
                self.option_picker = UIElementFinder.find_widget_by_name(
                    self.sequence_workbench, "option_picker"
                )
                self.beat_frame = UIElementFinder.find_widget_by_name(
                    self.sequence_workbench, "beat_frame"
                )

                print(f"🔍 Legacy option_picker: {self.option_picker}")
                print(f"🔍 Legacy beat_frame: {self.beat_frame}")

        except Exception as e:
            print(f"❌ Legacy component discovery failed: {e}")

    def get_start_position_buttons(self) -> List[QPushButton]:
        """Get all start position selection buttons."""
        if not self.sequence_workbench:
            return []

        buttons = UIElementFinder.find_all_buttons(self.sequence_workbench)
        start_buttons = []

        for button in buttons:
            text = button.text().lower()
            if any(pos in text for pos in ["alpha", "beta", "gamma"]):
                start_buttons.append(button)

        return start_buttons

    def get_option_picker_buttons(self) -> List[QPushButton]:
        """Get all option picker buttons."""
        if not self.option_picker:
            return []

        return UIElementFinder.find_all_buttons(self.option_picker)

    def get_clear_sequence_button(self) -> Optional[QPushButton]:
        """Find the clear sequence button."""
        return UIElementFinder.find_button_by_text(self.main_window, "clear")

    def click_start_position(self, position: str = "alpha1_alpha1") -> bool:
        """Click a specific start position."""
        try:
            buttons = self.get_start_position_buttons()
            for button in buttons:
                if position.lower() in button.text().lower():
                    print(f"🎯 Legacy: Clicking start position {position}")
                    QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                    QApplication.processEvents()
                    time.sleep(1)  # Wait for UI update
                    return True

            print(f"❌ Legacy: Start position button '{position}' not found")
            return False

        except Exception as e:
            print(f"❌ Legacy: Failed to click start position: {e}")
            return False

    def click_option_picker_item(self, index: int = 0) -> bool:
        """Click an option picker item by index."""
        try:
            buttons = self.get_option_picker_buttons()
            if index < len(buttons):
                button = buttons[index]
                print(
                    f"🎯 Legacy: Clicking option picker item {index} ({button.text()})"
                )
                QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                QApplication.processEvents()
                time.sleep(1)  # Wait for UI update
                return True

            print(f"❌ Legacy: Option picker item {index} not found")
            return False

        except Exception as e:
            print(f"❌ Legacy: Failed to click option picker item: {e}")
            return False

    def click_clear_sequence(self) -> bool:
        """Click the clear sequence button."""
        try:
            button = self.get_clear_sequence_button()
            if button:
                print(f"🎯 Legacy: Clicking clear sequence")
                QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                QApplication.processEvents()
                time.sleep(1)  # Wait for UI update
                return True

            print(f"❌ Legacy: Clear sequence button not found")
            return False

        except Exception as e:
            print(f"❌ Legacy: Failed to click clear sequence: {e}")
            return False

    def get_current_state(self) -> Dict[str, Any]:
        """Get current application state."""
        try:
            state = {
                "option_picker_count": len(self.get_option_picker_buttons()),
                "start_buttons_count": len(self.get_start_position_buttons()),
                "has_clear_button": self.get_clear_sequence_button() is not None,
                "sequence_length": 0,  # TODO: Extract from beat frame
            }

            # Try to get option picker button texts
            option_buttons = self.get_option_picker_buttons()
            state["option_picker_items"] = [
                btn.text() for btn in option_buttons[:10]
            ]  # First 10

            return state

        except Exception as e:
            print(f"❌ Legacy: Failed to get current state: {e}")
            return {}


class V2ApplicationController:
    """Controller for automated V2 application interaction."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.construct_tab = None
        self.option_picker = None
        self.beat_frame = None
        self._discover_components()

    def _discover_components(self):
        """Discover V2 application components."""
        try:
            # Find construct tab
            tabs = self.main_window.findChildren(QWidget)
            for widget in tabs:
                if "construct" in widget.__class__.__name__.lower():
                    self.construct_tab = widget
                    break

            print(f"🔍 V2 construct_tab: {self.construct_tab}")

            if self.construct_tab:
                # Find option picker and beat frame within construct tab
                self.option_picker = UIElementFinder.find_widget_by_name(
                    self.construct_tab, "option_picker"
                )
                self.beat_frame = UIElementFinder.find_widget_by_name(
                    self.construct_tab, "beat_frame"
                )

                print(f"🔍 V2 option_picker: {self.option_picker}")
                print(f"🔍 V2 beat_frame: {self.beat_frame}")

        except Exception as e:
            print(f"❌ V2 component discovery failed: {e}")

    def get_start_position_buttons(self) -> List[QPushButton]:
        """Get all start position selection buttons."""
        if not self.construct_tab:
            return []

        buttons = UIElementFinder.find_all_buttons(self.construct_tab)
        start_buttons = []

        for button in buttons:
            text = button.text().lower()
            if any(pos in text for pos in ["alpha", "beta", "gamma"]):
                start_buttons.append(button)

        return start_buttons

    def get_option_picker_buttons(self) -> List[QPushButton]:
        """Get all option picker buttons."""
        if not self.option_picker:
            # Try to find option picker in construct tab
            if self.construct_tab:
                return UIElementFinder.find_all_buttons(self.construct_tab)

        return (
            UIElementFinder.find_all_buttons(self.option_picker)
            if self.option_picker
            else []
        )

    def get_clear_sequence_button(self) -> Optional[QPushButton]:
        """Find the clear sequence button."""
        return UIElementFinder.find_button_by_text(self.main_window, "clear")

    def click_start_position(self, position: str = "alpha1_alpha1") -> bool:
        """Click a specific start position."""
        try:
            buttons = self.get_start_position_buttons()
            for button in buttons:
                if position.lower() in button.text().lower():
                    print(f"🎯 V2: Clicking start position {position}")
                    QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                    QApplication.processEvents()
                    time.sleep(1)  # Wait for UI update
                    return True

            print(f"❌ V2: Start position button '{position}' not found")
            return False

        except Exception as e:
            print(f"❌ V2: Failed to click start position: {e}")
            return False

    def click_option_picker_item(self, index: int = 0) -> bool:
        """Click an option picker item by index."""
        try:
            buttons = self.get_option_picker_buttons()
            if index < len(buttons):
                button = buttons[index]
                print(f"🎯 V2: Clicking option picker item {index} ({button.text()})")
                QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                QApplication.processEvents()
                time.sleep(1)  # Wait for UI update
                return True

            print(f"❌ V2: Option picker item {index} not found")
            return False

        except Exception as e:
            print(f"❌ V2: Failed to click option picker item: {e}")
            return False

    def click_clear_sequence(self) -> bool:
        """Click the clear sequence button."""
        try:
            button = self.get_clear_sequence_button()
            if button:
                print(f"🎯 V2: Clicking clear sequence")
                QTest.mouseClick(button, Qt.MouseButton.LeftButton)
                QApplication.processEvents()
                time.sleep(1)  # Wait for UI update
                return True

            print(f"❌ V2: Clear sequence button not found")
            return False

        except Exception as e:
            print(f"❌ V2: Failed to click clear sequence: {e}")
            return False

    def get_current_state(self) -> Dict[str, Any]:
        """Get current application state."""
        try:
            state = {
                "option_picker_count": len(self.get_option_picker_buttons()),
                "start_buttons_count": len(self.get_start_position_buttons()),
                "has_clear_button": self.get_clear_sequence_button() is not None,
                "sequence_length": 0,  # TODO: Extract from beat frame
            }

            # Try to get option picker button texts
            option_buttons = self.get_option_picker_buttons()
            state["option_picker_items"] = [
                btn.text() for btn in option_buttons[:10]
            ]  # First 10

            return state

        except Exception as e:
            print(f"❌ V2: Failed to get current state: {e}")
            return {}


class AutomatedUITester:
    """Main automated UI testing coordinator."""

    def __init__(self):
        self.legacy_controller: Optional[LegacyApplicationController] = None
        self.v2_controller: Optional[V2ApplicationController] = None
        self.test_results: List[Dict[str, Any]] = []

    def setup_controllers(self, legacy_window, v2_window):
        """Setup controllers for both applications."""
        self.legacy_controller = LegacyApplicationController(legacy_window)
        self.v2_controller = V2ApplicationController(v2_window)

    async def test_option_picker_dynamic_updates(self) -> Dict[str, Any]:
        """Test Primary Issue 1: Option Picker Dynamic Updates."""
        print("\n🤖 TESTING: Option Picker Dynamic Updates")
        print("=" * 50)

        test_result = {
            "test_name": "option_picker_dynamic_updates",
            "timestamp": time.time(),
            "success": False,
            "legacy_data": {},
            "v2_data": {},
            "comparison": {},
            "issues_found": [],
        }

        try:
            # Step 1: Get initial state
            print("📊 Step 1: Getting initial state...")
            legacy_initial = self.legacy_controller.get_current_state()
            v2_initial = self.v2_controller.get_current_state()

            test_result["legacy_data"]["initial"] = legacy_initial
            test_result["v2_data"]["initial"] = v2_initial

            print(
                f"   Legacy initial options: {legacy_initial.get('option_picker_count', 0)}"
            )
            print(f"   V2 initial options: {v2_initial.get('option_picker_count', 0)}")

            # Step 2: Select start position
            print("📊 Step 2: Selecting start position (alpha1_alpha1)...")
            legacy_start_success = self.legacy_controller.click_start_position(
                "alpha1_alpha1"
            )
            v2_start_success = self.v2_controller.click_start_position("alpha1_alpha1")

            await asyncio.sleep(2)  # Wait for option picker population

            # Step 3: Get state after start position selection
            print("📊 Step 3: Getting state after start position selection...")
            legacy_after_start = self.legacy_controller.get_current_state()
            v2_after_start = self.v2_controller.get_current_state()

            test_result["legacy_data"]["after_start"] = legacy_after_start
            test_result["v2_data"]["after_start"] = v2_after_start

            print(
                f"   Legacy options after start: {legacy_after_start.get('option_picker_count', 0)}"
            )
            print(
                f"   V2 options after start: {v2_after_start.get('option_picker_count', 0)}"
            )

            # Step 4: Select first beat from option picker
            print("📊 Step 4: Selecting first beat from option picker...")
            legacy_beat_success = self.legacy_controller.click_option_picker_item(0)
            v2_beat_success = self.v2_controller.click_option_picker_item(0)

            await asyncio.sleep(3)  # Wait for option picker update

            # Step 5: Get state after first beat selection (CRITICAL TEST)
            print("📊 Step 5: Getting state after first beat selection...")
            legacy_after_beat = self.legacy_controller.get_current_state()
            v2_after_beat = self.v2_controller.get_current_state()

            test_result["legacy_data"]["after_beat"] = legacy_after_beat
            test_result["v2_data"]["after_beat"] = v2_after_beat

            print(
                f"   Legacy options after beat: {legacy_after_beat.get('option_picker_count', 0)}"
            )
            print(
                f"   V2 options after beat: {v2_after_beat.get('option_picker_count', 0)}"
            )

            # Step 6: Compare and analyze
            print("📊 Step 6: Analyzing option picker update behavior...")

            # Check if option picker updated after beat selection
            legacy_updated = legacy_after_beat.get(
                "option_picker_count", 0
            ) != legacy_after_start.get("option_picker_count", 0)
            v2_updated = v2_after_beat.get(
                "option_picker_count", 0
            ) != v2_after_start.get("option_picker_count", 0)

            test_result["comparison"] = {
                "legacy_option_picker_updated": legacy_updated,
                "v2_option_picker_updated": v2_updated,
                "both_updated": legacy_updated and v2_updated,
                "equivalence": legacy_updated == v2_updated,
            }

            # Identify issues
            if not v2_updated and legacy_updated:
                test_result["issues_found"].append(
                    "V2 option picker failed to update after beat selection (Legacy updated correctly)"
                )

            if not legacy_updated and not v2_updated:
                test_result["issues_found"].append(
                    "Neither Legacy nor V2 option picker updated after beat selection"
                )

            test_result["success"] = len(test_result["issues_found"]) == 0

            return test_result

        except Exception as e:
            test_result["error"] = str(e)
            test_result["issues_found"].append(f"Test execution failed: {e}")
            return test_result

    async def test_sequence_clear_functionality(self) -> Dict[str, Any]:
        """Test Primary Issue 2: Sequence Clear Functionality."""
        print("\n🤖 TESTING: Sequence Clear Functionality")
        print("=" * 50)

        test_result = {
            "test_name": "sequence_clear_functionality",
            "timestamp": time.time(),
            "success": False,
            "legacy_data": {},
            "v2_data": {},
            "comparison": {},
            "issues_found": [],
        }

        try:
            # Step 1: Build a sequence first
            print("📊 Step 1: Building a sequence...")

            # Select start position
            self.legacy_controller.click_start_position("alpha1_alpha1")
            self.v2_controller.click_start_position("alpha1_alpha1")
            await asyncio.sleep(2)

            # Add a beat
            self.legacy_controller.click_option_picker_item(0)
            self.v2_controller.click_option_picker_item(0)
            await asyncio.sleep(2)

            # Get state with sequence
            legacy_with_sequence = self.legacy_controller.get_current_state()
            v2_with_sequence = self.v2_controller.get_current_state()

            test_result["legacy_data"]["with_sequence"] = legacy_with_sequence
            test_result["v2_data"]["with_sequence"] = v2_with_sequence

            # Step 2: Clear sequence
            print("📊 Step 2: Clearing sequence...")
            legacy_clear_success = self.legacy_controller.click_clear_sequence()
            v2_clear_success = self.v2_controller.click_clear_sequence()

            await asyncio.sleep(3)  # Wait for clear operation

            # Step 3: Get state after clear
            print("📊 Step 3: Getting state after clear...")
            legacy_after_clear = self.legacy_controller.get_current_state()
            v2_after_clear = self.v2_controller.get_current_state()

            test_result["legacy_data"]["after_clear"] = legacy_after_clear
            test_result["v2_data"]["after_clear"] = v2_after_clear

            # Step 4: Analyze clear behavior
            print("📊 Step 4: Analyzing clear behavior...")

            # Check if both returned to start position selection
            legacy_has_start_buttons = (
                legacy_after_clear.get("start_buttons_count", 0) > 0
            )
            v2_has_start_buttons = v2_after_clear.get("start_buttons_count", 0) > 0

            test_result["comparison"] = {
                "legacy_returned_to_start_selection": legacy_has_start_buttons,
                "v2_returned_to_start_selection": v2_has_start_buttons,
                "both_returned_to_start": legacy_has_start_buttons
                and v2_has_start_buttons,
                "equivalence": legacy_has_start_buttons == v2_has_start_buttons,
            }

            # Identify issues
            if not v2_has_start_buttons and legacy_has_start_buttons:
                test_result["issues_found"].append(
                    "V2 failed to return to start position selection after clear (Legacy returned correctly)"
                )

            if not legacy_has_start_buttons and not v2_has_start_buttons:
                test_result["issues_found"].append(
                    "Neither Legacy nor V2 returned to start position selection after clear"
                )

            test_result["success"] = len(test_result["issues_found"]) == 0

            return test_result

        except Exception as e:
            test_result["error"] = str(e)
            test_result["issues_found"].append(f"Test execution failed: {e}")
            return test_result

    def generate_test_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate comprehensive test report."""
        report = []
        report.append("🤖 TKA AUTOMATED UI TESTING REPORT")
        report.append("=" * 50)
        report.append(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Tests Executed: {len(results)}")
        report.append("")

        for result in results:
            test_name = result.get("test_name", "Unknown Test")
            success = result.get("success", False)
            issues = result.get("issues_found", [])

            report.append(f"📋 TEST: {test_name}")
            report.append("-" * 30)
            report.append(f"Result: {'✅ PASS' if success else '❌ FAIL'}")

            if issues:
                report.append("Issues Found:")
                for issue in issues:
                    report.append(f"  • {issue}")

            # Add detailed comparison data
            comparison = result.get("comparison", {})
            if comparison:
                report.append("Comparison Details:")
                for key, value in comparison.items():
                    report.append(f"  • {key}: {value}")

            report.append("")

        return "\n".join(report)


async def main():
    """Main automated testing routine."""
    print("🤖 TKA AUTOMATED UI TESTING FRAMEWORK")
    print("=" * 50)

    try:
        # Create applications
        print("🚀 Starting Legacy and V2 applications...")

        # Import and create Legacy application
        from main_window.main_window import MainWindow as LegacyMainWindow
        from settings_manager.settings_manager import SettingsManager
        from splash_screen.splash_screen import SplashScreen
        from profiler.profiler import Profiler

        app = QApplication(sys.argv)

        # Create Legacy
        settings_manager = SettingsManager()
        splash_screen = SplashScreen(app, settings_manager)
        profiler = Profiler()
        legacy_window = LegacyMainWindow(profiler, splash_screen)
        legacy_window.initialize_widgets()
        legacy_window.show()

        # Create V2
        from src.main import create_application

        v2_app, v2_window = create_application()
        v2_window.show()

        # Process events
        app.processEvents()
        await asyncio.sleep(3)  # Wait for full initialization

        print("✅ Both applications started successfully")

        # Create automated tester
        tester = AutomatedUITester()
        tester.setup_controllers(legacy_window, v2_window)

        # Run automated tests
        print("\n🎯 EXECUTING AUTOMATED TESTS")
        print("=" * 40)

        results = []

        # Test 1: Option Picker Dynamic Updates
        result1 = await tester.test_option_picker_dynamic_updates()
        results.append(result1)

        # Test 2: Sequence Clear Functionality
        result2 = await tester.test_sequence_clear_functionality()
        results.append(result2)

        # Generate and display report
        report = tester.generate_test_report(results)
        print("\n" + report)

        # Save report to file
        timestamp = int(time.time())
        report_filename = f"automated_ui_test_report_{timestamp}.txt"
        with open(report_filename, "w") as f:
            f.write(report)

        print(f"\n💾 Report saved: {report_filename}")

        return 0

    except Exception as e:
        print(f"❌ Automated testing failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
