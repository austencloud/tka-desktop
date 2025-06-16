#!/usr/bin/env python3
"""
Master Parallel Test Runner
===========================

Main entry point for TKA Legacy/Modern parallel testing.
Provides CLI interface for running parallel tests and generating reports.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Main test runner for Legacy/Modern functional equivalence validation

Usage:
    python master_parallel_test.py --scenario start_position_selection
    python master_parallel_test.py --all
    python master_parallel_test.py --all --report --output results.html
"""

import asyncio
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

from master_test_orchestrator import ParallelTestOrchestrator, TestConfiguration
from scenarios.basic_workflows import BasicWorkflowScenarios


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                f'parallel_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            ),
        ],
    )


def create_test_configuration(args) -> TestConfiguration:
    """Create test configuration from command line arguments."""
    config = TestConfiguration()

    # Override defaults with command line arguments
    if args.test_data_dir:
        config.test_data_dir = Path(args.test_data_dir)

    if args.timeout:
        config.action_timeout_ms = args.timeout * 1000

    if args.position_tolerance:
        config.position_tolerance = args.position_tolerance

    if args.rotation_tolerance:
        config.rotation_tolerance = args.rotation_tolerance

    config.enable_screenshots = not args.no_screenshots
    config.screenshot_on_failure = not args.no_failure_screenshots
    config.stop_on_first_failure = args.stop_on_failure
    config.verbose_logging = args.verbose

    return config


async def run_single_scenario(
    orchestrator: ParallelTestOrchestrator, scenario_name: str
):
    """Run a single test scenario."""
    print(f"\n🚀 Running scenario: {scenario_name}")
    print("=" * 60)

    try:
        result = await orchestrator.execute_scenario(scenario_name)

        # Print results
        status = "✅ PASSED" if result.success else "❌ FAILED"
        print(f"\n{status} - {scenario_name}")
        print(f"   Actions: {result.successful_actions}/{result.total_actions}")
        print(f"   Equivalence: {result.equivalence_score:.2%}")
        print(f"   Duration: {result.total_execution_time_ms:.0f}ms")

        if result.errors:
            print(f"   Errors: {len(result.errors)}")
            for error in result.errors[:3]:  # Show first 3 errors
                print(f"     - {error}")
            if len(result.errors) > 3:
                print(f"     ... and {len(result.errors) - 3} more")

        return result

    except Exception as e:
        print(f"❌ FAILED - {scenario_name}: {e}")
        return None


async def run_all_scenarios(orchestrator: ParallelTestOrchestrator):
    """Run all basic workflow scenarios."""
    print("\n🚀 Running all basic workflow scenarios")
    print("=" * 60)

    try:
        results = await orchestrator.execute_all_basic_scenarios()

        # Print summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.success)
        failed_tests = total_tests - passed_tests

        print(f"\n📊 Test Summary")
        print("=" * 30)
        print(f"Total scenarios: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(
            f"Pass rate: {passed_tests/total_tests:.1%}"
            if total_tests > 0
            else "Pass rate: N/A"
        )

        if results:
            avg_equivalence = sum(r.equivalence_score for r in results) / len(results)
            print(f"Average equivalence: {avg_equivalence:.2%}")

        return results

    except Exception as e:
        print(f"❌ Failed to run all scenarios: {e}")
        return []


