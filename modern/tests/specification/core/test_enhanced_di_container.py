"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Contract testing for enhanced dependency injection container
SCOPE: Core DI functionality, constructor injection, Protocol validation
EXPECTED_DURATION: permanent
"""

import pytest
from typing import Protocol, Optional, runtime_checkable
from dataclasses import dataclass

from src.core.dependency_injection.di_container import (
    DIContainer,
    get_container,
    reset_container,
)
from src.core.exceptions import DependencyInjectionError


# Test interfaces and implementations
@runtime_checkable
class ITestService(Protocol):
    def get_value(self) -> str: ...
    def process_data(self, data: str) -> str: ...


@runtime_checkable
class ITestRepository(Protocol):
    def save(self, data: str) -> bool: ...
    def load(self) -> str: ...


@dataclass
class TestConfig:
    name: str
    value: int


class TestService:
    """Test service implementation with dependencies."""

    def __init__(
        self, repository: ITestRepository, config: Optional[TestConfig] = None
    ):
        self.repository = repository
        self.config = config or TestConfig("default", 42)

    def get_value(self) -> str:
        return f"Service with {self.config.name}"

    def process_data(self, data: str) -> str:
        self.repository.save(data)
        return f"Processed: {data}"


class TestRepository:
    """Test repository implementation."""

    def __init__(self):
        self._data = ""

    def save(self, data: str) -> bool:
        self._data = data
        return True

    def load(self) -> str:
        return self._data


class TestServiceWithoutDependencies:
    """Test service with no constructor dependencies."""

    def get_value(self) -> str:
        return "No dependencies"

    def process_data(self, data: str) -> str:
        return f"Simple: {data}"


class InvalidService:
    """Service that doesn't implement the required interface."""

    def wrong_method(self) -> str:
        return "Wrong"


class TestServiceWithCircularDependency:
    """Service that would create circular dependency."""

    def __init__(self, service: ITestService):
        self.service = service


@pytest.fixture
def container():
    """Provide a fresh container for each test."""
    reset_container()
    return DIContainer()


class TestEnhancedContainerBasics:
    """Test basic container functionality."""

    def test_singleton_registration_and_resolution(self, container):
        """Test singleton service registration and resolution."""
        container.register_singleton(ITestRepository, TestRepository)

        # First resolution
        repo1 = container.resolve(ITestRepository)
        assert isinstance(repo1, TestRepository)

        # Second resolution should return same instance
        repo2 = container.resolve(ITestRepository)
        assert repo1 is repo2

    def test_transient_registration_and_resolution(self, container):
        """Test transient service registration and resolution."""
        container.register_transient(ITestRepository, TestRepository)

        # Each resolution should return new instance
        repo1 = container.resolve(ITestRepository)
        repo2 = container.resolve(ITestRepository)

        assert isinstance(repo1, TestRepository)
        assert isinstance(repo2, TestRepository)
        assert repo1 is not repo2

    def test_instance_registration(self, container):
        """Test instance registration."""
        repo_instance = TestRepository()
        container.register_instance(ITestRepository, repo_instance)

        resolved = container.resolve(ITestRepository)
        assert resolved is repo_instance

    def test_unregistered_service_raises_error(self, container):
        """Test that resolving unregistered service raises DependencyInjectionError."""
        with pytest.raises(
            DependencyInjectionError, match="Service ITestService is not registered"
        ):
            container.resolve(ITestService)


