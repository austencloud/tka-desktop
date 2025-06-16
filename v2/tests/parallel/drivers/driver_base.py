"""
Base Driver Interface
====================

Common interface and utilities for Legacy and Modern application drivers.
Provides standardized methods for application control and data extraction.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Common interface for Legacy/Modern application drivers in parallel testing
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
import logging
import time
from pathlib import Path

# Import actions with absolute path to avoid relative import issues
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from actions import UserAction, ActionType, ValidationResult


logger = logging.getLogger(__name__)


@dataclass
class ApplicationState:
    """Standardized application state representation."""

    # Application status
    is_running: bool = False
    is_ready: bool = False
    initialization_complete: bool = False

    # Sequence state
    sequence_initialized: bool = False
    start_position_selected: bool = False
    beat_count: int = 0
    current_beat_index: int = -1

    # UI state
    graph_editor_open: bool = False
    current_tab: str = "construct"
    window_size: Tuple[int, int] = (1200, 800)

    # Data state
    sequence_data: Dict[str, Any] = None
    pictograph_data: Dict[str, Any] = None

    # Error state
    last_error: Optional[str] = None
    error_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for comparison."""
        return {
            "is_running": self.is_running,
            "is_ready": self.is_ready,
            "initialization_complete": self.initialization_complete,
            "sequence_initialized": self.sequence_initialized,
            "start_position_selected": self.start_position_selected,
            "beat_count": self.beat_count,
            "current_beat_index": self.current_beat_index,
            "graph_editor_open": self.graph_editor_open,
            "current_tab": self.current_tab,
            "window_size": self.window_size,
            "sequence_data": self.sequence_data,
            "pictograph_data": self.pictograph_data,
            "last_error": self.last_error,
            "error_count": self.error_count,
        }


