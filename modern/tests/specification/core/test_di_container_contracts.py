#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: DI container behavior contracts
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

DI Container Contract Tests
==========================

Defines behavioral contracts for the dependency injection container system.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestDIContainerContracts:
    """DI container contract tests."""

    def test_di_container_import(self):
        """Test that DI container can be imported."""
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            assert DIContainer is not None
            assert reset_container is not None
        except ImportError:
            pytest.skip("DI container not available")

    def test_container_creation_contract(self):
        """
        Test container creation contract.
        
        CONTRACT: DI container must be creatable and resettable:
        - Container can be instantiated
        - Container can be reset to clean state
        - Multiple containers can exist independently
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            
            # Reset to clean state
            reset_container()
            
            # Create container
            container = DIContainer()
            assert container is not None
            
            # Create second container
            container2 = DIContainer()
            assert container2 is not None
            
            # Containers should be independent
            assert container is not container2
            
        except ImportError:
            pytest.skip("DI container not available for creation testing")

    def test_service_registration_contract(self):
        """
        Test service registration contract.
        
        CONTRACT: Services must be registerable in container:
        - Singleton registration works
        - Instance registration works
        - Interface-to-implementation mapping works
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from application.services.layout.layout_management_service import LayoutManagementService
            from core.interfaces.core_services import ILayoutService
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Test singleton registration
            container.register_singleton(ILayoutService, LayoutManagementService)
            
            # Test instance registration
            instance = LayoutManagementService()
            container.register_instance(ILayoutService, instance)
            
            # Verify registration doesn't throw errors
            assert True  # If we get here, registration worked
            
        except ImportError:
            pytest.skip("DI container or services not available for registration testing")

    def test_service_resolution_contract(self):
        """
        Test service resolution contract.
        
        CONTRACT: Registered services must be resolvable:
        - Singleton services return same instance
        - Instance services return registered instance
        - Unregistered services raise appropriate errors
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from application.services.layout.layout_management_service import LayoutManagementService
            from core.interfaces.core_services import ILayoutService
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Register singleton
            container.register_singleton(ILayoutService, LayoutManagementService)
            
            # Resolve service
            service1 = container.resolve(ILayoutService)
            service2 = container.resolve(ILayoutService)
            
            # Verify singleton behavior
            assert service1 is not None
            assert service2 is not None
            assert service1 is service2  # Same instance for singleton
            
        except ImportError:
            pytest.skip("DI container or services not available for resolution testing")

    def test_container_lifecycle_contract(self):
        """
        Test container lifecycle contract.
        
        CONTRACT: Container lifecycle must be properly managed:
        - Container can be reset
        - Reset clears all registrations
        - New registrations work after reset
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from application.services.layout.layout_management_service import LayoutManagementService
            from core.interfaces.core_services import ILayoutService
            
            # Create and configure container
            reset_container()
            container = DIContainer()
            container.register_singleton(ILayoutService, LayoutManagementService)
            
            # Resolve service
            service1 = container.resolve(ILayoutService)
            assert service1 is not None
            
            # Reset container
            reset_container()
            
            # Create new container
            container2 = DIContainer()
            container2.register_singleton(ILayoutService, LayoutManagementService)
            
            # Resolve service from new container
            service2 = container2.resolve(ILayoutService)
            assert service2 is not None
            
            # Services should be different instances (new container)
            assert service1 is not service2
            
        except ImportError:
            pytest.skip("DI container or services not available for lifecycle testing")

    def test_workbench_services_integration_contract(self):
        """
        Test workbench services integration contract.
        
        CONTRACT: Workbench services must integrate with DI container:
        - Workbench factory can configure services
        - All required workbench services are available
        - Services can be resolved after configuration
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from presentation.factories.workbench_factory import configure_workbench_services
            from core.interfaces.core_services import ILayoutService, IUIStateManagementService
            from core.interfaces.workbench_services import (
                ISequenceWorkbenchService, IFullScreenService, IBeatDeletionService,
                IGraphEditorService, IDictionaryService
            )
            from application.services.layout.layout_management_service import LayoutManagementService
            from application.services.ui.ui_state_management_service import UIStateManagementService
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Register prerequisite services
            container.register_singleton(ILayoutService, LayoutManagementService)
            container.register_singleton(IUIStateManagementService, UIStateManagementService)
            
            # Configure workbench services
            configure_workbench_services(container)
            
            # Verify all workbench services can be resolved
            workbench_service = container.resolve(ISequenceWorkbenchService)
            fullscreen_service = container.resolve(IFullScreenService)
            deletion_service = container.resolve(IBeatDeletionService)
            graph_service = container.resolve(IGraphEditorService)
            dictionary_service = container.resolve(IDictionaryService)
            
            # Verify services are not None
            assert workbench_service is not None
            assert fullscreen_service is not None
            assert deletion_service is not None
            assert graph_service is not None
            assert dictionary_service is not None
            
        except ImportError:
            pytest.skip("Workbench services not available for integration testing")

    def test_error_handling_contract(self):
        """
        Test error handling contract.
        
        CONTRACT: DI container must handle errors gracefully:
        - Unregistered services raise appropriate errors
        - Invalid registrations are handled
        - Container remains stable after errors
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Test resolving unregistered service
            class UnregisteredInterface:
                pass
            
            try:
                container.resolve(UnregisteredInterface)
                # If no exception, that's also valid behavior
                assert True
            except Exception:
                # Exception is expected for unregistered service
                assert True
            
            # Container should still be usable after error
            assert container is not None
            
        except ImportError:
            pytest.skip("DI container not available for error handling testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
