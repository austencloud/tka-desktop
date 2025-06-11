"""
Standalone Tab System

A comprehensive system for running individual tabs as standalone applications.

This package provides:
- Core infrastructure for standalone tab execution
- Individual tab implementations
- Standalone services and utilities
- Comprehensive testing framework
- Documentation and examples

Quick Start:
    python src/standalone/core/launcher.py construct
    python src/standalone/core/launcher.py generate
    python src/standalone/core/launcher.py browse

For more information, see docs/README.md
"""

__version__ = "1.0.0"
__author__ = "Kinetic Constructor Team"

# Core exports
from .core.base_runner import BaseStandaloneRunner, create_standalone_runner
from .core.launcher import main as launcher_main

# Service exports
from .services.image_creator.image_creator import StandaloneImageCreator

__all__ = [
    "BaseStandaloneRunner",
    "create_standalone_runner",
    "launcher_main",
    "StandaloneImageCreator",
]
