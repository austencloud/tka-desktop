"""
Circuit Breaker Pattern Implementation for TKA Desktop

A+ Enhancement: Provides resilient external dependency management with
configurable failure thresholds and graceful degradation strategies.

ARCHITECTURE: Implements the Circuit Breaker pattern to prevent cascade failures
and provide automatic recovery for external service dependencies.
"""

import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, Dict, Type, Union
from dataclasses import dataclass, field
from threading import Lock
from collections import deque

from ..exceptions import TKABaseException

logger = logging.getLogger(__name__)


class CircuitBreakerState(Enum):
    """Circuit breaker states following the standard pattern."""

    CLOSED = "closed"  # Normal operation - requests pass through
    OPEN = "open"  # Failing - reject requests immediately
    HALF_OPEN = "half_open"  # Testing recovery - limited requests allowed


class CircuitBreakerError(TKABaseException):
    """Raised when circuit breaker is open and blocking requests."""

    def __init__(
        self,
        service_name: str,
        state: CircuitBreakerState,
        context: Optional[Dict[str, Any]] = None,
    ):
        message = (
            f"Circuit breaker for '{service_name}' is {state.value} - request blocked"
        )
        super().__init__(message, context)
        self.service_name = service_name
        self.state = state


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""

    failure_threshold: int = 5  # Number of failures before opening
    recovery_timeout: float = 30.0  # Seconds before attempting recovery
    success_threshold: int = 3  # Successes needed to close from half-open
    timeout: float = 10.0  # Request timeout in seconds
    monitored_exceptions: tuple = (Exception,)  # Exceptions that count as failures


