#!/usr/bin/env python3
"""
Debug Option Picker Layout Issue

This script investigates why all pictographs are stacked on top of each other
instead of being laid out in a proper grid like V1.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class OptionPickerLayoutDebugWindow(QMainWindow):
    """Debug window for option picker layout issues"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Option Picker Layout Debug")
        self.setGeometry(100, 100, 1800, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Debug button
        debug_btn = QPushButton("🔍 Debug Layout Issue")
        debug_btn.clicked.connect(self.debug_layout_issue)
        layout.addWidget(debug_btn)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Set up automatic debugging after initialization
        QTimer.singleShot(1000, self.start_debugging)
        
    def start_debugging(self):
        """Start the debugging process"""
        print("🔍 Option Picker Layout Debug Started")
        print("=" * 70)
        
        # Trigger start position selection to populate option picker
        print("\n1️⃣ Triggering start position selection...")
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Debug after a short delay to allow processing
        QTimer.singleShot(1500, self.debug_layout_issue)
        
    def debug_layout_issue(self):
        """Debug the layout issue step by step"""
        print("\n🔍 DEBUGGING OPTION PICKER LAYOUT ISSUE")
        print("-" * 60)
        
        option_picker = self.construct_tab.option_picker
        
        if not option_picker:
            print("❌ Option picker not found")
            return
            
        # Check beat options
        beat_options = getattr(option_picker, '_beat_options', [])
        print(f"📊 Beat options count: {len(beat_options)}")
        
        if len(beat_options) == 0:
            print("❌ No beat options to debug")
            return
            
        # Check sections
        sections = getattr(option_picker, '_sections', {})
        print(f"📂 Sections count: {len(sections)}")
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            print(f"\n📂 Section {section_type}:")
            print(f"   Pictographs count: {len(pictographs)}")
            
            if len(pictographs) > 0:
                # Check the layout
                if hasattr(section, 'pictograph_layout'):
                    layout = section.pictograph_layout
                    print(f"   Layout type: {type(layout)}")
                    print(f"   Layout item count: {layout.count()}")
                    print(f"   Layout spacing: {layout.spacing()}")
                    print(f"   Layout margins: {layout.contentsMargins()}")
                    
                    # Check each item in the layout
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item:
                            widget = item.widget()
                            if widget:
                                row, col, rowspan, colspan = layout.getItemPosition(i)
                                print(f"     Item {i}: widget at ({row}, {col}) span({rowspan}, {colspan})")
                                print(f"       Widget size: {widget.size().width()}x{widget.size().height()}")
                                print(f"       Widget pos: ({widget.x()}, {widget.y()})")
                                print(f"       Widget visible: {widget.isVisible()}")
                            else:
                                print(f"     Item {i}: no widget")
                        else:
                            print(f"     Item {i}: no item")
                            
                    # Check column calculation
                    if hasattr(section, '_calculate_optimal_columns'):
                        columns = section._calculate_optimal_columns()
                        print(f"   Calculated columns: {columns}")
                        
                        # Verify the expected layout positions
                        print(f"   Expected layout positions:")
                        for i, pictograph in enumerate(pictographs):
                            expected_row = i // columns
                            expected_col = i % columns
                            print(f"     Pictograph {i}: should be at ({expected_row}, {expected_col})")
                            
                # Check container
                if hasattr(section, 'pictograph_container'):
                    container = section.pictograph_container
                    print(f"   Container size: {container.size().width()}x{container.size().height()}")
                    print(f"   Container visible: {container.isVisible()}")
                    print(f"   Container children: {len(container.children())}")
                    
        # Check if update_layout is being called
        print(f"\n🔧 Testing layout update...")
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            if len(pictographs) > 0:
                print(f"   Calling update_layout() on section {section_type}...")
                section.update_layout()
                
                # Check layout after update
                if hasattr(section, 'pictograph_layout'):
                    layout = section.pictograph_layout
                    print(f"   After update - Layout item count: {layout.count()}")
                    
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item and item.widget():
                            row, col, rowspan, colspan = layout.getItemPosition(i)
                            widget = item.widget()
                            print(f"     Updated Item {i}: widget at ({row}, {col})")
                            print(f"       Widget pos after update: ({widget.x()}, {widget.y()})")
                            
        print(f"\n🎯 Layout Debug Complete!")


def main():
    """Run the option picker layout debug"""
    print("🔍 Starting Option Picker Layout Debug...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Option Picker Layout Debug")
    
    # Create and show debug window
    window = OptionPickerLayoutDebugWindow()
    window.show()
    
    print("🔍 Debug window created")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
