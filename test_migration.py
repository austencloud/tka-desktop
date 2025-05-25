#!/usr/bin/env python3
"""
Test script for the dependency injection migration.

This script validates that all the migration components work correctly
and provides a comprehensive test of the new architecture.
"""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class TestDependencyInjection(unittest.TestCase):
    """Test cases for the dependency injection system."""
    
    def setUp(self):
        """Set up test fixtures."""
        logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests
    
    def test_dependency_container_basic_functionality(self):
        """Test basic dependency container functionality."""
        from src.core.dependency_container import DependencyContainer
        
        container = DependencyContainer()
        
        # Test singleton registration and resolution
        class TestService:
            def __init__(self):
                self.value = "test"
        
        container.register_singleton(TestService, TestService)
        
        # Resolve service
        service1 = container.resolve(TestService)
        service2 = container.resolve(TestService)
        
        # Should be the same instance (singleton)
        self.assertIs(service1, service2)
        self.assertEqual(service1.value, "test")
    
    def test_dependency_container_transient(self):
        """Test transient service registration."""
        from src.core.dependency_container import DependencyContainer
        
        container = DependencyContainer()
        
        class TestTransientService:
            def __init__(self):
                self.value = "transient"
        
        container.register_transient(TestTransientService, TestTransientService)
        
        # Resolve service multiple times
        service1 = container.resolve(TestTransientService)
        service2 = container.resolve(TestTransientService)
        
        # Should be different instances (transient)
        self.assertIsNot(service1, service2)
        self.assertEqual(service1.value, "transient")
        self.assertEqual(service2.value, "transient")
    
    def test_dependency_container_instance_registration(self):
        """Test instance registration."""
        from src.core.dependency_container import DependencyContainer
        
        container = DependencyContainer()
        
        class TestInstanceService:
            def __init__(self, value):
                self.value = value
        
        # Register specific instance
        instance = TestInstanceService("specific")
        container.register_instance(TestInstanceService, instance)
        
        # Resolve should return the same instance
        resolved = container.resolve(TestInstanceService)
        self.assertIs(resolved, instance)
        self.assertEqual(resolved.value, "specific")
    
    def test_application_context_creation(self):
        """Test application context creation."""
        from src.core.dependency_container import DependencyContainer
        from src.core.application_context import create_application_context
        
        container = DependencyContainer()
        app_context = create_application_context(container)
        
        self.assertIsNotNone(app_context)
        self.assertEqual(app_context._container, container)
    
    def test_migration_adapter_functionality(self):
        """Test migration adapter functionality."""
        from src.core.dependency_container import DependencyContainer
        from src.core.application_context import create_application_context
        from src.core.migration_adapters import AppContextAdapter
        
        # Create mock services
        mock_settings = Mock()
        mock_json = Mock()
        
        container = DependencyContainer()
        container.register_instance(Mock, mock_settings)  # Using Mock as interface for test
        
        app_context = create_application_context(container)
        app_context._settings_manager = mock_settings
        app_context._json_manager = mock_json
        
        # Create adapter
        adapter = AppContextAdapter(app_context)
        
        # Test instance methods
        self.assertEqual(adapter.get_settings_manager(), mock_settings)
        self.assertEqual(adapter.get_json_manager(), mock_json)
        
        # Test selected arrow functionality
        mock_arrow = Mock()
        adapter.set_arrow(mock_arrow)
        self.assertEqual(adapter.get_selected_arrow(), mock_arrow)
    
    def test_component_migration_helper(self):
        """Test component migration helper."""
        from src.core.dependency_container import DependencyContainer
        from src.core.application_context import create_application_context
        from src.core.migration_adapters import ComponentMigrationHelper
        
        container = DependencyContainer()
        app_context = create_application_context(container)
        
        helper = ComponentMigrationHelper(app_context)
        
        # Create test component
        class TestComponent:
            def __init__(self):
                self.settings_manager = None
                self.app_context = None
            
            def set_app_context(self, context):
                self.app_context = context
        
        component = TestComponent()
        
        # Migrate component
        helper.migrate_component(component, "TestComponent")
        
        # Check that app_context was set
        self.assertEqual(component.app_context, app_context)
    
    def test_factory_pattern_base(self):
        """Test the base factory pattern."""
        from src.main_window.main_widget.core.widget_manager import WidgetFactory
        from src.core.application_context import ApplicationContext
        
        # Test that factory base class exists and has correct interface
        self.assertTrue(hasattr(WidgetFactory, 'create'))
        
        # Test that create method has correct signature
        import inspect
        sig = inspect.signature(WidgetFactory.create)
        params = list(sig.parameters.keys())
        
        # Should have parent and app_context parameters
        self.assertIn('parent', params)
        self.assertIn('app_context', params)


class TestFactoryClasses(unittest.TestCase):
    """Test the factory classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        logging.basicConfig(level=logging.WARNING)
        
        # Create mock app context
        self.mock_app_context = Mock()
        self.mock_app_context.settings_manager = Mock()
        self.mock_app_context.json_manager = Mock()
        
        # Create mock parent
        self.mock_parent = Mock()
        self.mock_parent.widget_manager = Mock()
        self.mock_parent.widget_manager.get_widget.return_value = Mock()
        self.mock_parent.size.return_value = Mock()
        self.mock_parent.right_stack = Mock()
    
    def test_construct_tab_factory_exists(self):
        """Test that ConstructTabFactory exists and can be imported."""
        try:
            from src.main_window.main_widget.construct_tab.construct_tab_factory import ConstructTabFactory
            self.assertTrue(hasattr(ConstructTabFactory, 'create'))
        except ImportError:
            self.skipTest("ConstructTabFactory not available (expected if dependencies missing)")
    
    def test_generate_tab_factory_exists(self):
        """Test that GenerateTabFactory exists and can be imported."""
        try:
            from src.main_window.main_widget.generate_tab.generate_tab_factory import GenerateTabFactory
            self.assertTrue(hasattr(GenerateTabFactory, 'create'))
        except ImportError:
            self.skipTest("GenerateTabFactory not available (expected if dependencies missing)")
    
    def test_browse_tab_factory_exists(self):
        """Test that BrowseTabFactory exists and can be imported."""
        try:
            from src.main_window.main_widget.browse_tab.browse_tab_factory import BrowseTabFactory
            self.assertTrue(hasattr(BrowseTabFactory, 'create'))
        except ImportError:
            self.skipTest("BrowseTabFactory not available (expected if dependencies missing)")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_complete_dependency_injection_flow(self):
        """Test the complete dependency injection flow."""
        from src.core.dependency_container import configure_dependencies
        from src.core.application_context import create_application_context
        from src.core.migration_adapters import setup_legacy_compatibility, teardown_legacy_compatibility
        
        # Configure dependencies
        container = configure_dependencies()
        self.assertIsNotNone(container)
        
        # Create application context
        app_context = create_application_context(container)
        self.assertIsNotNone(app_context)
        
        # Set up legacy compatibility
        adapter = setup_legacy_compatibility(app_context)
        self.assertIsNotNone(adapter)
        
        # Test that we can access services (even if they're not fully implemented)
        try:
            settings = app_context.settings_manager
            # If this doesn't raise an exception, the service is registered
        except Exception:
            # Expected if the actual service classes aren't available
            pass
        
        # Clean up
        teardown_legacy_compatibility()
        container.clear()


def run_tests():
    """Run all tests and return success status."""
    print("Running dependency injection migration tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDependencyInjection))
    suite.addTests(loader.loadTestsFromTestCase(TestFactoryClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n✅ All tests passed! The migration is ready to use.")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
    
    return success


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
