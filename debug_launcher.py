#!/usr/bin/env python3
"""
Debug script to isolate TKA Launcher issues
"""

import sys
from pathlib import Path

# Add launcher to path
launcher_dir = Path(__file__).parent / "launcher"
sys.path.insert(0, str(launcher_dir))

def test_imports():
    """Test individual component imports"""
    print("Testing imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6.QtWidgets imported")
    except Exception as e:
        print(f"❌ PyQt6.QtWidgets failed: {e}")
        return False
    
    try:
        from launcher.ui.components.command_palette import CommandPalette
        print("✅ CommandPalette imported")
    except Exception as e:
        print(f"❌ CommandPalette failed: {e}")
    
    try:
        from launcher.ui.components.health_indicator import HealthIndicator
        print("✅ HealthIndicator imported")
    except Exception as e:
        print(f"❌ HealthIndicator failed: {e}")
    
    try:
        from launcher.ui.components.responsive_grid import ResponsiveAppGrid
        print("✅ ResponsiveAppGrid imported")
    except Exception as e:
        print(f"❌ ResponsiveAppGrid failed: {e}")
    
    try:
        from launcher.core.accessibility import AccessibilityManager
        print("✅ AccessibilityManager imported")
    except Exception as e:
        print(f"❌ AccessibilityManager failed: {e}")
    
    try:
        from launcher.core.animations import AnimationManager
        print("✅ AnimationManager imported")
    except Exception as e:
        print(f"❌ AnimationManager failed: {e}")
    
    return True

def test_basic_window():
    """Test basic window creation"""
    print("\nTesting basic window creation...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
        
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        window = QMainWindow()
        window.setWindowTitle("Debug Test")
        window.setCentralWidget(QLabel("Basic window test"))
        print("✅ Basic window created")
        
        window.show()
        print("✅ Basic window shown")
        
        # Don't run exec() in test
        window.close()
        return True
        
    except Exception as e:
        print(f"❌ Basic window test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_launcher_components():
    """Test launcher components individually"""
    print("\nTesting launcher components...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from launcher.core.accessibility import AccessibilityManager
        from launcher.core.animations import AnimationManager
        
        app = QApplication(sys.argv)
        print("✅ QApplication for components created")
        
        # Test AccessibilityManager
        accessibility = AccessibilityManager.instance()
        print("✅ AccessibilityManager created")
        
        # Test AnimationManager
        animations = AnimationManager()
        print("✅ AnimationManager created")
        
        # Test HealthIndicator
        from launcher.ui.components.health_indicator import HealthIndicator
        health = HealthIndicator()
        print("✅ HealthIndicator created")
        
        # Test CommandPalette
        from launcher.ui.components.command_palette import CommandPalette
        palette = CommandPalette()
        print("✅ CommandPalette created")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_window():
    """Test main window creation step by step"""
    print("\nTesting main window creation...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Import main window
        from launcher.ui.main_window import LauncherWindow
        print("✅ LauncherWindow imported")
        
        # Create window
        print("Creating LauncherWindow...")
        window = LauncherWindow()
        print("✅ LauncherWindow created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Main window creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 TKA Launcher Debug Session")
    print("=" * 50)
    
    # Run tests
    if not test_imports():
        sys.exit(1)
    
    if not test_basic_window():
        sys.exit(1)
    
    if not test_launcher_components():
        sys.exit(1)
    
    if not test_main_window():
        sys.exit(1)
    
    print("\n🎉 All tests passed! The launcher should work.")
