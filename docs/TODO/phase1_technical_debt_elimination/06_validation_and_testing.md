# **Task 1.5: Comprehensive DI Testing**

**Timeline**: Day 5  
**Priority**: CRITICAL  
**Goal**: Create bulletproof test suite for the enhanced DI container

---

## **Create Test Suite:**

### **FILE: tests/specification/core/test_enhanced_di_container.py**

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce enhanced DI container behavioral contracts
PERMANENT: Core infrastructure must be bulletproof
AUTHOR: @developer
"""

import pytest
from typing import Protocol, runtime_checkable
from src.core.dependency_injection.di_container import DIContainer

class TestEnhancedDIContainer:

    def test_auto_injection_with_complex_dependencies(self):
        """Test automatic injection of multi-level dependencies."""
        container = DIContainer()

        @runtime_checkable
        class IRepository(Protocol):
            def save(self, data: str) -> None: ...

        @runtime_checkable
        class IService(Protocol):
            def process(self, input: str) -> str: ...

        class Repository:
            def save(self, data: str) -> None:
                pass

        class Service:
            def __init__(self, repo: IRepository):
                self.repo = repo

            def process(self, input: str) -> str:
                return f"processed: {input}"

        class Controller:
            def __init__(self, service: IService, config: str = "default"):
                self.service = service
                self.config = config

        # Register services
        container.auto_register_with_validation(IRepository, Repository)
        container.auto_register_with_validation(IService, Service)

        # Test complex dependency resolution
        controller = container._create_instance(Controller)
        assert isinstance(controller.service, Service)
        assert controller.config == "default"

    def test_dependency_chain_validation(self):
        """Test validation of complete dependency chains."""
        container = DIContainer()

        class MissingDependency:
            pass

        class ServiceWithMissingDep:
            def __init__(self, missing: MissingDependency):
                self.missing = missing

        # Should raise error for missing dependency
        with pytest.raises(ValueError, match="is not registered"):
            container._validate_dependency_chain(ServiceWithMissingDep)

    def test_enhanced_error_reporting(self):
        """Test detailed error messages for resolution failures."""
        container = DIContainer()

        diagnosis = container.diagnose_resolution_failure(str)  # Unregistered type
        assert "is not registered" in diagnosis
        assert "Available interfaces:" in diagnosis

    def test_registration_validation(self):
        """Test comprehensive validation of all registrations."""
        container = DIContainer()

        class ValidService:
            pass

        container.register_singleton(str, ValidService)  # Valid registration

        # Should validate successfully
        container.validate_all_registrations()

    def test_primitive_type_handling(self):
        """Test that primitive types are handled correctly."""
        container = DIContainer()

        class ServiceWithPrimitives:
            def __init__(self, name: str = "default", count: int = 0, active: bool = True):
                self.name = name
                self.count = count
                self.active = active

        # Should create instance without trying to inject primitives
        instance = container._create_instance(ServiceWithPrimitives)
        assert instance.name == "default"
        assert instance.count == 0
        assert instance.active is True

    def test_circular_dependency_detection(self):
        """Test detection of circular dependencies."""
        container = DIContainer()

        class ServiceA:
            def __init__(self, service_b: 'ServiceB'):
                self.service_b = service_b

        class ServiceB:
            def __init__(self, service_a: ServiceA):
                self.service_a = service_a

        # Register services
        container.register_singleton(ServiceA, ServiceA)
        container.register_singleton(ServiceB, ServiceB)

        # Should detect circular dependency
        with pytest.raises(ValueError, match="Circular dependency detected"):
            container._detect_circular_dependencies(ServiceA)

    def test_optional_dependencies(self):
        """Test handling of Optional[T] dependencies."""
        from typing import Optional
        container = DIContainer()

        class OptionalService:
            pass

        class ServiceWithOptional:
            def __init__(self, optional_dep: Optional[OptionalService] = None):
                self.optional_dep = optional_dep

        # Should work even though OptionalService is not registered
        instance = container._create_instance(ServiceWithOptional)
        assert instance.optional_dep is None

    def test_protocol_validation(self):
        """Test protocol implementation validation."""
        container = DIContainer()

        @runtime_checkable
        class ITestProtocol(Protocol):
            def required_method(self) -> str: ...

        class ValidImplementation:
            def required_method(self) -> str:
                return "valid"

        class InvalidImplementation:
            pass  # Missing required_method

        # Valid implementation should work
        container._validate_protocol_implementation(ITestProtocol, ValidImplementation)

        # Invalid implementation should fail
        with pytest.raises(ValueError, match="does not implement"):
            container._validate_protocol_implementation(ITestProtocol, InvalidImplementation)

    def test_dependency_graph_generation(self):
        """Test dependency graph generation."""
        container = DIContainer()

        @runtime_checkable
        class IRepo(Protocol):
            pass

        @runtime_checkable
        class IService(Protocol):
            pass

        class Repo:
            pass

        class Service:
            def __init__(self, repo: IRepo):
                self.repo = repo

        container.auto_register_with_validation(IRepo, Repo)
        container.auto_register_with_validation(IService, Service)

        graph = container.get_dependency_graph()

        # Should show Service depends on IRepo
        service_key = next(key for key in graph.keys() if "IService" in key)
        assert "IRepo" in graph[service_key]

    def test_health_validation(self):
        """Test comprehensive health validation."""
        container = DIContainer()

        class HealthyService:
            pass

        class UnhealthyService:
            def __init__(self, missing: 'MissingService'):
                self.missing = missing

        container.register_singleton(HealthyService, HealthyService)
        container.register_singleton(UnhealthyService, UnhealthyService)

        health_ok, issues = container.validate_registration_health()

        assert not health_ok
        assert len(issues) > 0
        assert any("depends on unregistered" in issue for issue in issues)

    def test_resolution_path_tracing(self):
        """Test resolution path tracing for debugging."""
        container = DIContainer()

        @runtime_checkable
        class IRepo(Protocol):
            pass

        @runtime_checkable
        class IService(Protocol):
            pass

        class Repo:
            pass

        class Service:
            def __init__(self, repo: IRepo):
                self.repo = repo

        container.auto_register_with_validation(IRepo, Repo)
        container.auto_register_with_validation(IService, Service)

        path = container.get_resolution_path(IService)

        # Should show full resolution path
        assert len(path) >= 2  # IService and its IRepo dependency
        assert any("IService" in step for step in path)
        assert any("IRepo" in step for step in path)

class TestDIContainerIntegration:
    """Integration tests with real TKA services."""

    def test_tka_service_registration(self):
        """Test registration of actual TKA services."""
        from src.application.services.core.sequence_management_service import (
            ISequenceManagementService, SequenceManagementService
        )
        from src.core.events.event_bus import IEventBus, TypeSafeEventBus

        container = DIContainer()

        # Register dependencies first
        container.auto_register_with_validation(IEventBus, TypeSafeEventBus)

        # Register main service
        container.auto_register_with_validation(
            ISequenceManagementService,
            SequenceManagementService
        )

        # Should be able to resolve
        service = container.resolve(ISequenceManagementService)
        assert service is not None
        assert isinstance(service.event_bus, TypeSafeEventBus)

    def test_all_tka_services_health(self):
        """Test that all TKA services can be registered and resolved."""
        container = DIContainer()

        # Register all TKA services (you would add all your actual services here)
        service_registrations = [
            # Add your actual service registrations
            # (IEventBus, TypeSafeEventBus),
            # (ISequenceManagementService, SequenceManagementService),
            # ... etc
        ]

        for interface, implementation in service_registrations:
            container.auto_register_with_validation(interface, implementation)

        # Validate all can be resolved
        container.validate_all_registrations()

        # Check health
        health_ok, issues = container.validate_registration_health()
        if not health_ok:
            pytest.fail(f"Service health check failed: {issues}")

class TestDIContainerPerformance:
    """Performance tests for DI container."""

    def test_resolution_performance(self):
        """Test that resolution is fast enough for production use."""
        import time
        container = DIContainer()

        class SimpleService:
            pass

        container.register_singleton(SimpleService, SimpleService)

        # Warm up
        container.resolve(SimpleService)

        # Time multiple resolutions
        start_time = time.perf_counter()
        for _ in range(1000):
            container.resolve(SimpleService)
        end_time = time.perf_counter()

        avg_time_ms = ((end_time - start_time) / 1000) * 1000

        # Should be fast (less than 0.1ms per resolution on average)
        assert avg_time_ms < 0.1, f"Resolution too slow: {avg_time_ms:.3f}ms average"

    def test_complex_dependency_creation_performance(self):
        """Test performance of creating complex dependency chains."""
        import time
        container = DIContainer()

        class Level1:
            pass

        class Level2:
            def __init__(self, dep: Level1):
                self.dep = dep

        class Level3:
            def __init__(self, dep: Level2):
                self.dep = dep

        class Level4:
            def __init__(self, dep: Level3):
                self.dep = dep

        container.register_singleton(Level1, Level1)
        container.register_singleton(Level2, Level2)
        container.register_singleton(Level3, Level3)
        container.register_singleton(Level4, Level4)

        # Time creation of complex dependency chain
        start_time = time.perf_counter()
        for _ in range(100):
            container.resolve(Level4)
        end_time = time.perf_counter()

        avg_time_ms = ((end_time - start_time) / 100) * 1000

        # Should be reasonable (less than 1ms per complex creation)
        assert avg_time_ms < 1.0, f"Complex creation too slow: {avg_time_ms:.3f}ms average"

class TestDIContainerErrorScenarios:
    """Test error scenarios and edge cases."""

    def test_missing_type_hints(self):
        """Test behavior with missing type hints."""
        container = DIContainer()

        class ServiceWithoutHints:
            def __init__(self, some_param):  # No type hint
                self.some_param = some_param

        # Should handle gracefully (skip parameters without type hints)
        instance = container._create_instance(ServiceWithoutHints)
        # Should use default parameter handling

    def test_invalid_type_annotations(self):
        """Test behavior with invalid type annotations."""
        container = DIContainer()

        class ServiceWithInvalidAnnotation:
            def __init__(self, param: "NonExistentType"):
                self.param = param

        # Should handle gracefully or provide clear error
        with pytest.raises((ValueError, NameError)):
            container._create_instance(ServiceWithInvalidAnnotation)

    def test_constructor_exceptions(self):
        """Test behavior when constructor raises exceptions."""
        container = DIContainer()

        class BrokenService:
            def __init__(self):
                raise ValueError("Constructor always fails")

        container.register_singleton(BrokenService, BrokenService)

        # Should propagate the constructor exception with context
        with pytest.raises(RuntimeError, match="Dependency injection failed"):
            container.resolve(BrokenService)

    def test_very_deep_dependency_chain(self):
        """Test behavior with very deep dependency chains."""
        container = DIContainer()

        # Create a chain of 20 dependencies
        classes = []
        for i in range(20):
            if i == 0:
                # Base class with no dependencies
                class_def = type(f"Service{i}", (), {"__init__": lambda self: None})
            else:
                # Each class depends on the previous one
                prev_class = classes[i-1]
                def make_init(dep_class):
                    def __init__(self, dep: dep_class):
                        self.dep = dep
                    return __init__

                class_def = type(f"Service{i}", (), {"__init__": make_init(prev_class)})

            classes.append(class_def)
            container.register_singleton(class_def, class_def)

        # Should be able to resolve the final service
        final_service = container.resolve(classes[-1])
        assert final_service is not None

        # Verify the chain is intact
        current = final_service
        for i in range(19, 0, -1):
            assert hasattr(current, 'dep')
            current = current.dep

# Test fixtures and utilities
@pytest.fixture
def clean_container():
    """Provide a clean DI container for each test."""
    return DIContainer()

@pytest.fixture
def populated_container():
    """Provide a container with common test services registered."""
    container = DIContainer()

    @runtime_checkable
    class ITestRepo(Protocol):
        def save(self, data: str) -> None: ...

    @runtime_checkable
    class ITestService(Protocol):
        def process(self, input: str) -> str: ...

    class TestRepo:
        def save(self, data: str) -> None:
            pass

    class TestService:
        def __init__(self, repo: ITestRepo):
            self.repo = repo

        def process(self, input: str) -> str:
            return f"processed: {input}"

    container.auto_register_with_validation(ITestRepo, TestRepo)
    container.auto_register_with_validation(ITestService, TestService)

    return container
```

---

## **Additional Test Files:**

### **FILE: tests/specification/core/test_di_container_diagnostics.py**

```python
"""
Tests specifically for DI container diagnostic capabilities.
"""

import pytest
from src.core.dependency_injection.di_container import DIContainer

class TestDIContainerDiagnostics:

    def test_dependency_graph_generation(self):
        """Test dependency graph creation and format."""
        container = DIContainer()

        class ServiceA:
            pass

        class ServiceB:
            def __init__(self, a: ServiceA):
                self.a = a

        class ServiceC:
            def __init__(self, a: ServiceA, b: ServiceB):
                self.a = a
                self.b = b

        container.register_singleton(ServiceA, ServiceA)
        container.register_singleton(ServiceB, ServiceB)
        container.register_singleton(ServiceC, ServiceC)

        graph = container.get_dependency_graph()

        # Verify graph structure
        assert "ServiceA -> ServiceA" in graph
        assert "ServiceB -> ServiceB" in graph
        assert "ServiceC -> ServiceC" in graph

        # Verify dependencies
        assert "ServiceA" in graph["ServiceB -> ServiceB"]
        assert "ServiceA" in graph["ServiceC -> ServiceC"]
        assert "ServiceB" in graph["ServiceC -> ServiceC"]

    def test_resolution_path_accuracy(self):
        """Test that resolution paths are accurate."""
        container = DIContainer()

        class Level1:
            pass

        class Level2:
            def __init__(self, l1: Level1):
                self.l1 = l1

        class Level3:
            def __init__(self, l2: Level2):
                self.l2 = l2

        container.register_singleton(Level1, Level1)
        container.register_singleton(Level2, Level2)
        container.register_singleton(Level3, Level3)

        path = container.get_resolution_path(Level3)

        # Should show the complete resolution path
        path_str = "\n".join(path)
        assert "Level3 -> Level3" in path_str
        assert "Level2 -> Level2" in path_str
        assert "Level1 -> Level1" in path_str

    def test_health_validation_comprehensive(self):
        """Test comprehensive health validation scenarios."""
        container = DIContainer()

        # Scenario 1: Healthy services
        class HealthyA:
            pass

        class HealthyB:
            def __init__(self, a: HealthyA):
                self.a = a

        container.register_singleton(HealthyA, HealthyA)
        container.register_singleton(HealthyB, HealthyB)

        health_ok, issues = container.validate_registration_health()
        assert health_ok
        assert len(issues) == 0

        # Scenario 2: Missing dependency
        class UnhealthyC:
            def __init__(self, missing: 'MissingService'):
                self.missing = missing

        container.register_singleton(UnhealthyC, UnhealthyC)

        health_ok, issues = container.validate_registration_health()
        assert not health_ok
        assert len(issues) > 0
        assert any("depends on unregistered MissingService" in issue for issue in issues)
```

---

## **Test Configuration:**

### **FILE: tests/specification/core/conftest.py**

```python
"""
Configuration for DI container tests.
"""

import pytest
import logging
from src.core.dependency_injection.di_container import DIContainer

# Configure test logging
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="function")
def container():
    """Provide a fresh DI container for each test."""
    return DIContainer()

@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    import pathlib
    return pathlib.Path(__file__).parent / "test_data"

# Custom assertions for DI testing
def assert_can_resolve(container: DIContainer, interface_type):
    """Assert that an interface can be resolved."""
    try:
        instance = container.resolve(interface_type)
        assert instance is not None
    except Exception as e:
        pytest.fail(f"Could not resolve {interface_type.__name__}: {e}")

def assert_cannot_resolve(container: DIContainer, interface_type):
    """Assert that an interface cannot be resolved."""
    with pytest.raises((ValueError, RuntimeError)):
        container.resolve(interface_type)

# Add custom assertions to pytest namespace
pytest.assert_can_resolve = assert_can_resolve
pytest.assert_cannot_resolve = assert_cannot_resolve
```

---

## **Running the Tests:**

### **Test Execution Commands:**

```bash
# Run all DI container tests
python -m pytest tests/specification/core/test_enhanced_di_container.py -v

# Run with coverage
python -m pytest tests/specification/core/test_enhanced_di_container.py --cov=src.core.dependency_injection --cov-report=html

# Run performance tests only
python -m pytest tests/specification/core/test_enhanced_di_container.py::TestDIContainerPerformance -v

# Run integration tests only
python -m pytest tests/specification/core/test_enhanced_di_container.py::TestDIContainerIntegration -v

# Run with detailed output for debugging
python -m pytest tests/specification/core/test_enhanced_di_container.py -v -s --tb=long
```

### **Expected Results:**

```
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_auto_injection_with_complex_dependencies PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_dependency_chain_validation PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_enhanced_error_reporting PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_registration_validation PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_primitive_type_handling PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_circular_dependency_detection PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_optional_dependencies PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_protocol_validation PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_dependency_graph_generation PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_health_validation PASSED
tests/specification/core/test_enhanced_di_container.py::TestEnhancedDIContainer::test_resolution_path_tracing PASSED

========================= 11 passed in 0.15s =========================
```

---

## **Success Criteria:**

By the end of Task 1.5:

- ✅ **100% test coverage** for DI container functionality
- ✅ **All edge cases covered** in tests
- ✅ **Performance benchmarks** established
- ✅ **Integration tests** with real TKA services
- ✅ **Error scenario testing** comprehensive
- ✅ **Test suite runs fast** (< 1 second total)

---

## **Next Step**

After completing comprehensive testing, proceed to: [Task 1.6: Integration with Existing Services](07_service_integration.md)
