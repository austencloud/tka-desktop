#!/usr/bin/env python3
"""
DI Container Test Fixtures
==========================

Provides reusable dependency injection container fixtures for testing.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


@pytest.fixture
def clean_di_container():
    """Provide a clean DI container for testing."""
    try:
        from core.dependency_injection.di_container import DIContainer, reset_container
        
        # Reset container to clean state
        reset_container()
        
        # Create new container
        container = DIContainer()
        
        yield container
        
        # Cleanup after test
        reset_container()
        
    except ImportError:
        pytest.skip("DI container not available")


@pytest.fixture
def configured_di_container():
    """Provide a DI container with basic services configured."""
    try:
        from core.dependency_injection.di_container import DIContainer, reset_container
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from application.services.layout.layout_management_service import LayoutManagementService
        from application.services.ui.ui_state_management_service import UIStateManagementService
        
        # Reset container to clean state
        reset_container()
        
        # Create and configure container
        container = DIContainer()
        
        # Register core services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        
        yield container
        
        # Cleanup after test
        reset_container()
        
    except ImportError:
        pytest.skip("DI container or services not available")


@pytest.fixture
def workbench_di_container():
    """Provide a DI container with workbench services configured."""
    try:
        from core.dependency_injection.di_container import DIContainer, reset_container
        from presentation.factories.workbench_factory import configure_workbench_services
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from application.services.layout.layout_management_service import LayoutManagementService
        from application.services.ui.ui_state_management_service import UIStateManagementService
        
        # Reset container to clean state
        reset_container()
        
        # Create and configure container
        container = DIContainer()
        
        # Register core services first
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        
        # Configure workbench services
        configure_workbench_services(container)
        
        yield container
        
        # Cleanup after test
        reset_container()
        
    except ImportError:
        pytest.skip("Workbench services not available")


@pytest.fixture
def event_bus():
    """Provide a clean event bus for testing."""
    try:
        from core.events import get_event_bus, reset_event_bus
        
        # Reset event bus to clean state
        reset_event_bus()
        
        # Get clean event bus
        bus = get_event_bus()
        
        yield bus
        
        # Cleanup after test
        reset_event_bus()
        
    except ImportError:
        pytest.skip("Event bus not available")
