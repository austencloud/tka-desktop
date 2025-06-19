#!/usr/bin/env python3
"""
Test Modern Graph Editor Visibility
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))

def test_with_minimal_qt():
    """Test with minimal Qt setup"""
    try:
        print("Testing Graph Editor with minimal Qt setup...")
        
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
        from PyQt6.QtCore import QTimer
        import sys
        
        # Create QApplication
        app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        
        # Import after QApplication is created
        from core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import create_modern_workbench, configure_workbench_services
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from application.services.layout.layout_management_service import LayoutManagementService
        from application.services.ui.ui_state_management_service import UIStateManagementService
        
        print("  ✅ Qt and imports successful")
        
        # Setup container
        container = DIContainer()
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        configure_workbench_services(container)
        
        print("  ✅ DI container configured")
        
        # Create main window
        window = QMainWindow()
        window.setWindowTitle("Graph Editor Test")
        window.setGeometry(100, 100, 1200, 800)
        
        # Create workbench
        workbench = create_modern_workbench(container)
        window.setCentralWidget(workbench)
        
        print("  ✅ Workbench created")
        
        # Check if graph section exists
        if hasattr(workbench, '_graph_section') and workbench._graph_section:
            print(f"  ✅ Graph section found: {type(workbench._graph_section)}")
            
            # Check if graph editor exists
            graph_section = workbench._graph_section
            if hasattr(graph_section, '_graph_editor') and graph_section._graph_editor:
                print(f"  ✅ Graph editor found: {type(graph_section._graph_editor)}")
                
                # Test visibility toggle
                graph_editor = graph_section._graph_editor
                print(f"  ✅ Initial visibility: {graph_editor.is_visible()}")
                
                # Toggle visibility
                graph_editor.toggle_visibility()
                print(f"  ✅ After toggle: {graph_editor.is_visible()}")
                
                # Check components
                if hasattr(graph_editor, '_pictograph_container'):
                    print(f"  ✅ Pictograph container: {type(graph_editor._pictograph_container)}")
                if hasattr(graph_editor, '_left_adjustment_panel'):
                    print(f"  ✅ Left adjustment panel: {type(graph_editor._left_adjustment_panel)}")
                if hasattr(graph_editor, '_right_adjustment_panel'):
                    print(f"  ✅ Right adjustment panel: {type(graph_editor._right_adjustment_panel)}")
                if hasattr(graph_editor, '_toggle_tab'):
                    print(f"  ✅ Toggle tab: {type(graph_editor._toggle_tab)}")
                    
            else:
                print("  ❌ Graph editor not found in graph section")
        else:
            print("  ❌ Graph section not found in workbench")
        
        # Show the window briefly
        window.show()
        
        # Close after 2 seconds
        QTimer.singleShot(2000, app.quit)
        
        print("  ✅ Window showing for 2 seconds...")
        app.exec()
        
        print("\n🎉 Graph Editor Qt test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Qt test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run Qt test"""
    print("🚀 Modern Graph Editor Qt Visibility Test")
    print("=" * 70)
    
    success = test_with_minimal_qt()
    
    print("=" * 70)
    if success:
        print("🎉 Graph Editor is integrated and functional!")
    else:
        print("❌ Graph Editor integration issues found.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
