#!/usr/bin/env python3
"""
Integration tests for enhanced DI container with existing modern services.

Tests that the enhanced DI container works correctly with real modern services
and validates that existing service registrations continue to work.
"""

import sys
from pathlib import Path

# Add modern src to path
modern_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

import pytest
from unittest.mock import Mock

from core.dependency_injection.di_container import DIContainer, reset_container


class TestEnhancedDIWithExistingServices:
    """Test enhanced DI container with existing modern services."""

    def setup_method(self):
        """Reset container before each test."""
        reset_container()
        self.container = DIContainer()

    def test_simple_layout_service_integration(self):
        """Test that SimpleLayoutService works with enhanced DI."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService
            from core.interfaces.core_services import ILayoutService

            # Test auto-registration with validation
            self.container.auto_register_with_validation(
                ILayoutService, SimpleLayoutService
            )

            # Test resolution
            layout_service = self.container.resolve(ILayoutService)
            assert isinstance(layout_service, SimpleLayoutService)

            # Test that it's a singleton
            layout_service2 = self.container.resolve(ILayoutService)
            assert layout_service is layout_service2

        except ImportError as e:
            pytest.skip(f"SimpleLayoutService not available: {e}")

    def test_ui_state_management_service_integration(self):
        """Test that UIStateManagementService works with enhanced DI."""
        try:
            from application.services.ui.ui_state_management_service import (
                UIStateManagementService,
            )
            from core.interfaces.core_services import IUIStateManagementService

            # Test registration
            self.container.register_singleton(
                IUIStateManagementService, UIStateManagementService
            )

            # Test resolution
            ui_service = self.container.resolve(IUIStateManagementService)
            assert isinstance(ui_service, UIStateManagementService)

        except ImportError as e:
            pytest.skip(f"UIStateManagementService not available: {e}")

    def test_position_matching_service_integration(self):
        """Test that PositionMatchingService works with enhanced DI."""
        try:
            from application.services.positioning.position_matching_service import (
                PositionMatchingService,
            )

            # Test direct instantiation (no interface for this service)
            position_service = self.container._create_instance(PositionMatchingService)
            assert isinstance(position_service, PositionMatchingService)

        except ImportError as e:
            pytest.skip(f"PositionMatchingService not available: {e}")

    def test_pictograph_dataset_service_integration(self):
        """Test that PictographDatasetService works with enhanced DI."""
        try:
            from application.services.data.pictograph_dataset_service import (
                PictographDatasetService,
            )

            # Test direct instantiation
            dataset_service = self.container._create_instance(PictographDatasetService)
            assert isinstance(dataset_service, PictographDatasetService)

        except ImportError as e:
            pytest.skip(f"PictographDatasetService not available: {e}")

    def test_dependency_graph_with_real_services(self):
        """Test dependency graph generation with real services."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService
            from core.interfaces.core_services import ILayoutService

            self.container.register_singleton(ILayoutService, SimpleLayoutService)

            # Generate dependency graph
            graph = self.container.get_dependency_graph()

            # Should contain our registration
            assert any("ILayoutService" in key for key in graph.keys())

        except ImportError as e:
            pytest.skip(f"Services not available: {e}")

    def test_validate_all_with_real_services(self):
        """Test validation of all registrations with real services."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService
            from core.interfaces.core_services import ILayoutService

            self.container.register_singleton(ILayoutService, SimpleLayoutService)

            # This should pass - SimpleLayoutService should be instantiable
            self.container.validate_all_registrations()

        except ImportError as e:
            pytest.skip(f"Services not available: {e}")

    def test_enhanced_error_reporting_with_real_services(self):
        """Test enhanced error reporting with real service dependencies."""
        try:
            # Try to create a service that might have unregistered dependencies
            from application.services.workbench_services import SequenceWorkbenchService

            with pytest.raises((ValueError, RuntimeError)) as exc_info:
                self.container._create_instance(SequenceWorkbenchService)

            error_msg = str(exc_info.value)
            # Should contain helpful error information
            assert any(
                keyword in error_msg
                for keyword in [
                    "Cannot resolve dependency",
                    "Dependency injection failed",
                    "Available registrations",
                ]
            )

        except ImportError as e:
            pytest.skip(f"SequenceWorkbenchService not available: {e}")

    def test_primitive_type_handling_with_real_services(self):
        """Test that primitive types are handled correctly in real services."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService

            # SimpleLayoutService should be instantiable even if it has primitive parameters
            service = self.container._create_instance(SimpleLayoutService)
            assert isinstance(service, SimpleLayoutService)

        except ImportError as e:
            pytest.skip(f"SimpleLayoutService not available: {e}")

    def test_lifecycle_management_with_real_services(self):
        """Test lifecycle management with real services that might have lifecycle methods."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService

            # Test with lifecycle management
            service = self.container._create_with_lifecycle(SimpleLayoutService)
            assert isinstance(service, SimpleLayoutService)

            # If the service has lifecycle methods, they should be called
            if hasattr(service, "initialize"):
                # Should have been called during creation
                pass

            # Test cleanup
            initial_cleanup_count = len(self.container._cleanup_handlers)
            self.container.cleanup_all()
            # Cleanup handlers should be cleared
            assert len(self.container._cleanup_handlers) == 0

        except ImportError as e:
            pytest.skip(f"SimpleLayoutService not available: {e}")

    def test_complex_service_chain_with_real_services(self):
        """Test complex dependency chains with real modern services."""
        try:
            from application.services.simple_layout_service import SimpleLayoutService
            from application.services.ui.ui_state_management_service import (
                UIStateManagementService,
            )
            from core.interfaces.core_services import (
                ILayoutService,
                IUIStateManagementService,
            )

            # Register services in dependency order
            self.container.register_singleton(ILayoutService, SimpleLayoutService)
            self.container.register_singleton(
                IUIStateManagementService, UIStateManagementService
            )

            # Test that all can be resolved
            layout_service = self.container.resolve(ILayoutService)
            ui_service = self.container.resolve(IUIStateManagementService)

            assert isinstance(layout_service, SimpleLayoutService)
            assert isinstance(ui_service, UIStateManagementService)

            # Test validation of the entire chain
            self.container.validate_all_registrations()

        except ImportError as e:
            pytest.skip(f"Services not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
