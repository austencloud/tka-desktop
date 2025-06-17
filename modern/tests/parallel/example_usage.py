#!/usr/bin/env python3
"""
Example Usage of TKA Parallel Testing Framework
===============================================

Demonstrates how to use the parallel testing framework programmatically.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Example usage patterns for parallel testing framework
"""

import asyncio
import logging
from pathlib import Path

from master_test_orchestrator import ParallelTestOrchestrator, TestConfiguration
from actions import (
    UserAction,
    ActionType,
    GridPosition,
    ActionParameters,
    ExpectedOutcome,
)


async def example_single_action_test():
    """Example: Test a single action execution."""
    print("🔧 Example: Single Action Test")
    print("=" * 40)

    # Create configuration
    config = TestConfiguration(
        test_data_dir=Path("example_test_data"),
        verbose_logging=True,
        enable_screenshots=True,
    )

    # Create orchestrator
    orchestrator = ParallelTestOrchestrator(config)

    try:
        # Start applications
        print("Starting applications...")
        if not await orchestrator.start_applications():
            print("❌ Failed to start applications")
            return

        # Create a simple action
        action = UserAction(
            action_type=ActionType.SELECT_START_POSITION,
            description="Test alpha start position selection",
            parameters=ActionParameters(grid_position=GridPosition.ALPHA),
            expected_outcome=ExpectedOutcome(expected_data={"start_position": "alpha"}),
        )

        # Execute action on both versions
        result = await orchestrator._execute_parallel_action(action)

        # Print results
        if result["success"]:
            print("✅ Action executed successfully")
            print(f"   Legacy Success: {result['legacy_result'].success}")
            print(f"   Modern Success: {result['modern_result'].success}")
            print(f"   Equivalent: {result['comparison_result'].is_equivalent}")
        else:
            print(f"❌ Action failed: {result['error']}")

    finally:
        await orchestrator.stop_applications()


async def example_scenario_test():
    """Example: Test a complete scenario."""
    print("\n🔧 Example: Scenario Test")
    print("=" * 40)

    # Create configuration with custom settings
    config = TestConfiguration(
        test_data_dir=Path("example_test_data"),
        position_tolerance=1.5,  # More lenient for example
        rotation_tolerance=0.3,
        action_timeout_ms=8000,
        verbose_logging=False,
    )

    orchestrator = ParallelTestOrchestrator(config)

    try:
        # Start applications
        print("Starting applications...")
        if not await orchestrator.start_applications():
            print("❌ Failed to start applications")
            return

        # Run start position selection scenario
        result = await orchestrator.execute_scenario("start_position_selection")

        # Print detailed results
        print(f"\n📊 Scenario Results: {result.scenario_name}")
        print(f"   Success: {'✅' if result.success else '❌'}")
        print(f"   Actions: {result.successful_actions}/{result.total_actions}")
        print(f"   Equivalence: {result.equivalence_score:.2%}")
        print(f"   Duration: {result.total_execution_time_ms:.0f}ms")

        if result.errors:
            print(f"   Errors ({len(result.errors)}):")
            for error in result.errors:
                print(f"     - {error}")

        if result.warnings:
            print(f"   Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"     - {warning}")

    finally:
        await orchestrator.stop_applications()


async def example_custom_scenario():
    """Example: Create and run a custom scenario."""
    print("\n🔧 Example: Custom Scenario")
    print("=" * 40)

    from actions import ActionSequence

    # Create custom scenario
    custom_scenario = ActionSequence(
        name="Custom Example Scenario",
        description="Example of creating a custom test scenario",
        category="example",
    )

    # Add actions to scenario
    custom_scenario.add_action(
        UserAction(
            action_type=ActionType.CLEAR_SEQUENCE,
            description="Clear any existing sequence",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(sequence_length=0),
        )
    )

    custom_scenario.add_action(
        UserAction(
            action_type=ActionType.SELECT_START_POSITION,
            description="Select beta start position",
            parameters=ActionParameters(grid_position=GridPosition.BETA),
            expected_outcome=ExpectedOutcome(expected_data={"start_position": "beta"}),
        )
    )

    custom_scenario.add_action(
        UserAction(
            action_type=ActionType.SELECT_PICTOGRAPH_OPTION,
            description="Add first beat",
            parameters=ActionParameters(),
            expected_outcome=ExpectedOutcome(beat_count=1),
        )
    )

    # Execute custom scenario
    config = TestConfiguration(test_data_dir=Path("example_test_data"))
    orchestrator = ParallelTestOrchestrator(config)

    try:
        print("Starting applications...")
        if not await orchestrator.start_applications():
            print("❌ Failed to start applications")
            return

        # Manually execute scenario actions
        print(f"Executing custom scenario: {custom_scenario.name}")

        for i, action in enumerate(custom_scenario.actions):
            print(
                f"  Action {i+1}/{len(custom_scenario.actions)}: {action.description}"
            )

            result = await orchestrator._execute_parallel_action(action)

            if result["success"]:
                print(f"    ✅ Success")
            else:
                print(f"    ❌ Failed: {result['error']}")
                break

        print("Custom scenario completed!")

    finally:
        await orchestrator.stop_applications()


async def example_comparison_analysis():
    """Example: Analyze comparison results in detail."""
    print("\n🔧 Example: Comparison Analysis")
    print("=" * 40)

    config = TestConfiguration(test_data_dir=Path("example_test_data"))
    orchestrator = ParallelTestOrchestrator(config)

    try:
        print("Starting applications...")
        if not await orchestrator.start_applications():
            print("❌ Failed to start applications")
            return

        # Run a scenario and analyze results
        result = await orchestrator.execute_scenario("single_beat_creation")

        print(f"\n🔍 Detailed Analysis: {result.scenario_name}")

        # Analyze each comparison result
        for i, comparison in enumerate(result.comparison_results):
            print(f"\n  Action {i+1} Comparison:")
            print(f"    Equivalent: {comparison.is_equivalent}")
            print(f"    Score: {comparison.equivalence_score:.2%}")
            print(f"    Fields compared: {comparison.total_fields_compared}")
            print(f"    Fields matched: {comparison.fields_matched}")

            if comparison.differences:
                print(f"    Differences ({len(comparison.differences)}):")
                for diff in comparison.differences[:3]:  # Show first 3
                    print(
                        f"      - {diff.field_path}: {diff.legacy_value} vs {diff.modern_value}"
                    )
                if len(comparison.differences) > 3:
                    print(f"      ... and {len(comparison.differences) - 3} more")

            if comparison.warnings:
                print(f"    Warnings ({len(comparison.warnings)}):")
                for warning in comparison.warnings[:2]:  # Show first 2
                    print(f"      - {warning}")

    finally:
        await orchestrator.stop_applications()


async def main():
    """Run all examples."""
    print("🚀 TKA Parallel Testing Framework Examples")
    print("=" * 50)

    # Setup logging for examples
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Run examples
        await example_single_action_test()
        await example_scenario_test()
        await example_custom_scenario()
        await example_comparison_analysis()

        print("\n✅ All examples completed!")

    except KeyboardInterrupt:
        print("\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Examples failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
