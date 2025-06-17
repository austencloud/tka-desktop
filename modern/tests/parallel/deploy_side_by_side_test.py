#!/usr/bin/env python3
"""
Side-by-Side Parallel Testing Deployment
========================================

Deploy and run TKA Legacy and Modern applications side-by-side for visual parallel testing.
Opens Legacy on one monitor and Modern on another monitor for real-time comparison.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Visual validation of Legacy/Modern functional equivalence
"""

import asyncio
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Tuple
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QRect
from PyQt6.QtGui import QScreen

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from master_test_orchestrator import ParallelTestOrchestrator, TestConfiguration
from scenarios.basic_workflows import BasicWorkflowScenarios


class SideBySideTestDeployer:
    """Deploys Legacy and Modern applications side-by-side for visual testing."""

    def __init__(self):
        self.orchestrator: Optional[ParallelTestOrchestrator] = None
        self.legacy_window_geometry: Optional[QRect] = None
        self.modern_window_geometry: Optional[QRect] = None

    def setup_logging(self):
        """Setup logging for deployment."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(f"side_by_side_test_{int(time.time())}.log"),
            ],
        )

    def detect_monitor_configuration(self) -> Tuple[bool, str]:
        """Detect monitor configuration for optimal window placement."""
        try:
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)

            screens = app.screens()
            screen_count = len(screens)

            print(f"🖥️  Detected {screen_count} monitor(s)")

            if screen_count >= 2:
                # Multi-monitor setup - ideal for side-by-side
                primary_screen = app.primaryScreen()
                secondary_screen = None

                for screen in screens:
                    if screen != primary_screen:
                        secondary_screen = screen
                        break

                if secondary_screen:
                    primary_geometry = primary_screen.geometry()
                    secondary_geometry = secondary_screen.geometry()

                    print(
                        f"   📺 Primary Monitor: {primary_geometry.width()}x{primary_geometry.height()} at ({primary_geometry.x()}, {primary_geometry.y()})"
                    )
                    print(
                        f"   📺 Secondary Monitor: {secondary_geometry.width()}x{secondary_geometry.height()} at ({secondary_geometry.x()}, {secondary_geometry.y()})"
                    )

                    # Legacy on primary monitor (left side)
                    self.legacy_window_geometry = QRect(
                        primary_geometry.x() + 50,
                        primary_geometry.y() + 50,
                        primary_geometry.width() - 100,
                        primary_geometry.height() - 100,
                    )

                    # Modern on secondary monitor (right side)
                    self.modern_window_geometry = QRect(
                        secondary_geometry.x() + 50,
                        secondary_geometry.y() + 50,
                        secondary_geometry.width() - 100,
                        secondary_geometry.height() - 100,
                    )

                    return True, "dual_monitor"

            # Single monitor setup - split screen
            if screen_count == 1:
                primary_screen = app.primaryScreen()
                primary_geometry = primary_screen.geometry()

                print(
                    f"   📺 Single Monitor: {primary_geometry.width()}x{primary_geometry.height()}"
                )

                # Split screen - Legacy on left half, Modern on right half
                half_width = primary_geometry.width() // 2

                self.legacy_window_geometry = QRect(
                    primary_geometry.x() + 25,
                    primary_geometry.y() + 50,
                    half_width - 50,
                    primary_geometry.height() - 100,
                )

                self.modern_window_geometry = QRect(
                    primary_geometry.x() + half_width + 25,
                    primary_geometry.y() + 50,
                    half_width - 50,
                    primary_geometry.height() - 100,
                )

                return True, "split_screen"

            return False, "no_monitors"

        except Exception as e:
            print(f"❌ Failed to detect monitor configuration: {e}")
            return False, "detection_failed"

    def create_test_configuration(self) -> TestConfiguration:
        """Create optimized test configuration for side-by-side testing."""
        config = TestConfiguration(
            test_data_dir=Path("side_by_side_test_data"),
            enable_screenshots=True,
            screenshot_on_failure=True,
            verbose_logging=True,
            save_debug_snapshots=True,
            # Timing optimized for visual observation
            action_timeout_ms=15000,  # Longer timeout for visual inspection
            synchronization_timeout_ms=8000,  # More time for sync
            application_startup_timeout_ms=45000,  # Generous startup time
            # Tolerances for comparison
            position_tolerance=2.0,
            rotation_tolerance=0.5,
            turn_tolerance=0.001,
            # Don't stop on first failure for visual testing
            stop_on_first_failure=False,
            max_retries=2,
            retry_delay_ms=2000,
        )

        return config

    async def deploy_applications(self) -> bool:
        """Deploy both Legacy and Modern applications with optimal window positioning."""
        print("\n🚀 DEPLOYING SIDE-BY-SIDE APPLICATIONS")
        print("=" * 50)

        try:
            # Create orchestrator
            config = self.create_test_configuration()
            self.orchestrator = ParallelTestOrchestrator(config)

            print("1. Starting applications...")

            # Start both applications
            if not await self.orchestrator.start_applications():
                print("❌ Failed to start applications")
                return False

            print("✅ Both applications started successfully")

            # Position windows for optimal viewing
            print("2. Positioning windows for side-by-side viewing...")
            await self._position_windows()

            print("✅ Applications positioned for side-by-side testing")
            return True

        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    async def _position_windows(self):
        """Position Legacy and Modern windows for optimal side-by-side viewing."""
        try:
            # Give applications time to fully load
            await asyncio.sleep(3)

            # Position Legacy window
            if (
                self.orchestrator.legacy_driver.main_window
                and self.legacy_window_geometry
            ):
                legacy_window = self.orchestrator.legacy_driver.main_window
                legacy_window.setGeometry(self.legacy_window_geometry)
                legacy_window.setWindowTitle("TKA Legacy - Parallel Testing")
                legacy_window.raise_()
                print(f"   📍 Legacy positioned at: {self.legacy_window_geometry}")

            # Position Modern window
            if (
                self.orchestrator.modern_driver.main_window
                and self.modern_window_geometry
            ):
                modern_window = self.orchestrator.modern_driver.main_window
                modern_window.setGeometry(self.modern_window_geometry)
                modern_window.setWindowTitle("TKA Modern - Parallel Testing")
                modern_window.raise_()
                print(f"   📍 Modern positioned at: {self.modern_window_geometry}")

            # Process events to ensure positioning takes effect
            if QApplication.instance():
                QApplication.instance().processEvents()

        except Exception as e:
            print(f"⚠️  Window positioning failed: {e}")

    async def run_visual_test_scenario(self, scenario_name: str):
        """Run a test scenario with visual observation pauses."""
        print(f"\n🎬 RUNNING VISUAL TEST: {scenario_name}")
        print("=" * 50)

        try:
            # Get scenario
            scenarios = BasicWorkflowScenarios()
            scenario = scenarios.get_scenario(scenario_name)

            if not scenario:
                print(f"❌ Scenario not found: {scenario_name}")
                return

            print(f"📋 Scenario: {scenario.description}")
            print(f"📊 Actions: {len(scenario.actions)}")
            print(
                f"⏱️  Estimated Duration: {scenario.estimated_duration_ms / 1000:.1f} seconds"
            )

            # Execute scenario with visual pauses
            for i, action in enumerate(scenario.actions):
                print(
                    f"\n🎯 Action {i+1}/{len(scenario.actions)}: {action.description}"
                )

                # Execute action on both versions
                result = await self.orchestrator._execute_parallel_action(action)

                if result["success"]:
                    print(f"   ✅ Action completed successfully")
                    print(
                        f"   📊 Equivalence: {result['comparison_result'].equivalence_score:.2%}"
                    )
                else:
                    print(f"   ❌ Action failed: {result['error']}")

                # Visual observation pause
                if i < len(scenario.actions) - 1:  # Don't pause after last action
                    print(f"   ⏸️  Pausing for visual observation...")
                    await asyncio.sleep(3)  # 3 second pause for observation

            print(f"\n🎉 Scenario '{scenario_name}' completed!")

        except Exception as e:
            print(f"❌ Visual test failed: {e}")
            import traceback

            traceback.print_exc()

    async def run_interactive_session(self):
        """Run interactive session for manual testing."""
        print("\n🎮 INTERACTIVE TESTING SESSION")
        print("=" * 40)
        print("Available commands:")
        print("  1. start_position - Test start position selection")
        print("  2. single_beat - Test single beat creation")
        print("  3. sequence_building - Test sequence building")
        print("  4. motion_modification - Test motion modification")
        print("  5. graph_editor - Test graph editor toggle")
        print("  6. sequence_clear - Test sequence clearing")
        print("  7. all - Run all scenarios")
        print("  8. quit - Exit interactive session")

        scenarios = BasicWorkflowScenarios()
        scenario_map = {
            "1": "start_position_selection",
            "2": "single_beat_creation",
            "3": "sequence_building",
            "4": "motion_modification",
            "5": "graph_editor_toggle",
            "6": "sequence_clear",
            "start_position": "start_position_selection",
            "single_beat": "single_beat_creation",
            "sequence_building": "sequence_building",
            "motion_modification": "motion_modification",
            "graph_editor": "graph_editor_toggle",
            "sequence_clear": "sequence_clear",
        }

        while True:
            try:
                command = input("\n🎯 Enter command: ").strip().lower()

                if command in ["quit", "exit", "q", "8"]:
                    print("👋 Exiting interactive session...")
                    break

                elif command in ["all", "7"]:
                    print("🚀 Running all scenarios...")
                    for scenario_name in scenarios.get_all_scenarios().keys():
                        await self.run_visual_test_scenario(scenario_name)

                        # Pause between scenarios
                        input("\n⏸️  Press Enter to continue to next scenario...")

                elif command in scenario_map:
                    scenario_name = scenario_map[command]
                    await self.run_visual_test_scenario(scenario_name)

                else:
                    print(f"❌ Unknown command: {command}")
                    print("   Type 'quit' to exit or choose from the numbered options")

            except KeyboardInterrupt:
                print("\n⚠️  Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Command failed: {e}")

    async def cleanup(self):
        """Cleanup applications and resources."""
        print("\n🧹 CLEANING UP")
        print("=" * 20)

        try:
            if self.orchestrator:
                await self.orchestrator.stop_applications()
                print("✅ Applications stopped")

        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")


async def main():
    """Main deployment routine."""
    print("🚀 TKA SIDE-BY-SIDE PARALLEL TESTING DEPLOYMENT")
    print("=" * 60)

    deployer = SideBySideTestDeployer()
    deployer.setup_logging()

    try:
        # Detect monitor configuration
        print("🖥️  Detecting monitor configuration...")
        monitor_ok, monitor_type = deployer.detect_monitor_configuration()

        if not monitor_ok:
            print(f"❌ Monitor detection failed: {monitor_type}")
            return 1

        print(f"✅ Monitor configuration: {monitor_type}")

        # Deploy applications
        if not await deployer.deploy_applications():
            print("❌ Application deployment failed")
            return 1

        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 30)
        print("📺 Legacy and Modern applications are now running side-by-side")
        print("🎮 Ready for interactive testing...")

        # Run interactive session
        await deployer.run_interactive_session()

        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Deployment interrupted by user")
        return 1

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        await deployer.cleanup()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
