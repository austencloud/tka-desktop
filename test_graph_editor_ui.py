#!/usr/bin/env python3
"""
Test Modern Graph Editor UI Components
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))

def test_ui_imports():
    """Test UI component imports (without Qt instantiation)"""
    try:
        print("Testing UI component imports...")
        
        # Test graph editor components (just imports, no Qt)
        print("  - Testing graph_section import...")
        from presentation.components.workbench.graph_section import WorkbenchGraphSection
        print("    ✅ WorkbenchGraphSection import successful")
        
        print("  - Testing graph_editor import...")
        from presentation.components.workbench.graph_editor.graph_editor import GraphEditor
        print("    ✅ GraphEditor import successful")
        
        print("  - Testing pictograph_container import...")
        from presentation.components.workbench.graph_editor.pictograph_container import GraphEditorPictographContainer
        print("    ✅ GraphEditorPictographContainer import successful")
        
        print("  - Testing adjustment_panel import...")
        from presentation.components.workbench.graph_editor.adjustment_panel import AdjustmentPanel
        print("    ✅ AdjustmentPanel import successful")
        
        print("  - Testing modern_toggle_tab import...")
        from presentation.components.workbench.graph_editor.modern_toggle_tab import ModernToggleTab
        print("    ✅ ModernToggleTab import successful")
        
        print("\n🎉 All UI component imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ UI import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workbench_imports():
    """Test workbench imports"""
    try:
        print("\nTesting workbench imports...")
        
        print("  - Testing main workbench import...")
        from presentation.components.workbench.workbench import ModernSequenceWorkbench
        print("    ✅ ModernSequenceWorkbench import successful")
        
        print("  - Testing workbench factory import...")
        from presentation.factories.workbench_factory import create_modern_workbench
        print("    ✅ Workbench factory import successful")
        
        print("\n🎉 All workbench imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Workbench import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_service_integration():
    """Test that services integrate properly with workbench"""
    try:
        print("\nTesting service integration...")
        
        from core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import configure_workbench_services
        from core.interfaces.workbench_services import IGraphEditorService
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from application.services.ui.layout_management_service import LayoutManagementService
        from application.services.ui.ui_state_management_service import UIStateManagementService
        
        # Create container and configure basic services
        container = DIContainer()
        
        # Register prerequisite services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        
        print("  - Basic services registered")
        
        # Configure workbench services
        configure_workbench_services(container)
        print("  - Workbench services configured")
        
        # Test that graph editor service is available
        graph_service = container.resolve(IGraphEditorService)
        print(f"  - Graph service resolved: {type(graph_service)}")
        
        print("\n🎉 Service integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Service integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Modern Graph Editor UI Components Test")
    print("=" * 60)
    
    tests = [
        test_ui_imports,
        test_workbench_imports,
        test_service_integration,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Modern Graph Editor UI is ready for integration.")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
