#!/usr/bin/env python3
"""
Test Lifecycle Manager
=====================

Automated test lifecycle management for TKA Modern.
Identifies expired scaffolding tests and generates cleanup reports.
"""

import ast
import re
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TestMetadata:
    """Test metadata extracted from test files."""

    file_path: Path
    lifecycle: str
    purpose: str
    delete_after: Optional[date] = None
    created: Optional[date] = None
    author: Optional[str] = None
    related_issue: Optional[str] = None
    is_expired: bool = False


class TestLifecycleManager:
    """Manages test lifecycle and cleanup."""

    def __init__(self, tests_root: Path = None):
        self.tests_root = tests_root or Path(__file__).parent.parent
        self.scaffolding_dir = self.tests_root / "scaffolding"
        self.today = date.today()

    def scan_all_tests(self) -> List[TestMetadata]:
        """Scan all test files and extract metadata."""
        all_tests = []

        # Scan scaffolding tests
        for test_file in self.scaffolding_dir.rglob("*.py"):
            if test_file.name.startswith("test_"):
                metadata = self._extract_metadata(test_file)
                if metadata:
                    all_tests.append(metadata)

        return all_tests

    def find_expired_tests(self) -> List[TestMetadata]:
        """Find scaffolding tests that have expired."""
        all_tests = self.scan_all_tests()
        expired = []

        for test in all_tests:
            if test.lifecycle == "SCAFFOLDING" and test.delete_after:
                if test.delete_after <= self.today:
                    test.is_expired = True
                    expired.append(test)

        return expired

    def find_problematic_tests(self) -> Dict[str, List[TestMetadata]]:
        """Find tests with lifecycle problems."""
        all_tests = self.scan_all_tests()
        problems = {
            "missing_metadata": [],
            "old_scaffolding": [],
            "no_delete_date": [],
            "unclear_purpose": [],
        }

        for test in all_tests:
            # Missing lifecycle metadata
            if not test.lifecycle:
                problems["missing_metadata"].append(test)
                continue

            # Scaffolding tests without delete date
            if test.lifecycle == "SCAFFOLDING" and not test.delete_after:
                problems["no_delete_date"].append(test)

            # Old scaffolding tests (>30 days)
            if (
                test.lifecycle == "SCAFFOLDING"
                and test.created
                and (self.today - test.created).days > 30
            ):
                problems["old_scaffolding"].append(test)

            # Unclear purpose
            if not test.purpose or len(test.purpose.strip()) < 10:
                problems["unclear_purpose"].append(test)

        return problems

    def _extract_metadata(self, file_path: Path) -> Optional[TestMetadata]:
        """Extract metadata from test file."""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract docstring metadata
            lifecycle = self._extract_field(content, "TEST LIFECYCLE")
            purpose = self._extract_field(content, "PURPOSE")
            delete_after_str = self._extract_field(content, "DELETE_AFTER")
            created_str = self._extract_field(content, "CREATED")
            author = self._extract_field(content, "AUTHOR")
            related_issue = self._extract_field(content, "RELATED_ISSUE")

            # Parse dates
            delete_after = (
                self._parse_date(delete_after_str) if delete_after_str else None
            )
            created = self._parse_date(created_str) if created_str else None

            return TestMetadata(
                file_path=file_path,
                lifecycle=lifecycle or "",
                purpose=purpose or "",
                delete_after=delete_after,
                created=created,
                author=author,
                related_issue=related_issue,
            )

        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
            return None

    def _extract_field(self, content: str, field_name: str) -> Optional[str]:
        """Extract a field value from test file content."""
        pattern = rf"{field_name}:\s*(.+?)(?:\n|$)"
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parse date string in YYYY-MM-DD format."""
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except (ValueError, AttributeError):
            return None

    def generate_cleanup_report(self) -> str:
        """Generate comprehensive cleanup report."""
        expired_tests = self.find_expired_tests()
        problems = self.find_problematic_tests()

        report = f"# Test Lifecycle Cleanup Report\n\n"
        report += f"**Generated**: {datetime.now().isoformat()}\n"
        report += f"**Tests Root**: {self.tests_root}\n\n"

        # Expired tests section
        if expired_tests:
            report += "## 🗑️ Expired Tests (Safe to Delete)\n\n"
            for test in expired_tests:
                report += f"### {test.file_path.name}\n"
                report += (
                    f"- **Path**: `{test.file_path.relative_to(self.tests_root)}`\n"
                )
                report += f"- **Purpose**: {test.purpose}\n"
                report += f"- **Expired**: {test.delete_after}\n"
                report += f"- **Action**: ✅ Safe to delete\n\n"
        else:
            report += "## ✅ No Expired Tests Found\n\n"

        # Problematic tests section
        total_problems = sum(len(tests) for tests in problems.values())
        if total_problems > 0:
            report += "## ⚠️ Tests Needing Attention\n\n"

            for problem_type, tests in problems.items():
                if tests:
                    report += f"### {problem_type.replace('_', ' ').title()}\n"
                    for test in tests:
                        report += f"- `{test.file_path.relative_to(self.tests_root)}`\n"
                    report += "\n"

        # Summary
        report += "## 📊 Summary\n\n"
        report += f"- **Expired tests**: {len(expired_tests)}\n"
        report += f"- **Tests needing attention**: {total_problems}\n"
        report += f"- **Total scaffolding tests**: {len(self.scan_all_tests())}\n"

        return report

    def save_report(self, output_path: Path = None) -> Path:
        """Save cleanup report to file."""
        if not output_path:
            output_path = self.tests_root / "test_cleanup_report.md"

        report = self.generate_cleanup_report()
        output_path.write_text(report, encoding="utf-8")
        return output_path


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Manage test lifecycle")
    parser.add_argument("--report", action="store_true", help="Generate cleanup report")
    parser.add_argument("--expired", action="store_true", help="List expired tests")
    parser.add_argument(
        "--problems", action="store_true", help="List problematic tests"
    )
    parser.add_argument("--output", type=Path, help="Output file for report")

    args = parser.parse_args()

    manager = TestLifecycleManager()

    if args.expired:
        expired = manager.find_expired_tests()
        if expired:
            print("🗑️ Expired Tests:")
            for test in expired:
                print(f"  - {test.file_path.name} (expired: {test.delete_after})")
        else:
            print("✅ No expired tests found")

    elif args.problems:
        problems = manager.find_problematic_tests()
        total = sum(len(tests) for tests in problems.values())
        if total > 0:
            print("⚠️ Problematic Tests:")
            for problem_type, tests in problems.items():
                if tests:
                    print(f"  {problem_type}: {len(tests)} tests")
        else:
            print("✅ No problematic tests found")

    elif args.report:
        output_path = manager.save_report(args.output)
        print(f"📊 Report saved to: {output_path}")

    else:
        # Default: show summary
        expired = manager.find_expired_tests()
        problems = manager.find_problematic_tests()
        total_problems = sum(len(tests) for tests in problems.values())

        print("📊 Test Lifecycle Summary:")
        print(f"  - Expired tests: {len(expired)}")
        print(f"  - Tests needing attention: {total_problems}")
        print("\nUse --report to generate full cleanup report")


if __name__ == "__main__":
    main()
