"""
Result Comparison Engine
========================

Deep comparison engine for validating V1/V2 functional equivalence.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: V1 deprecation complete
PURPOSE: Provide result comparison capabilities for V1/V2 parallel testing
"""

from .result_comparer import (
    ComparisonType,
    ComparisonRule,
    FieldDifference,
    ComparisonResult,
    IResultComparer,
    ResultComparer,
    TKADataNormalizer,
)

__all__ = [
    # Core comparison types
    "ComparisonType",
    "ComparisonRule",
    "FieldDifference",
    "ComparisonResult",
    
    # Comparison interfaces and implementations
    "IResultComparer",
    "ResultComparer",
    
    # TKA-specific utilities
    "TKADataNormalizer",
]
