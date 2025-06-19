"""
Error Aggregation System for TKA Desktop

A+ Enhancement: Provides comprehensive batch operation error handling
with intelligent error grouping, correlation analysis, and structured reporting.

ARCHITECTURE: Collects and analyzes errors from batch operations to provide
actionable insights and prevent error cascade scenarios.
"""

import time
import logging
from typing import List, Dict, Any, Optional, Union, Callable, Type
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from enum import Enum
import traceback
import hashlib

from ..exceptions import TKABaseException

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels for classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ErrorRecord:
    """Individual error record with context and metadata."""

    timestamp: float
    exception: Exception
    item_id: Optional[str] = None
    operation: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    error_hash: Optional[str] = None
    stack_trace: Optional[str] = None

    def __post_init__(self):
        """Generate error hash and capture stack trace."""
        if self.error_hash is None:
            # Create hash from exception type and message for grouping
            error_signature = f"{type(self.exception).__name__}:{str(self.exception)}"
            self.error_hash = hashlib.md5(error_signature.encode()).hexdigest()[:8]

        if self.stack_trace is None:
            self.stack_trace = traceback.format_exc()


@dataclass
class ErrorGroup:
    """Group of similar errors for analysis."""

    error_hash: str
    exception_type: str
    message_pattern: str
    count: int = 0
    first_occurrence: Optional[float] = None
    last_occurrence: Optional[float] = None
    affected_items: List[str] = field(default_factory=list)
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    sample_error: Optional[ErrorRecord] = None


@dataclass
class ErrorSummary:
    """Comprehensive error summary for batch operations."""

    operation_name: str
    start_time: float
    end_time: float
    total_items: int
    successful_items: int
    failed_items: int
    error_groups: List[ErrorGroup]
    success_rate: float
    failure_rate: float
    most_common_errors: List[tuple]  # (error_type, count)
    critical_errors: List[ErrorRecord]
    recommendations: List[str] = field(default_factory=list)