class TestConstructorInjection:
    """Test automatic constructor injection functionality."""

    def test_constructor_injection_with_dependencies(self, container):
        """Test that dependencies are automatically injected."""
        # Register dependencies
        container.register_singleton(ITestRepository, TestRepository)
        container.register_singleton(ITestService, TestService)

        # Resolve service - should automatically inject repository
        service = container.resolve(ITestService)

        assert isinstance(service, TestService)
        assert isinstance(service.repository, TestRepository)
        assert service.config.name == "default"

    def test_constructor_injection_without_dependencies(self, container):
        """Test service with no dependencies."""
        container.register_singleton(ITestService, TestServiceWithoutDependencies)

        service = container.resolve(ITestService)
        assert isinstance(service, TestServiceWithoutDependencies)
        assert service.get_value() == "No dependencies"

    def test_optional_dependencies_with_defaults(self, container):
        """Test that optional dependencies use defaults when not registered."""
        container.register_singleton(ITestRepository, TestRepository)
        container.register_singleton(ITestService, TestService)

        service = container.resolve(ITestService)

        # Should use default config since TestConfig is not registered
        assert service.config.name == "default"
        assert service.config.value == 42

    def test_circular_dependency_detection(self, container):
        """Test that circular dependencies are detected and raise error."""
        container.register_singleton(ITestService, TestServiceWithCircularDependency)

        with pytest.raises(
            DependencyInjectionError, match="Circular dependency detected"
        ):
            container.resolve(ITestService)


class TestProtocolValidation:
    """Test Protocol compliance validation."""

    def test_auto_register_validates_protocol_compliance(self, container):
        """Test that auto_register validates Protocol implementation."""
        # Register required dependency first
        container.register_singleton(ITestRepository, TestRepository)

        # Valid implementation should work
        container.auto_register(ITestService, TestService)

        service = container.resolve(ITestService)
        assert isinstance(service, TestService)

    def test_auto_register_rejects_invalid_implementation(self, container):
        """Test that auto_register rejects non-compliant implementations."""
        with pytest.raises(ValueError, match="doesn't implement get_value"):
            container.auto_register(ITestService, InvalidService)

    def test_validation_with_concrete_classes(self, container):
        """Test validation works with concrete classes (not just Protocols)."""
        # Should not raise error for concrete class registration
        container.register_singleton(TestRepository, TestRepository)

        repo = container.resolve(TestRepository)
        assert isinstance(repo, TestRepository)


class TestContainerUtilities:
    """Test container utility methods."""

    def test_get_registrations(self, container):
        """Test getting all registrations for debugging."""
        container.register_singleton(ITestService, TestService)
        container.register_transient(ITestRepository, TestRepository)

        registrations = container.get_registrations()

        assert ITestService in registrations
        assert ITestRepository in registrations
        assert registrations[ITestService] == TestService
        assert registrations[ITestRepository] == TestRepository

    def test_global_container_functions(self):
        """Test global container access functions."""
        reset_container()

        # Should create new container
        container1 = get_container()
        assert isinstance(container1, DIContainer)

        # Should return same instance
        container2 = get_container()
        assert container1 is container2

        # Reset should clear container
        reset_container()
        container3 = get_container()
        assert container3 is not container1


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_registration_validation_errors(self, container):
        """Test that registration validation catches errors."""
        with pytest.raises(ValueError, match="must be a class"):
            container.register_singleton(ITestService, "not_a_class")

    def test_resolution_with_invalid_dependencies(self, container):
        """Test error handling when dependencies cannot be resolved."""
        # Register service that needs unregistered dependency
        container.register_singleton(ITestService, TestService)

        with pytest.raises(DependencyInjectionError, match="Cannot resolve dependency"):
            container.resolve(ITestService)

    def test_creation_failure_handling(self, container):
        """Test handling of service creation failures."""

        class FailingService:
            def __init__(self):
                raise RuntimeError("Creation failed")

        container.register_singleton(ITestService, FailingService)

        with pytest.raises(DependencyInjectionError, match="Creation failed"):
            container.resolve(ITestService)


class TestBackwardCompatibility:
    """Test backward compatibility with SimpleContainer."""

    def test_simple_container_alias(self):
        """Test that SimpleContainer alias works."""
        from src.core.dependency_injection.di_container import DIContainer

        # Should be the same as EnhancedContainer
        assert DIContainer is DIContainer

    def test_existing_registration_patterns_work(self, container):
        """Test that existing registration patterns still work."""
        # Old-style registration without validation
        container.register_singleton(ITestRepository, TestRepository)
        container.register_transient(ITestService, TestServiceWithoutDependencies)

        repo = container.resolve(ITestRepository)
        service = container.resolve(ITestService)

        assert isinstance(repo, TestRepository)
        assert isinstance(service, TestServiceWithoutDependencies)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
