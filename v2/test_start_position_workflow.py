#!/usr/bin/env python3
"""
Start Position Workflow Test - Kinetic Constructor v2

This test verifies that the start position selection workflow is properly
separated from sequence building and follows v1 behavior exactly.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class StartPositionWorkflowTestWindow(QMainWindow):
    """Test window for start position workflow verification"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Start Position Workflow Test")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Connect signals to monitor behavior
        self.construct_tab.start_position_set.connect(self.on_start_position_set)
        self.construct_tab.sequence_created.connect(self.on_sequence_created)
        self.construct_tab.sequence_modified.connect(self.on_sequence_modified)
        
        # Set up monitoring after a short delay
        QTimer.singleShot(1000, self.start_monitoring)
        
    def start_monitoring(self):
        """Start monitoring the workflow"""
        print("🎯 Start Position Workflow Test Started")
        print("=" * 60)
        print()
        print("📋 Expected V1 Workflow:")
        print("   1. User selects start position in start position picker")
        print("   2. Start position populates the (0,0) slot in beat frame")
        print("   3. START text overlay appears on the start position pictograph")
        print("   4. NO sequence beats are created or modified")
        print("   5. Start position data is stored separately from sequence")
        print("   6. Option picker becomes available for building sequence")
        print()
        print("🔍 Monitoring Signals:")
        print("   - start_position_set: Should fire when start position selected")
        print("   - sequence_created: Should NOT fire for start position selection")
        print("   - sequence_modified: Should NOT fire for start position selection")
        print()
        print("🎯 Instructions:")
        print("   1. Click on any start position in the picker")
        print("   2. Observe the beat frame (0,0) slot")
        print("   3. Verify no sequence beats are created")
        print("   4. Check that START text overlay is visible")
        print()
        
    def on_start_position_set(self, position_key: str):
        """Handle start position set signal"""
        print(f"✅ START POSITION SET: {position_key}")
        print("   - This is CORRECT behavior for start position selection")
        
        # Check the workbench state
        workbench = self.construct_tab.workbench
        start_position = workbench.get_start_position()
        current_sequence = workbench.get_sequence()
        
        print(f"   - Start position data: {start_position.letter if start_position else 'None'}")
        print(f"   - Current sequence beats: {len(current_sequence.beats) if current_sequence else 0}")
        
        if start_position and (not current_sequence or len(current_sequence.beats) == 0):
            print("   ✅ CORRECT: Start position set without creating sequence beats")
        else:
            print("   ❌ ERROR: Start position selection incorrectly modified sequence")
        print()
        
    def on_sequence_created(self, sequence):
        """Handle sequence created signal"""
        print(f"❌ SEQUENCE CREATED: {sequence.name} ({len(sequence.beats)} beats)")
        print("   - This should NOT happen for start position selection!")
        print("   - Start position should be separate from sequence beats")
        print()
        
    def on_sequence_modified(self, sequence):
        """Handle sequence modified signal"""
        print(f"❌ SEQUENCE MODIFIED: {sequence.name} ({len(sequence.beats)} beats)")
        print("   - This should NOT happen for start position selection!")
        print("   - Start position should be separate from sequence beats")
        print()


def main():
    """Run the start position workflow test"""
    print("🎯 Starting Start Position Workflow Test...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Start Position Workflow Test")
    
    # Create and show test window
    window = StartPositionWorkflowTestWindow()
    window.show()
    
    print("🎯 Test window created - interact with start position picker")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
