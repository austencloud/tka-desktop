#!/usr/bin/env python3
"""Debug script to investigate widget_factory import issues"""

import sys
import traceback
import os

# Add the source path
sys.path.append("modern/src")

print("=== Debug Import Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path includes: {[p for p in sys.path if 'tka-desktop' in p]}")

try:
    print("\n1. Testing basic imports...")
    from typing import Optional

    print("✓ typing imported")

    from PyQt6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QScrollArea,
        QSizePolicy,
        QApplication,
    )

    print("✓ PyQt6.QtWidgets imported")

    from PyQt6.QtCore import Qt

    print("✓ PyQt6.QtCore imported")

    from PyQt6.QtGui import QScreen

    print("✓ PyQt6.QtGui imported")

except Exception as e:
    print(f"✗ Basic imports failed: {e}")
    traceback.print_exc()

try:
    print("\n2. Testing core imports...")
    from core.dependency_injection.di_container import DIContainer

    print("✓ DIContainer imported")

    from core.interfaces.core_services import ILayoutService

    print("✓ ILayoutService imported")

except Exception as e:
    print(f"✗ Core imports failed: {e}")
    traceback.print_exc()

try:
    print("\n3. Testing option picker component imports...")
    from presentation.components.option_picker.option_picker_widget import (
        ModernOptionPickerWidget,
    )

    print("✓ ModernOptionPickerWidget imported")

    from presentation.components.option_picker.option_picker_filter import (
        OptionPickerFilter,
    )

    print("✓ OptionPickerFilter imported")

except Exception as e:
    print(f"✗ Option picker component imports failed: {e}")
    traceback.print_exc()

try:
    print("\n4. Testing widget_factory module import...")
    import presentation.factories.widget_factory as wf_module

    print("✓ widget_factory module imported")
    print(f"   Module file: {wf_module.__file__}")
    print(
        f"   Module attributes: {[attr for attr in dir(wf_module) if not attr.startswith('_')]}"
    )

except Exception as e:
    print(f"✗ widget_factory module import failed: {e}")
    traceback.print_exc()

try:
    print("\n5. Testing direct file execution...")
    with open("modern/src/presentation/factories/widget_factory.py", "r") as f:
        content = f.read()

    print(f"   File size: {len(content)} characters")
    print(
        f"   File contains 'class OptionPickerWidgetFactory': {'class OptionPickerWidgetFactory' in content}"
    )

    # Try to execute the file content manually
    exec(content, globals())
    print("✓ File content executed successfully")
    print(
        f"   OptionPickerWidgetFactory defined: {'OptionPickerWidgetFactory' in globals()}"
    )

except Exception as e:
    print(f"✗ Direct file execution failed: {e}")
    traceback.print_exc()

try:
    print("\n6. Testing specific class import...")
    from presentation.factories.widget_factory import OptionPickerWidgetFactory

    print("✓ OptionPickerWidgetFactory imported successfully")

except Exception as e:
    print(f"✗ OptionPickerWidgetFactory import failed: {e}")
    traceback.print_exc()

print("\n=== Debug Complete ===")
