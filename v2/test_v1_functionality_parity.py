#!/usr/bin/env python3
"""
V1 Functionality Parity Test - Kinetic Constructor v2

This test verifies the three critical V1 functionality gaps have been implemented:
1. Clear Sequence Button Functionality
2. START Text Overlay Display  
3. Start Position to Option Picker Integration

Tests each functionality independently and together to ensure V1 parity.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class V1FunctionalityParityTestWindow(QMainWindow):
    """Test window for V1 functionality parity verification"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 V1 Functionality Parity Test")
        self.setGeometry(100, 100, 1800, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create test control panel
        self._create_test_controls(layout)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Connect signals to monitor behavior
        self._connect_signals()
        
        # Set up monitoring after a short delay
        QTimer.singleShot(1000, self.start_monitoring)
        
    def _create_test_controls(self, layout):
        """Create test control buttons"""
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        
        # Test buttons
        self.test_clear_btn = QPushButton("🗑️ Test Clear Sequence")
        self.test_clear_btn.clicked.connect(self.test_clear_sequence)
        controls_layout.addWidget(self.test_clear_btn)
        
        self.test_start_text_btn = QPushButton("📝 Test START Text")
        self.test_start_text_btn.clicked.connect(self.test_start_text_overlay)
        controls_layout.addWidget(self.test_start_text_btn)
        
        self.test_integration_btn = QPushButton("🔗 Test Integration")
        self.test_integration_btn.clicked.connect(self.test_start_position_integration)
        controls_layout.addWidget(self.test_integration_btn)
        
        layout.addWidget(controls_widget)
        
    def _connect_signals(self):
        """Connect signals to monitor behavior"""
        self.construct_tab.start_position_set.connect(self.on_start_position_set)
        self.construct_tab.sequence_created.connect(self.on_sequence_created)
        self.construct_tab.sequence_modified.connect(self.on_sequence_modified)
        
    def start_monitoring(self):
        """Start monitoring the functionality"""
        print("🎯 V1 Functionality Parity Test Started")
        print("=" * 80)
        print()
        print("📋 Testing Three Critical V1 Functionality Gaps:")
        print("   1. Clear Sequence Button - preserves start position at (0,0)")
        print("   2. START Text Overlay - always visible on start position")
        print("   3. Start Position Integration - populates option picker")
        print()
        print("🔍 Instructions:")
        print("   1. Select a start position to test integration")
        print("   2. Use test buttons to verify each functionality")
        print("   3. Check that START text is always visible")
        print("   4. Verify clear preserves start position")
        print()
        
    def test_clear_sequence(self):
        """Test clear sequence functionality"""
        print("\n🗑️ TESTING CLEAR SEQUENCE FUNCTIONALITY")
        print("-" * 50)
        
        # Get current workbench state
        workbench = self.construct_tab.workbench
        start_position = workbench.get_start_position()
        current_sequence = workbench.get_sequence()
        
        print(f"   Before clear - Start position: {start_position.letter if start_position else 'None'}")
        print(f"   Before clear - Sequence beats: {len(current_sequence.beats) if current_sequence else 0}")
        
        # Trigger clear sequence
        workbench._handle_clear()
        
        # Check state after clear
        start_position_after = workbench.get_start_position()
        sequence_after = workbench.get_sequence()
        
        print(f"   After clear - Start position: {start_position_after.letter if start_position_after else 'None'}")
        print(f"   After clear - Sequence beats: {len(sequence_after.beats) if sequence_after else 0}")
        
        # Verify V1 behavior
        if start_position_after and (not sequence_after or len(sequence_after.beats) == 0):
            print("   ✅ PASS: Start position preserved, sequence beats cleared")
        else:
            print("   ❌ FAIL: Clear sequence not working correctly")
            
    def test_start_text_overlay(self):
        """Test START text overlay functionality"""
        print("\n📝 TESTING START TEXT OVERLAY FUNCTIONALITY")
        print("-" * 50)
        
        # Get beat frame and start position view
        beat_frame = self.construct_tab.workbench._beat_frame
        if beat_frame and beat_frame._start_position_view:
            start_view = beat_frame._start_position_view
            
            # Check if START text overlay exists
            if hasattr(start_view, '_start_text_overlay') and start_view._start_text_overlay:
                overlay = start_view._start_text_overlay
                is_visible = overlay.isVisible()
                
                print(f"   START text overlay exists: {overlay is not None}")
                print(f"   START text overlay visible: {is_visible}")
                
                if is_visible:
                    print("   ✅ PASS: START text overlay is visible")
                else:
                    print("   ❌ FAIL: START text overlay not visible")
                    # Try to show it
                    start_view._add_start_text_overlay()
                    print("   🔄 Attempted to re-initialize START text")
            else:
                print("   ❌ FAIL: START text overlay not found")
                print("   🔄 Attempting to initialize START text overlay")
                start_view._add_start_text_overlay()
        else:
            print("   ❌ FAIL: Beat frame or start position view not found")
            
    def test_start_position_integration(self):
        """Test start position to option picker integration"""
        print("\n🔗 TESTING START POSITION INTEGRATION")
        print("-" * 50)
        
        # Check if option picker has been populated
        option_picker = self.construct_tab.option_picker
        if option_picker:
            beat_options = getattr(option_picker, '_beat_options', [])
            print(f"   Option picker beat options: {len(beat_options)}")
            
            if len(beat_options) > 0:
                print("   ✅ PASS: Option picker has motion combinations")
                print(f"   Sample options: {[opt.letter for opt in beat_options[:5]]}")
            else:
                print("   ⚠️ WARNING: Option picker has no motion combinations")
                print("   💡 Select a start position to populate option picker")
        else:
            print("   ❌ FAIL: Option picker not found")
            
    def on_start_position_set(self, position_key: str):
        """Handle start position set signal"""
        print(f"\n✅ START POSITION SET: {position_key}")
        print("   - Start position data stored in workbench")
        print("   - Option picker should be populated with combinations")
        
        # Automatically test integration after start position is set
        QTimer.singleShot(500, self.test_start_position_integration)
        
    def on_sequence_created(self, sequence):
        """Handle sequence created signal"""
        print(f"\n📝 SEQUENCE CREATED: {sequence.name} ({len(sequence.beats)} beats)")
        
    def on_sequence_modified(self, sequence):
        """Handle sequence modified signal"""
        print(f"\n📝 SEQUENCE MODIFIED: {sequence.name} ({len(sequence.beats)} beats)")


def main():
    """Run the V1 functionality parity test"""
    print("🎯 Starting V1 Functionality Parity Test...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("V1 Functionality Parity Test")
    
    # Create and show test window
    window = V1FunctionalityParityTestWindow()
    window.show()
    
    print("🎯 Test window created - interact with components to test functionality")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
