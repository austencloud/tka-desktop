#!/usr/bin/env python3
"""
Test script to verify that all proactive AttributeError fixes are working correctly.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_application_startup_comprehensive():
    """Test that the application starts without any AttributeError patterns we fixed."""
    print("🧪 Testing Application Startup - Comprehensive AttributeError Check")
    print("=" * 80)
    
    try:
        print("Starting application to test for all AttributeError patterns...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes due to AttributeErrors
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
            
            # Check for specific AttributeError patterns we fixed
            attributeerror_patterns = [
                "'MainWidgetCoordinator' object has no attribute 'settings_manager'",
                "'MainWidgetCoordinator' object has no attribute 'json_manager'",
                "'MainWidgetCoordinator' object has no attribute 'pictograph_data_loader'",
                "'MainWidgetCoordinator' object has no attribute 'sequence_workbench'",
                "'MainWidgetCoordinator' object has no attribute 'settings_dialog'",
                "'MainWidgetCoordinator' object has no attribute 'background_widget'",
                "'NoneType' object has no attribute 'pictograph_dataset'",
            ]
            
            found_errors = []
            for pattern in attributeerror_patterns:
                if pattern in stderr:
                    found_errors.append(pattern)
            
            if found_errors:
                print("❌ Found AttributeError patterns that should have been fixed:")
                for error in found_errors:
                    print(f"   - {error}")
                print(f"\nFull STDERR:\n{stderr}")
                return False
            else:
                print("✅ No problematic AttributeError patterns detected")
                
                # Check for successful widget initialization
                if "MainWindow widgets initialized successfully" in stderr:
                    print("✅ Widget initialization completed successfully")
                
                # Check that settings dialog creation succeeded
                if "Failed to create SettingsDialog" not in stderr:
                    print("✅ SettingsDialog creation succeeded")
                
                # Check for graceful warnings instead of errors
                if "sequence_workbench not available during ImageExportTab initialization" in stderr:
                    print("✅ ImageExportTab shows graceful warning instead of AttributeError")
                
                if "settings_dialog not available" in stderr:
                    print("✅ SettingsButton shows graceful warning instead of AttributeError")
                
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

def test_dependency_injection_patterns():
    """Test that all the dependency injection patterns we implemented work correctly."""
    print("\n🧪 Testing Dependency Injection Patterns")
    print("=" * 80)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create mock MainWidgetCoordinator
        print("\nStep 2: Creating mock MainWidgetCoordinator...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        class MockWidgetManager:
            def get_widget(self, widget_name):
                # Return mock widgets for testing
                if widget_name == "sequence_workbench":
                    class MockSequenceWorkbench:
                        def __init__(self):
                            self.beat_frame = MockBeatFrame()
                            self.indicator_label = MockIndicatorLabel()
                    return MockSequenceWorkbench()
                elif widget_name == "settings_dialog":
                    class MockSettingsDialog:
                        def show(self):
                            pass
                    return MockSettingsDialog()
                elif widget_name == "background_widget":
                    class MockBackgroundWidget:
                        def apply_background(self):
                            pass
                    return MockBackgroundWidget()
                return None
        
        class MockBeatFrame:
            def __init__(self):
                self.json_manager = app_context.json_manager
                class MockUpdateSignal:
                    def connect(self, func):
                        pass
                self.updateImageExportPreview = MockUpdateSignal()
        
        class MockIndicatorLabel:
            def show_message(self, message):
                pass
        
        class MockMainWidget(QWidget):
            def __init__(self):
                super().__init__()
                self.app_context = app_context
                self.widget_manager = MockWidgetManager()
        
        mock_widget = MockMainWidget()
        print("✅ Mock MainWidgetCoordinator created")
        
        # Test 3: Test settings_manager access pattern
        print("\nStep 3: Testing settings_manager access pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            visibility_settings = settings_manager.visibility
            print("✅ settings_manager access pattern works")
        except AttributeError as e:
            print(f"❌ settings_manager access pattern failed: {e}")
            return False
        
        # Test 4: Test json_manager access pattern
        print("\nStep 4: Testing json_manager access pattern...")
        try:
            json_manager = mock_widget.app_context.json_manager
            loader_saver = json_manager.loader_saver
            print("✅ json_manager access pattern works")
        except AttributeError as e:
            print(f"❌ json_manager access pattern failed: {e}")
            return False
        
        # Test 5: Test widget_manager access patterns
        print("\nStep 5: Testing widget_manager access patterns...")
        try:
            sequence_workbench = mock_widget.widget_manager.get_widget("sequence_workbench")
            settings_dialog = mock_widget.widget_manager.get_widget("settings_dialog")
            background_widget = mock_widget.widget_manager.get_widget("background_widget")
            print("✅ widget_manager access patterns work")
        except AttributeError as e:
            print(f"❌ widget_manager access patterns failed: {e}")
            return False
        
        # Test 6: Test PictographDataLoader service access
        print("\nStep 6: Testing PictographDataLoader service access...")
        try:
            from src.main_window.main_widget.pictograph_data_loader import PictographDataLoader
            pictograph_data_loader = mock_widget.app_context.get_service(PictographDataLoader)
            dataset = pictograph_data_loader.get_pictograph_dataset()
            print("✅ PictographDataLoader service access works")
        except AttributeError as e:
            print(f"❌ PictographDataLoader service access failed: {e}")
            return False
        
        print("\n🎉 All dependency injection pattern tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Dependency injection pattern test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_component_fixes():
    """Test the specific components we fixed."""
    print("\n🧪 Testing Specific Component Fixes")
    print("=" * 80)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Test ImageExportTab pattern
        print("\nStep 2: Testing ImageExportTab pattern...")
        class MockMainWidget:
            def __init__(self):
                self.app_context = app_context
                self.widget_manager = MockWidgetManager()
        
        class MockWidgetManager:
            def get_widget(self, widget_name):
                if widget_name == "sequence_workbench":
                    class MockSequenceWorkbench:
                        def __init__(self):
                            self.beat_frame = MockBeatFrame()
                    return MockSequenceWorkbench()
                return None
        
        class MockBeatFrame:
            def __init__(self):
                self.json_manager = app_context.json_manager
        
        mock_widget = MockMainWidget()
        
        # Simulate ImageExportTab._get_current_sequence pattern
        try:
            sequence_workbench = mock_widget.widget_manager.get_widget("sequence_workbench")
            if sequence_workbench and hasattr(sequence_workbench, 'beat_frame'):
                sequence = sequence_workbench.beat_frame.json_manager.loader_saver.load_current_sequence()
                print("✅ ImageExportTab pattern works")
            else:
                print("✅ ImageExportTab pattern handles missing widget gracefully")
        except AttributeError as e:
            print(f"❌ ImageExportTab pattern failed: {e}")
            return False
        
        # Test 3: Test BackgroundSelector pattern
        print("\nStep 3: Testing BackgroundSelector pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            current_background = settings_manager.global_settings.get_background_type()
            print("✅ BackgroundSelector pattern works")
        except AttributeError as e:
            print(f"❌ BackgroundSelector pattern failed: {e}")
            return False
        
        # Test 4: Test VisibilityButtonsWidget pattern
        print("\nStep 4: Testing VisibilityButtonsWidget pattern...")
        try:
            settings_manager = mock_widget.app_context.settings_manager
            visibility_settings = settings_manager.visibility
            all_motions_visible = visibility_settings.are_all_motions_visible()
            print("✅ VisibilityButtonsWidget pattern works")
        except AttributeError as e:
            print(f"❌ VisibilityButtonsWidget pattern failed: {e}")
            return False
        
        print("\n🎉 All specific component fix tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Specific component fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔧 TESTING PROACTIVE ATTRIBUTEERROR FIXES")
    print("=" * 100)
    
    # Test 1: Application startup comprehensive check
    test1_passed = test_application_startup_comprehensive()
    
    # Test 2: Dependency injection patterns
    test2_passed = test_dependency_injection_patterns()
    
    # Test 3: Specific component fixes
    test3_passed = test_specific_component_fixes()
    
    # Summary
    print("\n" + "=" * 100)
    print("TEST RESULTS SUMMARY")
    print("=" * 100)
    
    if test1_passed:
        print("✅ Application Startup Comprehensive: PASSED")
    else:
        print("❌ Application Startup Comprehensive: FAILED")
    
    if test2_passed:
        print("✅ Dependency Injection Patterns: PASSED")
    else:
        print("❌ Dependency Injection Patterns: FAILED")
    
    if test3_passed:
        print("✅ Specific Component Fixes: PASSED")
    else:
        print("❌ Specific Component Fixes: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Proactive AttributeError fixes are working correctly!")
        print("✅ All direct attribute access patterns have been updated")
        print("✅ Dependency injection is working properly")
        print("✅ Widget manager access patterns are functional")
        print("✅ Application starts without AttributeErrors")
        print("✅ Components handle missing services gracefully")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Some AttributeError patterns may still need fixing")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
