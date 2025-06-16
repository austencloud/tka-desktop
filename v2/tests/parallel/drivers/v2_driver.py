"""
V2 Application Driver
====================

Driver for TKA V2 application in parallel testing.
Interfaces with V2's consolidated service architecture and main_widget.py.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Control V2 application for parallel testing with Legacy
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time

# Add V2 source to path
v2_src_path = Path(__file__).parent.parent.parent / "src"
if str(v2_src_path) not in sys.path:
    sys.path.insert(0, str(v2_src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QEventLoop
from PyQt6.QtGui import QPixmap

from .driver_base import BaseApplicationDriver, ApplicationState, ActionResult
from ..actions import UserAction, ActionType, GridPosition, MotionTypeValue


logger = logging.getLogger(__name__)


class V2ApplicationDriver(BaseApplicationDriver):
    """Driver for TKA V2 application."""

    def __init__(self, test_data_dir: Path):
        super().__init__("V2", test_data_dir)
        self.main_window = None
        self.app = None
        self.container = None
        self.sequence_service = None
        self.pictograph_service = None
        self.ui_state_service = None

    def _start_application_impl(self, **kwargs) -> bool:
        """Start V2 application."""
        try:
            # Import V2 components
            from main import KineticConstructorV2
            from infrastructure.dependency_injection.container import get_container

            # Create QApplication if not exists
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()

            # Get dependency injection container
            self.container = get_container()

            # Create main window
            self.main_window = KineticConstructorV2()

            # Get services from container
            self._initialize_services()

            # Show window
            self.main_window.show()

            # Process events to ensure initialization
            self.app.processEvents()

            logger.info("V2 application started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start V2 application: {e}")
            return False

    def _initialize_services(self):
        """Initialize V2 services from container."""
        try:
            from application.services import (
                SequenceManagementService,
                PictographManagementService,
                UIStateManagementService,
            )

            self.sequence_service = self.container.resolve(SequenceManagementService)
            self.pictograph_service = self.container.resolve(
                PictographManagementService
            )
            self.ui_state_service = self.container.resolve(UIStateManagementService)

            logger.debug("V2 services initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize V2 services: {e}")

    def _stop_application_impl(self) -> bool:
        """Stop V2 application."""
        try:
            if self.main_window:
                self.main_window.close()
                self.main_window = None

            if self.app:
                self.app.quit()
                self.app = None

            logger.info("V2 application stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to stop V2 application: {e}")
            return False

    def _execute_action_impl(self, action: UserAction) -> ActionResult:
        """Execute action on V2 application."""
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
        """Select start position in V2."""
        try:
            grid_position = action.parameters.grid_position

            # Map grid position to V2 format
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

            # Use V2 service to set start position
            if self.sequence_service:
                success = self.sequence_service.set_start_position(position_name)

                if success:
                    self.current_state.start_position_selected = True

                    return ActionResult(
                        success=True,
                        execution_time_ms=0,
                        data={"start_position": position_name},
                    )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Failed to set start position in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Start position selection failed: {e}",
            )

    def _select_pictograph_option(self, action: UserAction) -> ActionResult:
        """Select pictograph option in V2."""
        try:
            # Use V2 pictograph service to get and select options
            if self.pictograph_service:
                # Get available options
                options = self.pictograph_service.get_available_options()

                if options:
                    # Select first option (can be enhanced for specific selection)
                    selected_option = options[0]
                    success = self.pictograph_service.select_option(selected_option)

                    if success:
                        self.current_state.beat_count += 1

                        return ActionResult(
                            success=True,
                            execution_time_ms=0,
                            data={
                                "selected_option": selected_option,
                                "beat_count": self.current_state.beat_count,
                            },
                        )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="No pictograph options available in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Pictograph option selection failed: {e}",
            )

    def _add_beat(self, action: UserAction) -> ActionResult:
        """Add beat in V2."""
        try:
            if self.sequence_service:
                success = self.sequence_service.add_beat()

                if success:
                    self.current_state.beat_count += 1

                    return ActionResult(
                        success=True,
                        execution_time_ms=0,
                        data={
                            "beat_added": True,
                            "beat_count": self.current_state.beat_count,
                        },
                    )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Failed to add beat in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Beat addition failed: {e}",
            )

    def _adjust_turns(self, action: UserAction) -> ActionResult:
        """Adjust turns in V2."""
        try:
            turns = action.parameters.turns
            beat_index = action.parameters.beat_index or -1  # Default to last beat

            if self.sequence_service:
                success = self.sequence_service.adjust_turns(beat_index, turns)

                if success:
                    return ActionResult(
                        success=True,
                        execution_time_ms=0,
                        data={"turns_adjusted": turns, "beat_index": beat_index},
                    )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Failed to adjust turns in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Turn adjustment failed: {e}",
            )

    def _toggle_graph_editor(self, action: UserAction) -> ActionResult:
        """Toggle graph editor in V2."""
        try:
            if self.ui_state_service:
                success = self.ui_state_service.toggle_graph_editor()

                if success:
                    self.current_state.graph_editor_open = (
                        not self.current_state.graph_editor_open
                    )

                    return ActionResult(
                        success=True,
                        execution_time_ms=0,
                        data={
                            "graph_editor_open": self.current_state.graph_editor_open
                        },
                    )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Failed to toggle graph editor in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Graph editor toggle failed: {e}",
            )

    def _clear_sequence(self, action: UserAction) -> ActionResult:
        """Clear sequence in V2."""
        try:
            if self.sequence_service:
                success = self.sequence_service.clear_sequence()

                if success:
                    self.current_state.beat_count = 0
                    self.current_state.sequence_initialized = False
                    self.current_state.start_position_selected = False

                    return ActionResult(
                        success=True,
                        execution_time_ms=0,
                        data={"sequence_cleared": True},
                    )

            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message="Failed to clear sequence in V2",
            )

        except Exception as e:
            return ActionResult(
                success=False,
                execution_time_ms=0,
                error_message=f"Sequence clear failed: {e}",
            )

    def _extract_data(self, action: UserAction) -> ActionResult:
        """Extract current data from V2."""
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
        """Get current V2 application state."""
        try:
            # Update state from V2 services
            if self.sequence_service:
                sequence_data = self.sequence_service.get_current_sequence()
                if sequence_data:
                    self.current_state.beat_count = len(sequence_data.get("beats", []))
                    self.current_state.sequence_initialized = True

            if self.ui_state_service:
                ui_state = self.ui_state_service.get_current_state()
                if ui_state:
                    self.current_state.graph_editor_open = ui_state.get(
                        "graph_editor_open", False
                    )

            return self.current_state

        except Exception as e:
            logger.error(f"Failed to get V2 state: {e}")
            return self.current_state

    def extract_sequence_data(self) -> Dict[str, Any]:
        """Extract sequence data from V2."""
        try:
            if not self.sequence_service:
                return {}

            # Extract sequence data from V2 service
            sequence_data = self.sequence_service.get_current_sequence()

            if sequence_data:
                # Convert V2 sequence data to standardized format
                standardized_data = {
                    "beat_count": len(sequence_data.get("beats", [])),
                    "beats": [],
                    "version": "V2",
                    "start_position": sequence_data.get("start_position"),
                    "word": sequence_data.get("word", ""),
                }

                # Convert beats to standardized format
                for i, beat in enumerate(sequence_data.get("beats", [])):
                    beat_data = self._extract_v2_beat_data(beat, i)
                    standardized_data["beats"].append(beat_data)

                return standardized_data

            return {"beat_count": 0, "beats": [], "version": "V2"}

        except Exception as e:
            logger.error(f"Failed to extract V2 sequence data: {e}")
            return {}

    def extract_pictograph_data(self, beat_index: int = -1) -> Dict[str, Any]:
        """Extract pictograph data from V2."""
        try:
            if not self.pictograph_service:
                return {}

            # Extract pictograph data from V2 service
            pictograph_data = self.pictograph_service.get_pictograph_data(beat_index)

            if pictograph_data:
                # Convert V2 pictograph data to standardized format
                standardized_data = {
                    "beat_index": beat_index,
                    "arrows": {},
                    "props": {},
                    "version": "V2",
                    "grid_data": pictograph_data.get("grid_data", {}),
                    "letter": pictograph_data.get("letter", ""),
                }

                # Extract arrow data
                arrows = pictograph_data.get("arrows", {})
                for color, arrow_data in arrows.items():
                    standardized_data["arrows"][color] = self._extract_v2_arrow_data(
                        arrow_data
                    )

                # Extract prop data
                props = pictograph_data.get("props", {})
                for color, prop_data in props.items():
                    standardized_data["props"][color] = self._extract_v2_prop_data(
                        prop_data
                    )

                return standardized_data

            return {
                "beat_index": beat_index,
                "arrows": {},
                "props": {},
                "version": "V2",
            }

        except Exception as e:
            logger.error(f"Failed to extract V2 pictograph data: {e}")
            return {}

    def _extract_v2_beat_data(self, beat, index: int) -> Dict[str, Any]:
        """Extract data from a V2 beat based on verified V2 BeatData structure."""
        try:
            # VERIFIED: V2 uses BeatData with blue_motion/red_motion MotionData objects
            beat_data = {
                "index": index,
                "letter": beat.get("letter", ""),
                "duration": beat.get("duration", 1),
                "motions": {},
            }

            # VERIFIED: V2 BeatData has blue_motion/red_motion MotionData objects
            blue_motion = beat.get("blue_motion")
            if blue_motion:
                beat_data["motions"]["blue"] = self._extract_v2_motion_data(blue_motion)

            red_motion = beat.get("red_motion")
            if red_motion:
                beat_data["motions"]["red"] = self._extract_v2_motion_data(red_motion)

            return beat_data

        except Exception as e:
            logger.error(f"Failed to extract V2 beat data: {e}")
            return {"index": index, "error": str(e)}

    def _extract_v2_motion_data(self, motion) -> Dict[str, Any]:
        """Extract data from a V2 motion."""
        try:
            # VERIFIED: V2 MotionData has to_dict() method that returns enum values as strings
            if hasattr(motion, "to_dict"):
                return motion.to_dict()
            elif isinstance(motion, dict):
                # Already in dict format, extract enum values if needed
                motion_data = {}
                for key, value in motion.items():
                    if hasattr(value, "value"):  # Enum object
                        motion_data[key] = value.value
                    else:
                        motion_data[key] = value
                # Ensure prop_rot_dir is included
                if "prop_rot_dir" not in motion_data:
                    motion_data["prop_rot_dir"] = motion.get("prop_rot_dir", "no_rot")
                return motion_data
            else:
                # Fallback for unexpected format
                motion_data = {
                    "motion_type": getattr(motion, "motion_type", "static"),
                    "prop_rot_dir": getattr(motion, "prop_rot_dir", "no_rot"),
                    "turns": getattr(motion, "turns", 0),
                    "start_ori": getattr(motion, "start_ori", "in"),
                    "end_ori": getattr(motion, "end_ori", "in"),
                    "start_loc": getattr(motion, "start_loc", "n"),
                    "end_loc": getattr(motion, "end_loc", "n"),
                }
                return motion_data

        except Exception as e:
            logger.error(f"Failed to extract V2 motion data: {e}")
            return {"error": str(e)}

    def _extract_v2_arrow_data(self, arrow_data) -> Dict[str, Any]:
        """Extract data from a V2 arrow."""
        try:
            return {
                "position_x": arrow_data.get("position_x", 0),
                "position_y": arrow_data.get("position_y", 0),
                "rotation_angle": arrow_data.get("rotation_angle", 0),
                "color": arrow_data.get("color", ""),
                "is_mirrored": arrow_data.get("is_mirrored", False),
                "motion_data": arrow_data.get("motion_data", {}),
            }

        except Exception as e:
            logger.error(f"Failed to extract V2 arrow data: {e}")
            return {"error": str(e)}

    def _extract_v2_prop_data(self, prop_data) -> Dict[str, Any]:
        """Extract data from a V2 prop."""
        try:
            return {
                "position_x": prop_data.get("position_x", 0),
                "position_y": prop_data.get("position_y", 0),
                "rotation_angle": prop_data.get("rotation_angle", 0),
                "color": prop_data.get("color", ""),
                "prop_type": prop_data.get("prop_type", ""),
                "motion_data": prop_data.get("motion_data", {}),
            }

        except Exception as e:
            logger.error(f"Failed to extract V2 prop data: {e}")
            return {"error": str(e)}

    def wait_for_ready(self, timeout_ms: int = 10000) -> bool:
        """Wait for V2 application to be ready."""
        try:
            start_time = time.time()

            while (time.time() - start_time) * 1000 < timeout_ms:
                if self.main_window and self.main_window.isVisible():
                    if self.container and self.sequence_service:
                        # Application is ready when services are available
                        return True

                self.app.processEvents()
                time.sleep(0.1)

            return False

        except Exception as e:
            logger.error(f"Failed to wait for V2 ready: {e}")
            return False

    def _capture_screenshot_impl(self, filepath: str) -> bool:
        """Capture V2 application screenshot."""
        try:
            if self.main_window:
                pixmap = self.main_window.grab()
                return pixmap.save(filepath)
            return False

        except Exception as e:
            logger.error(f"Failed to capture V2 screenshot: {e}")
            return False
