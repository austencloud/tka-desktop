"""
TKA Desktop Exception Hierarchy

This module defines the complete exception hierarchy for the TKA Desktop application,
providing structured error handling with clear categorization and informative messages.

EXCEPTION HIERARCHY:
- TKABaseException: Root exception for all TKA-specific errors
  - ServiceOperationError: Service layer operation failures
  - ValidationError: Data validation and constraint violations
  - DependencyInjectionError: Dependency injection system errors
  - PerformanceError: Performance threshold violations
  - ConfigurationError: Configuration and settings errors
  - DataProcessingError: Data transformation and processing errors
"""

from typing import Optional, Dict, Any


class TKABaseException(Exception):
    """
    Base exception for TKA Desktop application.

    All TKA-specific exceptions should inherit from this class to provide
    consistent error handling and logging capabilities.
    """

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize TKA base exception.

        Args:
            message: Human-readable error message
            context: Additional context information for debugging
        """
        super().__init__(message)
        self.context = context or {}
        self.message = message

    def __str__(self) -> str:
        """Return formatted error message with context."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (Context: {context_str})"
        return self.message


class ServiceOperationError(TKABaseException):
    """
    Error in service layer operations.

    Raised when service methods fail to complete their operations due to
    business logic errors, external dependencies, or unexpected conditions.
    """

    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize service operation error.

        Args:
            message: Error description
            service_name: Name of the service that failed
            operation: Name of the operation that failed
            context: Additional context for debugging
        """
        enhanced_context = context or {}
        if service_name:
            enhanced_context["service"] = service_name
        if operation:
            enhanced_context["operation"] = operation

        super().__init__(message, enhanced_context)
        self.service_name = service_name
        self.operation = operation


class ValidationError(TKABaseException):
    """
    Data validation and constraint violation error.

    Raised when input data fails validation rules, constraints, or
    business logic requirements.
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize validation error.

        Args:
            message: Validation error description
            field: Name of the field that failed validation
            value: The invalid value
            context: Additional validation context
        """
        enhanced_context = context or {}
        if field:
            enhanced_context["field"] = field
        if value is not None:
            enhanced_context["value"] = str(value)

        super().__init__(message, enhanced_context)
        self.field = field
        self.value = value


class DependencyInjectionError(TKABaseException):
    """
    Dependency injection system error.

    Raised when the DI container fails to resolve dependencies, detects
    circular dependencies, or encounters registration issues.
    """

    def __init__(
        self,
        message: str,
        interface_name: Optional[str] = None,
        dependency_chain: Optional[list] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize dependency injection error.

        Args:
            message: DI error description
            interface_name: Name of the interface that failed to resolve
            dependency_chain: Chain of dependencies leading to the error
            context: Additional DI context
        """
        enhanced_context = context or {}
        if interface_name:
            enhanced_context["interface"] = interface_name
        if dependency_chain:
            enhanced_context["dependency_chain"] = " -> ".join(dependency_chain)

        super().__init__(message, enhanced_context)
        self.interface_name = interface_name
        self.dependency_chain = dependency_chain or []


class PerformanceError(TKABaseException):
    """
    Performance threshold exceeded error.

    Raised when operations exceed acceptable performance thresholds
    for duration, memory usage, or other performance metrics.
    """

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        threshold: Optional[float] = None,
        actual: Optional[float] = None,
        metric_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize performance error.

        Args:
            message: Performance error description
            operation: Name of the operation that exceeded thresholds
            threshold: The performance threshold that was exceeded
            actual: The actual performance value
            metric_type: Type of metric (duration_ms, memory_mb, etc.)
            context: Additional performance context
        """
        enhanced_context = context or {}
        if operation:
            enhanced_context["operation"] = operation
        if threshold is not None:
            enhanced_context["threshold"] = threshold
        if actual is not None:
            enhanced_context["actual"] = actual
        if metric_type:
            enhanced_context["metric_type"] = metric_type

        super().__init__(message, enhanced_context)
        self.operation = operation
        self.threshold = threshold
        self.actual = actual
        self.metric_type = metric_type


class ConfigurationError(TKABaseException):
    """
    Configuration and settings error.

    Raised when configuration files are invalid, missing required settings,
    or contain incompatible values.
    """

    def __init__(
        self,
        message: str,
        config_file: Optional[str] = None,
        setting_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize configuration error.

        Args:
            message: Configuration error description
            config_file: Name of the configuration file
            setting_name: Name of the problematic setting
            context: Additional configuration context
        """
        enhanced_context = context or {}
        if config_file:
            enhanced_context["config_file"] = config_file
        if setting_name:
            enhanced_context["setting"] = setting_name

        super().__init__(message, enhanced_context)
        self.config_file = config_file
        self.setting_name = setting_name


class DataProcessingError(TKABaseException):
    """
    Data transformation and processing error.

    Raised when data conversion, transformation, or processing operations
    fail due to invalid data formats or processing errors.
    """

    def __init__(
        self,
        message: str,
        data_type: Optional[str] = None,
        processing_stage: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize data processing error.

        Args:
            message: Data processing error description
            data_type: Type of data being processed
            processing_stage: Stage of processing where error occurred
            context: Additional processing context
        """
        enhanced_context = context or {}
        if data_type:
            enhanced_context["data_type"] = data_type
        if processing_stage:
            enhanced_context["stage"] = processing_stage

        super().__init__(message, enhanced_context)
        self.data_type = data_type
        self.processing_stage = processing_stage


# Convenience functions for common error scenarios
def service_error(
    message: str, service_name: str, operation: str, **context
) -> ServiceOperationError:
    """Create a service operation error with standard formatting."""
    return ServiceOperationError(
        message=f"{service_name}.{operation}: {message}",
        service_name=service_name,
        operation=operation,
        context=context,
    )


def validation_error(
    message: str, field: str, value: Any, **context
) -> ValidationError:
    """Create a validation error with standard formatting."""
    return ValidationError(
        message=f"Validation failed for {field}: {message}",
        field=field,
        value=value,
        context=context,
    )


def di_error(message: str, interface_name: str, **context) -> DependencyInjectionError:
    """Create a dependency injection error with standard formatting."""
    return DependencyInjectionError(
        message=f"DI resolution failed for {interface_name}: {message}",
        interface_name=interface_name,
        context=context,
    )
