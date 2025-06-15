# Quality Gates

## Task 3.4: Automated Quality Gates

**Comprehensive Quality Enforcement:**

```python
# FILE: src/infrastructure/quality/quality_gates.py

"""
Automated quality gates for TKA v2.
Enforces code quality, architecture compliance, and performance standards.
"""

import ast
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re
import importlib.util

class QualityLevel(Enum):
    """Quality issue severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class QualityIssue:
    """Represents a quality issue."""
    category: str
    level: QualityLevel
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

class ArchitectureAnalyzer:
    """Analyzes code for architecture compliance."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"

    def check_layer_dependencies(self) -> List[QualityIssue]:
        """Check that layers don't violate dependency rules."""
        issues = []

        # Define allowed dependencies
        layer_rules = {
            "domain": [],  # Domain should have no dependencies
            "application": ["domain"],  # Application can depend on domain
            "infrastructure": ["domain", "application"],  # Infrastructure can depend on both
            "presentation": ["domain", "application"]  # Presentation can depend on domain and application
        }

        for layer in layer_rules:
            layer_dir = self.src_dir / layer
            if not layer_dir.exists():
                continue

            for py_file in layer_dir.rglob("*.py"):
                violations = self._check_file_dependencies(py_file, layer, layer_rules[layer])
                issues.extend(violations)

        return issues

    def _check_file_dependencies(self, file_path: Path, current_layer: str, allowed_layers: List[str]) -> List[QualityIssue]:
        """Check dependencies in a single file."""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return issues

        try:
            tree = ast.parse(content)
        except:
            return issues

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_issues = self._analyze_import(node, file_path, current_layer, allowed_layers)
                issues.extend(import_issues)

        return issues

    def _analyze_import(self, node: ast.AST, file_path: Path, current_layer: str, allowed_layers: List[str]) -> List[QualityIssue]:
        """Analyze a single import statement."""
        issues = []

        if isinstance(node, ast.ImportFrom) and node.module:
            module_parts = node.module.split('.')

            # Check for src.layer imports
            if len(module_parts) >= 2 and module_parts[0] == "src":
                imported_layer = module_parts[1]

                # Check if this layer is allowed
                if imported_layer not in allowed_layers and imported_layer != current_layer:
                    issues.append(QualityIssue(
                        category="Architecture Violation",
                        level=QualityLevel.ERROR,
                        message=f"{current_layer} layer cannot import from {imported_layer} layer",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno,
                        suggestion=f"Move this dependency to an allowed layer: {allowed_layers}"
                    ))

        return issues

    def check_interface_compliance(self) -> List[QualityIssue]:
        """Check that services implement their interfaces correctly."""
        issues = []

        interfaces = self._find_interfaces()
        implementations = self._find_implementations()

        for interface_name, interface_info in interfaces.items():
            service_name = interface_name.replace("I", "", 1)  # IUserService -> UserService

            if service_name not in implementations:
                issues.append(QualityIssue(
                    category="Missing Implementation",
                    level=QualityLevel.ERROR,
                    message=f"Interface {interface_name} has no implementation",
                    suggestion=f"Create {service_name} class implementing {interface_name}"
                ))
                continue

            impl_info = implementations[service_name]

            # Check method compliance
            missing_methods = set(interface_info["methods"]) - set(impl_info["methods"])
            for method in missing_methods:
                issues.append(QualityIssue(
                    category="Interface Violation",
                    level=QualityLevel.ERROR,
                    message=f"{service_name} missing method: {method}",
                    file_path=impl_info["file_path"],
                    suggestion=f"Implement {method} method from {interface_name}"
                ))

        return issues

    def _find_interfaces(self) -> Dict[str, Dict[str, Any]]:
        """Find all interface definitions."""
        interfaces = {}

        # Look in application/interfaces
        interfaces_dir = self.src_dir / "application" / "interfaces"
        if interfaces_dir.exists():
            for py_file in interfaces_dir.glob("*.py"):
                file_interfaces = self._extract_interfaces_from_file(py_file)
                interfaces.update(file_interfaces)

        return interfaces

    def _find_implementations(self) -> Dict[str, Dict[str, Any]]:
        """Find all service implementations."""
        implementations = {}

        # Look in application/services
        services_dir = self.src_dir / "application" / "services"
        if services_dir.exists():
            for py_file in services_dir.glob("*.py"):
                file_implementations = self._extract_implementations_from_file(py_file)
                implementations.update(file_implementations)

        return implementations

    def _extract_interfaces_from_file(self, file_path: Path) -> Dict[str, Dict[str, Any]]:
        """Extract interface definitions from a file."""
        interfaces = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except:
            return interfaces

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a Protocol (interface)
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "Protocol":
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        interfaces[node.name] = {
                            "methods": methods,
                            "file_path": str(file_path.relative_to(self.project_root))
                        }
                        break

        return interfaces

    def _extract_implementations_from_file(self, file_path: Path) -> Dict[str, Dict[str, Any]]:
        """Extract service implementations from a file."""
        implementations = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except:
            return implementations

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.endswith("Service"):
                methods = [n.name for n in node.body
                          if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
                implementations[node.name] = {
                    "methods": methods,
                    "file_path": str(file_path.relative_to(self.project_root))
                }

        return implementations

class CodeQualityChecker:
    """Checks code quality metrics."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"

    def check_complexity(self) -> List[QualityIssue]:
        """Check cyclomatic complexity."""
        issues = []

        for py_file in self.src_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            file_issues = self._check_file_complexity(py_file)
            issues.extend(file_issues)

        return issues

    def _check_file_complexity(self, file_path: Path) -> List[QualityIssue]:
        """Check complexity in a single file."""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except:
            return issues

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)

                if complexity > 10:
                    level = QualityLevel.ERROR if complexity > 15 else QualityLevel.WARNING
                    issues.append(QualityIssue(
                        category="High Complexity",
                        level=level,
                        message=f"Function {node.name} has complexity {complexity} (threshold: 10)",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno,
                        suggestion="Consider breaking this function into smaller functions"
                    ))

        return issues

    def _calculate_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for node in ast.walk(func_node):
            # Add complexity for control flow statements
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def check_naming_conventions(self) -> List[QualityIssue]:
        """Check naming convention compliance."""
        issues = []

        for py_file in self.src_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            file_issues = self._check_file_naming(py_file)
            issues.extend(file_issues)

        return issues

    def _check_file_naming(self, file_path: Path) -> List[QualityIssue]:
        """Check naming conventions in a file."""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except:
            return issues

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append(QualityIssue(
                        category="Naming Convention",
                        level=QualityLevel.WARNING,
                        message=f"Class {node.name} should use PascalCase",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno
                    ))

            elif isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name) and not node.name.startswith('__'):
                    issues.append(QualityIssue(
                        category="Naming Convention",
                        level=QualityLevel.WARNING,
                        message=f"Function {node.name} should use snake_case",
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_number=node.lineno
                    ))

        return issues

class TestCoverageChecker:
    """Checks test coverage and quality."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def check_coverage(self) -> List[QualityIssue]:
        """Check test coverage."""
        issues = []

        try:
            # Run coverage analysis
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--cov=src",
                "--cov-report=json:coverage.json",
                "--quiet"
            ], cwd=self.project_root, capture_output=True, text=True)

            if result.returncode != 0:
                issues.append(QualityIssue(
                    category="Test Execution",
                    level=QualityLevel.ERROR,
                    message="Tests are failing",
                    suggestion="Fix failing tests before deployment"
                ))
                return issues

            # Analyze coverage report
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                coverage_issues = self._analyze_coverage_report(coverage_file)
                issues.extend(coverage_issues)

        except Exception as e:
            issues.append(QualityIssue(
                category="Coverage Analysis",
                level=QualityLevel.WARNING,
                message=f"Could not analyze test coverage: {e}"
            ))

        return issues

    def _analyze_coverage_report(self, coverage_file: Path) -> List[QualityIssue]:
        """Analyze coverage report for issues."""
        issues = []

        try:
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)

            total_coverage = coverage_data["totals"]["percent_covered"]

            if total_coverage < 80:
                level = QualityLevel.ERROR if total_coverage < 60 else QualityLevel.WARNING
                issues.append(QualityIssue(
                    category="Low Test Coverage",
                    level=level,
                    message=f"Total coverage is {total_coverage:.1f}% (target: 80%)",
                    suggestion="Add more unit tests to increase coverage"
                ))

            # Check individual files
            for file_path, file_data in coverage_data["files"].items():
                file_coverage = file_data["summary"]["percent_covered"]

                if file_coverage < 70 and not self._is_excluded_from_coverage(file_path):
                    issues.append(QualityIssue(
                        category="Low File Coverage",
                        level=QualityLevel.WARNING,
                        message=f"{file_path} has {file_coverage:.1f}% coverage",
                        file_path=file_path,
                        suggestion="Add tests for uncovered code paths"
                    ))

        except Exception as e:
            issues.append(QualityIssue(
                category="Coverage Parsing",
                level=QualityLevel.WARNING,
                message=f"Could not parse coverage report: {e}"
            ))

        return issues

    def _is_excluded_from_coverage(self, file_path: str) -> bool:
        """Check if file should be excluded from coverage requirements."""
        excluded_patterns = [
            "__init__.py",
            "conftest.py",
            "migrations/",
            "test_",
            "main.py"
        ]

        return any(pattern in file_path for pattern in excluded_patterns)

class PerformanceChecker:
    """Checks performance requirements."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def check_performance_regressions(self) -> List[QualityIssue]:
        """Check for performance regressions."""
        issues = []

        # This would integrate with the performance monitoring system
        # For now, we'll check basic performance indicators

        performance_file = self.project_root / "performance_baseline.json"
        if not performance_file.exists():
            issues.append(QualityIssue(
                category="Performance Baseline",
                level=QualityLevel.INFO,
                message="No performance baseline found",
                suggestion="Run performance tests to establish baseline"
            ))
            return issues

        # Load and check performance data
        try:
            with open(performance_file, 'r') as f:
                baseline = json.load(f)

            current_performance = self._get_current_performance()
            regression_issues = self._compare_performance(baseline, current_performance)
            issues.extend(regression_issues)

        except Exception as e:
            issues.append(QualityIssue(
                category="Performance Check",
                level=QualityLevel.WARNING,
                message=f"Could not check performance: {e}"
            ))

        return issues

    def _get_current_performance(self) -> Dict[str, float]:
        """Get current performance metrics."""
        # This would integrate with the performance monitoring system
        # For now, return mock data
        return {
            "startup_time": 2.5,
            "memory_usage": 150.0,
            "avg_response_time": 0.1
        }

    def _compare_performance(self, baseline: Dict[str, float], current: Dict[str, float]) -> List[QualityIssue]:
        """Compare current performance against baseline."""
        issues = []

        thresholds = {
            "startup_time": 1.2,  # 20% increase threshold
            "memory_usage": 1.3,  # 30% increase threshold
            "avg_response_time": 1.5  # 50% increase threshold
        }

        for metric, baseline_value in baseline.items():
            if metric in current:
                current_value = current[metric]
                threshold = thresholds.get(metric, 1.2)

                if current_value > baseline_value * threshold:
                    increase_pct = ((current_value - baseline_value) / baseline_value) * 100
                    issues.append(QualityIssue(
                        category="Performance Regression",
                        level=QualityLevel.ERROR,
                        message=f"{metric} increased by {increase_pct:.1f}%: {baseline_value} -> {current_value}",
                        suggestion="Investigate and fix performance regression"
                    ))

        return issues

class QualityGateRunner:
    """Main quality gate runner."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[QualityIssue] = []

        # Initialize checkers
        self.architecture_analyzer = ArchitectureAnalyzer(project_root)
        self.code_quality_checker = CodeQualityChecker(project_root)
        self.coverage_checker = TestCoverageChecker(project_root)
        self.performance_checker = PerformanceChecker(project_root)

    def run_all_checks(self) -> bool:
        """Run all quality checks."""
        print("🔍 Running TKA v2 Quality Gates...")

        # Architecture checks
        print("  📐 Checking architecture compliance...")
        self.issues.extend(self.architecture_analyzer.check_layer_dependencies())
        self.issues.extend(self.architecture_analyzer.check_interface_compliance())

        # Code quality checks
        print("  📊 Checking code quality...")
        self.issues.extend(self.code_quality_checker.check_complexity())
        self.issues.extend(self.code_quality_checker.check_naming_conventions())

        # Test coverage checks
        print("  🧪 Checking test coverage...")
        self.issues.extend(self.coverage_checker.check_coverage())

        # Performance checks
        print("  ⚡ Checking performance...")
        self.issues.extend(self.performance_checker.check_performance_regressions())

        # Report results
        self._report_results()

        # Return success if no errors
        error_count = len([i for i in self.issues if i.level == QualityLevel.ERROR])
        return error_count == 0

    def _report_results(self) -> None:
        """Report quality gate results."""
        error_count = len([i for i in self.issues if i.level == QualityLevel.ERROR])
        warning_count = len([i for i in self.issues if i.level == QualityLevel.WARNING])

        print(f"\n📊 Quality Gate Results:")
        print(f"  ❌ Errors: {error_count}")
        print(f"  ⚠️ Warnings: {warning_count}")
        print(f"  ℹ️ Info: {len(self.issues) - error_count - warning_count}")

        if self.issues:
            print("\n📋 Issues Found:")
            for issue in self.issues:
                icon = "❌" if issue.level == QualityLevel.ERROR else "⚠️"
                print(f"  {icon} [{issue.category}] {issue.message}")
                if issue.file_path:
                    print(f"      File: {issue.file_path}")
                    if issue.line_number:
                        print(f"      Line: {issue.line_number}")

        if error_count == 0:
            print("\n🎉 All quality gates passed!")
        else:
            print(f"\n💥 Quality gates failed with {error_count} errors")

def main():
    """CLI entry point for quality gates."""
    import argparse

    parser = argparse.ArgumentParser(description="Run TKA v2 quality gates")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--fail-on-warning", action="store_true",
                       help="Fail on warnings as well as errors")

    args = parser.parse_args()

    project_root = Path(args.project_root).absolute()
    runner = QualityGateRunner(project_root)

    success = runner.run_all_checks()

    if args.fail_on_warning:
        warning_count = len([i for i in runner.issues if i.level == QualityLevel.WARNING])
        if warning_count > 0:
            success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```
