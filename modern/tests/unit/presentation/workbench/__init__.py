"""
TKA Modern Test Suite
================

Comprehensive testing framework for The Kinetic Constructor.

Test Categories:
- unit/: Fast service layer tests (<1s total)
- integration/: Component communication tests (<10s total)
- ui/: User interface behavior tests (<30s total)
- parity/: Legacy functionality parity tests (<60s total)

Usage:
    python -m pytest tests/                    # Run all tests
    python -m pytest tests/unit/              # Run only unit tests
    python -m pytest tests/integration/       # Run only integration tests
    python -m pytest tests/ui/                # Run only UI tests
    python -m pytest tests/parity/            # Run only parity tests
    python -m pytest -m "not slow"            # Skip slow tests
"""

__version__ = "2.0.0"
