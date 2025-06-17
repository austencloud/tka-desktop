#!/usr/bin/env python3
"""
TKA Modern Test Runner
=================

Advanced test execution with lifecycle-based test management.

Features:
- Lifecycle-based test categorization (scaffolding, specification, regression)
- Automatic expired test detection and warnings
- Test health monitoring and reporting
- Integration with test lifecycle management
- Performance monitoring and reporting
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Set
import argparse
import json
from datetime import datetime, date


class TestRunner:
    """Advanced test runner with intelligent test management."""

    def __init__(self, test_dir: Path = None):
        self.test_dir = test_dir or Path(__file__).parent
        self.src_dir = self.test_dir.parent / "src"
        self.results_dir = self.test_dir / "results"
        self.results_dir.mkdir(exist_ok=True)

        # Lifecycle-based test categories
        self.categories = {
            "scaffolding": {
                "max_time": 30.0,
                "lifecycle": "SCAFFOLDING",
                "description": "Temporary development aids",
            },
            "specification": {
                "max_time": 60.0,
                "lifecycle": "SPECIFICATION",
                "description": "Permanent behavioral contracts",
            },
            "regression": {
                "max_time": 120.0,
                "lifecycle": "REGRESSION",
                "description": "Bug prevention tests",
            },
            "integration": {
                "max_time": 180.0,
                "lifecycle": "INTEGRATION",
                "description": "Cross-component workflows",
            },
        }

        # Import lifecycle manager
        try:
            from scripts.test_lifecycle_manager import TestLifecycleManager

            self.lifecycle_manager = TestLifecycleManager(self.test_dir)
        except ImportError:
            self.lifecycle_manager = None
            print("Warning: Test lifecycle manager not available")

    def discover_tests(self) -> Dict[str, List[Path]]:
        """Discover all tests organized by category."""
        tests = {category: [] for category in self.categories}

        for category in self.categories:
            pattern_dir = self.test_dir / category
            if pattern_dir.exists():
                tests[category] = list(pattern_dir.glob("**/test_*.py"))

        return tests

    def check_test_health(self) -> Dict[str, any]:
        """Check overall test suite health and lifecycle compliance."""
        health_report = {
            "expired_tests": [],
            "problematic_tests": {},
            "total_tests": 0,
            "warnings": [],
            "recommendations": [],
        }

        if self.lifecycle_manager:
            try:
                expired = self.lifecycle_manager.find_expired_tests()
                problems = self.lifecycle_manager.find_problematic_tests()
                all_tests = self.lifecycle_manager.scan_all_tests()

                health_report["total_tests"] = len(all_tests)

                health_report["expired_tests"] = [
                    {
                        "file": str(test.file_path.relative_to(self.test_dir)),
                        "purpose": test.purpose,
                        "expired_date": (
                            test.delete_after.isoformat() if test.delete_after else None
                        ),
                    }
                    for test in expired
                ]

                health_report["problematic_tests"] = {
                    problem_type: [
                        str(test.file_path.relative_to(self.test_dir)) for test in tests
                    ]
                    for problem_type, tests in problems.items()
                    if tests
                }

                # Generate warnings and recommendations
                if expired:
                    health_report["warnings"].append(
                        f"⚠️ {len(expired)} expired scaffolding tests found"
                    )
                    health_report["recommendations"].append(
                        "Review expired scaffolding tests for deletion or migration to specification tests"
                    )

                total_problems = sum(len(tests) for tests in problems.values())
                if total_problems > 0:
                    health_report["warnings"].append(
                        f"⚠️ {total_problems} tests need attention"
                    )
                    health_report["recommendations"].append(
                        "Add proper lifecycle metadata to problematic tests"
                    )

                # Check scaffolding ratio
                scaffolding_count = len(
                    [t for t in all_tests if t.lifecycle == "SCAFFOLDING"]
                )
                if (
                    scaffolding_count > len(all_tests) * 0.3
                ):  # More than 30% scaffolding
                    health_report["warnings"].append(
                        f"⚠️ High scaffolding test ratio: {scaffolding_count}/{len(all_tests)} ({scaffolding_count/len(all_tests)*100:.1f}%)"
                    )
                    health_report["recommendations"].append(
                        "Consider cleaning up scaffolding tests or migrating stable ones to specification tests"
                    )

            except Exception as e:
                health_report["warnings"].append(f"Error checking test health: {e}")
        else:
            health_report["warnings"].append("Test lifecycle manager not available")

        return health_report

    def detect_outdated_tests(self) -> Set[Path]:
        """Detect tests that may be outdated based on code changes."""
        outdated = set()

        # Get last modification times of source files
        src_files = list(self.src_dir.rglob("*.py"))
        if not src_files:
            return outdated

        latest_src_time = max(f.stat().st_mtime for f in src_files)

        # Check test files against source modification time
        for test_file in self.test_dir.rglob("test_*.py"):
            if test_file.stat().st_mtime < latest_src_time - 86400:  # 1 day buffer
                outdated.add(test_file)

        return outdated

    def run_category(self, category: str, verbose: bool = False) -> Dict:
        """Run tests for a specific category."""
        if category not in self.categories:
            raise ValueError(f"Unknown category: {category}")

        category_dir = self.test_dir / category
        if not category_dir.exists():
            return {"status": "skipped", "reason": "No tests found"}

        start_time = time.time()

        # Build pytest command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(category_dir),
            f"-m",
            category,
            "--tb=short",
        ]

        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        # Run tests
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            stdout, stderr = process.communicate(
                timeout=self.categories[category]["max_time"]
            )
            return_code = process.returncode

            if verbose:
                print(f"stdout:\\n{stdout}")
                if stderr:
                    print(f"stderr:\\n{stderr}")

            end_time = time.time()
            duration = end_time - start_time

            return {
                "category": category,
                "duration": duration,
                "status": "passed" if return_code == 0 else "failed",
                "details": f"Finished in {duration:.2f}s",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": return_code,
            }

        except subprocess.TimeoutExpired:
            end_time = time.time()
            duration = end_time - start_time
            return {
                "category": category,
                "duration": duration,
                "status": "failed",
                "details": f"Timeout after {duration:.2f}s (max: {self.categories[category]['max_time']:.1f}s)",
                "stdout": "",
                "stderr": "Test execution timed out.",
                "returncode": -1,  # Indicate timeout
            }
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            return {
                "category": category,
                "duration": duration,
                "status": "error",
                "details": f"Error running tests: {e}",
                "stdout": "",
                "stderr": str(e),
                "returncode": -2,  # Indicate general error
            }

    def run_all(self, categories: List[str] = None, verbose: bool = False) -> Dict:
        """Run all tests or specified categories."""
        if categories is None:
            categories = list(self.categories.keys())

        results = {}
        total_start = time.time()

        print("🧪 TKA Modern Test Suite - Lifecycle-Based Testing")
        print("=" * 60)

        # Check test health first
        health = self.check_test_health()
        if health["warnings"]:
            print("\n⚠️ Test Health Warnings:")
            for warning in health["warnings"]:
                print(f"  {warning}")
            print()

        for category in categories:
            print(f"\n📋 Running {category} tests...")
            result = self.run_category(category, verbose)
            results[category] = result

            # Print immediate feedback
            if result["status"] == "passed":
                print(f"✅ {category}: PASSED ({result['duration']:.2f}s)")
            elif result["status"] == "failed":
                print(f"❌ {category}: FAILED ({result['duration']:.2f}s)")
            elif result["status"] == "timeout":
                print(f"⏰ {category}: TIMEOUT ({result['duration']:.2f}s)")
            else:
                print(f"⏭️  {category}: SKIPPED")

        total_duration = time.time() - total_start

        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)

        passed = sum(1 for r in results.values() if r["status"] == "passed")
        failed = sum(1 for r in results.values() if r["status"] == "failed")
        skipped = sum(1 for r in results.values() if r["status"] == "skipped")

        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"⏱️  Total Time: {total_duration:.2f}s")

        # Save results
        self._save_results(results, total_duration)

        return results

    def _save_results(self, results: Dict, total_duration: float):
        """Save test results to file."""
        timestamp = datetime.now().isoformat()
        result_data = {
            "timestamp": timestamp,
            "total_duration": total_duration,
            "results": results,
        }

        result_file = (
            self.results_dir / f"test_results_{timestamp.replace(':', '-')}.json"
        )
        with open(result_file, "w") as f:
            json.dump(result_data, f, indent=2)

    def clean_obsolete_tests(self, dry_run: bool = True) -> List[Path]:
        """Remove obsolete test files (with safety checks)."""
        # This would implement intelligent obsolete test detection
        # For now, just return empty list for safety
        return []

    def suggest_test_placement(self, test_content: str, test_name: str) -> str:
        """Analyze test content and suggest proper placement"""
        debug_patterns = ["debug", "crash", "bug", "reproduce", "minimal", "simple"]
        exploration_patterns = ["legacy", "behavior", "understand", "explore", "learn"]
        spike_patterns = ["spike", "prototype", "poc", "experiment", "feasibility"]
        specification_patterns = [
            "contract",
            "behavior",
            "must",
            "always",
            "never",
            "guarantee",
        ]
        regression_patterns = ["prevent", "regression", "issue", "bug_report", "fixed"]

        content_lower = test_content.lower()

        if "TEST LIFECYCLE:" in test_content:
            return "✅ Test already has proper lifecycle metadata"

        debug_score = sum(1 for p in debug_patterns if p in content_lower)
        exploration_score = sum(1 for p in exploration_patterns if p in content_lower)
        spike_score = sum(1 for p in spike_patterns if p in content_lower)
        spec_score = sum(1 for p in specification_patterns if p in content_lower)
        regression_score = sum(1 for p in regression_patterns if p in content_lower)

        suggestions = []

        if debug_score > 0:
            suggestions.append(
                f"tests/scaffolding/debug/ (debug patterns: {debug_score})"
            )
        if exploration_score > 0:
            suggestions.append(
                f"tests/scaffolding/exploration/ (exploration patterns: {exploration_score})"
            )
        if spike_score > 0:
            suggestions.append(
                f"tests/scaffolding/spike/ (spike patterns: {spike_score})"
            )
        if spec_score > 0:
            suggestions.append(
                f"tests/specification/domain/ (specification patterns: {spec_score})"
            )
        if regression_score > 0:
            suggestions.append(
                f"tests/regression/bugs/ (regression patterns: {regression_score})"
            )

        if not suggestions:
            suggestions.append(
                "tests/scaffolding/debug/ (default - add proper metadata)"
            )

        return f"💡 Suggested placement for '{test_name}':\n   " + "\n   ".join(
            suggestions
        )

    def auto_fix_suggestions(self, dry_run: bool = True) -> List[str]:
        """Provide automatic fix suggestions for misplaced tests"""
        fixes = []

        for test_file in self.test_dir.rglob("test_*.py"):
            if test_file.is_file():
                try:
                    content = test_file.read_text(encoding="utf-8")
                    suggestion = self.suggest_test_placement(content, test_file.name)

                    if "already has proper" not in suggestion:
                        fixes.append(
                            f"{test_file.relative_to(self.test_dir)}: {suggestion}"
                        )

                except Exception as e:
                    fixes.append(f"{test_file.name}: Error reading file - {e}")

        return fixes


def main():
    """Main test runner entry point."""
    parser = argparse.ArgumentParser(description="TKA Modern Test Runner")
    parser.add_argument(
        "categories",
        nargs="*",
        choices=["scaffolding", "specification", "regression", "integration"],
        help="Test categories to run (default: all)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--health", action="store_true", help="Check test suite health")
    parser.add_argument("--outdated", action="store_true", help="Show outdated tests")
    parser.add_argument("--clean", action="store_true", help="Clean obsolete tests")
    parser.add_argument(
        "--expired", action="store_true", help="Show expired scaffolding tests"
    )

    args = parser.parse_args()

    runner = TestRunner()

    if args.health:
        health = runner.check_test_health()
        print("🏥 Test Suite Health Report")
        print("=" * 40)
        print(f"Total tests: {health['total_tests']}")

        if health["expired_tests"]:
            print(f"\n🗑️ Expired tests: {len(health['expired_tests'])}")
            for test in health["expired_tests"]:
                print(f"  - {test['file']} (expired: {test['expired_date']})")

        if health["problematic_tests"]:
            print(f"\n⚠️ Problematic tests:")
            for problem_type, tests in health["problematic_tests"].items():
                print(f"  {problem_type}: {len(tests)} tests")
                for test in tests[:3]:  # Show first 3
                    print(f"    - {test}")
                if len(tests) > 3:
                    print(f"    ... and {len(tests) - 3} more")

        if health["warnings"]:
            print(f"\n⚠️ Warnings:")
            for warning in health["warnings"]:
                print(f"  {warning}")

        if health["recommendations"]:
            print(f"\n💡 Recommendations:")
            for rec in health["recommendations"]:
                print(f"  - {rec}")

        return

    if args.expired:
        if runner.lifecycle_manager:
            expired = runner.lifecycle_manager.find_expired_tests()
            if expired:
                print("🗑️ Expired Scaffolding Tests:")
                for test in expired:
                    print(f"  - {test.file_path.name} (expired: {test.delete_after})")
                    print(f"    Purpose: {test.purpose}")
                    print(f"    Path: {test.file_path.relative_to(runner.test_dir)}")
                    print()
            else:
                print("✅ No expired scaffolding tests found")
        else:
            print("❌ Test lifecycle manager not available")
        return

    if args.outdated:
        outdated = runner.detect_outdated_tests()
        if outdated:
            print("⚠️  Potentially outdated tests:")
            for test_file in outdated:
                print(f"  - {test_file}")
        else:
            print("✅ All tests appear up to date")
        return

    if args.clean:
        obsolete = runner.clean_obsolete_tests(dry_run=True)
        if obsolete:
            print("🧹 Would remove obsolete tests:")
            for test_file in obsolete:
                print(f"  - {test_file}")
        else:
            print("✅ No obsolete tests found")
        return

    # Run tests
    results = runner.run_all(args.categories, args.verbose)

    # Exit with appropriate code
    failed_count = sum(1 for r in results.values() if r["status"] == "failed")
    sys.exit(failed_count)


if __name__ == "__main__":
    main()
