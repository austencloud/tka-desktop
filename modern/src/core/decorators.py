"""
TKA Desktop Decorators

This module provides decorators for cross-cutting concerns like error handling,
performance monitoring, and logging across the TKA Desktop application.

DECORATORS:
- handle_service_errors: Standardized error handling for service methods
- validate_inputs: Input validation decorator
- log_operation: Operation logging decorator
- retry_on_failure: Retry decorator for transient failures
"""

import logging
import time
import functools
from typing import Callable, Any, Optional, Type, Union, Dict
from .exceptions import (
    ServiceOperationError,
    ValidationError,
    TKABaseException,
    service_error,
)

# Configure logger for decorators
logger = logging.getLogger(__name__)


def handle_service_errors(
    operation_name: Optional[str] = None,
    reraise_validation_errors: bool = True,
    default_return: Any = None,
    log_level: int = logging.ERROR,
) -> Callable:
    """
    Decorator for standardized service error handling.

    This decorator provides consistent error handling across all service methods,
    converting unexpected exceptions to ServiceOperationError while preserving
    validation errors and providing detailed logging.

    Args:
        operation_name: Custom operation name (defaults to class.method)
        reraise_validation_errors: Whether to re-raise ValidationError as-is
        default_return: Default return value on error (if not re-raising)
        log_level: Logging level for error messages

    Returns:
        Decorated function with error handling

    Example:
        @handle_service_errors("calculate_layout")
        def calculate_layout(self, data: LayoutData) -> LayoutResult:
            # Implementation here
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Determine operation name
            if operation_name:
                op_name = operation_name
            else:
                class_name = self.__class__.__name__
                method_name = func.__name__
                op_name = f"{class_name}.{method_name}"

            # Extract service name from class
            service_name = self.__class__.__name__

            try:
                return func(self, *args, **kwargs)

            except ValidationError:
                # Re-raise validation errors as-is if requested
                if reraise_validation_errors:
                    raise
                logger.log(log_level, f"Validation error in {op_name}")
                return default_return

            except TKABaseException:
                # Re-raise other TKA exceptions as-is
                raise

            except Exception as e:
                # Convert unexpected exceptions to ServiceOperationError
                error_context = {
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys()) if kwargs else [],
                    "error_type": type(e).__name__,
                }

                logger.log(
                    log_level,
                    f"Service operation failed: {op_name}",
                    extra={
                        "service": service_name,
                        "operation": func.__name__,
                        "error": str(e),
                        "context": error_context,
                    },
                )

                raise service_error(
                    message=str(e),
                    service_name=service_name,
                    operation=func.__name__,
                    **error_context,
                ) from e

        return wrapper

    return decorator


def validate_inputs(**validators: Callable[[Any], bool]) -> Callable:
    """
    Decorator for input validation.

    Args:
        validators: Dictionary mapping parameter names to validation functions

    Returns:
        Decorated function with input validation

    Example:
        @validate_inputs(
            data=lambda x: x is not None,
            size=lambda x: isinstance(x, tuple) and len(x) == 2
        )
        def process_data(self, data: Any, size: tuple) -> Any:
            # Implementation here
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature to map args to parameter names
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate each specified parameter
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValidationError(
                            message=f"Validation failed for parameter {param_name}",
                            field=param_name,
                            value=value,
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_operation(
    log_level: int = logging.INFO,
    include_args: bool = False,
    include_result: bool = False,
    include_duration: bool = True,
) -> Callable:
    """
    Decorator for operation logging.

    Args:
        log_level: Logging level for operation messages
        include_args: Whether to log function arguments
        include_result: Whether to log function result
        include_duration: Whether to log operation duration

    Returns:
        Decorated function with operation logging
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter() if include_duration else None

            # Determine operation name
            if args and hasattr(args[0], "__class__"):
                op_name = f"{args[0].__class__.__name__}.{func.__name__}"
            else:
                op_name = func.__name__

            # Log operation start
            log_data = {"operation": op_name}
            if include_args:
                log_data["args"] = str(args[1:])  # Skip self
                log_data["kwargs"] = str(kwargs)

            logger.log(log_level, f"Starting operation: {op_name}", extra=log_data)

            try:
                result = func(*args, **kwargs)

                # Log operation completion
                if include_duration and start_time:
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    log_data["duration_ms"] = str(round(duration_ms, 2))

                if include_result:
                    log_data["result_type"] = type(result).__name__

                logger.log(log_level, f"Completed operation: {op_name}", extra=log_data)
                return result

            except Exception as e:
                # Log operation failure
                if include_duration and start_time:
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    log_data["duration_ms"] = str(round(duration_ms, 2))

                log_data["error"] = str(e)
                log_data["error_type"] = type(e).__name__

                logger.log(
                    logging.ERROR, f"Failed operation: {op_name}", extra=log_data
                )
                raise

        return wrapper

    return decorator


def retry_on_failure(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
) -> Callable:
    """
    Decorator for retrying operations on failure.

    Args:
        max_attempts: Maximum number of retry attempts
        delay_seconds: Initial delay between retries
        backoff_multiplier: Multiplier for exponential backoff
        exceptions: Exception types to retry on

    Returns:
        Decorated function with retry logic
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = delay_seconds

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:  # Don't delay after last attempt
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_multiplier
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )

            # Re-raise the last exception if all attempts failed
            raise last_exception

        return wrapper

    return decorator


def performance_critical(
    max_duration_ms: Optional[float] = None,
    max_memory_mb: Optional[float] = None,
    warn_threshold_ms: Optional[float] = None,
) -> Callable:
    """
    Decorator for performance-critical operations.

    Args:
        max_duration_ms: Maximum allowed duration in milliseconds
        max_memory_mb: Maximum allowed memory usage in MB
        warn_threshold_ms: Warning threshold for duration

    Returns:
        Decorated function with performance monitoring
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import psutil
            from .exceptions import PerformanceError

            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024

            try:
                result = func(*args, **kwargs)

                # Check performance metrics
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024

                duration_ms = (end_time - start_time) * 1000
                memory_used_mb = end_memory - start_memory

                op_name = (
                    f"{args[0].__class__.__name__}.{func.__name__}"
                    if args
                    else func.__name__
                )

                # Check duration thresholds
                if max_duration_ms and duration_ms > max_duration_ms:
                    raise PerformanceError(
                        message=f"Operation exceeded maximum duration",
                        operation=op_name,
                        threshold=max_duration_ms,
                        actual=duration_ms,
                        metric_type="duration_ms",
                    )

                if warn_threshold_ms and duration_ms > warn_threshold_ms:
                    logger.warning(
                        f"Performance warning: {op_name} took {duration_ms:.1f}ms "
                        f"(threshold: {warn_threshold_ms}ms)"
                    )

                # Check memory thresholds
                if max_memory_mb and memory_used_mb > max_memory_mb:
                    raise PerformanceError(
                        message=f"Operation exceeded maximum memory usage",
                        operation=op_name,
                        threshold=max_memory_mb,
                        actual=memory_used_mb,
                        metric_type="memory_mb",
                    )

                return result

            except Exception:
                raise

        return wrapper

    return decorator
