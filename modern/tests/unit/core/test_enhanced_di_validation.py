"""
Test enhanced dependency injection validation and error handling.

This test suite validates the enhanced DI container features including:
- Comprehensive error handling with custom exceptions
- Circular dependency detection with detailed error messages
- Registration validation
- Dependency graph generation
"""

import pytest
from typing import Protocol
from abc import ABC, abstractmethod

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from src.core.dependency_injection.di_container import DIContainer
from src.core.exceptions import DependencyInjectionError


# Test interfaces and implementations
class IRepository(Protocol):
    def get_data(self) -> str: ...


class IService(Protocol):
    def process(self) -> str: ...


class IController(Protocol):
    def handle_request(self) -> str: ...


class Repository:
    def get_data(self) -> str:
        return "data"


class Service:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def process(self) -> str:
        return f"processed: {self.repository.get_data()}"


class Controller:
    def __init__(self, service: IService):
        self.service = service

    def handle_request(self) -> str:
        return f"handled: {self.service.process()}"


class CircularA:
    def __init__(self, b: "CircularB"):
        self.b = b


class CircularB:
    def __init__(self, a: CircularA):
        self.a = a


class InvalidService:
    def __init__(self, missing_dependency: "NonExistentService"):
        self.missing = missing_dependency


class TestEnhancedDIValidation:
    """Test enhanced DI container validation and error handling."""

    def setup_method(self):
        """Set up test container for each test."""
        self.container = DIContainer()

    def test_successful_registration_validation(self):
        """Test that valid registrations pass validation."""
        # Register valid services
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)
        self.container.register_singleton(IController, Controller)

        # Validation should pass without errors
        self.container.validate_all_registrations()

    def test_missing_dependency_validation_error(self):
        """Test that missing dependencies are caught during validation."""
        # Register service with missing dependency
        self.container.register_singleton(IService, InvalidService)

        # Validation should fail with detailed error
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.validate_all_registrations()

        error = exc_info.value
        assert "Registration validation failed" in str(error)
        assert "NonExistentService" in str(error)
        assert "is not registered" in str(error)

    def test_circular_dependency_detection(self):
        """Test circular dependency detection with detailed error messages."""
        # Register circular dependencies
        self.container.register_singleton(CircularA, CircularA)
        self.container.register_singleton(CircularB, CircularB)

        # Resolution should fail with circular dependency error
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(CircularA)

        error = exc_info.value
        assert "Circular dependency detected" in str(error)
        assert error.interface_name == "CircularA"
        assert error.dependency_chain is not None
        assert len(error.dependency_chain) > 0

    def test_enhanced_error_messages_for_missing_service(self):
        """Test enhanced error messages when resolving unregistered services."""
        # Register some services for context
        self.container.register_singleton(IRepository, Repository)

        # Try to resolve unregistered service
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IService)

        error = exc_info.value
        assert "IService is not registered" in str(error)
        assert "Available services:" in str(error)
        assert "IRepository" in str(error)
        assert error.interface_name == "IService"

    def test_dependency_resolution_error_context(self):
        """Test that dependency resolution errors include proper context."""
        # Register service with missing dependency
        self.container.register_singleton(IService, InvalidService)

        # Try to resolve - should fail with context
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IService)

        error = exc_info.value
        assert "Cannot resolve dependency" in str(error)
        assert "NonExistentService" in str(error)
        assert "for parameter 'missing_dependency'" in str(error)
        assert "in InvalidService" in str(error)

    def test_dependency_graph_generation(self):
        """Test dependency graph generation for debugging."""
        # Register services with dependencies
        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, Service)
        self.container.register_singleton(IController, Controller)

        # Generate dependency graph
        graph = self.container.get_dependency_graph()

        # Verify graph structure
        assert "IRepository" in graph
        assert "IService" in graph
        assert "IController" in graph

        # Repository has no dependencies
        assert graph["IRepository"] == []

        # Service depends on Repository
        assert "IRepository" in graph["IService"]

        # Controller depends on Service
        assert "IService" in graph["IController"]

    def test_singleton_instance_creation_error(self):
        """Test error handling during singleton instance creation."""

        class FailingService:
            def __init__(self):
                raise ValueError("Initialization failed")

        self.container.register_singleton(IService, FailingService)

        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IService)

        error = exc_info.value
        assert "Failed to create singleton instance" in str(error)
        assert "Initialization failed" in str(error)
        assert error.interface_name == "IService"

    def test_transient_instance_creation_error(self):
        """Test error handling during transient instance creation."""

        class FailingService:
            def __init__(self):
                raise RuntimeError("Transient creation failed")

        self.container.register_transient(IService, FailingService)

        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IService)

        error = exc_info.value
        assert "Failed to create transient instance" in str(error)
        assert "Transient creation failed" in str(error)
        assert error.interface_name == "IService"

    def test_complex_dependency_chain_error(self):
        """Test error reporting in complex dependency chains."""

        # Create a chain: Controller -> Service -> InvalidService (missing dependency)
        class ChainedService:
            def __init__(self, invalid: InvalidService):
                self.invalid = invalid

        self.container.register_singleton(IRepository, Repository)
        self.container.register_singleton(IService, ChainedService)
        self.container.register_singleton(IController, Controller)
        self.container.register_singleton(InvalidService, InvalidService)

        # Try to resolve controller - should fail with detailed chain info
        with pytest.raises(DependencyInjectionError) as exc_info:
            self.container.resolve(IController)

        error = exc_info.value
        # Should contain information about the dependency chain
        assert "Cannot resolve dependency" in str(error)
        assert "NonExistentService" in str(error)


if __name__ == "__main__":
    pytest.main([__file__])
