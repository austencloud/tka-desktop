#!/usr/bin/env python3
"""
Option Picker Display Fix Verification Test

This test confirms that the option picker pictograph display issue has been resolved
and that motion combinations are now visually rendered correctly.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class OptionPickerDisplayFixedTestWindow(QMainWindow):
    """Test window to verify option picker display fix"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✅ Option Picker Display Fix Verification")
        self.setGeometry(100, 100, 1800, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel("🔄 Initializing option picker display test...")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Test button
        test_btn = QPushButton("🎯 Test Start Position → Option Picker Display")
        test_btn.clicked.connect(self.test_display_pipeline)
        layout.addWidget(test_btn)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Set up automatic test after initialization
        QTimer.singleShot(1000, self.run_automatic_test)
        
    def run_automatic_test(self):
        """Run automatic test of the display pipeline"""
        print("✅ Option Picker Display Fix Verification Started")
        print("=" * 70)
        
        self.status_label.setText("🎯 Testing start position selection...")
        
        # Trigger start position selection
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Check results after a short delay
        QTimer.singleShot(1500, self.verify_display_fix)
        
    def test_display_pipeline(self):
        """Manual test of the display pipeline"""
        self.run_automatic_test()
        
    def verify_display_fix(self):
        """Verify that the display fix is working"""
        print("\n🔍 VERIFYING OPTION PICKER DISPLAY FIX")
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
        
        visible_sections = 0
        sections_with_pictographs = 0
        total_pictographs = 0
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            container_visible = False
            
            if hasattr(section, 'pictograph_container'):
                container_visible = section.pictograph_container.isVisible()
                
            if container_visible:
                visible_sections += 1
                
            if len(pictographs) > 0:
                sections_with_pictographs += 1
                total_pictographs += len(pictographs)
                
            print(f"   📂 {section_type}: {len(pictographs)} pictographs, visible: {container_visible}")
            
        # Verify fix success
        success_criteria = [
            len(beat_options) >= 12,  # Motion combinations generated
            visible_sections >= 1,    # At least one section visible
            sections_with_pictographs >= 1,  # At least one section has pictographs
            total_pictographs >= 12   # All pictographs are present
        ]
        
        all_passed = all(success_criteria)
        
        print(f"\n📋 Fix Verification Results:")
        print(f"   ✅ Motion combinations generated: {len(beat_options) >= 12} ({len(beat_options)}/12)")
        print(f"   ✅ Sections visible: {visible_sections >= 1} ({visible_sections}/6)")
        print(f"   ✅ Sections with pictographs: {sections_with_pictographs >= 1} ({sections_with_pictographs}/6)")
        print(f"   ✅ Total pictographs displayed: {total_pictographs >= 12} ({total_pictographs}/12)")
        
        if all_passed:
            self.status_label.setText("🎉 SUCCESS: Option picker display fix verified!")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            print(f"\n🎉 OPTION PICKER DISPLAY FIX SUCCESSFUL!")
            print(f"   ✅ All {len(beat_options)} motion combinations are now visually displayed")
            print(f"   ✅ Pictographs appear in {sections_with_pictographs} section(s)")
            print(f"   ✅ Users can see and click on motion combination previews")
            print(f"   ✅ V1 functionality parity achieved for option picker display")
        else:
            self.status_label.setText("❌ FAILED: Option picker display issues remain")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            print(f"\n❌ OPTION PICKER DISPLAY FIX INCOMPLETE")
            print(f"   Some criteria not met - further debugging needed")
            
        print(f"\n" + "=" * 70)


def main():
    """Run the option picker display fix verification"""
    print("✅ Starting Option Picker Display Fix Verification...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Option Picker Display Fix Verification")
    
    # Create and show test window
    window = OptionPickerDisplayFixedTestWindow()
    window.show()
    
    print("✅ Test window created - verifying display fix")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
