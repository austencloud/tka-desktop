#!/usr/bin/env python3
"""
Component Testing Suite Runner

This script runs the comprehensive component testing suite and validates
that the modern component architecture works flawlessly.

Usage:
    python run_component_tests.py
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

def run_basic_component_tests():
    """Run basic component architecture tests."""
    print("=" * 60)
    print("COMPONENT ARCHITECTURE VALIDATION")
    print("=" * 60)
    
    from presentation.components import ViewableComponentBase, AsyncViewableComponentBase
    from core.dependency_injection.di_container import DIContainer
    from core.interfaces.core_services import ILayoutService
    from unittest.mock import Mock
    
    # Mock Qt classes
    class MockQWidget:
        def __init__(self):
            self._enabled = True
            self._visible = True
            self._width = 800
            self._height = 600
        
        def setEnabled(self, enabled):
            self._enabled = enabled
        
        def isEnabled(self):
            return self._enabled
        
        def setVisible(self, visible):
            self._visible = visible
        
        def isVisible(self):
            return self._visible
        
        def width(self):
            return self._width
        
        def height(self):
            return self._height
        
        def resize(self, width, height):
            self._width = width
            self._height = height
        
        def deleteLater(self):
            pass
    
    tests_passed = 0
    tests_total = 0
    
    def test(description, test_func):
        nonlocal tests_passed, tests_total
        tests_total += 1
        try:
            test_func()
            print(f"✓ {description}")
            tests_passed += 1
        except Exception as e:
            print(f"✗ {description}: {e}")
    
    # Test 1: Abstract class enforcement
    def test_abstract_enforcement():
        container = DIContainer()
        try:
            ViewableComponentBase(container)
            raise AssertionError("Should not be able to instantiate abstract class")
        except TypeError:
            pass  # Expected
    
    test("Abstract class cannot be instantiated", test_abstract_enforcement)
    
    # Test 2: Complete implementation works
    def test_complete_implementation():
        container = DIContainer()
        
        class TestComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()
            
            def get_widget(self):
                return self._widget
        
        component = TestComponent(container)
        assert not component.is_initialized
        
        component.initialize()
        assert component.is_initialized
        
        widget = component.get_widget()
        assert widget is not None
    
    test("Complete component implementation works", test_complete_implementation)
    
    # Test 3: Dependency injection integration
    def test_dependency_injection():
        container = DIContainer()
        
        # Register mock service
        mock_service = Mock()
        mock_service.get_data.return_value = "test_data"
        container.register_factory(ILayoutService, lambda: mock_service)
        
        class DIComponent(ViewableComponentBase):
            def initialize(self):
                self.service = self.resolve_service(ILayoutService)
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()
            
            def get_widget(self):
                return self._widget
        
        component = DIComponent(container)
        component.initialize()
        
        assert hasattr(component, 'service')
        assert component.service.get_data() == "test_data"
    
    test("Dependency injection integration works", test_dependency_injection)
    
    # Test 4: Signal system functionality
    def test_signal_system():
        container = DIContainer()
        
        class SignalComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()
            
            def get_widget(self):
                return self._widget
        
        component = SignalComponent(container)
        
        signals_received = []
        component.component_ready.connect(lambda: signals_received.append("ready"))
        component.component_error.connect(lambda msg: signals_received.append(f"error: {msg}"))
        
        component.initialize()
        assert len(signals_received) == 1
        assert signals_received[0] == "ready"
        
        component.emit_error("test error")
        assert len(signals_received) == 2
        assert "error:" in signals_received[1]
    
    test("Signal system functionality works", test_signal_system)
    
    # Test 5: Component lifecycle management
    def test_lifecycle_management():
        container = DIContainer()
        
        class LifecycleComponent(ViewableComponentBase):
            def __init__(self, container, parent=None):
                super().__init__(container, parent)
                self.cleanup_called = False
            
            def initialize(self):
                self._widget = MockQWidget()
                self.add_cleanup_handler(lambda: setattr(self, 'cleanup_called', True))
                self._initialized = True
                self.component_ready.emit()
            
            def get_widget(self):
                return self._widget
        
        component = LifecycleComponent(container)
        component.initialize()
        
        assert component.is_initialized
        assert component.widget is not None
        
        component.cleanup()
        assert component.cleanup_called
        assert not component.is_initialized
        assert component.widget is None
    
    test("Component lifecycle management works", test_lifecycle_management)
    
    return tests_passed, tests_total

def run_option_picker_tests():
    """Run OptionPicker retrofit validation tests."""
    print("\n" + "=" * 60)
    print("OPTION PICKER RETROFIT VALIDATION")
    print("=" * 60)
    
    from presentation.components import ViewableComponentBase
    from presentation.components.option_picker import OptionPicker
    from core.dependency_injection.di_container import DIContainer
    from core.interfaces.core_services import ILayoutService
    from unittest.mock import Mock
    
    tests_passed = 0
    tests_total = 0
    
    def test(description, test_func):
        nonlocal tests_passed, tests_total
        tests_total += 1
        try:
            test_func()
            print(f"✓ {description}")
            tests_passed += 1
        except Exception as e:
            print(f"✗ {description}: {e}")
    
    # Test 1: Inheritance verification
    def test_inheritance():
        container = DIContainer()
        option_picker = OptionPicker(container)
        
        assert isinstance(option_picker, ViewableComponentBase)
        assert hasattr(option_picker, 'component_ready')
        assert hasattr(option_picker, 'component_error')
        assert hasattr(option_picker, 'initialize')
        assert hasattr(option_picker, 'get_widget')
    
    test("OptionPicker inherits from ViewableComponentBase", test_inheritance)
    
    # Test 2: Constructor compatibility
    def test_constructor_compatibility():
        container = DIContainer()
        progress_callback = Mock()
        
        # Test with progress callback (existing pattern)
        option_picker1 = OptionPicker(container, progress_callback=progress_callback)
        assert option_picker1.progress_callback is progress_callback
        
        # Test with parent parameter (new pattern)
        option_picker2 = OptionPicker(container, parent=None)
        assert option_picker2.container is container
    
    test("Constructor maintains backward compatibility", test_constructor_compatibility)
    
    # Test 3: Abstract methods implemented
    def test_abstract_methods():
        container = DIContainer()
        option_picker = OptionPicker(container)
        
        assert callable(option_picker.initialize)
        assert callable(option_picker.get_widget)
        
        # Test get_widget before initialization
        try:
            option_picker.get_widget()
            raise AssertionError("Should raise error before initialization")
        except RuntimeError:
            pass  # Expected
    
    test("Abstract methods properly implemented", test_abstract_methods)
    
    # Test 4: Existing methods preserved
    def test_existing_methods():
        container = DIContainer()
        option_picker = OptionPicker(container)
        
        existing_methods = [
            'load_motion_combinations',
            'refresh_options',
            'refresh_options_from_sequence',
            'refresh_options_from_modern_sequence',
            'get_beat_data_for_option',
            'set_enabled',
            'get_size',
            'log_dimensions'
        ]
        
        for method_name in existing_methods:
            assert hasattr(option_picker, method_name)
            assert callable(getattr(option_picker, method_name))
    
    test("All existing methods preserved", test_existing_methods)
    
    # Test 5: Signal integration
    def test_signal_integration():
        container = DIContainer()
        option_picker = OptionPicker(container)
        
        signals_received = []
        option_picker.component_ready.connect(lambda: signals_received.append("ready"))
        option_picker.component_error.connect(lambda msg: signals_received.append(f"error: {msg}"))
        option_picker.option_selected.connect(lambda opt: signals_received.append(f"option: {opt}"))
        
        # Test signal emissions
        option_picker.component_ready.emit()
        option_picker.component_error.emit("test error")
        option_picker.option_selected.emit("test_option")
        
        assert len(signals_received) == 3
        assert "ready" in signals_received
        assert any("error:" in s for s in signals_received)
        assert any("option:" in s for s in signals_received)
    
    test("Signal integration works correctly", test_signal_integration)
    
    return tests_passed, tests_total

def main():
    """Run all component tests and report results."""
    print("MODERN COMPONENT ARCHITECTURE TESTING SUITE")
    print("=" * 60)
    print("Validating world-class component architecture...")
    print()
    
    total_passed = 0
    total_tests = 0
    
    # Run component base tests
    passed, total = run_basic_component_tests()
    total_passed += passed
    total_tests += total
    
    # Run OptionPicker tests
    passed, total = run_option_picker_tests()
    total_passed += passed
    total_tests += total
    
    # Final results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Tests Passed: {total_passed}/{total_tests}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Component architecture is WORLD-CLASS!")
        print("✅ ViewableComponentBase foundation is solid")
        print("✅ OptionPicker retrofit is successful")
        print("✅ Dependency injection works flawlessly")
        print("✅ Signal system is fully functional")
        print("✅ Component lifecycle is properly managed")
        return 0
    else:
        print(f"\n❌ {total_tests - total_passed} tests failed. Architecture needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
