#!/usr/bin/env python3
"""
Visual Layout Issues Debug Tool

This tool provides comprehensive visual debugging for the option picker layout issues,
including colored borders, position overlays, and interactive testing.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLabel, QHBoxLayout, QCheckBox, QSpinBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class VisualLayoutDebugWindow(QMainWindow):
    """Visual debugging window for layout issues"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Visual Layout Issues Debug Tool")
        self.setGeometry(50, 50, 1900, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget with debug controls
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Debug controls panel
        controls_panel = self._create_debug_controls()
        main_layout.addWidget(controls_panel, 0)  # Fixed width
        
        # Main application area
        app_area = QWidget()
        app_layout = QVBoxLayout(app_area)
        
        # Status label
        self.status_label = QLabel("🔄 Initializing visual layout debug...")
        self.status_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        app_layout.addWidget(self.status_label)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=app_area)
        app_layout.addWidget(self.construct_tab)
        
        main_layout.addWidget(app_area, 1)  # Expanding
        
        # Set up automatic debugging
        QTimer.singleShot(1000, self.start_visual_debugging)
        
    def _create_debug_controls(self):
        """Create debug controls panel"""
        panel = QWidget()
        panel.setFixedWidth(300)
        panel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("🔧 Debug Controls")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Visual debugging options
        self.show_borders_cb = QCheckBox("Show Widget Borders")
        self.show_borders_cb.toggled.connect(self.toggle_widget_borders)
        layout.addWidget(self.show_borders_cb)
        
        self.show_positions_cb = QCheckBox("Show Position Labels")
        self.show_positions_cb.toggled.connect(self.toggle_position_labels)
        layout.addWidget(self.show_positions_cb)
        
        self.highlight_containers_cb = QCheckBox("Highlight Containers")
        self.highlight_containers_cb.toggled.connect(self.toggle_container_highlighting)
        layout.addWidget(self.highlight_containers_cb)
        
        # Test buttons
        layout.addWidget(QLabel("🎯 Testing:"))
        
        test_selection_btn = QPushButton("Test Pictograph Selection")
        test_selection_btn.clicked.connect(self.test_pictograph_selection)
        layout.addWidget(test_selection_btn)
        
        force_layout_btn = QPushButton("Force Layout Update")
        force_layout_btn.clicked.connect(self.force_layout_update)
        layout.addWidget(force_layout_btn)
        
        # Panel ratio controls
        layout.addWidget(QLabel("📐 Panel Ratios:"))
        
        self.ratio_spinbox = QSpinBox()
        self.ratio_spinbox.setRange(30, 70)
        self.ratio_spinbox.setValue(50)
        self.ratio_spinbox.setSuffix("% left panel")
        self.ratio_spinbox.valueChanged.connect(self.adjust_panel_ratio)
        layout.addWidget(self.ratio_spinbox)
        
        # Info display
        layout.addWidget(QLabel("📊 Current Status:"))
        self.info_label = QLabel("Ready for debugging")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background-color: white; padding: 5px; border: 1px solid #ddd;")
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        return panel
        
    def start_visual_debugging(self):
        """Start the visual debugging process"""
        print("🔍 Visual Layout Debug Started")
        print("=" * 60)
        
        self.status_label.setText("🎯 Triggering start position selection...")
        
        # Trigger start position selection to populate option picker
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Start debugging after layout is populated
        QTimer.singleShot(2000, self.analyze_visual_layout)
        
    def analyze_visual_layout(self):
        """Analyze the actual visual layout"""
        print("\n🔍 ANALYZING VISUAL LAYOUT")
        print("-" * 40)
        
        option_picker = self.construct_tab.option_picker
        
        if not option_picker:
            self.update_info("❌ Option picker not found")
            return
            
        # Get sections
        sections = getattr(option_picker, '_sections', {})
        
        visual_issues = []
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            
            if len(pictographs) > 0:
                print(f"\n📂 Analyzing Section {section_type}:")
                
                # Check container
                if hasattr(section, 'pictograph_container'):
                    container = section.pictograph_container
                    container_geom = container.geometry()
                    print(f"   Container geometry: {container_geom.x()},{container_geom.y()} {container_geom.width()}x{container_geom.height()}")
                    
                    # Check if container is actually visible
                    if not container.isVisible():
                        visual_issues.append(f"Section {section_type} container not visible")
                        
                    # Check container size
                    if container_geom.height() < 100:
                        visual_issues.append(f"Section {section_type} container too small: {container_geom.height()}px")
                        
                # Check individual pictographs
                actual_positions = []
                visual_positions = []
                
                for i, pictograph in enumerate(pictographs):
                    # Get actual widget geometry
                    geom = pictograph.geometry()
                    actual_pos = (geom.x(), geom.y())
                    actual_positions.append(actual_pos)
                    
                    # Get visual position relative to parent
                    global_pos = pictograph.mapToGlobal(pictograph.rect().topLeft())
                    parent_pos = section.mapFromGlobal(global_pos)
                    visual_pos = (parent_pos.x(), parent_pos.y())
                    visual_positions.append(visual_pos)
                    
                    print(f"     Pictograph {i}: actual({actual_pos}) visual({visual_pos}) size({geom.width()}x{geom.height()})")
                    
                    # Check if widget is actually visible
                    if not pictograph.isVisible():
                        visual_issues.append(f"Pictograph {i} in {section_type} not visible")
                        
                # Check for overlapping
                unique_actual = len(set(actual_positions))
                unique_visual = len(set(visual_positions))
                
                print(f"   Unique actual positions: {unique_actual}/{len(pictographs)}")
                print(f"   Unique visual positions: {unique_visual}/{len(pictographs)}")
                
                if unique_actual < len(pictographs):
                    visual_issues.append(f"Section {section_type}: {len(pictographs) - unique_actual} overlapping actual positions")
                    
                if unique_visual < len(pictographs):
                    visual_issues.append(f"Section {section_type}: {len(pictographs) - unique_visual} overlapping visual positions")
                    
        # Update status
        if visual_issues:
            issue_text = "\n".join([f"• {issue}" for issue in visual_issues])
            self.update_info(f"❌ Visual Issues Found:\n{issue_text}")
            self.status_label.setText(f"❌ Found {len(visual_issues)} visual layout issues")
        else:
            self.update_info("✅ No visual layout issues detected")
            self.status_label.setText("✅ Visual layout appears correct")
            
    def toggle_widget_borders(self, enabled):
        """Toggle widget borders for visual debugging"""
        if not hasattr(self, 'construct_tab'):
            return
            
        option_picker = self.construct_tab.option_picker
        if not option_picker:
            return
            
        sections = getattr(option_picker, '_sections', {})
        
        for section in sections.values():
            pictographs = getattr(section, 'pictographs', [])
            for pictograph in pictographs:
                if enabled:
                    pictograph.setStyleSheet(pictograph.styleSheet() + "; border: 2px solid red;")
                else:
                    # Remove border styling
                    style = pictograph.styleSheet().replace("; border: 2px solid red;", "")
                    pictograph.setStyleSheet(style)
                    
    def toggle_position_labels(self, enabled):
        """Toggle position labels on pictographs"""
        # This would add text overlays showing positions - simplified for now
        self.update_info(f"Position labels: {'Enabled' if enabled else 'Disabled'}")
        
    def toggle_container_highlighting(self, enabled):
        """Toggle container highlighting"""
        if not hasattr(self, 'construct_tab'):
            return
            
        option_picker = self.construct_tab.option_picker
        if not option_picker:
            return
            
        sections = getattr(option_picker, '_sections', {})
        
        for section in sections.values():
            if hasattr(section, 'pictograph_container'):
                container = section.pictograph_container
                if enabled:
                    container.setStyleSheet(container.styleSheet() + "; border: 3px solid blue; background-color: rgba(0,0,255,50);")
                else:
                    style = container.styleSheet().replace("; border: 3px solid blue; background-color: rgba(0,0,255,50);", "")
                    container.setStyleSheet(style)
                    
    def test_pictograph_selection(self):
        """Test pictograph selection by simulating clicks"""
        self.update_info("🎯 Testing pictograph selection...")
        # This would simulate clicks at different positions
        
    def force_layout_update(self):
        """Force layout update on all sections"""
        if not hasattr(self, 'construct_tab'):
            return
            
        option_picker = self.construct_tab.option_picker
        if not option_picker:
            return
            
        sections = getattr(option_picker, '_sections', {})
        
        for section in sections.values():
            if hasattr(section, 'update_layout'):
                section.update_layout()
                
        self.update_info("🔄 Forced layout update on all sections")
        
        # Re-analyze after update
        QTimer.singleShot(500, self.analyze_visual_layout)
        
    def adjust_panel_ratio(self, value):
        """Adjust panel ratio for construct tab"""
        self.update_info(f"📐 Panel ratio: {value}% left, {100-value}% right")
        
    def update_info(self, text):
        """Update info label"""
        self.info_label.setText(text)
        print(f"ℹ️ {text}")


def main():
    """Run the visual layout debug tool"""
    print("🔍 Starting Visual Layout Issues Debug Tool...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Visual Layout Debug Tool")
    
    # Create and show debug window
    window = VisualLayoutDebugWindow()
    window.show()
    
    print("🔍 Debug tool ready - use controls to investigate layout issues")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
