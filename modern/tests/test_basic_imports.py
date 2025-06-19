#!/usr/bin/env python3
"""
Test basic imports to identify hanging issues
"""

print("Starting basic import test...")

try:
    print("1. Testing sys import...")
    import sys
    print("   ✅ sys imported")
    
    print("2. Testing PyQt6 import...")
    import PyQt6.QtWidgets
    print("   ✅ PyQt6.QtWidgets imported")
    
    print("3. Testing pathlib import...")
    from pathlib import Path
    print("   ✅ pathlib imported")
    
    print("4. Adding src to path...")
    sys.path.insert(0, str(Path('src')))
    print("   ✅ src added to path")
    
    print("5. Testing core imports...")
    from core.dependency_injection.di_container import DIContainer
    print("   ✅ DIContainer imported")
    
    print("6. Testing presentation imports...")
    from presentation.components.component_base import ViewableComponentBase
    print("   ✅ ViewableComponentBase imported")
    
    print("\n🎉 All basic imports successful!")
    print("The issue is likely in main.py execution, not imports.")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
