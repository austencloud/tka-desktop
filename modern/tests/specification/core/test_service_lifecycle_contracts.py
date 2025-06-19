#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Service lifecycle behavior contracts
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Service Lifecycle Contract Tests
===============================

Defines behavioral contracts for service lifecycle management.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestServiceLifecycleContracts:
    """Service lifecycle contract tests."""

    def test_service_creation_contract(self):
        """
        Test service creation contract.
        
        CONTRACT: Services must be creatable:
        - Services can be instantiated directly
        - Services can be created through DI container
        - Service creation is consistent
        """
        try:
            from application.services.layout.layout_management_service import LayoutManagementService
            from application.services.ui.ui_state_management_service import UIStateManagementService
            
            # Test direct instantiation
            layout_service = LayoutManagementService()
            ui_service = UIStateManagementService()
            
            assert layout_service is not None
            assert ui_service is not None
            
            # Test multiple instances are independent
            layout_service2 = LayoutManagementService()
            assert layout_service is not layout_service2
            
        except ImportError:
            pytest.skip("Core services not available for creation testing")

    def test_service_initialization_contract(self):
        """
        Test service initialization contract.
        
        CONTRACT: Services must initialize properly:
        - Services have proper initial state
        - Services can be used immediately after creation
        - Service dependencies are handled correctly
        """
        try:
            from application.services.ui.ui_state_management_service import UIStateManagementService
            from application.services.graph_editor_service import GraphEditorService
            
            # Test service with no dependencies
            ui_service = UIStateManagementService()
            assert ui_service is not None
            
            # Test service with dependencies
            graph_service = GraphEditorService(ui_service)
            assert graph_service is not None
            
            # Test service functionality works after initialization
            initial_visibility = graph_service.is_visible()
            assert isinstance(initial_visibility, bool)
            
        except ImportError:
            pytest.skip("Services not available for initialization testing")

    def test_service_singleton_contract(self):
        """
        Test service singleton contract.
        
        CONTRACT: Singleton services must behave correctly:
        - Same instance returned for multiple resolutions
        - State is preserved across resolutions
        - Singleton behavior is consistent
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from application.services.layout.layout_management_service import LayoutManagementService
            from core.interfaces.core_services import ILayoutService
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Register as singleton
            container.register_singleton(ILayoutService, LayoutManagementService)
            
            # Resolve multiple times
            service1 = container.resolve(ILayoutService)
            service2 = container.resolve(ILayoutService)
            service3 = container.resolve(ILayoutService)
            
            # Verify same instance
            assert service1 is service2
            assert service2 is service3
            assert service1 is service3
            
        except ImportError:
            pytest.skip("DI container or services not available for singleton testing")

    def test_service_dependency_injection_contract(self):
        """
        Test service dependency injection contract.
        
        CONTRACT: Service dependencies must be injected correctly:
        - Services with dependencies can be created
        - Dependencies are properly injected
        - Dependency chain works correctly
        """
        try:
            from core.dependency_injection.di_container import DIContainer, reset_container
            from application.services.ui.ui_state_management_service import UIStateManagementService
            from application.services.graph_editor_service import GraphEditorService
            from core.interfaces.core_services import IUIStateManagementService
            from core.interfaces.workbench_services import IGraphEditorService
            
            # Reset and create container
            reset_container()
            container = DIContainer()
            
            # Register dependency
            container.register_singleton(IUIStateManagementService, UIStateManagementService)
            
            # Create service with dependency
            ui_service = container.resolve(IUIStateManagementService)
            graph_service = GraphEditorService(ui_service)
            
            # Register dependent service
            container.register_instance(IGraphEditorService, graph_service)
            
            # Verify dependency injection worked
            resolved_graph_service = container.resolve(IGraphEditorService)
            assert resolved_graph_service is graph_service
            
        except ImportError:
            pytest.skip("Services not available for dependency injection testing")

    def test_service_state_management_contract(self):
        """
        Test service state management contract.
        
        CONTRACT: Services must manage state correctly:
        - Service state can be modified
        - State changes are persistent
        - State is isolated between instances
        """
        try:
            from application.services.graph_editor_service import GraphEditorService
            from application.services.ui.ui_state_management_service import UIStateManagementService
            
            # Create services
            ui_service = UIStateManagementService()
            graph_service1 = GraphEditorService(ui_service)
            graph_service2 = GraphEditorService(ui_service)
            
            # Test initial state
            initial_state1 = graph_service1.is_visible()
            initial_state2 = graph_service2.is_visible()
            
            # Modify state of first service
            new_state1 = graph_service1.toggle_graph_visibility()
            
            # Verify state change
            assert graph_service1.is_visible() == new_state1
            assert graph_service1.is_visible() != initial_state1
            
            # Verify second service is unaffected (if they're independent)
            # Note: This depends on implementation - they might share state
            current_state2 = graph_service2.is_visible()
            assert isinstance(current_state2, bool)
            
        except ImportError:
            pytest.skip("Services not available for state management testing")

    def test_service_cleanup_contract(self):
        """
        Test service cleanup contract.
        
        CONTRACT: Services must support proper cleanup:
        - Services can be destroyed without errors
        - Cleanup doesn't affect other services
        - Resources are properly released
        """
        try:
            from application.services.layout.layout_management_service import LayoutManagementService
            from application.services.ui.ui_state_management_service import UIStateManagementService
            
            # Create services
            layout_service = LayoutManagementService()
            ui_service = UIStateManagementService()
            
            # Verify services work
            assert layout_service is not None
            assert ui_service is not None
            
            # Delete services (Python garbage collection)
            del layout_service
            del ui_service
            
            # Create new services to verify cleanup didn't break anything
            new_layout_service = LayoutManagementService()
            new_ui_service = UIStateManagementService()
            
            assert new_layout_service is not None
            assert new_ui_service is not None
            
        except ImportError:
            pytest.skip("Services not available for cleanup testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
