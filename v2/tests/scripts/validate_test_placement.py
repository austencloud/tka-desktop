#!/usr/bin/env python3
"""
Test Placement Validation Script
Enforces test lifecycle organization rules automatically
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict


class TestPlacementValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_test_file(self, file_path: Path) -> bool:
        if not file_path.name.startswith("test_"):
            return True

        content = file_path.read_text(encoding="utf-8")

        # Check for lifecycle metadata
        if not self._has_lifecycle_metadata(content):
            self.errors.append(f"{file_path}: Missing TEST LIFECYCLE metadata")
            return False

        lifecycle_type = self._extract_lifecycle_type(content)
        expected_location = self._get_expected_location(lifecycle_type, content)
        actual_location = self._get_actual_location(file_path)

        if actual_location != expected_location:
            self.errors.append(
                f"{file_path}: Wrong location. Expected: {expected_location}, Got: {actual_location}"
            )
            return False

        # Validate scaffolding tests have DELETE_AFTER
        if lifecycle_type == "SCAFFOLDING" and not self._has_delete_after(content):
            self.errors.append(
                f"{file_path}: Scaffolding test missing DELETE_AFTER date"
            )
            return False

        return True

    def _has_lifecycle_metadata(self, content: str) -> bool:
        return bool(
            re.search(
                r"TEST LIFECYCLE:\s*(SCAFFOLDING|SPECIFICATION|REGRESSION)", content
            )
        )

    def _extract_lifecycle_type(self, content: str) -> str:
        match = re.search(
            r"TEST LIFECYCLE:\s*(SCAFFOLDING|SPECIFICATION|REGRESSION)", content
        )
        return match.group(1) if match else "UNKNOWN"

    def _has_delete_after(self, content: str) -> bool:
        return bool(re.search(r"DELETE_AFTER:\s*\d{4}-\d{2}-\d{2}", content))

    def _get_expected_location(self, lifecycle_type: str, content: str) -> str:
        if lifecycle_type == "SCAFFOLDING":
            if re.search(r"debug|crash|bug|reproduce", content, re.IGNORECASE):
                return "tests/scaffolding/debug"
            elif re.search(
                r"exploration|legacy|behavior|understand", content, re.IGNORECASE
            ):
                return "tests/scaffolding/exploration"
            elif re.search(r"spike|prototype|poc|concept", content, re.IGNORECASE):
                return "tests/scaffolding/spike"
            return "tests/scaffolding/debug"  # default
        elif lifecycle_type == "SPECIFICATION":
            if re.search(r"domain|business|model", content, re.IGNORECASE):
                return "tests/specification/domain"
            elif re.search(r"service|application", content, re.IGNORECASE):
                return "tests/specification/application"
            elif re.search(r"ui|presentation|component", content, re.IGNORECASE):
                return "tests/specification/presentation"
            return "tests/specification/domain"  # default
        elif lifecycle_type == "REGRESSION":
            if re.search(r"performance|speed|memory", content, re.IGNORECASE):
                return "tests/regression/performance"
            return "tests/regression/bugs"  # default
        return "tests/unknown"

    def _get_actual_location(self, file_path: Path) -> str:
        parts = file_path.parts
        tests_index = next(i for i, part in enumerate(parts) if part == "tests")
        return "/".join(parts[tests_index:-1])

    def validate_all_tests(self, tests_dir: Path) -> bool:
        all_valid = True
        for test_file in tests_dir.rglob("test_*.py"):
            if not self.validate_test_file(test_file):
                all_valid = False
        return all_valid

    def print_results(self):
        if self.errors:
            print("❌ TEST PLACEMENT VALIDATION FAILED:")
            for error in self.errors:
                print(f"  {error}")
            return False
        else:
            print("✅ All tests are properly placed")
            return True


def main():
    validator = TestPlacementValidator()
    tests_dir = Path(__file__).parent.parent

    if validator.validate_all_tests(tests_dir):
        if validator.print_results():
            sys.exit(0)

    validator.print_results()
    sys.exit(1)


if __name__ == "__main__":
    main()
