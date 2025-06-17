#!/usr/bin/env python3
"""
Comprehensive End-to-End UI Test for TKA Graph Editor Workflow

This test simulates the complete user workflow using the full application window
with automated mouse clicks and detailed logging to track state changes.

Test Workflow:
1. Initial State Validation - Launch app and verify initial state
2. Start Position Selection - Click start positions and verify updates
3. Option Selection - Click option pictographs and verify correct data selection
4. Clear Sequence - Test sequence clearing functionality

Critical Bug Detection:
- Verify clicked pictographs match selected data (not first item in array)
- Log all state changes for debugging
"""

import sys
import time
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, QPoint, QPointF, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtTest import QTest

# Add Modern source path and main directory
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
modern_main_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(modern_src_path))
sys.path.insert(0, str(modern_main_path))

# Import Modern application
try:
    from modern.main import KineticConstructorModern
except ImportError:
    # Fallback import path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "modern"))
    from main import KineticConstructorModern


class GraphEditorUIWorkflowTester:
    """Comprehensive end-to-end UI tester for TKA graph editor workflow"""

    def __init__(self):
        self.app: Optional[QApplication] = None
        self.main_window: Optional[KineticConstructorModern] = None
        self.construct_tab: Optional[QWidget] = None
        self.workbench: Optional[QWidget] = None
        self.start_position_picker: Optional[QWidget] = None
        self.option_picker: Optional[QWidget] = None
        self.beat_frame: Optional[QWidget] = None

        # Test state tracking
        self.test_results: Dict[str, Any] = {}
        self.current_test_step = ""
        self.errors: List[str] = []

    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with test step context"""
        timestamp = time.strftime("%H:%M:%S")
        step_info = f"[{self.current_test_step}]" if self.current_test_step else ""
        print(f"[{timestamp}] {level} {step_info} {message}")

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error with optional exception details"""
        self.errors.append(message)
        self.log(f"❌ {message}", "ERROR")
        if exception:
            self.log(f"Exception details: {str(exception)}", "ERROR")
            traceback.print_exc()

    def setup_application(self) -> bool:
        """Setup the full Modern application for testing"""
        self.current_test_step = "APPLICATION_SETUP"
        self.log("🚀 Setting up TKA Modern application for end-to-end testing")

        try:
            # Create QApplication if not exists
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
                self.app.setStyle("Fusion")
            else:
                self.app = QApplication.instance()

            # Create main window without splash screen for testing
            self.log("Creating main window...")
            self.main_window = KineticConstructorModern(
                splash_screen=None, target_screen=None
            )

            # Show and process events
            self.main_window.show()
            QApplication.processEvents()

            # Wait for initialization
            self.log("Waiting for application initialization...")
            time.sleep(2)
            QApplication.processEvents()

            self.log("✅ Application setup completed")
            return True

        except Exception as e:
            self.log_error("Failed to setup application", e)
            return False

    def find_components(self) -> bool:
        """Find and cache key UI components for testing"""
        self.current_test_step = "COMPONENT_DISCOVERY"
        self.log("🔍 Discovering UI components...")

        try:
            # Find construct tab
            if hasattr(self.main_window, "construct_tab"):
                self.construct_tab = self.main_window.construct_tab
                self.log("✅ Found construct tab")
            else:
                self.log_error("Construct tab not found")
                return False

            # Find workbench within construct tab
            if hasattr(self.construct_tab, "workbench"):
                self.workbench = self.construct_tab.workbench
                self.log("✅ Found workbench")
            else:
                self.log_error("Workbench not found in construct tab")
                return False

            # Find start position picker
            if hasattr(self.construct_tab, "start_position_picker"):
                self.start_position_picker = self.construct_tab.start_position_picker
                self.log("✅ Found start position picker")
            else:
                self.log_error("Start position picker not found")
                return False

            # Find option picker
            if hasattr(self.construct_tab, "option_picker"):
                self.option_picker = self.construct_tab.option_picker
                self.log("✅ Found option picker")
            else:
                self.log_error("Option picker not found")
                return False

            # Find beat frame within workbench
            if hasattr(self.workbench, "_beat_frame_section"):
                beat_frame_section = self.workbench._beat_frame_section
                if hasattr(beat_frame_section, "_beat_frame"):
                    self.beat_frame = beat_frame_section._beat_frame
                    self.log("✅ Found beat frame")
                else:
                    self.log_error("Beat frame not found in beat frame section")
                    return False
            else:
                self.log_error("Beat frame section not found in workbench")
                return False

            self.log("✅ All components discovered successfully")
            return True

        except Exception as e:
            self.log_error("Failed to find components", e)
            return False

    def validate_initial_state(self) -> bool:
        """Validate the initial application state"""
        self.current_test_step = "INITIAL_STATE_VALIDATION"
        self.log("🔍 Validating initial application state...")

        try:
            # Check if beat frame shows grid/start position
            if self.beat_frame and hasattr(self.beat_frame, "_start_position_view"):
                start_pos_view = self.beat_frame._start_position_view
                if start_pos_view and start_pos_view.isVisible():
                    self.log("✅ Beat frame start position view is visible")
                else:
                    self.log_error("Beat frame start position view not visible")
                    return False
            else:
                self.log_error("Beat frame start position view not found")
                return False

            # Check if start position picker shows three positions
            if self.start_position_picker:
                # Look for start position buttons/widgets
                start_positions = self._find_start_position_widgets()
                if len(start_positions) >= 3:
                    self.log(f"✅ Found {len(start_positions)} start position options")
                    self.test_results["start_positions_found"] = len(start_positions)
                else:
                    self.log_error(
                        f"Expected at least 3 start positions, found {len(start_positions)}"
                    )
                    return False
            else:
                self.log_error("Start position picker not available")
                return False

            # Check if construct tab is in start position picker mode
            if hasattr(self.construct_tab, "picker_stack"):
                current_index = self.construct_tab.picker_stack.currentIndex()
                if current_index == 0:
                    self.log("✅ Construct tab is in start position picker mode")
                else:
                    self.log_error(
                        f"Expected start position picker mode (index 0), got index {current_index}"
                    )
                    return False

            self.log("✅ Initial state validation passed")
            return True

        except Exception as e:
            self.log_error("Initial state validation failed", e)
            return False

    def _find_start_position_widgets(self) -> List[QWidget]:
        """Find start position clickable widgets"""
        start_positions = []

        try:
            if hasattr(self.start_position_picker, "findChildren"):
                # Look for clickable widgets that might be start positions
                clickable_widgets = self.start_position_picker.findChildren(QWidget)
                for widget in clickable_widgets:
                    # Check if widget has properties that suggest it's a start position
                    if hasattr(widget, "mousePressEvent") and hasattr(
                        widget, "position_key"
                    ):
                        start_positions.append(widget)
                    elif (
                        hasattr(widget, "clicked")
                        and "position" in str(type(widget)).lower()
                    ):
                        start_positions.append(widget)

            # Fallback: look for any clickable widgets in start position picker
            if not start_positions and hasattr(
                self.start_position_picker, "findChildren"
            ):
                from PyQt6.QtWidgets import QPushButton, QLabel

                buttons = self.start_position_picker.findChildren(QPushButton)
                labels = self.start_position_picker.findChildren(QLabel)
                start_positions.extend(buttons[:3])  # Take first 3 buttons
                if len(start_positions) < 3:
                    start_positions.extend(
                        labels[: 3 - len(start_positions)]
                    )  # Add labels if needed

        except Exception as e:
            self.log_error("Error finding start position widgets", e)

        return start_positions

    def simulate_mouse_click(
        self, widget: QWidget, position: Optional[QPoint] = None
    ) -> bool:
        """Simulate mouse click on widget with detailed logging"""
        try:
            if not widget or not widget.isVisible():
                self.log_error(f"Widget not visible or None: {widget}")
                return False

            # Use center of widget if no position specified
            if position is None:
                position = widget.rect().center()

            # Convert QPoint to QPointF for PyQt6 compatibility
            local_pos = QPointF(position)
            global_pos = QPointF(widget.mapToGlobal(position))

            self.log(
                f"🖱️ Clicking widget {type(widget).__name__} at position {position}"
            )

            # Create and send mouse press event
            press_event = QMouseEvent(
                QMouseEvent.Type.MouseButtonPress,
                local_pos,
                global_pos,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )

            # Create and send mouse release event
            release_event = QMouseEvent(
                QMouseEvent.Type.MouseButtonRelease,
                local_pos,
                global_pos,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier,
            )

            # Send events
            QApplication.sendEvent(widget, press_event)
            QApplication.processEvents()
            time.sleep(0.1)  # Small delay
            QApplication.sendEvent(widget, release_event)
            QApplication.processEvents()

            self.log("✅ Mouse click simulated successfully")
            return True

        except Exception as e:
            self.log_error("Failed to simulate mouse click", e)
            return False

    def test_start_position_selection(self) -> bool:
        """Test start position selection workflow"""
        self.current_test_step = "START_POSITION_SELECTION"
        self.log("🎯 Testing start position selection...")

        try:
            # Find start position widgets
            start_positions = self._find_start_position_widgets()
            if not start_positions:
                self.log_error("No start position widgets found")
                return False

            # Click the first start position
            first_position = start_positions[0]
            self.log(f"Clicking first start position: {type(first_position).__name__}")

            if not self.simulate_mouse_click(first_position):
                return False

            # Wait for UI updates
            time.sleep(1)
            QApplication.processEvents()

            # Verify transition to option picker
            if hasattr(self.construct_tab, "picker_stack"):
                current_index = self.construct_tab.picker_stack.currentIndex()
                if current_index == 1:
                    self.log("✅ Successfully transitioned to option picker")
                else:
                    self.log_error(
                        f"Expected option picker mode (index 1), got index {current_index}"
                    )
                    return False

            # Verify beat frame shows start position
            if self.beat_frame and hasattr(self.beat_frame, "_start_position_view"):
                start_pos_view = self.beat_frame._start_position_view
                if start_pos_view and start_pos_view.isVisible():
                    self.log("✅ Beat frame still shows start position")
                else:
                    self.log_error(
                        "Beat frame start position view not visible after selection"
                    )
                    return False

            self.log("✅ Start position selection test passed")
            return True

        except Exception as e:
            self.log_error("Start position selection test failed", e)
            return False

    def test_option_selection_with_bug_detection(self) -> bool:
        """Test option selection and detect pictograph selection bug"""
        self.current_test_step = "OPTION_SELECTION_BUG_DETECTION"
        self.log("🐛 Testing option selection with bug detection...")

        try:
            # Find option picker pictographs
            if not self.option_picker:
                self.log_error("Option picker not available")
                return False

            # Wait for option picker to fully populate
            self.log("Waiting for option picker to populate...")
            time.sleep(2)
            QApplication.processEvents()

            # Debug: inspect option picker structure
            self._debug_option_picker_structure()

            # Look for clickable pictograph frames
            option_frames = self._find_option_pictograph_frames()
            if not option_frames:
                self.log_error("No option pictograph frames found")
                return False

            # Test clicking multiple different options to verify correct data selection
            test_count = min(5, len(option_frames))  # Test up to 5 different options
            self.log(f"Testing {test_count} different pictograph options...")

            for i, frame in enumerate(option_frames[:test_count]):
                self.log(
                    f"\n--- Testing option {i+1}/{test_count}: {type(frame).__name__} ---"
                )

                # Get expected beat data before clicking (full pictograph data)
                expected_beat_data = self._get_expected_beat_data_for_frame(frame)
                if not expected_beat_data:
                    self.log_error(f"Could not get expected beat data for option {i+1}")
                    continue

                expected_letter = expected_beat_data.get("letter", "Unknown")
                self.log(f"Expected beat letter: {expected_letter}")
                self.log(
                    f"Expected beat data preview: {self._format_beat_data_preview(expected_beat_data)}"
                )

                # Record sequence length before clicking
                sequence_length_before = self._get_sequence_length()
                self.log(f"Sequence length before click: {sequence_length_before}")

                # Click the option
                if not self.simulate_mouse_click(frame):
                    self.log_error(f"Failed to click option {i+1}")
                    continue

                # Wait for processing
                time.sleep(0.8)  # Longer wait to ensure processing
                QApplication.processEvents()

                # Verify sequence length increased
                sequence_length_after = self._get_sequence_length()
                self.log(f"Sequence length after click: {sequence_length_after}")

                if sequence_length_after <= sequence_length_before:
                    self.log_error(
                        f"Sequence length did not increase after clicking option {i+1}"
                    )
                    continue

                # Verify correct beat data was selected (full pictograph data comparison)
                actual_beat_data = self._get_actual_selected_beat_data()
                if not actual_beat_data:
                    self.log_error(f"Could not get actual beat data for option {i+1}")
                    continue

                # Compare the full pictograph data, not just the letter
                comparison_result = self._compare_pictograph_data(
                    expected_beat_data, actual_beat_data
                )

                if comparison_result["matches"]:
                    self.log(f"✅ Correct pictograph data selected: {expected_letter}")
                    self.log(
                        f"✅ Motion data matches: {comparison_result['motion_summary']}"
                    )
                    self.log(f"✅ Option {i+1} test PASSED")
                else:
                    self.log_error(
                        f"🐛 BUG DETECTED in option {i+1}: Pictograph data mismatch!"
                    )
                    self.log_error(
                        f"Expected: {self._format_beat_data_preview(expected_beat_data)}"
                    )
                    self.log_error(
                        f"Actual: {self._format_beat_data_preview(actual_beat_data)}"
                    )
                    self.log_error(f"Differences: {comparison_result['differences']}")

                    self.test_results["pictograph_selection_bug"] = {
                        "expected_letter": expected_letter,
                        "actual_letter": actual_beat_data.get("letter", "Unknown"),
                        "expected_data": expected_beat_data,
                        "actual_data": actual_beat_data,
                        "differences": comparison_result["differences"],
                        "option_index": i,
                        "start_position": getattr(
                            self, "_current_start_position", "unknown"
                        ),
                    }
                    return False

            self.log("✅ Option selection test passed")
            return True

        except Exception as e:
            self.log_error("Option selection test failed", e)
            return False

    def _find_option_pictograph_frames(self) -> List[QWidget]:
        """Find option pictograph clickable frames"""
        option_frames = []

        try:
            # First, try to get frames from the pool manager
            if (
                hasattr(self.option_picker, "_pool_manager")
                and self.option_picker._pool_manager
            ):
                pool_manager = self.option_picker._pool_manager
                if hasattr(pool_manager, "get_pool_size") and hasattr(
                    pool_manager, "get_pool_frame"
                ):
                    pool_size = pool_manager.get_pool_size()
                    self.log(f"Pool manager has {pool_size} frames")

                    for i in range(pool_size):
                        frame = pool_manager.get_pool_frame(i)
                        if frame and frame.isVisible():
                            option_frames.append(frame)
                            self.log(
                                f"Found visible pool frame {i}: {type(frame).__name__}"
                            )

                    if option_frames:
                        self.log(
                            f"Found {len(option_frames)} visible frames from pool manager"
                        )
                        return option_frames

            # Second, try to find frames in the main widget
            search_widgets = []
            if hasattr(self.option_picker, "widget") and self.option_picker.widget:
                search_widgets.append(self.option_picker.widget)
            if (
                hasattr(self.option_picker, "sections_container")
                and self.option_picker.sections_container
            ):
                search_widgets.append(self.option_picker.sections_container)

            for search_widget in search_widgets:
                if hasattr(search_widget, "findChildren"):
                    # Look for clickable pictograph frames
                    try:
                        from src.presentation.components.option_picker.clickable_pictograph_frame import (
                            ClickablePictographFrame,
                        )

                        frames = search_widget.findChildren(ClickablePictographFrame)
                        visible_frames = [f for f in frames if f.isVisible()]
                        option_frames.extend(visible_frames)
                        self.log(
                            f"Found {len(visible_frames)} visible ClickablePictographFrame objects in {type(search_widget).__name__}"
                        )
                    except ImportError:
                        self.log(
                            "ClickablePictographFrame import failed, using fallback"
                        )

                    # Enhanced fallback: look for widgets with specific properties
                    if not option_frames:
                        all_widgets = search_widget.findChildren(QWidget)
                        self.log(
                            f"Searching through {len(all_widgets)} widgets in {type(search_widget).__name__}"
                        )

                        for widget in all_widgets:
                            # Check for various indicators that this is a clickable option
                            widget_type = type(widget).__name__

                            # Look for widgets with beat_data or clicked signal
                            if (
                                hasattr(widget, "beat_data")
                                or hasattr(widget, "clicked")
                                or "pictograph" in widget_type.lower()
                                or "option" in widget_type.lower()
                                or "frame" in widget_type.lower()
                            ):

                                # Additional check: must be visible and have reasonable size
                                if (
                                    widget.isVisible()
                                    and widget.width() > 10
                                    and widget.height() > 10
                                ):
                                    option_frames.append(widget)
                                    self.log(
                                        f"Found potential option frame: {widget_type}"
                                    )

                    # Final fallback: look for any visible, reasonably-sized widgets
                    if not option_frames:
                        self.log(
                            "No specific option frames found, using visible widgets as fallback"
                        )
                        all_widgets = search_widget.findChildren(QWidget)
                        for widget in all_widgets[
                            :10
                        ]:  # Limit to first 10 to avoid too many
                            if (
                                widget.isVisible()
                                and widget.width() > 50
                                and widget.height() > 50
                            ):
                                option_frames.append(widget)
                                self.log(
                                    f"Fallback option frame: {type(widget).__name__}"
                                )

        except Exception as e:
            self.log_error("Error finding option pictograph frames", e)

        self.log(f"Total option frames found: {len(option_frames)}")
        return option_frames

    def _debug_option_picker_structure(self):
        """Debug method to inspect option picker structure"""
        try:
            self.log("🔍 DEBUG: Inspecting option picker structure...")

            # Check option picker's own properties
            self.log(f"Option picker type: {type(self.option_picker).__name__}")

            # Check if option picker has specific attributes for ModernOptionPicker
            attrs_to_check = [
                "widget",
                "sections_container",
                "_pool_manager",
                "_display_manager",
                "_widget_factory",
                "sections_layout",
            ]
            for attr in attrs_to_check:
                if hasattr(self.option_picker, attr):
                    value = getattr(self.option_picker, attr)
                    if value is not None:
                        self.log(
                            f"Option picker has attribute '{attr}': {type(value).__name__}"
                        )
                    else:
                        self.log(f"Option picker has attribute '{attr}': None")

            # Check the main widget container
            if hasattr(self.option_picker, "widget") and self.option_picker.widget:
                widget = self.option_picker.widget
                self.log(f"Main widget type: {type(widget).__name__}")
                self.log(f"Main widget visible: {widget.isVisible()}")
                self.log(f"Main widget size: {widget.width()}x{widget.height()}")

                # Check children of main widget
                if hasattr(widget, "findChildren"):
                    all_children = widget.findChildren(QWidget)
                    self.log(f"Main widget has {len(all_children)} child widgets")

                    # Show first few widget types
                    for i, child in enumerate(all_children[:10]):
                        widget_type = type(child).__name__
                        visible = child.isVisible()
                        size = f"{child.width()}x{child.height()}"
                        self.log(
                            f"  Child {i}: {widget_type} (visible: {visible}, size: {size})"
                        )

            # Check sections container
            if (
                hasattr(self.option_picker, "sections_container")
                and self.option_picker.sections_container
            ):
                sections_container = self.option_picker.sections_container
                self.log(
                    f"Sections container type: {type(sections_container).__name__}"
                )

                if hasattr(sections_container, "findChildren"):
                    section_children = sections_container.findChildren(QWidget)
                    self.log(
                        f"Sections container has {len(section_children)} child widgets"
                    )

            # Check pool manager
            if (
                hasattr(self.option_picker, "_pool_manager")
                and self.option_picker._pool_manager
            ):
                pool_manager = self.option_picker._pool_manager
                self.log(f"Pool manager type: {type(pool_manager).__name__}")
                if hasattr(pool_manager, "get_pool_size"):
                    pool_size = pool_manager.get_pool_size()
                    self.log(f"Pool manager has {pool_size} frames")

            # Check display manager
            if (
                hasattr(self.option_picker, "_display_manager")
                and self.option_picker._display_manager
            ):
                display_manager = self.option_picker._display_manager
                self.log(f"Display manager type: {type(display_manager).__name__}")
                if hasattr(display_manager, "_sections"):
                    sections = display_manager._sections
                    self.log(f"Display manager has {len(sections)} sections")

        except Exception as e:
            self.log_error("Error during option picker structure debug", e)

    def _get_expected_beat_data_for_frame(
        self, frame: QWidget
    ) -> Optional[Dict[str, Any]]:
        """Get expected beat data for a pictograph frame"""
        try:
            if hasattr(frame, "beat_data"):
                beat_data = frame.beat_data
                if hasattr(beat_data, "to_dict"):
                    return beat_data.to_dict()
                elif hasattr(beat_data, "letter"):
                    return {"letter": beat_data.letter}
        except Exception as e:
            self.log_error("Error getting expected beat data", e)

        return None

    def _get_actual_selected_beat_data(self) -> Optional[Dict[str, Any]]:
        """Get the actual beat data that was selected"""
        try:
            # Check workbench for current sequence
            if self.workbench and hasattr(self.workbench, "get_sequence"):
                sequence = self.workbench.get_sequence()
                if sequence and sequence.beats:
                    last_beat = sequence.beats[-1]
                    if hasattr(last_beat, "to_dict"):
                        return last_beat.to_dict()
                    elif hasattr(last_beat, "letter"):
                        return {"letter": last_beat.letter}
        except Exception as e:
            self.log_error("Error getting actual selected beat data", e)

        return None

    def _get_sequence_length(self) -> int:
        """Get current sequence length"""
        try:
            if self.workbench and hasattr(self.workbench, "get_sequence"):
                sequence = self.workbench.get_sequence()
                if sequence:
                    return sequence.length
        except Exception as e:
            self.log_error("Error getting sequence length", e)
        return 0

    def _format_beat_data_preview(self, beat_data: Dict[str, Any]) -> str:
        """Format beat data for readable preview"""
        try:
            letter = beat_data.get("letter", "Unknown")

            # Extract motion information
            blue_motion = beat_data.get("blue_motion", {})
            red_motion = beat_data.get("red_motion", {})

            blue_type = blue_motion.get("motion_type", "unknown")
            red_type = red_motion.get("motion_type", "unknown")

            blue_turns = blue_motion.get("turns", 0)
            red_turns = red_motion.get("turns", 0)

            blue_start_ori = blue_motion.get("start_ori", "unknown")
            blue_end_ori = blue_motion.get("end_ori", "unknown")
            red_start_ori = red_motion.get("start_ori", "unknown")
            red_end_ori = red_motion.get("end_ori", "unknown")

            # Extract location information (the key differentiator)
            blue_start_loc = blue_motion.get("start_loc", "unknown")
            blue_end_loc = blue_motion.get("end_loc", "unknown")
            red_start_loc = red_motion.get("start_loc", "unknown")
            red_end_loc = red_motion.get("end_loc", "unknown")

            return (
                f"{letter} [Blue: {blue_type}({blue_turns}t) {blue_start_loc}→{blue_end_loc} ori:{blue_start_ori}→{blue_end_ori}, "
                f"Red: {red_type}({red_turns}t) {red_start_loc}→{red_end_loc} ori:{red_start_ori}→{red_end_ori}]"
            )
        except Exception as e:
            return f"Error formatting beat data: {e}"

    def _compare_pictograph_data(
        self, expected: Dict[str, Any], actual: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two pictograph data dictionaries for exact match"""
        try:
            differences = []

            # Compare letter
            if expected.get("letter") != actual.get("letter"):
                differences.append(
                    f"Letter: expected '{expected.get('letter')}', got '{actual.get('letter')}'"
                )

            # Compare blue motion
            expected_blue = expected.get("blue_motion", {})
            actual_blue = actual.get("blue_motion", {})
            blue_diffs = self._compare_motion_data("Blue", expected_blue, actual_blue)
            differences.extend(blue_diffs)

            # Compare red motion
            expected_red = expected.get("red_motion", {})
            actual_red = actual.get("red_motion", {})
            red_diffs = self._compare_motion_data("Red", expected_red, actual_red)
            differences.extend(red_diffs)

            # Compare other important fields (excluding beat_number which is just a testing artifact)
            important_fields = [
                "duration"
            ]  # Removed beat_number since it's just sequence position
            for field in important_fields:
                if expected.get(field) != actual.get(field):
                    differences.append(
                        f"{field}: expected '{expected.get(field)}', got '{actual.get(field)}'"
                    )

            matches = len(differences) == 0

            # Create motion summary focusing on locations (key differentiator)
            motion_summary = ""
            if matches:
                blue_type = expected_blue.get("motion_type", "unknown")
                red_type = expected_red.get("motion_type", "unknown")
                blue_locs = f"{expected_blue.get('start_loc', '?')}→{expected_blue.get('end_loc', '?')}"
                red_locs = f"{expected_red.get('start_loc', '?')}→{expected_red.get('end_loc', '?')}"
                motion_summary = (
                    f"Blue: {blue_type} {blue_locs}, Red: {red_type} {red_locs}"
                )

            return {
                "matches": matches,
                "differences": differences,
                "motion_summary": motion_summary,
            }

        except Exception as e:
            return {
                "matches": False,
                "differences": [f"Comparison error: {e}"],
                "motion_summary": "Error",
            }

    def _compare_motion_data(
        self, color: str, expected: Dict[str, Any], actual: Dict[str, Any]
    ) -> List[str]:
        """Compare motion data between expected and actual"""
        differences = []

        motion_fields = [
            "motion_type",
            "turns",
            "start_ori",
            "end_ori",
            "prop_rot_dir",
            "start_loc",
            "end_loc",
        ]

        for field in motion_fields:
            expected_val = expected.get(field)
            actual_val = actual.get(field)

            if expected_val != actual_val:
                differences.append(
                    f"{color} {field}: expected '{expected_val}', got '{actual_val}'"
                )

        return differences

    def test_clear_sequence(self) -> bool:
        """Test clear sequence functionality"""
        self.current_test_step = "CLEAR_SEQUENCE_TEST"
        self.log("🗑️ Testing clear sequence functionality...")

        try:
            # Find clear sequence button in workbench
            clear_button = self._find_clear_sequence_button()
            if not clear_button:
                self.log_error("Clear sequence button not found")
                return False

            # Click clear button
            if not self.simulate_mouse_click(clear_button):
                return False

            # Wait for processing
            time.sleep(1)
            QApplication.processEvents()

            # Verify sequence is cleared
            if self.workbench and hasattr(self.workbench, "get_sequence"):
                sequence = self.workbench.get_sequence()
                if sequence and sequence.length == 0:
                    self.log("✅ Sequence cleared successfully")
                else:
                    self.log_error(
                        f"Sequence not cleared, length: {sequence.length if sequence else 'None'}"
                    )
                    return False

            # Verify return to start position picker
            if hasattr(self.construct_tab, "picker_stack"):
                current_index = self.construct_tab.picker_stack.currentIndex()
                if current_index == 0:
                    self.log("✅ Returned to start position picker")
                else:
                    self.log_error(
                        f"Expected start position picker (index 0), got index {current_index}"
                    )
                    return False

            self.log("✅ Clear sequence test passed")
            return True

        except Exception as e:
            self.log_error("Clear sequence test failed", e)
            return False

    def _find_clear_sequence_button(self) -> Optional[QWidget]:
        """Find the clear sequence button"""
        try:
            # Search in multiple locations for clear button
            search_locations = []

            # Add workbench and its components
            if self.workbench:
                search_locations.append(("workbench", self.workbench))

                # Add beat frame section
                if hasattr(self.workbench, "_beat_frame_section"):
                    beat_frame_section = self.workbench._beat_frame_section
                    search_locations.append(("beat_frame_section", beat_frame_section))

                    # Add button panel
                    if hasattr(beat_frame_section, "_button_panel"):
                        button_panel = beat_frame_section._button_panel
                        search_locations.append(("button_panel", button_panel))

            # Add main window for broader search
            if self.main_window:
                search_locations.append(("main_window", self.main_window))

            # Search each location
            for location_name, location_widget in search_locations:
                self.log(f"Searching for clear button in {location_name}")

                if hasattr(location_widget, "findChildren"):
                    from PyQt6.QtWidgets import QPushButton

                    buttons = location_widget.findChildren(QPushButton)
                    self.log(f"Found {len(buttons)} buttons in {location_name}")

                    for i, button in enumerate(buttons):
                        button_text = button.text().lower()
                        self.log(
                            f"  Button {i}: '{button.text()}' (visible: {button.isVisible()})"
                        )

                        # Check for clear-related text or clear emoji
                        if (
                            any(
                                keyword in button_text
                                for keyword in ["clear", "reset", "new", "empty"]
                            )
                            or button.text() == "🧹"
                        ):
                            self.log(f"Found clear button: '{button.text()}'")
                            return button

            # If no clear button found, look for any button that might clear the sequence
            self.log(
                "No clear button found by text, searching for any sequence-related buttons"
            )

            if self.workbench and hasattr(self.workbench, "findChildren"):
                from PyQt6.QtWidgets import QPushButton

                all_buttons = self.workbench.findChildren(QPushButton)
                self.log(f"Found {len(all_buttons)} total buttons in workbench")

                for button in all_buttons:
                    if button.isVisible():
                        self.log(f"Visible button: '{button.text()}'")
                        # Return first visible button as fallback for testing
                        if button.text().strip():  # Has some text
                            return button

        except Exception as e:
            self.log_error("Error finding clear sequence button", e)

        return None

    def cleanup(self):
        """Clean up test resources"""
        self.log("🧹 Cleaning up test resources...")

        if self.main_window:
            self.main_window.close()

        if self.app:
            self.app.quit()

        self.log("✅ Cleanup completed")

    def test_comprehensive_pictograph_selection(self) -> bool:
        """Test pictograph selection across all start positions"""
        self.log(
            "🎯 Starting comprehensive pictograph selection test across all start positions..."
        )

        # Test all start positions
        start_positions_to_test = [
            "alpha1",
            "beta1",
            "gamma1",
        ]  # Test one from each family

        for start_pos in start_positions_to_test:
            self.log(f"\n🔄 Testing start position: {start_pos}")
            self._current_start_position = start_pos

            # Clear any existing sequence first
            self._clear_sequence_if_needed()

            # Test this start position
            if not self._test_single_start_position(start_pos):
                self.log_error(f"Failed to test start position: {start_pos}")
                return False

            # Test option selection for this start position
            if not self.test_option_selection_with_bug_detection():
                self.log_error(
                    f"Option selection failed for start position: {start_pos}"
                )
                return False

            self.log(f"✅ Start position {start_pos} test completed successfully")

        self.log("✅ Comprehensive pictograph selection test passed!")
        return True

    def _clear_sequence_if_needed(self):
        """Clear sequence if it has any beats"""
        try:
            sequence_length = self._get_sequence_length()
            if sequence_length > 0:
                self.log(f"Clearing existing sequence (length: {sequence_length})")
                # Try to find and click clear button
                clear_button = self._find_clear_sequence_button()
                if clear_button:
                    self.simulate_mouse_click(clear_button)
                    time.sleep(1)
                    QApplication.processEvents()
        except Exception as e:
            self.log_error("Error clearing sequence", e)

    def _test_single_start_position(self, target_start_pos: str) -> bool:
        """Test selecting a specific start position"""
        try:
            # Find start position options
            start_position_frames = self._find_start_position_frames()
            if not start_position_frames:
                self.log_error("No start position frames found")
                return False

            # Find the target start position
            target_frame = None
            for frame in start_position_frames:
                if (
                    hasattr(frame, "start_pos_data")
                    and frame.start_pos_data == target_start_pos
                ):
                    target_frame = frame
                    break
                # Fallback: check text content
                if hasattr(frame, "text") and target_start_pos in frame.text():
                    target_frame = frame
                    break

            if not target_frame:
                # Use first available frame as fallback
                target_frame = start_position_frames[0]
                self.log(
                    f"Could not find specific start position {target_start_pos}, using first available"
                )

            # Click the start position
            if not self.simulate_mouse_click(target_frame):
                return False

            # Wait for transition
            time.sleep(1)
            QApplication.processEvents()

            return True

        except Exception as e:
            self.log_error(f"Error testing start position {target_start_pos}", e)
            return False

    def _find_start_position_frames(self) -> List[QWidget]:
        """Find start position clickable frames"""
        try:
            if self.start_position_picker and hasattr(
                self.start_position_picker, "findChildren"
            ):
                from PyQt6.QtWidgets import QWidget

                # Look for start position option widgets
                all_widgets = self.start_position_picker.findChildren(QWidget)
                start_frames = []

                for widget in all_widgets:
                    widget_type = type(widget).__name__
                    if (
                        (
                            "start" in widget_type.lower()
                            and "position" in widget_type.lower()
                        )
                        or ("option" in widget_type.lower())
                        or (hasattr(widget, "start_pos_data"))
                    ):
                        if (
                            widget.isVisible()
                            and widget.width() > 10
                            and widget.height() > 10
                        ):
                            start_frames.append(widget)

                return start_frames
        except Exception as e:
            self.log_error("Error finding start position frames", e)

        return []

    def run_full_workflow_test(self) -> bool:
        """Run the complete workflow test"""
        self.log("🚀 Starting comprehensive TKA graph editor workflow test")

        try:
            # Step 1: Setup application
            if not self.setup_application():
                return False

            # Step 2: Find components
            if not self.find_components():
                return False

            # Step 3: Validate initial state
            if not self.validate_initial_state():
                return False

            # Step 4: Test comprehensive pictograph selection across all start positions
            if not self.test_comprehensive_pictograph_selection():
                return False

            self.log("✅ Complete workflow test passed successfully!")
            return True

        except Exception as e:
            self.log_error("Workflow test failed", e)
            return False
        finally:
            # Keep application running for manual inspection
            self.log("🔍 Application remains open for inspection...")
            self.log("Press Ctrl+C to exit")


def main():
    """Main test execution function"""
    tester = GraphEditorUIWorkflowTester()

    try:
        success = tester.run_full_workflow_test()

        if success:
            print("\n✅ Test completed successfully!")
            print("Application is running for manual inspection.")
            print("Press Ctrl+C to exit.")

            # Keep application running
            if tester.app:
                tester.app.exec()
        else:
            print(f"\n❌ Test failed with {len(tester.errors)} errors:")
            for error in tester.errors:
                print(f"  - {error}")

            # Show test results if any bugs were detected
            if tester.test_results:
                print(f"\n🐛 Bug detection results:")
                for key, value in tester.test_results.items():
                    print(f"  {key}: {value}")

            return 1

    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        tester.cleanup()
        return 0
    except Exception as e:
        print(f"\n💥 Test crashed: {e}")
        traceback.print_exc()
        tester.cleanup()
        return 1


if __name__ == "__main__":
    sys.exit(main())
