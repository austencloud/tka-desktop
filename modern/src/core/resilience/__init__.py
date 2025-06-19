"""
TKA Desktop Resilience Module

A+ Enhancement: Comprehensive resilience patterns for robust error handling,
circuit breaker protection, and error aggregation capabilities.

ARCHITECTURE: Provides enterprise-grade resilience patterns including:
- Circuit Breaker Pattern for external dependency protection
- Error Aggregation System for batch operation error handling
- Predictive Error Detection for proactive error prevention
- Graceful Degradation Strategies for service failures

EXPORTS:
- CircuitBreaker: Circuit breaker implementation
- circuit_breaker: Circuit breaker decorator
- ErrorAggregator: Error aggregation system
- aggregate_errors: Error aggregation decorator
- Error severity and state enums
"""

# Circuit Breaker Pattern
from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerState,
    CircuitBreakerError,
    CircuitBreakerConfig,
    CircuitBreakerMetrics,
    circuit_breaker,
)

# Error Aggregation System
from .error_aggregation import (
    ErrorAggregator,
    ErrorRecord,
    ErrorGroup,
    ErrorSummary,
    ErrorSeverity,
    aggregate_errors,
)

__all__ = [
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerState", 
    "CircuitBreakerError",
    "CircuitBreakerConfig",
    "CircuitBreakerMetrics",
    "circuit_breaker",
    
    # Error Aggregation
    "ErrorAggregator",
    "ErrorRecord",
    "ErrorGroup", 
    "ErrorSummary",
    "ErrorSeverity",
    "aggregate_errors",
]
