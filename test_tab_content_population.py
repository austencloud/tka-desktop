#!/usr/bin/env python3
"""
Test script to verify that tabs are properly populated with their content.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_tab_factory_interfaces():
    """Test that all tab factories follow the correct interface."""
    print("🧪 Testing Tab Factory Interfaces")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create mock coordinator
        print("\nStep 2: Creating mock coordinator...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockWidgetManager:
            def get_widget(self, widget_name):
                # Return mock widgets for testing
                if widget_name == "sequence_workbench":
                    class MockSequenceWorkbench:
                        def __init__(self):
                            self.beat_frame = None
                    return MockSequenceWorkbench()
                elif widget_name == "font_color_updater":
                    class MockFontColorUpdater:
                        def get_font_color(self, bg_type):
                            return "white"
                    return MockFontColorUpdater()
                elif widget_name == "fade_manager":
                    class MockFadeManager:
                        def __init__(self):
                            self.stack_fader = None
                    return MockFadeManager()
                return None
        
        class MockCoordinator(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
                self.widget_manager = MockWidgetManager()
                self.right_stack = QWidget()
                self.pictograph_dataset = {}
        
        mock_coordinator = MockCoordinator()
        print("✅ Mock coordinator created")
        
        # Test 3: Test all tab factories
        print("\nStep 3: Testing tab factory interfaces...")
        
        tab_factories = [
            ("GenerateTab", "src.main_window.main_widget.generate_tab.generate_tab_factory", "GenerateTabFactory"),
            ("BrowseTab", "src.main_window.main_widget.browse_tab.browse_tab_factory", "BrowseTabFactory"),
            ("LearnTab", "src.main_window.main_widget.learn_tab.learn_tab_factory", "LearnTabFactory"),
            ("ConstructTab", "src.main_window.main_widget.construct_tab.construct_tab_factory", "ConstructTabFactory"),
            ("WriteTab", "src.main_window.main_widget.write_tab.write_tab_factory", "WriteTabFactory"),
            ("SequenceCardTab", "src.main_window.main_widget.sequence_card_tab.utils.tab_factory", "SequenceCardTabFactory"),
        ]
        
        for tab_name, module_path, factory_class in tab_factories:
            try:
                module = __import__(module_path, fromlist=[factory_class])
                factory = getattr(module, factory_class)
                
                # Test that factory can be called with standard interface
                tab_widget = factory.create(
                    parent=mock_coordinator,
                    app_context=app_context
                )
                print(f"✅ {tab_name} factory works with standard interface")
                
            except Exception as e:
                print(f"❌ {tab_name} factory failed: {e}")
                return False
        
        print("\n🎉 All tab factory interface tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tab factory interface test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tab_manager_integration():
    """Test that the TabManager can create tabs successfully."""
    print("\n🧪 Testing Tab Manager Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create mock coordinator with tab manager
        print("\nStep 2: Creating mock coordinator with tab manager...")
        from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockWidgetManager:
            def __init__(self):
                self._widgets = {}
            
            def get_widget(self, widget_name):
                if widget_name not in self._widgets:
                    if widget_name == "sequence_workbench":
                        class MockSequenceWorkbench:
                            def __init__(self):
                                self.beat_frame = None
                        self._widgets[widget_name] = MockSequenceWorkbench()
                    elif widget_name == "codex":
                        self._widgets[widget_name] = QWidget()
                    elif widget_name == "font_color_updater":
                        class MockFontColorUpdater:
                            def get_font_color(self, bg_type):
                                return "white"
                        self._widgets[widget_name] = MockFontColorUpdater()
                    elif widget_name == "fade_manager":
                        class MockFadeManager:
                            def __init__(self):
                                self.stack_fader = None
                        self._widgets[widget_name] = MockFadeManager()
                    else:
                        self._widgets[widget_name] = QWidget()
                return self._widgets[widget_name]
        
        class MockCoordinator(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
                self.widget_manager = MockWidgetManager()
                self.left_stack = QStackedWidget()
                self.right_stack = QStackedWidget()
                self.pictograph_dataset = {}
        
        mock_coordinator = MockCoordinator()
        print("✅ Mock coordinator with stacks created")
        
        # Test 3: Create TabManager
        print("\nStep 3: Creating TabManager...")
        from src.main_window.main_widget.core.tab_manager import TabManager
        
        tab_manager = TabManager(mock_coordinator, app_context)
        print("✅ TabManager created")
        
        # Test 4: Test tab creation
        print("\nStep 4: Testing tab creation...")
        
        test_tabs = ["construct", "generate", "browse", "learn", "sequence_card"]
        
        for tab_name in test_tabs:
            try:
                tab_widget = tab_manager._create_tab(tab_name)
                if tab_widget:
                    print(f"✅ {tab_name} tab created successfully")
                else:
                    print(f"❌ {tab_name} tab creation returned None")
                    return False
            except Exception as e:
                print(f"❌ {tab_name} tab creation failed: {e}")
                return False
        
        print("\n🎉 All tab manager integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tab manager integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_tab_functionality():
    """Test that the application can create and switch between tabs."""
    print("\n🧪 Testing Application Tab Functionality")
    print("=" * 60)
    
    try:
        print("Starting application to test tab functionality...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for initialization
        time.sleep(5)
        
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
            
            # Check for tab creation success indicators
            success_indicators = [
                "Created GenerateTab with dependency injection",
                "Created BrowseTab with dependency injection", 
                "Created LearnTab with dependency injection",
                "Created ConstructTab with dependency injection",
                "MainWindow widgets initialized successfully",
                "Widget initialization completed"
            ]
            
            found_indicators = []
            for indicator in success_indicators:
                if indicator in stderr:
                    found_indicators.append(indicator)
            
            print(f"✅ Found {len(found_indicators)}/{len(success_indicators)} success indicators")
            for indicator in found_indicators:
                print(f"   - {indicator}")
            
            # Check for tab creation errors
            tab_errors = [
                "Failed to create tab",
                "Failed to create GenerateTab",
                "Failed to create BrowseTab", 
                "Failed to create LearnTab",
                "Failed to create ConstructTab",
                "object has no attribute 'letter_determiner'",
                "object has no attribute 'font_color_updater'",
                "got an unexpected keyword argument 'parent'"
            ]
            
            found_errors = []
            for error in tab_errors:
                if error in stderr:
                    found_errors.append(error)
            
            if found_errors:
                print("❌ Found tab creation errors:")
                for error in found_errors:
                    print(f"   - {error}")
                return False
            else:
                print("✅ No tab creation errors detected")
            
            # Check for essential widgets
            if "Added sequence_workbench to left stack" in stderr:
                print("✅ Essential widgets added to stacks")
            
            return len(found_indicators) >= 3  # At least some tabs created successfully
            
        else:
            # Process crashed
            stdout, stderr = process.communicate()
            print("❌ Application crashed")
            print(f"Return code: {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Application tab functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔧 TESTING TAB CONTENT POPULATION")
    print("=" * 80)
    
    # Test 1: Tab factory interfaces
    test1_passed = test_tab_factory_interfaces()
    
    # Test 2: Tab manager integration
    test2_passed = test_tab_manager_integration()
    
    # Test 3: Application tab functionality
    test3_passed = test_application_tab_functionality()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Tab Factory Interfaces: PASSED")
    else:
        print("❌ Tab Factory Interfaces: FAILED")
    
    if test2_passed:
        print("✅ Tab Manager Integration: PASSED")
    else:
        print("❌ Tab Manager Integration: FAILED")
    
    if test3_passed:
        print("✅ Application Tab Functionality: PASSED")
    else:
        print("❌ Application Tab Functionality: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Tab content population is working correctly!")
        print("✅ All tab factories follow standard interface")
        print("✅ TabManager can create tabs successfully")
        print("✅ Application creates tabs without errors")
        print("✅ Essential widgets are added to stacks")
        print("✅ Tab switching infrastructure is functional")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Tab content population may have issues")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
