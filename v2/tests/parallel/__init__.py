"""
TKA Parallel Testing Framework
=============================

Comprehensive parallel testing system that validates functional equivalence
between V1 and V2 implementations during the migration process.

This framework ensures V2 maintains exact parity with V1's behavior while
respecting the consolidated service architecture and preventing regressions
in critical systems like arrow rendering.

Components:
- actions/: Action abstraction layer with validation
- drivers/: Version-specific application drivers  
- comparison/: Deep result comparison engine
- scenarios/: Comprehensive test scenarios
- reporting/: Automated reporting system

Usage:
    python tests/parallel/master_parallel_test.py --scenario basic_workflows
    python tests/parallel/master_parallel_test.py --all --report
"""

__version__ = "1.0.0"

# Test lifecycle metadata
TEST_LIFECYCLE = "SCAFFOLDING"
DELETE_AFTER = "V1 deprecation complete"
PURPOSE = "Validate V1/V2 functional equivalence during migration"
CREATED = "2025-06-15"
AUTHOR = "Augment Agent"
