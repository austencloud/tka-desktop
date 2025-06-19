#!/usr/bin/env python3
"""
Test Modern Graph Editor UI Visibility
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))


def test_ui_with_qt():
    """Test UI components with actual Qt application"""
    try:
        print("🎨 Testing Graph Editor UI Visibility...")

        # Import Qt components
        from PyQt6.QtWidgets import (
            QApplication,
            QMainWindow,
            QVBoxLayout,
            QWidget,
            QPushButton,
        )
        from PyQt6.QtCore import QTimer

        # Import our components
        from core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import (
            create_modern_workbench,
            configure_workbench_services,
        )
        from core.interfaces.core_services import (
            ILayoutService,
            IUIStateManagementService,
        )
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )

        # Create Qt application
        app = QApplication(sys.argv)

        # Create DI container and configure services
        container = DIContainer()
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(
            IUIStateManagementService, UIStateManagementService
        )
        configure_workbench_services(container)

        print("  ✅ Services configured")

        # Create main window
        window = QMainWindow()
        window.setWindowTitle("Graph Editor Visibility Test")
        window.setGeometry(100, 100, 1200, 800)

        # Create workbench
        workbench = create_modern_workbench(container, window)
        window.setCentralWidget(workbench)

        print("  ✅ Workbench created")

        # Show window
        window.show()

        print("  ✅ Window shown")

        # Check if graph section exists
        if hasattr(workbench, "_graph_section") and workbench._graph_section:
            graph_section = workbench._graph_section
            print(f"  ✅ Graph section found: {type(graph_section).__name__}")

            # Check if graph editor exists
            if hasattr(graph_section, "_graph_editor") and graph_section._graph_editor:
                graph_editor = graph_section._graph_editor
                print(f"  ✅ Graph editor found: {type(graph_editor).__name__}")
                print(f"      Graph editor visible: {graph_editor.isVisible()}")
                print(
                    f"      Graph editor size: {graph_editor.size().width()}x{graph_editor.size().height()}"
                )

                # Check if toggle tab exists
                if hasattr(graph_editor, "_toggle_tab") and graph_editor._toggle_tab:
                    toggle_tab = graph_editor._toggle_tab
                    print(f"  ✅ Toggle tab found: {type(toggle_tab).__name__}")
                    print(f"      Toggle tab visible: {toggle_tab.isVisible()}")
                    print(
                        f"      Toggle tab position: {toggle_tab.pos().x()}, {toggle_tab.pos().y()}"
                    )
                    print(
                        f"      Toggle tab size: {toggle_tab.size().width()}x{toggle_tab.size().height()}"
                    )

                    # Force toggle tab to be visible and positioned
                    def show_toggle_tab():
                        toggle_tab.show()
                        toggle_tab.raise_()
                        print(f"  🔧 Forced toggle tab to show")

                    QTimer.singleShot(500, show_toggle_tab)
                else:
                    print("  ❌ Toggle tab not found")
            else:
                print("  ❌ Graph editor not found")
        else:
            print("  ❌ Graph section not found")

        print(f"\n📊 Window will stay open for 10 seconds for visual inspection...")

        # Create timer to close after 10 seconds
        def close_app():
            print("🔚 Closing application")
            app.quit()

        QTimer.singleShot(10000, close_app)

        # Run the application
        app.exec()
        print("✅ Qt application test completed")
        return True

    except Exception as e:
        print(f"❌ Qt test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run UI visibility test"""
    print("🚀 Modern Graph Editor UI Visibility Test")
    print("=" * 60)

    success = test_ui_with_qt()

    print("=" * 60)
    if success:
        print("🎉 Test completed successfully!")
        print("Check the window that appeared to see if the toggle tab is visible.")
    else:
        print("❌ Test failed.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
