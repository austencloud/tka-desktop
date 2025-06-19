#!/usr/bin/env python3
"""
Interactive Graph Editor Test - Shows toggle tab immediately
"""

import sys
import os
from pathlib import Path

# Add the modern source to path
modern_src = Path(__file__).parent / "modern" / "src"
sys.path.insert(0, str(modern_src))

def create_test_app():
    """Create an interactive test application"""
    try:
        print("🎨 Creating Interactive Graph Editor Test...")
        
        # Import Qt components
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
        from PyQt6.QtCore import QTimer
        
        # Import our components
        from core.dependency_injection.di_container import DIContainer
        from presentation.factories.workbench_factory import create_modern_workbench, configure_workbench_services
        from core.interfaces.core_services import ILayoutService, IUIStateManagementService
        from application.services.layout.layout_management_service import LayoutManagementService
        from application.services.ui.ui_state_management_service import UIStateManagementService
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create DI container and configure services
        container = DIContainer()
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(IUIStateManagementService, UIStateManagementService)
        configure_workbench_services(container)
        
        # Create main window with controls
        window = QMainWindow()
        window.setWindowTitle("🎯 Graph Editor Interactive Test")
        window.setGeometry(100, 100, 1200, 800)
        
        # Main widget with controls and workbench
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Status label
        status_label = QLabel("Graph Editor Status: Not initialized")
        control_layout.addWidget(status_label)
        
        # Toggle button
        toggle_btn = QPushButton("Toggle Graph Editor")
        control_layout.addWidget(toggle_btn)
        
        # Show toggle tab button
        show_tab_btn = QPushButton("Force Show Toggle Tab")
        control_layout.addWidget(show_tab_btn)
        
        main_layout.addWidget(control_panel)
        
        # Create workbench
        workbench = create_modern_workbench(container, main_widget)
        main_layout.addWidget(workbench)
        
        window.setCentralWidget(main_widget)
        
        # Get references to graph components
        graph_section = workbench._graph_section
        graph_editor = graph_section._graph_editor
        toggle_tab = graph_editor._toggle_tab
        
        def update_status():
            """Update status display"""
            status = f"Graph Editor: {'Visible' if graph_editor.isVisible() else 'Hidden'}, "
            status += f"Height: {graph_editor.height()}, "
            status += f"Toggle Tab: {'Visible' if toggle_tab.isVisible() else 'Hidden'}"
            status_label.setText(status)
        
        def toggle_graph():
            """Toggle graph editor visibility"""
            print("🔽 Toggle button clicked")
            graph_editor.toggle_visibility()
            QTimer.singleShot(100, update_status)
        
        def force_show_tab():
            """Force toggle tab to be visible"""
            print("👁️ Forcing toggle tab to show")
            toggle_tab.show()
            toggle_tab.raise_()
            toggle_tab._position_tab()
            update_status()
        
        # Connect buttons
        toggle_btn.clicked.connect(toggle_graph)
        show_tab_btn.clicked.connect(force_show_tab)
        
        # Initial setup
        def initial_setup():
            print("🔧 Setting up initial state...")
            # Force the toggle tab to be visible immediately
            toggle_tab.show()
            toggle_tab.raise_()
            toggle_tab._position_tab()
            update_status()
            print("✅ Toggle tab should now be visible!")
        
        QTimer.singleShot(500, initial_setup)
        
        # Update status every second
        status_timer = QTimer()
        status_timer.timeout.connect(update_status)
        status_timer.start(1000)
        
        # Show window
        window.show()
        
        print("✅ Interactive test window created")
        print("📋 Instructions:")
        print("  1. Look for the toggle tab at the bottom of the window")
        print("  2. Click 'Force Show Toggle Tab' if you don't see it")
        print("  3. Click the toggle tab or 'Toggle Graph Editor' to show/hide the graph editor")
        print("  4. Test the graph editor functionality")
        
        return app, window
        
    except Exception as e:
        print(f"❌ Failed to create test app: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """Run interactive test"""
    print("🚀 Interactive Graph Editor Test")
    print("=" * 60)
    
    app, window = create_test_app()
    
    if app and window:
        print("🎉 Test application ready!")
        print("Press Ctrl+C to exit when done testing.")
        try:
            app.exec()
        except KeyboardInterrupt:
            print("\n🔚 Test interrupted by user")
        print("✅ Test completed")
        return True
    else:
        print("❌ Failed to create test application")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
