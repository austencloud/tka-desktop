#!/usr/bin/env python3
"""
Migrate Existing Tests to Lifecycle-Based Structure
==================================================

This script helps migrate existing tests from the old structure to the new
lifecycle-based structure with proper categorization and metadata.
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date, timedelta


class TestMigrator:
    """Migrates existing tests to lifecycle-based structure."""

    def __init__(self, tests_root: Path = None):
        self.tests_root = tests_root or Path(__file__).parent.parent
        self.modern_root = self.tests_root.parent

        # Patterns to identify test types
        self.debug_patterns = [
            r"debug",
            r"crash",
            r"bug",
            r"fix",
            r"issue",
            r"critical",
            r"simple",
            r"minimal",
            r"reproduce",
            r"test_.*_debug",
        ]

        self.exploration_patterns = [
            r"exploration",
            r"understand",
            r"legacy.*behavior",
            r"parity.*test",
            r"investigate",
            r"analyze",
            r"study",
        ]

        self.spike_patterns = [
            r"spike",
            r"prototype",
            r"proof.*concept",
            r"poc",
            r"experiment",
            r"trial",
            r"test.*concept",
        ]

        self.specification_patterns = [
            r"contract",
            r"behavior",
            r"specification",
            r"requirement",
            r"interface",
            r"api",
            r"workflow",
            r"immutability",
        ]

        self.regression_patterns = [
            r"regression",
            r"prevent",
            r"issue_\d+",
            r"bug_\d+",
            r"fix_\d+",
        ]

    def analyze_test_file(self, file_path: Path) -> Dict[str, any]:
        """Analyze a test file to determine its lifecycle category."""
        try:
            content = file_path.read_text(encoding="utf-8")
            filename = file_path.name.lower()

            analysis = {
                "file_path": file_path,
                "suggested_category": "specification",  # Default
                "confidence": 0.0,
                "reasons": [],
                "existing_metadata": self._extract_existing_metadata(content),
                "has_lifecycle_metadata": "TEST LIFECYCLE:" in content,
            }

            # Check for debug patterns
            debug_score = self._calculate_pattern_score(
                filename + content.lower(), self.debug_patterns
            )
            if debug_score > 0.3:
                analysis["suggested_category"] = "scaffolding"
                analysis["confidence"] = debug_score
                analysis["reasons"].append(
                    f"Debug patterns detected (score: {debug_score:.2f})"
                )

            # Check for exploration patterns
            exploration_score = self._calculate_pattern_score(
                filename + content.lower(), self.exploration_patterns
            )
            if exploration_score > 0.3:
                analysis["suggested_category"] = "scaffolding"
                analysis["confidence"] = max(analysis["confidence"], exploration_score)
                analysis["reasons"].append(
                    f"Exploration patterns detected (score: {exploration_score:.2f})"
                )

            # Check for spike patterns
            spike_score = self._calculate_pattern_score(
                filename + content.lower(), self.spike_patterns
            )
            if spike_score > 0.3:
                analysis["suggested_category"] = "scaffolding"
                analysis["confidence"] = max(analysis["confidence"], spike_score)
                analysis["reasons"].append(
                    f"Spike patterns detected (score: {spike_score:.2f})"
                )

            # Check for regression patterns
            regression_score = self._calculate_pattern_score(
                filename + content.lower(), self.regression_patterns
            )
            if regression_score > 0.4:
                analysis["suggested_category"] = "regression"
                analysis["confidence"] = regression_score
                analysis["reasons"].append(
                    f"Regression patterns detected (score: {regression_score:.2f})"
                )

            # Check for specification patterns
            spec_score = self._calculate_pattern_score(
                filename + content.lower(), self.specification_patterns
            )
            if spec_score > 0.3 and analysis["suggested_category"] == "specification":
                analysis["confidence"] = spec_score
                analysis["reasons"].append(
                    f"Specification patterns detected (score: {spec_score:.2f})"
                )

            # Analyze file age and modification patterns
            file_age_days = (
                datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
            ).days
            if file_age_days < 7 and "debug" in filename:
                analysis["suggested_category"] = "scaffolding"
                analysis["confidence"] = max(analysis["confidence"], 0.8)
                analysis["reasons"].append(
                    f"Recent debug file (age: {file_age_days} days)"
                )

            return analysis

        except Exception as e:
            return {
                "file_path": file_path,
                "suggested_category": "specification",
                "confidence": 0.0,
                "reasons": [f"Error analyzing file: {e}"],
                "existing_metadata": {},
                "has_lifecycle_metadata": False,
            }

    def _calculate_pattern_score(self, text: str, patterns: List[str]) -> float:
        """Calculate how well text matches a set of patterns."""
        matches = 0
        total_patterns = len(patterns)

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1

        return matches / total_patterns if total_patterns > 0 else 0.0

    def _extract_existing_metadata(self, content: str) -> Dict[str, str]:
        """Extract any existing metadata from test file."""
        metadata = {}

        # Look for common metadata patterns
        patterns = {
            "purpose": r"PURPOSE:\s*(.+?)(?:\n|$)",
            "author": r"AUTHOR:\s*(.+?)(?:\n|$)",
            "created": r"CREATED:\s*(.+?)(?:\n|$)",
            "issue": r"(?:ISSUE|BUG):\s*(.+?)(?:\n|$)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()

        return metadata

    def generate_migration_plan(self) -> Dict[str, List[Dict]]:
        """Generate a migration plan for all test files."""
        plan = {
            "scaffolding": [],
            "specification": [],
            "regression": [],
            "integration": [],
            "unknown": [],
        }

        # Find all test files in the modern directory
        test_files = []

        # Root level test files
        for test_file in self.modern_root.glob("test_*.py"):
            test_files.append(test_file)

        # Existing organized test files
        for test_file in self.tests_root.rglob("test_*.py"):
            if "templates" not in str(test_file) and "scripts" not in str(test_file):
                test_files.append(test_file)

        # Analyze each test file
        for test_file in test_files:
            analysis = self.analyze_test_file(test_file)
            category = analysis["suggested_category"]

            if category in plan:
                plan[category].append(analysis)
            else:
                plan["unknown"].append(analysis)

        return plan

    def create_migration_report(self, plan: Dict[str, List[Dict]]) -> str:
        """Create a detailed migration report."""
        report = "# Test Migration Plan\n\n"
        report += f"**Generated**: {datetime.now().isoformat()}\n\n"

        total_files = sum(len(files) for files in plan.values())
        report += f"**Total test files found**: {total_files}\n\n"

        for category, files in plan.items():
            if not files:
                continue

            report += f"## {category.title()} Tests ({len(files)} files)\n\n"

            for analysis in files:
                file_path = analysis["file_path"]
                relative_path = file_path.relative_to(self.modern_root)

                report += f"### {file_path.name}\n"
                report += f"- **Current Path**: `{relative_path}`\n"
                report += (
                    f"- **Suggested Category**: {analysis['suggested_category']}\n"
                )
                report += f"- **Confidence**: {analysis['confidence']:.2f}\n"
                report += f"- **Has Lifecycle Metadata**: {'✅' if analysis['has_lifecycle_metadata'] else '❌'}\n"

                if analysis["reasons"]:
                    report += f"- **Reasons**: {', '.join(analysis['reasons'])}\n"

                if analysis["existing_metadata"]:
                    report += (
                        f"- **Existing Metadata**: {analysis['existing_metadata']}\n"
                    )

                # Suggest target path
                target_subdir = self._suggest_target_subdir(analysis)
                target_path = f"tests/{analysis['suggested_category']}/{target_subdir}/{file_path.name}"
                report += f"- **Suggested Target**: `{target_path}`\n"

                report += "\n"

        return report

    def _suggest_target_subdir(self, analysis: Dict) -> str:
        """Suggest target subdirectory based on analysis."""
        category = analysis["suggested_category"]
        filename = analysis["file_path"].name.lower()

        if category == "scaffolding":
            if any(pattern in filename for pattern in ["debug", "crash", "bug", "fix"]):
                return "debug"
            elif any(
                pattern in filename
                for pattern in ["exploration", "understand", "legacy"]
            ):
                return "exploration"
            elif any(pattern in filename for pattern in ["spike", "prototype", "poc"]):
                return "spike"
            else:
                return "debug"  # Default for scaffolding

        elif category == "specification":
            if any(pattern in filename for pattern in ["domain", "model", "sequence"]):
                return "domain"
            elif any(pattern in filename for pattern in ["service", "application"]):
                return "application"
            elif any(
                pattern in filename for pattern in ["ui", "component", "view", "frame"]
            ):
                return "presentation"
            else:
                return "domain"  # Default for specification

        elif category == "regression":
            if "performance" in filename:
                return "performance"
            else:
                return "bugs"

        else:  # integration
            return "workflows"

    def save_migration_report(self, output_path: Path = None) -> Path:
        """Save migration report to file."""
        if not output_path:
            output_path = self.tests_root / "migration_plan.md"

        plan = self.generate_migration_plan()
        report = self.create_migration_report(plan)

        output_path.write_text(report, encoding="utf-8")
        return output_path


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate existing tests to lifecycle structure"
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate migration report"
    )
    parser.add_argument("--output", type=Path, help="Output file for report")

    args = parser.parse_args()

    migrator = TestMigrator()

    if args.report:
        output_path = migrator.save_migration_report(args.output)
        print(f"📊 Migration report saved to: {output_path}")
    else:
        # Default: show summary
        plan = migrator.generate_migration_plan()
        total_files = sum(len(files) for files in plan.values())

        print("📊 Test Migration Summary:")
        print(f"  Total test files: {total_files}")
        for category, files in plan.items():
            if files:
                print(f"  {category}: {len(files)} files")
        print("\nUse --report to generate detailed migration plan")


if __name__ == "__main__":
    main()
