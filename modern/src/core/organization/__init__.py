"""
TKA Desktop Code Organization Module

A+ Enhancement: Comprehensive code organization tools for import standardization,
component hierarchy optimization, and architectural consistency enforcement.

ARCHITECTURE: Provides automated tools to maintain code organization standards
and enforce architectural best practices across the TKA Desktop codebase.

EXPORTS:
- ImportStandardizer: Tool for enforcing consistent import patterns
- ComponentHierarchyOptimizer: Tool for optimizing component hierarchies
- Analysis and report classes for code organization metrics
"""

# Import Standardization
from .import_standardizer import (
    ImportStandardizer,
    ComponentHierarchyOptimizer,
    ImportAnalysis,
    ImportStandardizationReport,
    ComponentHierarchyAnalysis,
)

__all__ = [
    "ImportStandardizer",
    "ComponentHierarchyOptimizer", 
    "ImportAnalysis",
    "ImportStandardizationReport",
    "ComponentHierarchyAnalysis",
]
