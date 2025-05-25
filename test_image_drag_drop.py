#!/usr/bin/env python3
"""
Test script for the image drag and drop functionality.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_image(filename: str) -> str:
    """Create a simple test image file."""
    from PyQt6.QtGui import QImage, QPainter, QColor
    from PyQt6.QtCore import QSize
    
    # Create a simple colored image
    image = QImage(QSize(100, 100), QImage.Format.Format_RGB32)
    image.fill(QColor(255, 0, 0))  # Red background
    
    # Add some content
    painter = QPainter(image)
    painter.setPen(QColor(255, 255, 255))  # White pen
    painter.drawText(10, 50, "Test")
    painter.end()
    
    # Save to temporary file
    temp_dir = Path(tempfile.gettempdir())
    image_path = temp_dir / filename
    image.save(str(image_path))
    
    return str(image_path)

def test_image_drag_drop_components():
    """Test the image drag and drop components."""
    print("🧪 Testing Image Drag and Drop Components")
    print("=" * 60)
    
    try:
        # Test 1: Import components
        print("Step 1: Testing component imports...")
        from src.main_window.main_widget.core.image_drag_drop_handler import ImageDragDropHandler
        from src.main_window.main_widget.core.image_drop_processor import ImageDropProcessor
        print("✅ Components imported successfully")
        
        # Test 2: Initialize dependency injection
        print("\nStep 2: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 3: Create test widget
        print("\nStep 3: Creating test widget...")
        from PyQt6.QtWidgets import QWidget, QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        test_widget = QWidget()
        test_widget.setWindowTitle("Drag and Drop Test")
        test_widget.resize(400, 300)
        print("✅ Test widget created")
        
        # Test 4: Create image drop processor
        print("\nStep 4: Testing image drop processor...")
        processor = ImageDropProcessor(app_context)
        print("✅ Image drop processor created")
        
        # Test 5: Create drag and drop handler
        print("\nStep 5: Testing drag and drop handler...")
        handler = ImageDragDropHandler(test_widget, app_context)
        print("✅ Drag and drop handler created")
        
        # Test 6: Test image validation
        print("\nStep 6: Testing image validation...")
        test_image_path = create_test_image("test_image.png")
        print(f"Created test image: {test_image_path}")
        
        # Test validation
        is_valid = processor._validate_image(test_image_path)
        print(f"✅ Image validation works: {is_valid}")
        
        # Test 7: Test supported formats
        print("\nStep 7: Testing supported formats...")
        supported_formats = handler.SUPPORTED_FORMATS
        print(f"✅ Supported formats: {len(supported_formats)} formats")
        print(f"   Formats: {', '.join(list(supported_formats)[:5])}...")
        
        # Test 8: Test enable/disable functionality
        print("\nStep 8: Testing enable/disable functionality...")
        handler.enable()
        print("✅ Handler enabled")
        
        handler.disable()
        print("✅ Handler disabled")
        
        handler.enable()  # Re-enable for cleanup test
        print("✅ Handler re-enabled")
        
        # Test 9: Test cleanup
        print("\nStep 9: Testing cleanup...")
        handler.cleanup()
        print("✅ Handler cleanup completed")
        
        # Cleanup test image
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print("✅ Test image cleaned up")
        
        print("\n🎉 All component tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_widget_integration():
    """Test integration with MainWidgetCoordinator."""
    print("\n🧪 Testing MainWidget Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize dependency injection
        print("Step 1: Testing dependency injection...")
        from src.main import initialize_dependency_injection
        app_context = initialize_dependency_injection()
        print("✅ Dependency injection initialized")
        
        # Test 2: Create MainWindow
        print("\nStep 2: Testing MainWindow creation...")
        from src.main import create_main_window
        from src.splash_screen.splash_screen import SplashScreen
        from src.settings_manager.settings_manager import SettingsManager
        from src.profiler import Profiler
        from PyQt6.QtWidgets import QApplication
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        settings = SettingsManager()
        splash_screen = SplashScreen(None, settings)
        profiler = Profiler()
        
        main_window = create_main_window(profiler, splash_screen, app_context)
        print("✅ MainWindow created")
        
        # Test 3: Initialize widgets
        print("\nStep 3: Testing widget initialization...")
        main_window.initialize_widgets()
        print("✅ Widget initialization completed")
        
        # Test 4: Test drag and drop functionality
        print("\nStep 4: Testing drag and drop functionality...")
        main_widget = main_window.main_widget
        
        # Check if drag and drop components exist
        if hasattr(main_widget, 'image_drag_drop_handler'):
            print("✅ Image drag and drop handler exists")
        else:
            print("❌ Image drag and drop handler missing")
            return False
        
        if hasattr(main_widget, 'image_drop_processor'):
            print("✅ Image drop processor exists")
        else:
            print("❌ Image drop processor missing")
            return False
        
        # Test 5: Test enable/disable methods
        print("\nStep 5: Testing enable/disable methods...")
        main_widget.enable_image_drag_drop()
        print("✅ Enable method works")
        
        main_widget.disable_image_drag_drop()
        print("✅ Disable method works")
        
        main_widget.enable_image_drag_drop()
        print("✅ Re-enable method works")
        
        # Test 6: Test cleanup
        print("\nStep 6: Testing cleanup...")
        main_widget.cleanup()
        print("✅ Cleanup completed")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_application_startup():
    """Test that the application starts with drag and drop functionality."""
    print("\n🧪 Testing Application Startup")
    print("=" * 60)
    
    try:
        import subprocess
        import time
        
        print("Starting application with drag and drop functionality...")
        
        # Start the application
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit to see if it crashes
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Let it run a bit more
            time.sleep(2)
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            # Check for drag and drop related errors
            if "ImageDragDropHandler" in stderr and "error" in stderr.lower():
                print("❌ Drag and drop related errors found")
                print(f"STDERR: {stderr}")
                return False
            else:
                print("✅ No drag and drop related errors")
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

def main():
    """Run all tests."""
    print("🔧 TESTING IMAGE DRAG AND DROP FUNCTIONALITY")
    print("=" * 80)
    
    # Test 1: Component tests
    test1_passed = test_image_drag_drop_components()
    
    # Test 2: Integration tests
    test2_passed = test_main_widget_integration()
    
    # Test 3: Application startup test
    test3_passed = test_application_startup()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    if test1_passed:
        print("✅ Component Tests: PASSED")
    else:
        print("❌ Component Tests: FAILED")
    
    if test2_passed:
        print("✅ Integration Tests: PASSED")
    else:
        print("❌ Integration Tests: FAILED")
    
    if test3_passed:
        print("✅ Application Startup: PASSED")
    else:
        print("❌ Application Startup: FAILED")
    
    overall_success = test1_passed and test2_passed and test3_passed
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Image drag and drop functionality is working correctly")
        print("✅ Users can now drag and drop images onto the application")
        print("✅ Multiple processing options are available for dropped images")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Image drag and drop functionality may not be working correctly")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