def generate_html_report(test_results, output_file: str):
    """Generate HTML report from test results."""
    try:
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TKA Legacy/Modern Parallel Test Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .scenario {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .passed {{ border-left: 5px solid #4CAF50; }}
        .failed {{ border-left: 5px solid #f44336; }}
        .metrics {{ display: flex; gap: 20px; }}
        .metric {{ text-align: center; }}
        .error {{ color: #f44336; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TKA Legacy/Modern Parallel Test Results</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""

        if test_results:
            # Summary statistics
            total_tests = len(test_results)
            passed_tests = sum(1 for r in test_results if r.success)
            failed_tests = total_tests - passed_tests
            avg_equivalence = (
                sum(r.equivalence_score for r in test_results) / total_tests
            )

            html_content += f"""
    <div class="summary">
        <h2>Summary</h2>
        <div class="metrics">
            <div class="metric">
                <h3>{total_tests}</h3>
                <p>Total Tests</p>
            </div>
            <div class="metric">
                <h3>{passed_tests}</h3>
                <p>Passed</p>
            </div>
            <div class="metric">
                <h3>{failed_tests}</h3>
                <p>Failed</p>
            </div>
            <div class="metric">
                <h3>{passed_tests/total_tests:.1%}</h3>
                <p>Pass Rate</p>
            </div>
            <div class="metric">
                <h3>{avg_equivalence:.1%}</h3>
                <p>Avg Equivalence</p>
            </div>
        </div>
    </div>
    
    <h2>Test Results</h2>
"""

            # Individual test results
            for result in test_results:
                status_class = "passed" if result.success else "failed"
                status_text = "PASSED" if result.success else "FAILED"

                html_content += f"""
    <div class="scenario {status_class}">
        <h3>{result.scenario_name} - {status_text}</h3>
        <p><strong>Actions:</strong> {result.successful_actions}/{result.total_actions}</p>
        <p><strong>Equivalence:</strong> {result.equivalence_score:.2%}</p>
        <p><strong>Duration:</strong> {result.total_execution_time_ms:.0f}ms</p>
"""

                if result.errors:
                    html_content += "<h4>Errors:</h4><ul>"
                    for error in result.errors:
                        html_content += f'<li class="error">{error}</li>'
                    html_content += "</ul>"

                html_content += "</div>"

        else:
            html_content += "<p>No test results available.</p>"

        html_content += """
</body>
</html>
"""

        # Write to file
        with open(output_file, "w") as f:
            f.write(html_content)

        print(f"📄 HTML report generated: {output_file}")

    except Exception as e:
        print(f"❌ Failed to generate HTML report: {e}")


def save_json_results(test_results, output_file: str):
    """Save test results as JSON."""
    try:
        # Convert results to JSON-serializable format
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(test_results),
            "results": [],
        }

        for result in test_results:
            json_data["results"].append(
                {
                    "scenario_name": result.scenario_name,
                    "success": result.success,
                    "total_actions": result.total_actions,
                    "successful_actions": result.successful_actions,
                    "failed_actions": result.failed_actions,
                    "equivalence_score": result.equivalence_score,
                    "execution_time_ms": result.total_execution_time_ms,
                    "errors": result.errors,
                    "warnings": result.warnings,
                }
            )

        with open(output_file, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"💾 JSON results saved: {output_file}")

    except Exception as e:
        print(f"❌ Failed to save JSON results: {e}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TKA Legacy/Modern Parallel Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scenario start_position_selection
  %(prog)s --all --report
  %(prog)s --all --output results.html --json results.json
        """,
    )

    # Test selection
    parser.add_argument("--scenario", help="Run specific scenario")
    parser.add_argument("--all", action="store_true", help="Run all basic scenarios")
    parser.add_argument("--list", action="store_true", help="List available scenarios")

    # Configuration
    parser.add_argument("--test-data-dir", help="Test data directory")
    parser.add_argument(
        "--timeout", type=int, default=10, help="Action timeout in seconds"
    )
    parser.add_argument(
        "--position-tolerance",
        type=float,
        default=2.0,
        help="Position tolerance in pixels",
    )
    parser.add_argument(
        "--rotation-tolerance",
        type=float,
        default=0.5,
        help="Rotation tolerance in degrees",
    )

    # Options
    parser.add_argument(
        "--no-screenshots", action="store_true", help="Disable screenshot capture"
    )
    parser.add_argument(
        "--no-failure-screenshots",
        action="store_true",
        help="Disable failure screenshots",
    )
    parser.add_argument(
        "--stop-on-failure", action="store_true", help="Stop on first failure"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    # Output
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument(
        "--output", default="test_results.html", help="HTML report output file"
    )
    parser.add_argument("--json", help="JSON results output file")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # List scenarios if requested
    if args.list:
        scenarios = BasicWorkflowScenarios()
        print("Available scenarios:")
        for name, scenario in scenarios.get_all_scenarios().items():
            print(f"  {name}: {scenario.description}")
        return

    # Validate arguments
    if not args.scenario and not args.all:
        parser.error("Must specify either --scenario or --all")

    # Create configuration and orchestrator
    config = create_test_configuration(args)
    orchestrator = ParallelTestOrchestrator(config)

    try:
        # Start applications
        print("🔧 Starting TKA Legacy and Modern applications...")
        if not await orchestrator.start_applications():
            print("❌ Failed to start applications")
            return 1

        print("✅ Applications started successfully")

        # Run tests
        test_results = []

        if args.scenario:
            result = await run_single_scenario(orchestrator, args.scenario)
            if result:
                test_results.append(result)

        elif args.all:
            test_results = await run_all_scenarios(orchestrator)

        # Generate reports
        if test_results:
            if args.report:
                generate_html_report(test_results, args.output)

            if args.json:
                save_json_results(test_results, args.json)

        # Print final summary
        summary = orchestrator.get_test_summary()
        if summary.get("total_tests", 0) > 0:
            print(
                f"\n🎯 Final Results: {summary['passed_tests']}/{summary['total_tests']} passed "
                f"({summary['pass_rate']:.1%})"
            )

        return 0 if summary.get("pass_rate", 0) == 1.0 else 1

    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        return 1

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return 1

    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        await orchestrator.stop_applications()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