@dataclass
class ActionResult:
    """Result of executing an action on an application."""

    # Execution status
    success: bool
    execution_time_ms: float
    error_message: Optional[str] = None

    # State changes
    state_before: Optional[ApplicationState] = None
    state_after: Optional[ApplicationState] = None

    # Data results
    data: Dict[str, Any] = None
    screenshots: List[str] = None

    # Validation results
    validation_result: Optional[ValidationResult] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for comparison."""
        return {
            "success": self.success,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
            "state_before": self.state_before.to_dict() if self.state_before else None,
            "state_after": self.state_after.to_dict() if self.state_after else None,
            "data": self.data,
            "screenshots": self.screenshots,
            "validation_result": (
                {
                    "is_valid": self.validation_result.is_valid,
                    "errors": self.validation_result.errors,
                    "warnings": self.validation_result.warnings,
                }
                if self.validation_result
                else None
            ),
        }


class IApplicationDriver(ABC):
    """Interface for application drivers."""

    @abstractmethod
    def start_application(self, **kwargs) -> bool:
        """Start the application in test mode."""
        pass

    @abstractmethod
    def stop_application(self) -> bool:
        """Stop the application and cleanup."""
        pass

    @abstractmethod
    def execute_action(self, action: UserAction) -> ActionResult:
        """Execute a user action and return the result."""
        pass

    @abstractmethod
    def get_current_state(self) -> ApplicationState:
        """Get current application state."""
        pass

    @abstractmethod
    def extract_sequence_data(self) -> Dict[str, Any]:
        """Extract current sequence data."""
        pass

    @abstractmethod
    def extract_pictograph_data(self, beat_index: int = -1) -> Dict[str, Any]:
        """Extract pictograph data for specified beat."""
        pass

    @abstractmethod
    def capture_screenshot(self, filename: Optional[str] = None) -> str:
        """Capture application screenshot."""
        pass

    @abstractmethod
    def wait_for_ready(self, timeout_ms: int = 10000) -> bool:
        """Wait for application to be ready."""
        pass


class BaseApplicationDriver(IApplicationDriver):
    """Base implementation with common functionality."""

    def __init__(self, version: str, test_data_dir: Path):
        self.version = version
        self.test_data_dir = test_data_dir
        self.application = None
        self.current_state = ApplicationState()
        self.action_history: List[Tuple[UserAction, ActionResult]] = []

        # Create test data directory
        self.test_data_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir = self.test_data_dir / "screenshots" / version
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def start_application(self, **kwargs) -> bool:
        """Base application startup logic."""
        try:
            logger.info(f"Starting {self.version} application...")

            # Version-specific startup will be implemented in subclasses
            success = self._start_application_impl(**kwargs)

            if success:
                self.current_state.is_running = True
                logger.info(f"{self.version} application started successfully")

                # Wait for application to be ready
                if self.wait_for_ready():
                    self.current_state.is_ready = True
                    logger.info(f"{self.version} application ready")
                else:
                    logger.warning(f"{self.version} application started but not ready")

            return success

        except Exception as e:
            logger.error(f"Failed to start {self.version} application: {e}")
            self.current_state.last_error = str(e)
            self.current_state.error_count += 1
            return False

    def stop_application(self) -> bool:
        """Base application shutdown logic."""
        try:
            logger.info(f"Stopping {self.version} application...")

            success = self._stop_application_impl()

            if success:
                self.current_state.is_running = False
                self.current_state.is_ready = False
                logger.info(f"{self.version} application stopped successfully")

            return success

        except Exception as e:
            logger.error(f"Failed to stop {self.version} application: {e}")
            self.current_state.last_error = str(e)
            self.current_state.error_count += 1
            return False

    def execute_action(self, action: UserAction) -> ActionResult:
        """Base action execution with timing and state capture."""
        start_time = time.time()
        state_before = self.get_current_state()

        try:
            logger.debug(f"Executing action: {action.action_type.name}")

            # Execute version-specific action implementation
            result = self._execute_action_impl(action)

            # Capture state after execution
            state_after = self.get_current_state()
            result.state_before = state_before
            result.state_after = state_after

            # Calculate execution time
            result.execution_time_ms = (time.time() - start_time) * 1000

            # Store in history
            self.action_history.append((action, result))

            logger.debug(
                f"Action completed: {action.action_type.name} - Success: {result.success}"
            )

            return result

        except Exception as e:
            logger.error(f"Action execution failed: {action.action_type.name} - {e}")

            # Create error result
            result = ActionResult(
                success=False,
                execution_time_ms=(time.time() - start_time) * 1000,
                error_message=str(e),
                state_before=state_before,
                state_after=self.get_current_state(),
            )

            self.action_history.append((action, result))
            return result

    def capture_screenshot(self, filename: Optional[str] = None) -> str:
        """Base screenshot capture."""
        if not filename:
            timestamp = int(time.time() * 1000)
            filename = f"{self.version}_screenshot_{timestamp}.png"

        screenshot_path = self.screenshots_dir / filename

        try:
            # Version-specific screenshot implementation
            success = self._capture_screenshot_impl(str(screenshot_path))

            if success:
                logger.debug(f"Screenshot captured: {screenshot_path}")
                return str(screenshot_path)
            else:
                logger.warning(f"Failed to capture screenshot: {screenshot_path}")
                return ""

        except Exception as e:
            logger.error(f"Screenshot capture error: {e}")
            return ""

    def get_action_history(self) -> List[Tuple[UserAction, ActionResult]]:
        """Get complete action execution history."""
        return self.action_history.copy()

    def clear_action_history(self) -> None:
        """Clear action execution history."""
        self.action_history.clear()

    # Abstract methods to be implemented by subclasses
    @abstractmethod
    def _start_application_impl(self, **kwargs) -> bool:
        """Version-specific application startup."""
        pass

    @abstractmethod
    def _stop_application_impl(self) -> bool:
        """Version-specific application shutdown."""
        pass

    @abstractmethod
    def _execute_action_impl(self, action: UserAction) -> ActionResult:
        """Version-specific action execution."""
        pass

    @abstractmethod
    def _capture_screenshot_impl(self, filepath: str) -> bool:
        """Version-specific screenshot capture."""
        pass
