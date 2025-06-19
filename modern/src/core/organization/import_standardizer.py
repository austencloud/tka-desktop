"""
Import Standardization Tool for TKA Desktop

A+ Enhancement: Automated tool to enforce consistent import patterns
across the entire codebase using established TKA conventions.

ARCHITECTURE: Analyzes and standardizes import statements to ensure
consistent module-relative imports without src. prefix.
"""

import ast
import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Union
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class ImportAnalysis:
    """Analysis results for import patterns in a file."""

    file_path: Path
    total_imports: int
    relative_imports: int
    absolute_imports: int
    src_prefix_imports: int
    inconsistent_imports: List[str]
    recommendations: List[str]
    compliance_score: float


@dataclass
class ImportStandardizationReport:
    """Comprehensive report of import standardization across codebase."""

    total_files_analyzed: int
    total_imports_found: int
    compliant_files: int
    non_compliant_files: int
    average_compliance_score: float
    common_violations: Dict[str, int]
    files_needing_fixes: List[Path]
    standardization_recommendations: List[str]


class ImportStandardizer:
    """
    Import standardization tool for TKA Desktop codebase.

    A+ Enhancement: Enforces consistent import patterns using established
    TKA conventions (module-relative imports without src. prefix).
    """

    def __init__(self, project_root: Path):
        """
        Initialize import standardizer.

        Args:
            project_root: Root directory of the TKA Desktop project
        """
        self.project_root = project_root
        self.src_root = project_root / "src"

        # TKA Desktop standard import patterns
        self.standard_patterns = {
            "domain_models": r"^from domain\.models\.",
            "application_services": r"^from application\.services\.",
            "presentation_components": r"^from presentation\.components\.",
            "core_modules": r"^from core\.",
            "infrastructure": r"^from infrastructure\.",
        }

        # Patterns to avoid (violations)
        self.violation_patterns = {
            "src_prefix": r"^from src\.",
            "absolute_with_modern": r"^from modern\.",
            "deep_relative": r"^from \.\.\.\.+",  # More than 3 levels
        }

        # Internal relative imports (allowed)
        self.allowed_relative_patterns = {
            "single_level": r"^from \.",
            "parent_level": r"^from \.\.",
            "grandparent_level": r"^from \.\.\.",
        }

        logger.info(f"Import standardizer initialized for project: {project_root}")

    def analyze_file(self, file_path: Path) -> ImportAnalysis:
        """
        Analyze import patterns in a single Python file.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            ImportAnalysis with detailed import pattern analysis
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            total_imports = 0
            relative_imports = 0
            absolute_imports = 0
            src_prefix_imports = 0
            inconsistent_imports = []
            recommendations = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    total_imports += 1

                    if isinstance(node, ast.ImportFrom):
                        module_name = node.module or ""

                        # Check for relative imports
                        if node.level > 0:
                            relative_imports += 1

                            # Check for excessive relative import depth
                            if node.level > 3:
                                inconsistent_imports.append(
                                    f"Excessive relative import depth: {'.' * node.level}{module_name}"
                                )
                                recommendations.append(
                                    "Reduce relative import depth to maximum 3 levels"
                                )

                        else:
                            absolute_imports += 1

                            # Check for src. prefix violations
                            if module_name.startswith("src."):
                                src_prefix_imports += 1
                                inconsistent_imports.append(
                                    f"src. prefix violation: {module_name}"
                                )
                                recommendations.append(
                                    f"Remove 'src.' prefix: {module_name} -> {module_name[4:]}"
                                )

                            # Check for standard TKA patterns
                            elif not self._is_standard_tka_import(module_name):
                                if not self._is_external_library(module_name):
                                    inconsistent_imports.append(
                                        f"Non-standard TKA import: {module_name}"
                                    )
                                    recommendations.append(
                                        f"Use standard TKA pattern for: {module_name}"
                                    )

            # Calculate compliance score
            compliance_score = self._calculate_compliance_score(
                total_imports, src_prefix_imports, len(inconsistent_imports)
            )

            return ImportAnalysis(
                file_path=file_path,
                total_imports=total_imports,
                relative_imports=relative_imports,
                absolute_imports=absolute_imports,
                src_prefix_imports=src_prefix_imports,
                inconsistent_imports=inconsistent_imports,
                recommendations=list(set(recommendations)),  # Remove duplicates
                compliance_score=compliance_score,
            )

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return ImportAnalysis(
                file_path=file_path,
                total_imports=0,
                relative_imports=0,
                absolute_imports=0,
                src_prefix_imports=0,
                inconsistent_imports=[f"Analysis failed: {e}"],
                recommendations=["Fix syntax errors before import analysis"],
                compliance_score=0.0,
            )

    def _is_standard_tka_import(self, module_name: str) -> bool:
        """Check if import follows standard TKA patterns."""
        for pattern in self.standard_patterns.values():
            if re.match(pattern, f"from {module_name}"):
                return True
        return False

    def _is_external_library(self, module_name: str) -> bool:
        """Check if import is from external library."""
        external_prefixes = [
            "typing",
            "pathlib",
            "os",
            "sys",
            "json",
            "logging",
            "dataclasses",
            "enum",
            "abc",
            "collections",
            "itertools",
            "functools",
            "operator",
            "time",
            "datetime",
            "threading",
            "asyncio",
            "concurrent",
            "multiprocessing",
            "PyQt6",
            "PySide6",
            "pytest",
            "hypothesis",
            "numpy",
            "pandas",
            "requests",
            "fastapi",
            "uvicorn",
            "pydantic",
        ]

        return any(module_name.startswith(prefix) for prefix in external_prefixes)

    def _calculate_compliance_score(
        self, total_imports: int, violations: int, inconsistencies: int
    ) -> float:
        """Calculate compliance score for import patterns."""
        if total_imports == 0:
            return 100.0

        # Deduct points for violations
        violation_penalty = (
            violations / total_imports
        ) * 50  # Up to 50% penalty for src. prefix
        inconsistency_penalty = (
            inconsistencies / total_imports
        ) * 30  # Up to 30% penalty for other issues

        score = 100.0 - violation_penalty - inconsistency_penalty
        return max(0.0, score)

    def analyze_codebase(self) -> ImportStandardizationReport:
        """
        Analyze import patterns across the entire codebase.

        Returns:
            ImportStandardizationReport with comprehensive analysis
        """
        python_files = list(self.src_root.rglob("*.py"))
        file_analyses = []

        logger.info(f"Analyzing {len(python_files)} Python files...")

        for file_path in python_files:
            # Skip __pycache__ and other generated files
            if "__pycache__" in str(file_path) or ".pyc" in str(file_path):
                continue

            analysis = self.analyze_file(file_path)
            file_analyses.append(analysis)

        # Generate comprehensive report
        total_files = len(file_analyses)
        total_imports = sum(analysis.total_imports for analysis in file_analyses)
        compliant_files = sum(
            1 for analysis in file_analyses if analysis.compliance_score >= 95.0
        )
        non_compliant_files = total_files - compliant_files

        average_compliance = (
            sum(analysis.compliance_score for analysis in file_analyses) / total_files
            if total_files > 0
            else 0.0
        )

        # Collect common violations
        common_violations = defaultdict(int)
        files_needing_fixes = []

        for analysis in file_analyses:
            if analysis.compliance_score < 95.0:
                files_needing_fixes.append(analysis.file_path)

            for violation in analysis.inconsistent_imports:
                violation_type = self._categorize_violation(violation)
                common_violations[violation_type] += 1

        # Generate standardization recommendations
        recommendations = self._generate_standardization_recommendations(file_analyses)

        return ImportStandardizationReport(
            total_files_analyzed=total_files,
            total_imports_found=total_imports,
            compliant_files=compliant_files,
            non_compliant_files=non_compliant_files,
            average_compliance_score=average_compliance,
            common_violations=dict(common_violations),
            files_needing_fixes=files_needing_fixes,
            standardization_recommendations=recommendations,
        )

    def _categorize_violation(self, violation: str) -> str:
        """Categorize violation type for reporting."""
        if "src. prefix" in violation:
            return "src_prefix_violations"
        elif "relative import depth" in violation:
            return "excessive_relative_depth"
        elif "Non-standard TKA import" in violation:
            return "non_standard_patterns"
        else:
            return "other_violations"

    def _generate_standardization_recommendations(
        self, analyses: List[ImportAnalysis]
    ) -> List[str]:
        """Generate actionable recommendations for import standardization."""
        recommendations = []

        # Count violation types
        src_prefix_count = sum(analysis.src_prefix_imports for analysis in analyses)
        non_compliant_count = sum(
            1 for analysis in analyses if analysis.compliance_score < 95.0
        )

        if src_prefix_count > 0:
            recommendations.append(
                f"Remove 'src.' prefix from {src_prefix_count} import statements across codebase"
            )

        if non_compliant_count > 0:
            recommendations.append(
                f"Standardize imports in {non_compliant_count} files to follow TKA conventions"
            )

        # Add specific pattern recommendations
        recommendations.extend(
            [
                "Use 'from domain.models.core_models import ...' for domain models",
                "Use 'from application.services import ...' for application services",
                "Use 'from presentation.components import ...' for UI components",
                "Use 'from core.interfaces import ...' for core interfaces",
                "Limit relative imports to maximum 3 levels (../../..)",
                "Use relative imports only within the same module hierarchy",
            ]
        )

        return recommendations

    def fix_file_imports(self, file_path: Path, dry_run: bool = True) -> bool:
        """
        Fix import patterns in a single file.

        Args:
            file_path: Path to the file to fix
            dry_run: If True, only show what would be changed

        Returns:
            True if fixes were applied (or would be applied in dry_run)
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Fix src. prefix violations
            content = re.sub(r"^from src\.", "from ", content, flags=re.MULTILINE)

            # Fix other common patterns
            content = re.sub(
                r"^from modern\.src\.", "from ", content, flags=re.MULTILINE
            )

            if content != original_content:
                if dry_run:
                    logger.info(f"Would fix imports in: {file_path}")
                    return True
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"Fixed imports in: {file_path}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error fixing imports in {file_path}: {e}")
            return False

    def standardize_codebase(
        self, dry_run: bool = True
    ) -> Dict[str, Union[int, float]]:
        """
        Standardize imports across the entire codebase.

        Args:
            dry_run: If True, only show what would be changed

        Returns:
            Dictionary with fix statistics
        """
        report = self.analyze_codebase()

        fixed_files = 0
        total_fixes = 0

        for file_path in report.files_needing_fixes:
            if self.fix_file_imports(file_path, dry_run):
                fixed_files += 1
                total_fixes += 1

        logger.info(
            f"Import standardization {'simulation' if dry_run else 'execution'} complete:"
        )
        logger.info(f"  - Files {'would be' if dry_run else ''} fixed: {fixed_files}")
        logger.info(
            f"  - Total fixes {'would be' if dry_run else ''} applied: {total_fixes}"
        )

        return {
            "files_fixed": fixed_files,
            "total_fixes": total_fixes,
            "compliance_improvement": self._estimate_compliance_improvement(report),
        }

    def _estimate_compliance_improvement(
        self, report: ImportStandardizationReport
    ) -> float:
        """Estimate compliance improvement after standardization."""
        # Estimate improvement based on common violations
        src_prefix_violations = report.common_violations.get("src_prefix_violations", 0)
        total_violations = sum(report.common_violations.values())

        if total_violations == 0:
            return 0.0

        # Estimate that fixing src. prefix violations improves compliance by ~20%
        improvement = (src_prefix_violations / total_violations) * 20.0
        return min(improvement, 25.0)  # Cap at 25% improvement