class ErrorAggregator:
    """
    Error aggregation system for batch operations.

    A+ Enhancement: Provides intelligent error collection, grouping,
    and analysis for comprehensive batch operation error handling.
    """

    def __init__(self, operation_name: str, auto_classify_severity: bool = True):
        """
        Initialize error aggregator for a batch operation.

        Args:
            operation_name: Name of the batch operation
            auto_classify_severity: Whether to automatically classify error severity
        """
        self.operation_name = operation_name
        self.auto_classify_severity = auto_classify_severity
        self.start_time = time.time()

        # Error tracking
        self.errors: List[ErrorRecord] = []
        self.success_count = 0
        self.total_count = 0

        # Error grouping
        self.error_groups: Dict[str, ErrorGroup] = {}

        # Severity classification rules
        self.severity_rules = {
            "ValidationError": ErrorSeverity.LOW,
            "FileNotFoundError": ErrorSeverity.MEDIUM,
            "PermissionError": ErrorSeverity.HIGH,
            "MemoryError": ErrorSeverity.CRITICAL,
            "SystemError": ErrorSeverity.CRITICAL,
        }

        logger.debug(f"Error aggregator initialized for operation: {operation_name}")

    def record_success(self, item_id: Optional[str] = None):
        """Record a successful operation."""
        self.success_count += 1
        self.total_count += 1

        if item_id:
            logger.debug(f"Success recorded for item: {item_id}")

    def record_error(
        self,
        exception: Exception,
        item_id: Optional[str] = None,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        severity: Optional[ErrorSeverity] = None,
    ):
        """
        Record an error with context and metadata.

        Args:
            exception: The exception that occurred
            item_id: Identifier for the item that failed
            operation: Specific operation that failed
            context: Additional context information
            severity: Error severity (auto-classified if not provided)
        """
        self.total_count += 1

        # Auto-classify severity if not provided
        if severity is None and self.auto_classify_severity:
            severity = self._classify_severity(exception)

        # Create error record
        error_record = ErrorRecord(
            timestamp=time.time(),
            exception=exception,
            item_id=item_id,
            operation=operation or self.operation_name,
            context=context or {},
            severity=severity or ErrorSeverity.MEDIUM,
        )

        self.errors.append(error_record)

        # Group similar errors
        self._group_error(error_record)

        logger.warning(
            f"Error recorded in {self.operation_name}: {type(exception).__name__}: {exception}"
            + (f" (item: {item_id})" if item_id else "")
        )

    def _classify_severity(self, exception: Exception) -> ErrorSeverity:
        """Automatically classify error severity based on exception type."""
        exception_name = type(exception).__name__

        # Check specific rules
        if exception_name in self.severity_rules:
            return self.severity_rules[exception_name]

        # Check inheritance hierarchy
        if isinstance(exception, (MemoryError, SystemError)):
            return ErrorSeverity.CRITICAL
        elif isinstance(exception, (PermissionError, OSError)):
            return ErrorSeverity.HIGH
        elif isinstance(exception, (ValueError, TypeError)):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _group_error(self, error_record: ErrorRecord):
        """Group similar errors for analysis."""
        error_hash = error_record.error_hash
        if error_hash is None:
            return  # Skip if no hash available

        if error_hash not in self.error_groups:
            # Create new error group
            self.error_groups[error_hash] = ErrorGroup(
                error_hash=error_hash,
                exception_type=type(error_record.exception).__name__,
                message_pattern=str(error_record.exception),
                first_occurrence=error_record.timestamp,
                severity=error_record.severity,
                sample_error=error_record,
            )

        # Update existing group
        group = self.error_groups[error_hash]
        group.count += 1
        group.last_occurrence = error_record.timestamp

        if error_record.item_id:
            group.affected_items.append(error_record.item_id)

        # Update severity to highest in group
        if (
            error_record.severity.value == "critical"
            or group.severity.value != "critical"
        ):
            if self._severity_priority(error_record.severity) > self._severity_priority(
                group.severity
            ):
                group.severity = error_record.severity

    def _severity_priority(self, severity: ErrorSeverity) -> int:
        """Get numeric priority for severity comparison."""
        priorities = {
            ErrorSeverity.LOW: 1,
            ErrorSeverity.MEDIUM: 2,
            ErrorSeverity.HIGH: 3,
            ErrorSeverity.CRITICAL: 4,
        }
        return priorities.get(severity, 1)

    def get_error_summary(self) -> ErrorSummary:
        """
        Generate comprehensive error summary.

        Returns:
            ErrorSummary with detailed analysis and recommendations
        """
        end_time = time.time()
        failed_items = len(self.errors)

        # Calculate rates
        success_rate = (
            self.success_count / self.total_count if self.total_count > 0 else 0.0
        )
        failure_rate = failed_items / self.total_count if self.total_count > 0 else 0.0

        # Get most common errors
        error_types = [type(error.exception).__name__ for error in self.errors]
        most_common_errors = Counter(error_types).most_common(5)

        # Get critical errors
        critical_errors = [
            error for error in self.errors if error.severity == ErrorSeverity.CRITICAL
        ]

        # Generate recommendations
        recommendations = self._generate_recommendations()

        return ErrorSummary(
            operation_name=self.operation_name,
            start_time=self.start_time,
            end_time=end_time,
            total_items=self.total_count,
            successful_items=self.success_count,
            failed_items=failed_items,
            error_groups=list(self.error_groups.values()),
            success_rate=success_rate,
            failure_rate=failure_rate,
            most_common_errors=most_common_errors,
            critical_errors=critical_errors,
            recommendations=recommendations,
        )

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on error patterns."""
        recommendations = []

        if not self.errors:
            return ["No errors detected - operation completed successfully"]

        # High failure rate
        failure_rate = (
            len(self.errors) / self.total_count if self.total_count > 0 else 0
        )
        if failure_rate > 0.5:
            recommendations.append(
                "High failure rate detected - consider reviewing input data quality"
            )

        # Critical errors
        critical_count = sum(
            1 for error in self.errors if error.severity == ErrorSeverity.CRITICAL
        )
        if critical_count > 0:
            recommendations.append(
                f"Found {critical_count} critical errors - immediate attention required"
            )

        # Common error patterns
        error_types = [type(error.exception).__name__ for error in self.errors]
        most_common = Counter(error_types).most_common(1)
        if most_common and most_common[0][1] > len(self.errors) * 0.3:
            error_type = most_common[0][0]
            recommendations.append(
                f"Dominant error type: {error_type} - consider targeted fixes"
            )

        # Permission errors
        permission_errors = [
            error
            for error in self.errors
            if isinstance(error.exception, PermissionError)
        ]
        if permission_errors:
            recommendations.append(
                "Permission errors detected - check file/directory access rights"
            )

        # Memory errors
        memory_errors = [
            error for error in self.errors if isinstance(error.exception, MemoryError)
        ]
        if memory_errors:
            recommendations.append(
                "Memory errors detected - consider processing smaller batches"
            )

        return recommendations

    def raise_if_errors(
        self,
        threshold: float = 0.1,
        severity_threshold: ErrorSeverity = ErrorSeverity.HIGH,
    ):
        """
        Raise exception if error rate exceeds threshold or critical errors found.

        Args:
            threshold: Maximum acceptable failure rate (0.0 to 1.0)
            severity_threshold: Minimum severity to trigger exception
        """
        if not self.errors:
            return

        failure_rate = (
            len(self.errors) / self.total_count if self.total_count > 0 else 0
        )

        # Check failure rate threshold
        if failure_rate > threshold:
            summary = self.get_error_summary()
            raise TKABaseException(
                f"Batch operation '{self.operation_name}' exceeded error threshold: "
                f"{failure_rate:.1%} failure rate (threshold: {threshold:.1%})",
                context={
                    "error_summary": summary.__dict__,
                    "failure_rate": failure_rate,
                    "threshold": threshold,
                },
            )

        # Check severity threshold
        severe_errors = [
            error
            for error in self.errors
            if self._severity_priority(error.severity)
            >= self._severity_priority(severity_threshold)
        ]

        if severe_errors:
            raise TKABaseException(
                f"Batch operation '{self.operation_name}' encountered {len(severe_errors)} "
                f"errors at or above {severity_threshold.value} severity",
                context={
                    "severe_errors": [str(error.exception) for error in severe_errors],
                    "severity_threshold": severity_threshold.value,
                },
            )

    def clear(self):
        """Clear all recorded errors and reset counters."""
        self.errors.clear()
        self.error_groups.clear()
        self.success_count = 0
        self.total_count = 0
        self.start_time = time.time()

        logger.debug(f"Error aggregator cleared for operation: {self.operation_name}")


# ============================================================================
# ERROR AGGREGATION DECORATOR - A+ Enhancement
# ============================================================================


def aggregate_errors(
    operation_name: Optional[str] = None,
    error_threshold: float = 0.1,
    severity_threshold: ErrorSeverity = ErrorSeverity.HIGH,
    auto_raise: bool = True,
) -> Callable:
    """
    Decorator to automatically aggregate errors in batch operations.

    A+ Enhancement: Provides declarative error aggregation for functions
    that process multiple items or perform batch operations.

    Args:
        operation_name: Name of the operation (defaults to function name)
        error_threshold: Maximum acceptable failure rate
        severity_threshold: Minimum severity to trigger exception
        auto_raise: Whether to automatically raise on threshold breach

    Returns:
        Decorated function with error aggregation
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"
            aggregator = ErrorAggregator(name)

            try:
                result = func(*args, aggregator=aggregator, **kwargs)

                if auto_raise:
                    aggregator.raise_if_errors(error_threshold, severity_threshold)

                return result

            except Exception as e:
                # Record the function-level error
                aggregator.record_error(e, operation="function_execution")

                if auto_raise:
                    aggregator.raise_if_errors(error_threshold, severity_threshold)

                raise

        return wrapper

    return decorator
