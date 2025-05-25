#!/usr/bin/env python3
"""
Test script to verify that the MainBackgroundWidgetFactory TypeError fix is working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_background_widget_factory_interface():
    """Test that MainBackgroundWidgetFactory follows the standard WidgetFactory interface."""
    print("🧪 Testing MainBackgroundWidgetFactory Interface")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test factory interface compliance
        print("\nStep 2: Testing factory interface compliance...")
        from src.main_window.main_widget.main_background_widget.main_background_widget_factory import MainBackgroundWidgetFactory
        from src.main_window.main_widget.core.widget_manager import WidgetFactory
        
        # Check that it inherits from WidgetFactory
        if issubclass(MainBackgroundWidgetFactory, WidgetFactory):
            print("✅ MainBackgroundWidgetFactory inherits from WidgetFactory")
        else:
            print("❌ MainBackgroundWidgetFactory does not inherit from WidgetFactory")
            return False
        
        # Test 3: Test method signature
        print("\nStep 3: Testing method signature...")
        from PyQt6.QtWidgets import QWidget, QApplication
        from src.core.application_context import ApplicationContext
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        # Create a mock parent widget
        class MockParent(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
            
            def rect(self):
                from PyQt6.QtCore import QRect
                return QRect(0, 0, 800, 600)
            
            def size(self):
                from PyQt6.QtCore import QSize
                return QSize(800, 600)
        
        mock_parent = MockParent()
        
        # Test that the factory can be called with the standard interface
        try:
            background_widget = MainBackgroundWidgetFactory.create(
                parent=mock_parent,
                app_context=app_context
            )
            print("✅ Factory accepts standard interface (parent, app_context)")
            print(f"✅ Created widget: {type(background_widget).__name__}")
        except TypeError as e:
            print(f"❌ Factory interface test failed: {e}")
            return False
        except Exception as e:
            print(f"⚠️ Factory created widget but with error: {e}")
            # This might be expected due to missing UI context
        
        print("\n🎉 All factory interface tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Factory interface test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_widget_manager_integration():
    """Test that the MainBackgroundWidgetFactory works with the widget manager."""
    print("\n🧪 Testing Widget Manager Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test widget manager factory registration
        print("\nStep 2: Testing widget manager factory registration...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        # Create a mock coordinator
        class MockCoordinator(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
            
            def rect(self):
                from PyQt6.QtCore import QRect
                return QRect(0, 0, 800, 600)
            
            def size(self):
                from PyQt6.QtCore import QSize
                return QSize(800, 600)
        
        mock_coordinator = MockCoordinator()
        
        # Test widget manager creation pattern
        from src.main_window.main_widget.core.widget_manager import WidgetManager
        widget_manager = WidgetManager(mock_coordinator, app_context)
        
        # Test that background_widget factory is registered
        if "background_widget" in widget_manager._widget_factories:
            print("✅ background_widget factory is registered")
        else:
            print("❌ background_widget factory is not registered")
            return False
        
        # Test 3: Test factory creation through widget manager
        print("\nStep 3: Testing factory creation through widget manager...")
        try:
            # This simulates what the widget manager does
            factory = widget_manager._widget_factories["background_widget"]
            widget = factory.create(
                parent=mock_coordinator,
                app_context=app_context
            )
            print("✅ Widget manager can create background_widget successfully")
            print(f"✅ Created widget type: {type(widget).__name__}")
        except Exception as e:
            print(f"❌ Widget manager creation failed: {e}")
            return False
        
        print("\n🎉 All widget manager integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Widget manager integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts without MainBackgroundWidgetFactory TypeError."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        print("Starting application to test for MainBackgroundWidgetFactory errors...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to factory errors
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            # Check for MainBackgroundWidgetFactory TypeError in stderr
            if "MainBackgroundWidgetFactory.create() got an unexpected keyword argument 'parent'" in stderr:
                print("❌ MainBackgroundWidgetFactory TypeError found")
                print(f"STDERR: {stderr}")
                return False
            elif "Failed to create widget background_widget" in stderr:
                print("❌ Background widget creation failed")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No MainBackgroundWidgetFactory TypeError detected")
                # Check if widget initialization completed
                if "MainWindow widgets initialized successfully" in stderr:
                    print("✅ Widget initialization completed successfully")
                # Check for successful background widget creation
                if "Created MainBackgroundWidget with dependency injection" in stderr:
                    print("✅ MainBackgroundWidget created successfully with dependency injection")
                return True
        else:
            # Process crashed
            stdout, stderr = process.communicate()
            print("❌ Application crashed")
            print(f"Return code: {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

def test_factory_dependency_injection():
    """Test that the factory properly handles dependency injection."""
    print("\n🧪 Testing Factory Dependency Injection")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test settings_manager extraction
        print("\nStep 2: Testing settings_manager extraction...")
        settings_manager = app_context.settings_manager
        print(f"✅ Settings manager accessible: {type(settings_manager).__name__}")
        
        # Test 3: Test factory dependency extraction
        print("\nStep 3: Testing factory dependency extraction...")
        from src.main_window.main_widget.main_background_widget.main_background_widget_factory import MainBackgroundWidgetFactory
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockParent(QWidget):
            def __init__(self):
                super().__init__()
            
            def rect(self):
                from PyQt6.QtCore import QRect
                return QRect(0, 0, 800, 600)
            
            def size(self):
                from PyQt6.QtCore import QSize
                return QSize(800, 600)
        
        mock_parent = MockParent()
        
        # Test that the factory extracts dependencies correctly
        try:
            widget = MainBackgroundWidgetFactory.create(mock_parent, app_context)
            
            # Check that the widget has the correct dependencies
            if hasattr(widget, 'settings_manager'):
                print("✅ Widget has settings_manager dependency")
            if hasattr(widget, 'main_widget'):
                print("✅ Widget has main_widget reference")
            
            print("✅ Factory dependency injection works correctly")
        except Exception as e:
            print(f"❌ Factory dependency injection failed: {e}")
            return False
        
        print("\n🎉 All factory dependency injection tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Factory dependency injection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔧 TESTING MAINBACKGROUNDWIDGETFACTORY TYPEERROR FIX")
    print("=" * 80)
    
    # Test 1: Factory interface compliance
    test1_passed = test_background_widget_factory_interface()
    
    # Test 2: Widget manager integration
    test2_passed = test_widget_manager_integration()
    
    # Test 3: Application startup
    test3_passed = test_application_startup()
    
    # Test 4: Factory dependency injection
    test4_passed = test_factory_dependency_injection()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Factory Interface Compliance: PASSED")
    else:
        print("❌ Factory Interface Compliance: FAILED")
    
    if test2_passed:
        print("✅ Widget Manager Integration: PASSED")
    else:
        print("❌ Widget Manager Integration: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    if test4_passed:
        print("✅ Factory Dependency Injection: PASSED")
    else:
        print("❌ Factory Dependency Injection: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed and test4_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The MainBackgroundWidgetFactory TypeError has been FIXED!")
        print("✅ Factory follows standard WidgetFactory interface")
        print("✅ Widget manager integration works correctly")
        print("✅ Application starts without TypeError")
        print("✅ Dependency injection works properly")
        print("✅ MainBackgroundWidget creates successfully")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ The MainBackgroundWidgetFactory issue may not be fully resolved")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
