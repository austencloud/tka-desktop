"""
Master Test Orchestrator
========================

Main coordination logic for TKA Legacy/Modern parallel testing.
Executes synchronized actions across both versions and manages test lifecycle.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Orchestrate parallel testing between Legacy and Modern for functional equivalence validation
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from .drivers import (
    LegacyApplicationDriver,
    ModernApplicationDriver,
    ApplicationState,
    ActionResult,
)
from .actions import (
    UserAction,
    ActionSequence,
    ActionValidatorFactory,
    ValidationResult,
)
from .comparison import ResultComparer, ComparisonResult, TKADataNormalizer
from .scenarios.basic_workflows import BasicWorkflowScenarios


logger = logging.getLogger(__name__)


@dataclass
class TestExecutionResult:
    """Result of executing a test scenario."""

    # Test identity
    test_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_name: str = ""
    execution_time: datetime = field(default_factory=datetime.now)

    # Execution results
    success: bool = False
    total_actions: int = 0
    successful_actions: int = 0
    failed_actions: int = 0

    # Legacy/Modern results
    legacy_results: List[ActionResult] = field(default_factory=list)
    modern_results: List[ActionResult] = field(default_factory=list)

    # Comparison results
    comparison_results: List[ComparisonResult] = field(default_factory=list)
    equivalence_score: float = 0.0

    # Error information
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Performance metrics
    total_execution_time_ms: float = 0.0
    average_action_time_ms: float = 0.0


@dataclass
class TestConfiguration:
    """Configuration for parallel testing."""

    # Test environment
    test_data_dir: Path = Path("test_data")
    enable_screenshots: bool = True
    screenshot_on_failure: bool = True

    # Timing configuration
    action_timeout_ms: int = 10000
    synchronization_timeout_ms: int = 5000
    application_startup_timeout_ms: int = 30000

    # Comparison configuration
    position_tolerance: float = 2.0  # pixels
    rotation_tolerance: float = 0.5  # degrees
    turn_tolerance: float = 0.001  # turn precision

    # Test execution
    stop_on_first_failure: bool = False
    max_retries: int = 3
    retry_delay_ms: int = 1000

    # Debugging
    verbose_logging: bool = True
    save_debug_snapshots: bool = True
    debug_snapshot_dir: Path = Path("debug_snapshots")


class ParallelTestOrchestrator:
    """
    Master orchestrator for TKA Legacy/Modern parallel testing.

    Coordinates execution of identical actions across both versions,
    compares results, and provides comprehensive reporting.
    """

    def __init__(self, config: TestConfiguration):
        self.config = config
        self.test_results: List[TestExecutionResult] = []

        # Initialize components
        self.legacy_driver = LegacyApplicationDriver(config.test_data_dir / "legacy")
        self.modern_driver = ModernApplicationDriver(config.test_data_dir / "modern")
        self.result_comparer = ResultComparer()
        self.data_normalizer = TKADataNormalizer()
        self.scenario_provider = BasicWorkflowScenarios()

        # Test state
        self.is_running = False
        self.current_test_id = None

        # Setup directories
        self._setup_test_environment()

    def _setup_test_environment(self):
        """Setup test environment directories."""
        self.config.test_data_dir.mkdir(parents=True, exist_ok=True)
        self.config.debug_snapshot_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        if self.config.verbose_logging:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )

    async def start_applications(self) -> bool:
        """Start both Legacy and Modern applications."""
        logger.info(
            "Starting TKA Legacy and Modern applications for parallel testing..."
        )

        try:
            # Start applications concurrently
            legacy_task = asyncio.create_task(self._start_legacy_application())
            modern_task = asyncio.create_task(self._start_modern_application())

            legacy_success, modern_success = await asyncio.gather(
                legacy_task, modern_task
            )

            if legacy_success and modern_success:
                logger.info("Both applications started successfully")
                return True
            else:
                logger.error(
                    f"Application startup failed: Legacy={legacy_success}, Modern={modern_success}"
                )
                return False

        except Exception as e:
            logger.error(f"Failed to start applications: {e}")
            return False

    async def _start_legacy_application(self) -> bool:
        """Start Legacy application with timeout."""
        try:
            success = self.legacy_driver.start_application()
            if success:
                # Wait for application to be ready
                ready = await asyncio.wait_for(
                    self._wait_for_legacy_ready(),
                    timeout=self.config.application_startup_timeout_ms / 1000,
                )
                return ready
            return False
        except asyncio.TimeoutError:
            logger.error("Legacy application startup timed out")
            return False
        except Exception as e:
            logger.error(f"Legacy application startup failed: {e}")
            return False

    async def _start_modern_application(self) -> bool:
        """Start Modern application with timeout."""
        try:
            success = self.modern_driver.start_application()
            if success:
                # Wait for application to be ready
                ready = await asyncio.wait_for(
                    self._wait_for_modern_ready(),
                    timeout=self.config.application_startup_timeout_ms / 1000,
                )
                return ready
            return False
        except asyncio.TimeoutError:
            logger.error("Modern application startup timed out")
            return False
        except Exception as e:
            logger.error(f"Modern application startup failed: {e}")
            return False

    async def _wait_for_legacy_ready(self) -> bool:
        """Wait for Legacy to be ready."""
        return self.legacy_driver.wait_for_ready(
            self.config.application_startup_timeout_ms
        )

    async def _wait_for_modern_ready(self) -> bool:
        """Wait for Modern to be ready."""
        return self.modern_driver.wait_for_ready(
            self.config.application_startup_timeout_ms
        )

    async def stop_applications(self):
        """Stop both applications."""
        logger.info("Stopping TKA applications...")

        try:
            # Stop applications concurrently
            legacy_task = asyncio.create_task(self._stop_legacy_application())
            modern_task = asyncio.create_task(self._stop_modern_application())

            await asyncio.gather(legacy_task, modern_task, return_exceptions=True)
            logger.info("Applications stopped")

        except Exception as e:
            logger.error(f"Error stopping applications: {e}")

    async def _stop_legacy_application(self):
        """Stop Legacy application."""
        try:
            self.legacy_driver.stop_application()
        except Exception as e:
            logger.error(f"Error stopping Legacy: {e}")

    async def _stop_modern_application(self):
        """Stop Modern application."""
        try:
            self.modern_driver.stop_application()
        except Exception as e:
            logger.error(f"Error stopping Modern: {e}")

    async def execute_scenario(self, scenario_name: str) -> TestExecutionResult:
        """Execute a test scenario and return results."""
        logger.info(f"Executing scenario: {scenario_name}")

        scenario = self.scenario_provider.get_scenario(scenario_name)
        if not scenario:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        result = TestExecutionResult(
            scenario_name=scenario_name, total_actions=len(scenario.actions)
        )

        start_time = time.time()

        try:
            self.current_test_id = result.test_id
            self.is_running = True

            # Execute each action in the scenario
            for action in scenario.actions:
                action_result = await self._execute_parallel_action(action)

                if action_result["success"]:
                    result.successful_actions += 1
                else:
                    result.failed_actions += 1
                    result.errors.append(action_result.get("error", "Unknown error"))

                    if self.config.stop_on_first_failure:
                        break

                # Store results
                result.legacy_results.append(action_result["legacy_result"])
                result.modern_results.append(action_result["modern_result"])
                result.comparison_results.append(action_result["comparison_result"])

            # Calculate overall success and metrics
            result.success = result.failed_actions == 0
            result.total_execution_time_ms = (time.time() - start_time) * 1000
            result.average_action_time_ms = (
                result.total_execution_time_ms / result.total_actions
                if result.total_actions > 0
                else 0
            )

            # Calculate equivalence score
            if result.comparison_results:
                scores = [cr.equivalence_score for cr in result.comparison_results]
                result.equivalence_score = sum(scores) / len(scores)

            logger.info(
                f"Scenario completed: {scenario_name} - Success: {result.success}"
            )

        except Exception as e:
            logger.error(f"Scenario execution failed: {e}")
            result.success = False
            result.errors.append(str(e))

        finally:
            self.is_running = False
            self.current_test_id = None
            self.test_results.append(result)

        return result

    async def _execute_parallel_action(self, action: UserAction) -> Dict[str, Any]:
        """Execute an action on both Legacy and Modern and compare results."""
        logger.debug(f"Executing parallel action: {action.action_type.name}")

        # Validate action prerequisites
        legacy_state = self.legacy_driver.get_current_state()
        modern_state = self.modern_driver.get_current_state()

        validation_result = ActionValidatorFactory.validate_action(
            action, legacy_state.to_dict()
        )
        if not validation_result.is_valid:
            return {
                "success": False,
                "error": f"Action validation failed: {validation_result.errors}",
                "legacy_result": None,
                "modern_result": None,
                "comparison_result": None,
            }

        try:
            # Execute action on both versions concurrently
            legacy_task = asyncio.create_task(self._execute_legacy_action(action))
            modern_task = asyncio.create_task(self._execute_modern_action(action))

            legacy_result, modern_result = await asyncio.gather(
                legacy_task, modern_task
            )

            # Wait for both versions to stabilize
            await self._wait_for_synchronization(action.action_type)

            # Compare results
            comparison_result = self._compare_action_results(
                action, legacy_result, modern_result
            )

            # Take screenshots on failure if enabled
            if (
                not comparison_result.is_equivalent
                and self.config.screenshot_on_failure
            ):
                await self._capture_failure_screenshots(action)

            return {
                "success": comparison_result.is_equivalent,
                "error": (
                    None
                    if comparison_result.is_equivalent
                    else "Results not equivalent"
                ),
                "legacy_result": legacy_result,
                "modern_result": modern_result,
                "comparison_result": comparison_result,
            }

        except Exception as e:
            logger.error(f"Parallel action execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "legacy_result": None,
                "modern_result": None,
                "comparison_result": None,
            }

    async def _execute_legacy_action(self, action: UserAction) -> ActionResult:
        """Execute action on Legacy with timeout."""
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(self.legacy_driver.execute_action, action),
                timeout=self.config.action_timeout_ms / 1000,
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Legacy action timed out: {action.action_type.name}")
            return ActionResult(
                success=False,
                execution_time_ms=self.config.action_timeout_ms,
                error_message="Action timed out",
            )

    async def _execute_modern_action(self, action: UserAction) -> ActionResult:
        """Execute action on Modern with timeout."""
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(self.modern_driver.execute_action, action),
                timeout=self.config.action_timeout_ms / 1000,
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Modern action timed out: {action.action_type.name}")
            return ActionResult(
                success=False,
                execution_time_ms=self.config.action_timeout_ms,
                error_message="Action timed out",
            )

    async def _wait_for_synchronization(self, action_type):
        """Wait for both versions to synchronize after action execution."""
        # TKA-specific synchronization delays based on action type
        sync_delays = {
            "SELECT_START_POSITION": 1.0,  # Wait for option picker updates
            "SELECT_PICTOGRAPH_OPTION": 1.5,  # Wait for beat creation and rendering
            "TOGGLE_GRAPH_EDITOR": 0.8,  # Wait for animation completion
            "ADJUST_TURNS": 0.5,  # Wait for motion updates
            "CLEAR_SEQUENCE": 0.3,  # Wait for UI reset
        }

        delay = sync_delays.get(action_type.name, 0.2)  # Default delay
        await asyncio.sleep(delay)

    def _compare_action_results(
        self,
        action: UserAction,
        legacy_result: ActionResult,
        modern_result: ActionResult,
    ) -> ComparisonResult:
        """Compare Legacy and Modern action results."""
        try:
            # Convert results to comparable format
            legacy_data = self._normalize_legacy_result(legacy_result)
            modern_data = self._normalize_modern_result(modern_result)

            # Perform comparison
            comparison = self.result_comparer.compare_results(legacy_data, modern_data)

            return comparison

        except Exception as e:
            logger.error(f"Result comparison failed: {e}")
            # Return failed comparison
            from .comparison import ComparisonResult, FieldDifference

            failed_comparison = ComparisonResult(
                is_equivalent=False, equivalence_score=0.0
            )
            failed_comparison.add_difference(
                FieldDifference(
                    field_path="comparison.error",
                    legacy_value="N/A",
                    modern_value="N/A",
                    difference_type="comparison_error",
                    is_critical=True,
                    description=f"Comparison failed: {e}",
                )
            )
            return failed_comparison

    def _normalize_legacy_result(self, result: ActionResult) -> Dict[str, Any]:
        """Normalize Legacy result for comparison."""
        normalized = {
            "success": result.success,
            "execution_time_ms": result.execution_time_ms,
            "error_message": result.error_message,
            "data": {},
        }

        if result.data:
            # Normalize sequence data if present
            if "sequence_data" in result.data:
                sequence_data = result.data["sequence_data"]
                normalized_beats = []

                for beat in sequence_data.get("beats", []):
                    normalized_beat = self.data_normalizer.normalize_legacy_beat_data(
                        beat
                    )
                    normalized_beats.append(normalized_beat)

                normalized["data"]["sequence_data"] = {
                    "beat_count": sequence_data.get("beat_count", 0),
                    "beats": normalized_beats,
                    "start_position": sequence_data.get("start_position", ""),
                    "version": "Legacy",
                }

            # Copy other data as-is
            for key, value in result.data.items():
                if key not in ["sequence_data"]:
                    normalized["data"][key] = value

        return normalized

    def _normalize_modern_result(self, result: ActionResult) -> Dict[str, Any]:
        """Normalize Modern result for comparison."""
        normalized = {
            "success": result.success,
            "execution_time_ms": result.execution_time_ms,
            "error_message": result.error_message,
            "data": {},
        }

        if result.data:
            # Normalize sequence data if present
            if "sequence_data" in result.data:
                sequence_data = result.data["sequence_data"]
                normalized_beats = []

                for beat in sequence_data.get("beats", []):
                    normalized_beat = self.data_normalizer.normalize_modern_beat_data(
                        beat
                    )
                    normalized_beats.append(normalized_beat)

                normalized["data"]["sequence_data"] = {
                    "beat_count": sequence_data.get("beat_count", 0),
                    "beats": normalized_beats,
                    "start_position": sequence_data.get("start_position", ""),
                    "version": "Modern",
                }

            # Copy other data as-is
            for key, value in result.data.items():
                if key not in ["sequence_data"]:
                    normalized["data"][key] = value

        return normalized

    async def _capture_failure_screenshots(self, action: UserAction):
        """Capture screenshots when action comparison fails."""
        try:
            timestamp = int(time.time() * 1000)
            action_name = action.action_type.name.lower()

            legacy_screenshot = self.legacy_driver.capture_screenshot(
                f"legacy_{action_name}_{timestamp}.png"
            )
            modern_screenshot = self.modern_driver.capture_screenshot(
                f"modern_{action_name}_{timestamp}.png"
            )

            if legacy_screenshot and modern_screenshot:
                logger.info(
                    f"Failure screenshots captured: {legacy_screenshot}, {modern_screenshot}"
                )

        except Exception as e:
            logger.error(f"Failed to capture screenshots: {e}")

    async def execute_all_basic_scenarios(self) -> List[TestExecutionResult]:
        """Execute all basic workflow scenarios."""
        logger.info("Executing all basic workflow scenarios...")

        scenarios = self.scenario_provider.get_all_scenarios()
        results = []

        for scenario_name in scenarios.keys():
            try:
                result = await self.execute_scenario(scenario_name)
                results.append(result)

                logger.info(
                    f"Scenario {scenario_name}: {'PASSED' if result.success else 'FAILED'} "
                    f"(Equivalence: {result.equivalence_score:.2%})"
                )

            except Exception as e:
                logger.error(f"Failed to execute scenario {scenario_name}: {e}")

        return results

    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of all test results."""
        if not self.test_results:
            return {"message": "No tests executed"}

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests

        total_actions = sum(result.total_actions for result in self.test_results)
        successful_actions = sum(
            result.successful_actions for result in self.test_results
        )

        avg_equivalence = (
            sum(result.equivalence_score for result in self.test_results) / total_tests
        )

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "action_success_rate": (
                successful_actions / total_actions if total_actions > 0 else 0
            ),
            "average_equivalence_score": avg_equivalence,
            "test_results": self.test_results,
        }