# ============================================================================
# COMPONENT HIERARCHY OPTIMIZER - A+ Enhancement
# ============================================================================


@dataclass
class ComponentHierarchyAnalysis:
    """Analysis of component hierarchy depth and structure."""

    component_path: Path
    hierarchy_depth: int
    class_count: int
    method_count: int
    complexity_score: float
    responsibilities: List[str]
    recommendations: List[str]


class ComponentHierarchyOptimizer:
    """
    Component hierarchy optimization tool for TKA Desktop.

    A+ Enhancement: Analyzes and optimizes component hierarchies to ensure
    maximum 3-level nesting and single responsibility principle adherence.
    """

    def __init__(self, project_root: Path):
        """Initialize component hierarchy optimizer."""
        self.project_root = project_root
        self.presentation_root = project_root / "src" / "presentation" / "components"

        # Maximum allowed hierarchy depth
        self.max_hierarchy_depth = 3

        # Complexity thresholds
        self.max_methods_per_class = 15
        self.max_lines_per_method = 50

        logger.info(f"Component hierarchy optimizer initialized for: {project_root}")

    def analyze_component_hierarchy(self) -> List[ComponentHierarchyAnalysis]:
        """Analyze component hierarchy across presentation layer."""
        if not self.presentation_root.exists():
            logger.warning(
                f"Presentation components directory not found: {self.presentation_root}"
            )
            return []

        analyses = []

        for component_file in self.presentation_root.rglob("*.py"):
            if component_file.name.startswith("__"):
                continue

            analysis = self._analyze_single_component(component_file)
            if analysis:
                analyses.append(analysis)

        return analyses

    def _analyze_single_component(
        self, component_path: Path
    ) -> Optional[ComponentHierarchyAnalysis]:
        """Analyze a single component file."""
        try:
            # Calculate hierarchy depth from path
            relative_path = component_path.relative_to(self.presentation_root)
            hierarchy_depth = len(relative_path.parts) - 1  # Subtract filename

            with open(component_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            class_count = 0
            method_count = 0
            responsibilities = []
            recommendations = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_count += 1

                    # Analyze class methods
                    class_methods = [
                        n for n in node.body if isinstance(n, ast.FunctionDef)
                    ]
                    method_count += len(class_methods)

                    # Check for excessive methods
                    if len(class_methods) > self.max_methods_per_class:
                        recommendations.append(
                            f"Class {node.name} has {len(class_methods)} methods "
                            f"(max: {self.max_methods_per_class}) - consider decomposition"
                        )

                    # Identify responsibilities from method names
                    responsibilities.extend(
                        self._extract_responsibilities(class_methods)
                    )

            # Check hierarchy depth
            if hierarchy_depth > self.max_hierarchy_depth:
                recommendations.append(
                    f"Hierarchy depth {hierarchy_depth} exceeds maximum {self.max_hierarchy_depth} "
                    f"- consider flattening structure"
                )

            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(
                hierarchy_depth, class_count, method_count
            )

            return ComponentHierarchyAnalysis(
                component_path=component_path,
                hierarchy_depth=hierarchy_depth,
                class_count=class_count,
                method_count=method_count,
                complexity_score=complexity_score,
                responsibilities=list(set(responsibilities)),
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error analyzing component {component_path}: {e}")
            return None

    def _extract_responsibilities(self, methods: List[ast.FunctionDef]) -> List[str]:
        """Extract responsibilities from method names."""
        responsibilities = []

        for method in methods:
            method_name = method.name

            # Skip special methods
            if method_name.startswith("__"):
                continue

            # Categorize by method name patterns
            if any(
                pattern in method_name.lower() for pattern in ["load", "fetch", "get"]
            ):
                responsibilities.append("data_loading")
            elif any(
                pattern in method_name.lower()
                for pattern in ["save", "store", "persist"]
            ):
                responsibilities.append("data_persistence")
            elif any(
                pattern in method_name.lower()
                for pattern in ["render", "draw", "paint"]
            ):
                responsibilities.append("rendering")
            elif any(
                pattern in method_name.lower()
                for pattern in ["handle", "on_", "process"]
            ):
                responsibilities.append("event_handling")
            elif any(
                pattern in method_name.lower()
                for pattern in ["validate", "check", "verify"]
            ):
                responsibilities.append("validation")
            elif any(
                pattern in method_name.lower()
                for pattern in ["update", "refresh", "sync"]
            ):
                responsibilities.append("state_management")
            else:
                responsibilities.append("business_logic")

        return responsibilities

    def _calculate_complexity_score(
        self, depth: int, classes: int, methods: int
    ) -> float:
        """Calculate component complexity score."""
        # Base score starts at 100
        score = 100.0

        # Deduct for excessive depth
        if depth > self.max_hierarchy_depth:
            score -= (depth - self.max_hierarchy_depth) * 15

        # Deduct for too many classes in one file
        if classes > 3:
            score -= (classes - 3) * 10

        # Deduct for too many methods
        if methods > 20:
            score -= (methods - 20) * 2

        return max(0.0, score)

    def generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations for component hierarchy."""
        analyses = self.analyze_component_hierarchy()

        recommendations = []

        # Find components with excessive depth
        deep_components = [
            a for a in analyses if a.hierarchy_depth > self.max_hierarchy_depth
        ]
        if deep_components:
            recommendations.append(
                f"Flatten {len(deep_components)} components with excessive hierarchy depth"
            )

        # Find components with multiple responsibilities
        complex_components = [a for a in analyses if len(a.responsibilities) > 3]
        if complex_components:
            recommendations.append(
                f"Decompose {len(complex_components)} components with multiple responsibilities"
            )

        # Find components with low complexity scores
        low_score_components = [a for a in analyses if a.complexity_score < 70]
        if low_score_components:
            recommendations.append(
                f"Refactor {len(low_score_components)} components with high complexity"
            )

        return recommendations