@dataclass
class CircuitBreakerMetrics:
    """Metrics for circuit breaker monitoring."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rejected_requests: int = 0
    state_changes: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    failure_rate: float = 0.0

    def update_failure_rate(self):
        """Update the failure rate calculation."""
        if self.total_requests > 0:
            self.failure_rate = self.failed_requests / self.total_requests
        else:
            self.failure_rate = 0.0


class CircuitBreaker:
    """
    Circuit Breaker implementation for resilient external service calls.

    A+ Enhancement: Provides automatic failure detection, request blocking,
    and recovery testing to prevent cascade failures.
    """

    def __init__(
        self, service_name: str, config: Optional[CircuitBreakerConfig] = None
    ):
        """
        Initialize circuit breaker for a specific service.

        Args:
            service_name: Name of the service being protected
            config: Circuit breaker configuration
        """
        self.service_name = service_name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitBreakerState.CLOSED
        self.metrics = CircuitBreakerMetrics()

        # Thread safety
        self._lock = Lock()

        # Failure tracking
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._recent_failures = deque(maxlen=self.config.failure_threshold * 2)

        logger.info(f"Circuit breaker initialized for service '{service_name}'")

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function call through the circuit breaker.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerError: If circuit is open
            Original exception: If function fails and circuit allows it
        """
        with self._lock:
            self.metrics.total_requests += 1

            # Check if circuit should block the request
            if self._should_block_request():
                self.metrics.rejected_requests += 1
                raise CircuitBreakerError(
                    self.service_name,
                    self.state,
                    context={
                        "failure_count": self._failure_count,
                        "last_failure_time": self._last_failure_time,
                        "metrics": self.metrics.__dict__,
                    },
                )

        # Execute the function
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time

            # Record success
            with self._lock:
                self._record_success(execution_time)

            return result

        except self.config.monitored_exceptions as e:
            execution_time = time.perf_counter() - start_time

            # Record failure
            with self._lock:
                self._record_failure(e, execution_time)

            raise

    def _should_block_request(self) -> bool:
        """Determine if the request should be blocked based on circuit state."""
        current_time = time.time()

        if self.state == CircuitBreakerState.CLOSED:
            return False

        elif self.state == CircuitBreakerState.OPEN:
            # Check if recovery timeout has passed
            if current_time - self._last_failure_time >= self.config.recovery_timeout:
                self._transition_to_half_open()
                return False
            return True

        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Allow limited requests to test recovery
            return False

        return False

    def _record_success(self, execution_time: float):
        """Record a successful operation."""
        self.metrics.successful_requests += 1
        self.metrics.last_success_time = time.time()
        self.metrics.update_failure_rate()

        if self.state == CircuitBreakerState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.config.success_threshold:
                self._transition_to_closed()

        logger.debug(
            f"Circuit breaker '{self.service_name}': Success recorded (time: {execution_time:.3f}s)"
        )

    def _record_failure(self, exception: Exception, execution_time: float):
        """Record a failed operation."""
        current_time = time.time()

        self.metrics.failed_requests += 1
        self.metrics.last_failure_time = current_time
        self.metrics.update_failure_rate()

        self._failure_count += 1
        self._last_failure_time = current_time
        self._recent_failures.append((current_time, str(exception)))

        # Check if we should open the circuit
        if self.state == CircuitBreakerState.CLOSED:
            if self._failure_count >= self.config.failure_threshold:
                self._transition_to_open()

        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Any failure in half-open state goes back to open
            self._transition_to_open()

        logger.warning(
            f"Circuit breaker '{self.service_name}': Failure recorded "
            f"(count: {self._failure_count}, time: {execution_time:.3f}s, error: {exception})"
        )

    def _transition_to_open(self):
        """Transition circuit breaker to OPEN state."""
        if self.state != CircuitBreakerState.OPEN:
            self.state = CircuitBreakerState.OPEN
            self.metrics.state_changes += 1
            self._success_count = 0

            logger.error(
                f"Circuit breaker '{self.service_name}' OPENED - "
                f"failure threshold ({self.config.failure_threshold}) exceeded"
            )

    def _transition_to_half_open(self):
        """Transition circuit breaker to HALF_OPEN state."""
        if self.state != CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.HALF_OPEN
            self.metrics.state_changes += 1
            self._success_count = 0

            logger.info(
                f"Circuit breaker '{self.service_name}' HALF-OPEN - "
                f"testing recovery after {self.config.recovery_timeout}s timeout"
            )

    def _transition_to_closed(self):
        """Transition circuit breaker to CLOSED state."""
        if self.state != CircuitBreakerState.CLOSED:
            self.state = CircuitBreakerState.CLOSED
            self.metrics.state_changes += 1
            self._failure_count = 0
            self._success_count = 0
            self._recent_failures.clear()

            logger.info(
                f"Circuit breaker '{self.service_name}' CLOSED - "
                f"recovery successful after {self.config.success_threshold} successes"
            )

    def get_metrics(self) -> CircuitBreakerMetrics:
        """Get current circuit breaker metrics."""
        with self._lock:
            return CircuitBreakerMetrics(
                total_requests=self.metrics.total_requests,
                successful_requests=self.metrics.successful_requests,
                failed_requests=self.metrics.failed_requests,
                rejected_requests=self.metrics.rejected_requests,
                state_changes=self.metrics.state_changes,
                last_failure_time=self.metrics.last_failure_time,
                last_success_time=self.metrics.last_success_time,
                failure_rate=self.metrics.failure_rate,
            )

    def reset(self):
        """Reset circuit breaker to initial state."""
        with self._lock:
            self.state = CircuitBreakerState.CLOSED
            self.metrics = CircuitBreakerMetrics()
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = 0.0
            self._recent_failures.clear()

        logger.info(f"Circuit breaker '{self.service_name}' reset to initial state")


# ============================================================================
# CIRCUIT BREAKER DECORATOR - A+ Enhancement
# ============================================================================


def circuit_breaker(
    service_name: Optional[str] = None,
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
    success_threshold: int = 3,
    monitored_exceptions: tuple = (Exception,),
) -> Callable:
    """
    Decorator to apply circuit breaker pattern to functions.

    A+ Enhancement: Provides declarative circuit breaker protection
    for external service calls and critical operations.

    Args:
        service_name: Name of the service (defaults to function name)
        failure_threshold: Failures before opening circuit
        recovery_timeout: Seconds before testing recovery
        success_threshold: Successes needed to close circuit
        monitored_exceptions: Exception types that trigger circuit

    Returns:
        Decorated function with circuit breaker protection
    """

    def decorator(func: Callable) -> Callable:
        # Create circuit breaker for this function
        name = service_name or f"{func.__module__}.{func.__name__}"
        config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            success_threshold=success_threshold,
            monitored_exceptions=monitored_exceptions,
        )
        breaker = CircuitBreaker(name, config)

        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)

        # Attach circuit breaker to function for monitoring
        wrapper._circuit_breaker = breaker
        return wrapper

    return decorator
