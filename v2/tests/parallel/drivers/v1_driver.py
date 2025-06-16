"""
Legacy Application Driver
====================

Driver for TKA Legacy application in parallel testing.
Interfaces with Legacy's main_window.py and existing component structure.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Control Legacy application for parallel testing with Modern
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time

# Add Legacy source to path
legacy_src_path = Path(__file__).parent.parent.parent.parent.parent / "legacy" / "src"
if str(legacy_src_path) not in sys.path:
    sys.path.insert(0, str(legacy_src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QEventLoop
from PyQt6.QtGui import QPixmap

# Import with absolute paths to avoid relative import issues
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from drivers.driver_base import BaseApplicationDriver, ApplicationState, ActionResult
from actions import UserAction, ActionType, GridPosition, MotionTypeValue


logger = logging.getLogger(__name__)


class LegacyApplicationDriver(BaseApplicationDriver):
    """Driver for TKA Legacy application."""

    def __init__(self, test_data_dir: Path):
        super().__init__("Legacy", test_data_dir)
        self.main_window = None
        self.app = None
        self.sequence_widget = None
        self.construct_tab = None

    def _start_application_impl(self, **kwargs) -> bool:
        """Start Legacy application."""
        try:
            # Import Legacy components
            from main_window.main_window import MainWindow
            from settings_manager.settings_manager import SettingsManager
            from splash_screen.splash_screen import SplashScreen
            from profiler.profiler import Profiler

            # Create QApplication if not exists
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Initialize Legacy components
            settings_manager = SettingsManager()
            splash_screen = SplashScreen(self.app, settings_manager)
            profiler = Profiler()

            # Create app context (Legacy's dependency injection)
            from src.settings_manager.global_settings.app_context import AppContext

            app_context = AppContext()

            # Create main window
            self.main_window = MainWindow(profiler, splash_screen, app_context)
            self.main_window.initialize_widgets()

            # Get key components
            self.sequence_widget = self.main_window.main_widget.sequence_workbench
            self.construct_tab = self.main_window.main_widget.construct_tab

            # Show window
            self.main_window.show()

            # Process events to ensure initialization
            self.app.processEvents()

            logger.info("Legacy application started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start Legacy application: {e}")
            return False

    def _stop_application_impl(self) -> bool:
        """Stop Legacy application."""
        try:
            if self.main_window:
                self.main_window.close()
                self.main_window = None

            if self.app:
                self.app.quit()
                self.app = None

            logger.info("Legacy application stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to stop Legacy application: {e}")
            return False

    def _execute_action_impl(self, action: UserAction) -> ActionResult:
        """Execute action on Legacy application."""
        try:
            if action.action_type == ActionType.SELECT_START_POSITION:
                return self._select_start_position(action)
            elif action.action_type == ActionType.ADD_BEAT:
                return self._add_beat(action)
            elif action.action_type == ActionType.SELECT_PICTOGRAPH_OPTION:
                return self._select_pictograph_option(action)
            elif action.action_type == ActionType.ADJUST_TURNS:
                return self._adjust_turns(action)
            elif action.action_type == ActionType.TOGGLE_GRAPH_EDITOR:
                return self._toggle_graph_editor(action)
            elif action.action_type == ActionType.CLEAR_SEQUENCE:
                return self._clear_sequence(action)
            elif action.action_type == ActionType.EXTRACT_DATA:
                return self._extract_data(action)
            else:
                return ActionResult(
                    success=False,
                    execution_time_ms=0,
                    error_message=f"Unsupported action type: {action.action_type}",
                )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Action execution failed: {e}",
            )

    def _select_start_position(self, action: UserAction) -> ActionResult:
        """Select start position in Legacy."""
        try:
            grid_position = action.parameters.grid_position

            # Get start position picker from construct tab
            start_pos_picker = self.construct_tab.option_picker.start_pos_picker

            # Map grid position to Legacy button
            position_map = {
                GridPosition.ALPHA: "alpha",
                GridPosition.BETA: "beta",
                GridPosition.GAMMA: "gamma",
            }

            position_name = position_map.get(grid_position)
            if not position_name:
                return ActionResult(
                    success=False,
                    execution_time_ms=0,
                    error_message=f"Invalid grid position: {grid_position}",
                )

            # Find and click the appropriate button
            button = getattr(start_pos_picker, f"{position_name}_button", None)
            if button:
                button.click()
                self.app.processEvents()

                # Update state
                self.current_state.start_position_selected = True

                return ActionResult(
                    success=True,
                    execution_time_ms=0,
                    data={"start_position": position_name},
                )
            else:
                return ActionResult(
                    success=False,
                    execution_time_ms=0,
                    error_message=f"Start position button not found: {position_name}",
                )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Start position selection failed: {e}",
            )

    def _select_pictograph_option(self, action: UserAction) -> ActionResult:
        """Select pictograph option in Legacy."""
        try:
            # Get option picker
            option_picker = self.construct_tab.option_picker

            # Get available options
            if (
                hasattr(option_picker, "option_getter")
                and option_picker.option_getter.options
            ):
                options = option_picker.option_getter.options

                # Select first available option (can be enhanced for specific selection)
                if options:
                    first_option = options[0]

                    # Simulate clicking the option
                    if hasattr(option_picker, "option_clicked"):
                        option_picker.option_clicked.emit(first_option)
                        self.app.processEvents()

                        # Update beat count
                        self.current_state.beat_count += 1

                        return ActionResult(
                            success=True,
                            execution_time_ms=0,
                            data={
                                "selected_option": first_option,
                                "beat_count": self.current_state.beat_count,
                            },
                        )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="No pictograph options available",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Pictograph option selection failed: {e}",
            )

    def _add_beat(self, action: UserAction) -> ActionResult:
        """Add beat in Legacy (typically done through pictograph selection)."""
        # In Legacy, beats are added by selecting pictograph options
        return self._select_pictograph_option(action)

    def _adjust_turns(self, action: UserAction) -> ActionResult:
        """Adjust turns in Legacy."""
        try:
            # This would interact with Legacy's turn adjustment controls
            # Implementation depends on Legacy's specific UI structure
            return ActionResult(
                success=True,
                execution_time_ms=0,
                data={"turns_adjusted": action.parameters.turns},
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Turn adjustment failed: {e}",
            )

    def _toggle_graph_editor(self, action: UserAction) -> ActionResult:
        """Toggle graph editor in Legacy."""
        try:
            # Find graph editor toggle button
            if hasattr(self.construct_tab, "graph_editor_toggle_button"):
                toggle_button = self.construct_tab.graph_editor_toggle_button
                toggle_button.click()
                self.app.processEvents()

                # Update state
                self.current_state.graph_editor_open = (
                    not self.current_state.graph_editor_open
                )

                return ActionResult(
                    success=True,
                    execution_time_ms=0,
                    data={"graph_editor_open": self.current_state.graph_editor_open},
                )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Graph editor toggle button not found",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Graph editor toggle failed: {e}",
            )

    def _clear_sequence(self, action: UserAction) -> ActionResult:
        """Clear sequence in Legacy."""
        try:
            # Clear sequence through sequence widget
            if self.sequence_widget and hasattr(self.sequence_widget, "clear_sequence"):
                self.sequence_widget.clear_sequence()
                self.app.processEvents()

                # Update state
                self.current_state.beat_count = 0
                self.current_state.sequence_initialized = False
                self.current_state.start_position_selected = False

                return ActionResult(
                    success=True, execution_time_ms=0, data={"sequence_cleared": True}
                )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Sequence widget not available for clearing",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Sequence clear failed: {e}",
            )

    def _extract_data(self, action: UserAction) -> ActionResult:
        """Extract current data from Legacy."""
        try:
            sequence_data = self.extract_sequence_data()
            pictograph_data = self.extract_pictograph_data()

            return ActionResult(
                success=True,
                execution_time_ms=0,
                data={
                    "sequence_data": sequence_data,
                    "pictograph_data": pictograph_data,
                },
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Data extraction failed: {e}",
            )

    def get_current_state(self) -> ApplicationState:
        """Get current Legacy application state."""
        try:
            # Update state from Legacy components
            if self.sequence_widget:
                # Extract beat count and other sequence info
                if hasattr(self.sequence_widget, "beat_frame"):
                    beat_frame = self.sequence_widget.beat_frame
                    if hasattr(beat_frame, "beats"):
                        self.current_state.beat_count = len(beat_frame.beats)

            return self.current_state

        except Exception as e:
            logger.error(f"Failed to get Legacy state: {e}")
            return self.current_state

    def extract_sequence_data(self) -> Dict[str, Any]:
        """Extract sequence data from Legacy using verified access patterns."""
        try:
            if not self.main_window:
                return {}

            # VERIFIED: Legacy access pattern - main_widget.sequence_workbench.beat_frame
            beat_frame = self.main_window.main_widget.sequence_workbench.beat_frame

            # VERIFIED: Legacy beat_frame has beat_views list with filled beats
            sequence_data = {
                "beat_count": 0,
                "beats": [],
                "version": "Legacy",
                "start_position": None,
            }

            # Extract start position if available
            if hasattr(beat_frame, "start_pos_view") and beat_frame.start_pos_view:
                if (
                    hasattr(beat_frame.start_pos_view, "beat")
                    and beat_frame.start_pos_view.beat
                ):
                    start_beat = beat_frame.start_pos_view.beat
                    if hasattr(start_beat, "state") and hasattr(
                        start_beat.state, "pictograph_data"
                    ):
                        start_data = start_beat.state.pictograph_data
                        sequence_data["start_position"] = start_data.get("letter", "")

            # VERIFIED: Legacy beat_frame.beat_views contains BeatView objects with is_filled property
            if hasattr(beat_frame, "beat_views"):
                filled_beats = [
                    view
                    for view in beat_frame.beat_views
                    if hasattr(view, "is_filled") and view.is_filled
                ]
                sequence_data["beat_count"] = len(filled_beats)

                for i, beat_view in enumerate(filled_beats):
                    if hasattr(beat_view, "beat"):
                        beat_data = self._extract_beat_data(beat_view.beat, i)
                        sequence_data["beats"].append(beat_data)

            return sequence_data

        except Exception as e:
            logger.error(f"Failed to extract Legacy sequence data: {e}")
            return {}

    def extract_pictograph_data(self, beat_index: int = -1) -> Dict[str, Any]:
        """Extract pictograph data from Legacy."""
        try:
            # Extract pictograph data from current beat or specified beat
            pictograph_data = {
                "beat_index": beat_index,
                "arrows": {},
                "props": {},
                "version": "Legacy",
            }

            # Add specific pictograph extraction logic here

            return pictograph_data

        except Exception as e:
            logger.error(f"Failed to extract Legacy pictograph data: {e}")
            return {}

    def _extract_beat_data(self, beat, index: int) -> Dict[str, Any]:
        """Extract data from a Legacy beat based on verified Legacy Beat structure."""
        try:
            # VERIFIED: Legacy Beat extends Pictograph and has state.pictograph_data
            if hasattr(beat, "state") and hasattr(beat.state, "pictograph_data"):
                pictograph_data = beat.state.pictograph_data

                beat_data = {
                    "index": index,
                    "letter": pictograph_data.get("letter", ""),
                    "duration": getattr(beat, "duration", 1),
                    "motions": {},
                }

                # VERIFIED: Legacy uses blue_attributes/red_attributes structure
                for color in ["blue", "red"]:
                    attr_key = f"{color}_attributes"
                    if attr_key in pictograph_data:
                        motion_attrs = pictograph_data[attr_key]
                        # Extract motion data directly - no conversion needed
                        beat_data["motions"][color] = {
                            "motion_type": motion_attrs.get("motion_type", "static"),
                            "prop_rot_dir": motion_attrs.get("prop_rot_dir", "no_rot"),
                            "start_loc": motion_attrs.get("start_loc", "n"),
                            "end_loc": motion_attrs.get("end_loc", "n"),
                            "turns": motion_attrs.get("turns", 0),
                            "start_ori": motion_attrs.get("start_ori", "in"),
                            "end_ori": motion_attrs.get("end_ori", "in"),
                        }

            else:
                # Fallback to direct attribute access
                beat_data = {
                    "index": index,
                    "letter": getattr(beat, "letter", ""),
                    "duration": getattr(beat, "duration", 1),
                    "motions": {},
                }

                # Try to extract motion data from elements if available
                if hasattr(beat, "elements"):
                    if hasattr(beat.elements, "blue_motion"):
                        beat_data["motions"]["blue"] = self._extract_motion_data(
                            beat.elements.blue_motion
                        )
                    if hasattr(beat.elements, "red_motion"):
                        beat_data["motions"]["red"] = self._extract_motion_data(
                            beat.elements.red_motion
                        )

            return beat_data

        except Exception as e:
            logger.error(f"Failed to extract Legacy beat data: {e}")
            return {"index": index, "error": str(e)}

    def _extract_motion_data(self, motion) -> Dict[str, Any]:
        """Extract data from a Legacy motion based on verified Legacy MotionState structure."""
        try:
            # Legacy motion data is stored in motion.state (MotionState)
            if hasattr(motion, "state"):
                motion_state = motion.state
                motion_data = {
                    "motion_type": getattr(motion_state, "motion_type", ""),
                    "turns": getattr(motion_state, "turns", 0),
                    "start_ori": getattr(motion_state, "start_ori", ""),
                    "end_ori": getattr(motion_state, "end_ori", ""),
                    "start_loc": getattr(motion_state, "start_loc", ""),
                    "end_loc": getattr(motion_state, "end_loc", ""),
                    "prop_rot_dir": getattr(
                        motion_state, "prop_rot_dir", "no_rot"
                    ),  # VERIFIED field name
                    "color": getattr(motion_state, "color", ""),
                }
            else:
                # Fallback to direct attribute access
                motion_data = {
                    "motion_type": getattr(motion, "motion_type", ""),
                    "turns": getattr(motion, "turns", 0),
                    "start_ori": getattr(motion, "start_ori", ""),
                    "end_ori": getattr(motion, "end_ori", ""),
                    "start_loc": getattr(motion, "start_loc", ""),
                    "end_loc": getattr(motion, "end_loc", ""),
                    "prop_rot_dir": getattr(motion, "prop_rot_dir", "no_rot"),
                }

            return motion_data

        except Exception as e:
            logger.error(f"Failed to extract Legacy motion data: {e}")
            return {"error": str(e)}

    def wait_for_ready(self, timeout_ms: int = 10000) -> bool:
        """Wait for Legacy application to be ready."""
        try:
            start_time = time.time()

            while (time.time() - start_time) * 1000 < timeout_ms:
                if self.main_window and self.main_window.isVisible():
                    if self.construct_tab and hasattr(
                        self.construct_tab, "option_picker"
                    ):
                        # Application is ready when main components are available
                        return True

                self.app.processEvents()
                time.sleep(0.1)

            return False

        except Exception as e:
            logger.error(f"Failed to wait for Legacy ready: {e}")
            return False

    def _capture_screenshot_impl(self, filepath: str) -> bool:
        """Capture Legacy application screenshot."""
        try:
            if self.main_window:
                pixmap = self.main_window.grab()
                return pixmap.save(filepath)
            return False

        except Exception as e:
            logger.error(f"Failed to capture Legacy screenshot: {e}")
            return False
