#!/usr/bin/env python3
"""
Minimal test version of main.py to isolate hanging issues
"""

print("Starting minimal main test...")

try:
    print("1. Testing basic imports...")
    import sys
    from pathlib import Path
    print("   ✅ Basic imports OK")
    
    print("2. Testing PyQt6 imports...")
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QGuiApplication
    print("   ✅ PyQt6 imports OK")
    
    print("3. Adding src to path...")
    modern_src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(modern_src_path))
    print("   ✅ Path added")
    
    print("4. Testing core imports...")
    from core.dependency_injection.di_container import get_container
    print("   ✅ DI container import OK")
    
    print("5. Testing interface imports...")
    from core.interfaces.core_services import IUIStateManagementService, ILayoutService
    print("   ✅ Interface imports OK")
    
    print("6. Testing presentation imports...")
    from presentation.components.ui.splash_screen import SplashScreen
    print("   ✅ Splash screen import OK")
    
    print("7. Creating minimal QApplication...")
    app = QApplication(sys.argv)
    print("   ✅ QApplication created")
    
    print("8. Creating minimal window...")
    window = QMainWindow()
    window.setWindowTitle("Minimal Test")
    window.resize(400, 300)
    print("   ✅ Window created")
    
    print("9. Testing window show...")
    window.show()
    print("   ✅ Window shown")
    
    print("\n🎉 Minimal main test successful!")
    print("The issue is likely in the full main.py execution, not basic imports.")
    
    # Don't run the event loop to avoid hanging
    # app.exec()
    
except Exception as e:
    print(f"\n❌ Minimal main test failed: {e}")
    import traceback
    traceback.print_exc()
