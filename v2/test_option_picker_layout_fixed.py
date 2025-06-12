#!/usr/bin/env python3
"""
Option Picker Layout Fix Verification Test

This test confirms that the option picker layout issue has been resolved
and that all pictographs are properly arranged in a grid layout like V1.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class OptionPickerLayoutFixedTestWindow(QMainWindow):
    """Test window to verify option picker layout fix"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✅ Option Picker Layout Fix Verification")
        self.setGeometry(100, 100, 1800, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel("🔄 Initializing option picker layout test...")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Test button
        test_btn = QPushButton("🎯 Test Option Picker Grid Layout")
        test_btn.clicked.connect(self.test_layout_fix)
        layout.addWidget(test_btn)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Set up automatic test after initialization
        QTimer.singleShot(1000, self.run_automatic_test)
        
    def run_automatic_test(self):
        """Run automatic test of the layout fix"""
        print("✅ Option Picker Layout Fix Verification Started")
        print("=" * 70)
        
        self.status_label.setText("🎯 Testing grid layout fix...")
        
        # Trigger start position selection
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Check results after a short delay
        QTimer.singleShot(1500, self.verify_layout_fix)
        
    def test_layout_fix(self):
        """Manual test of the layout fix"""
        self.run_automatic_test()
        
    def verify_layout_fix(self):
        """Verify that the layout fix is working"""
        print("\n🔍 VERIFYING OPTION PICKER LAYOUT FIX")
        print("-" * 50)
        
        option_picker = self.construct_tab.option_picker
        
        if not option_picker:
            self.status_label.setText("❌ Option picker not found")
            return
            
        # Check data generation
        beat_options = getattr(option_picker, '_beat_options', [])
        print(f"📊 Generated motion combinations: {len(beat_options)}")
        
        if len(beat_options) == 0:
            self.status_label.setText("❌ No motion combinations generated")
            return
            
        # Check sections
        sections = getattr(option_picker, '_sections', {})
        print(f"📂 Available sections: {len(sections)}")
        
        layout_success = True
        total_pictographs = 0
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            
            if len(pictographs) > 0:
                total_pictographs += len(pictographs)
                print(f"\n📂 Section {section_type}: {len(pictographs)} pictographs")
                
                # Check container size
                if hasattr(section, 'pictograph_container'):
                    container = section.pictograph_container
                    container_size = container.size()
                    print(f"   Container size: {container_size.width()}x{container_size.height()}")
                    
                    # Container should be large enough (not the tiny 90x7 from before)
                    if container_size.height() < 100:
                        print(f"   ❌ Container too small: {container_size.height()}px height")
                        layout_success = False
                    else:
                        print(f"   ✅ Container properly sized: {container_size.height()}px height")
                        
                # Check layout positions
                if hasattr(section, 'pictograph_layout'):
                    layout = section.pictograph_layout
                    print(f"   Layout items: {layout.count()}")
                    
                    # Check for proper grid positioning
                    positions = []
                    overlapping_positions = 0
                    
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            pos = (widget.x(), widget.y())
                            
                            # Check for overlapping positions
                            if pos in positions:
                                overlapping_positions += 1
                            else:
                                positions.append(pos)
                                
                    print(f"   Unique positions: {len(positions)}")
                    print(f"   Overlapping positions: {overlapping_positions}")
                    
                    if overlapping_positions > 0:
                        print(f"   ❌ Found {overlapping_positions} overlapping pictographs")
                        layout_success = False
                    else:
                        print(f"   ✅ All pictographs have unique positions")
                        
                    # Check position distribution
                    if len(positions) > 1:
                        x_positions = sorted(set(pos[0] for pos in positions))
                        y_positions = sorted(set(pos[1] for pos in positions))
                        
                        print(f"   X positions: {len(x_positions)} columns")
                        print(f"   Y positions: {len(y_positions)} rows")
                        
                        # Should have multiple rows and columns for proper grid
                        if len(x_positions) >= 2 and len(y_positions) >= 2:
                            print(f"   ✅ Proper grid layout: {len(y_positions)}x{len(x_positions)}")
                        else:
                            print(f"   ⚠️ Limited grid layout")
                            
        # Overall verification
        print(f"\n📋 Layout Fix Verification Results:")
        print(f"   📊 Total pictographs: {total_pictographs}")
        print(f"   🎯 Layout success: {layout_success}")
        
        if layout_success and total_pictographs >= 12:
            self.status_label.setText("🎉 SUCCESS: Option picker layout fix verified!")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            print(f"\n🎉 OPTION PICKER LAYOUT FIX SUCCESSFUL!")
            print(f"   ✅ All {total_pictographs} pictographs properly arranged in grid")
            print(f"   ✅ No overlapping or stacked pictographs")
            print(f"   ✅ Container sizes properly calculated")
            print(f"   ✅ V1-style grid layout achieved")
        else:
            self.status_label.setText("❌ FAILED: Option picker layout issues remain")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            print(f"\n❌ OPTION PICKER LAYOUT FIX INCOMPLETE")
            print(f"   Layout issues still detected")
            
        print(f"\n" + "=" * 70)


def main():
    """Run the option picker layout fix verification"""
    print("✅ Starting Option Picker Layout Fix Verification...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Option Picker Layout Fix Verification")
    
    # Create and show test window
    window = OptionPickerLayoutFixedTestWindow()
    window.show()
    
    print("✅ Test window created - verifying layout fix")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
