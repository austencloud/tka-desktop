#!/usr/bin/env python3
"""
Visual Fixes Verification Test

This test provides comprehensive verification of both critical visual layout fixes:
1. Option picker pictograph visual stacking issue
2. Construct tab panel proportions (50%:50% vs 66%:33%)
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLabel, QHBoxLayout, QCheckBox, QFrame, QSplitter
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class VisualFixesVerificationWindow(QMainWindow):
    """Comprehensive verification window for visual fixes"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✅ Visual Fixes Verification - V1 Parity Test")
        self.setGeometry(50, 50, 1900, 1200)
        
        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title and status
        title = QLabel("🔍 Visual Fixes Verification - V1 Parity Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.status_label = QLabel("🔄 Initializing verification tests...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Test controls
        controls_layout = QHBoxLayout()
        
        # Visual debugging controls
        self.highlight_borders_cb = QCheckBox("🔍 Highlight Widget Borders")
        self.highlight_borders_cb.toggled.connect(self.toggle_border_highlighting)
        controls_layout.addWidget(self.highlight_borders_cb)
        
        self.show_measurements_cb = QCheckBox("📐 Show Panel Measurements")
        self.show_measurements_cb.toggled.connect(self.toggle_measurements)
        controls_layout.addWidget(self.show_measurements_cb)
        
        # Test buttons
        test_stacking_btn = QPushButton("🎯 Test Pictograph Stacking")
        test_stacking_btn.clicked.connect(self.test_pictograph_stacking)
        controls_layout.addWidget(test_stacking_btn)
        
        test_panels_btn = QPushButton("📐 Test Panel Ratios")
        test_panels_btn.clicked.connect(self.test_panel_ratios)
        controls_layout.addWidget(test_panels_btn)
        
        verify_all_btn = QPushButton("✅ Verify All Fixes")
        verify_all_btn.clicked.connect(self.verify_all_fixes)
        controls_layout.addWidget(verify_all_btn)
        
        layout.addLayout(controls_layout)
        
        # Results display
        self.results_label = QLabel("📊 Test Results: Ready for verification")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 10px;
                margin: 5px;
            }
        """)
        layout.addWidget(self.results_label)
        
        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)
        
        # Set up automatic verification
        QTimer.singleShot(1000, self.start_verification)
        
    def start_verification(self):
        """Start the verification process"""
        print("✅ Visual Fixes Verification Started")
        print("=" * 60)
        
        self.status_label.setText("🎯 Triggering start position selection...")
        
        # Trigger start position selection to populate option picker
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")
        
        # Start verification after layout is populated
        QTimer.singleShot(2000, self.verify_all_fixes)
        
    def test_pictograph_stacking(self):
        """Test for pictograph stacking issues"""
        print("\n🎯 TESTING PICTOGRAPH STACKING")
        print("-" * 40)
        
        option_picker = self.construct_tab.option_picker
        
        if not option_picker:
            self.update_results("❌ Option picker not found")
            return
            
        sections = getattr(option_picker, '_sections', {})
        stacking_issues = []
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            
            if len(pictographs) > 0:
                print(f"📂 Testing Section {section_type}: {len(pictographs)} pictographs")
                
                # Check for overlapping positions
                positions = []
                overlapping = 0
                
                for i, pictograph in enumerate(pictographs):
                    geom = pictograph.geometry()
                    pos = (geom.x(), geom.y())
                    
                    if pos in positions:
                        overlapping += 1
                        print(f"   ❌ Pictograph {i} overlapping at {pos}")
                    else:
                        positions.append(pos)
                        print(f"   ✅ Pictograph {i} unique at {pos}")
                        
                if overlapping > 0:
                    stacking_issues.append(f"Section {section_type}: {overlapping} overlapping pictographs")
                    
        if stacking_issues:
            result = f"❌ Stacking Issues Found:\n" + "\n".join([f"• {issue}" for issue in stacking_issues])
        else:
            result = "✅ No Pictograph Stacking Issues - All pictographs have unique positions"
            
        self.update_results(f"🎯 Pictograph Stacking Test:\n{result}")
        return len(stacking_issues) == 0
        
    def test_panel_ratios(self):
        """Test panel ratio compliance with V1 (50%:50%)"""
        print("\n📐 TESTING PANEL RATIOS")
        print("-" * 40)
        
        # Find the splitter in the construct tab
        splitter = None
        for child in self.construct_tab.findChildren(QSplitter):
            if child.orientation() == Qt.Orientation.Horizontal:
                splitter = child
                break
                
        if not splitter:
            self.update_results("❌ Panel splitter not found")
            return False
            
        # Get splitter sizes
        sizes = splitter.sizes()
        if len(sizes) != 2:
            self.update_results(f"❌ Expected 2 panels, found {len(sizes)}")
            return False
            
        total_width = sum(sizes)
        left_percent = (sizes[0] / total_width) * 100
        right_percent = (sizes[1] / total_width) * 100
        
        print(f"📊 Panel sizes: {sizes[0]}px ({left_percent:.1f}%) | {sizes[1]}px ({right_percent:.1f}%)")
        
        # Check if it's close to 50%:50% (allow 5% tolerance)
        is_equal_ratio = abs(left_percent - 50) < 5 and abs(right_percent - 50) < 5
        
        if is_equal_ratio:
            result = f"✅ Panel Ratios Correct: {left_percent:.1f}% : {right_percent:.1f}% (V1 Parity Achieved)"
        else:
            result = f"❌ Panel Ratios Incorrect: {left_percent:.1f}% : {right_percent:.1f}% (Should be ~50% : ~50%)"
            
        self.update_results(f"📐 Panel Ratio Test:\n{result}")
        return is_equal_ratio
        
    def verify_all_fixes(self):
        """Verify all visual fixes comprehensively"""
        print("\n✅ VERIFYING ALL VISUAL FIXES")
        print("-" * 50)
        
        self.status_label.setText("🔍 Running comprehensive verification...")
        
        # Test 1: Pictograph stacking
        stacking_ok = self.test_pictograph_stacking()
        
        # Test 2: Panel ratios
        ratios_ok = self.test_panel_ratios()
        
        # Test 3: Visual clickability (simulated)
        clickability_ok = self.test_visual_clickability()
        
        # Overall results
        all_passed = stacking_ok and ratios_ok and clickability_ok
        
        if all_passed:
            overall_result = "🎉 ALL VISUAL FIXES VERIFIED SUCCESSFULLY!\n✅ V1 Functionality Parity Achieved"
            self.status_label.setText("🎉 All visual fixes verified!")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            failed_tests = []
            if not stacking_ok:
                failed_tests.append("Pictograph Stacking")
            if not ratios_ok:
                failed_tests.append("Panel Ratios")
            if not clickability_ok:
                failed_tests.append("Visual Clickability")
                
            overall_result = f"❌ VISUAL FIXES INCOMPLETE\nFailed: {', '.join(failed_tests)}"
            self.status_label.setText("❌ Some visual fixes need attention")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            
        self.update_results(f"🎯 COMPREHENSIVE VERIFICATION:\n{overall_result}")
        
        print(f"\n{'='*60}")
        print(f"VERIFICATION COMPLETE: {'PASSED' if all_passed else 'FAILED'}")
        print(f"{'='*60}")
        
    def test_visual_clickability(self):
        """Test that pictographs are visually clickable (not stacked)"""
        print("\n🖱️ TESTING VISUAL CLICKABILITY")
        print("-" * 40)
        
        option_picker = self.construct_tab.option_picker
        
        if not option_picker:
            return False
            
        sections = getattr(option_picker, '_sections', {})
        
        for section_type, section in sections.items():
            pictographs = getattr(section, 'pictographs', [])
            
            if len(pictographs) > 0:
                # Check if pictographs are in different visual areas
                visual_areas = set()
                
                for pictograph in pictographs:
                    geom = pictograph.geometry()
                    # Create a visual "area" based on position (rounded to 50px grid)
                    area = (geom.x() // 50, geom.y() // 50)
                    visual_areas.add(area)
                    
                clickable_ratio = len(visual_areas) / len(pictographs)
                print(f"📂 Section {section_type}: {len(visual_areas)} visual areas for {len(pictographs)} pictographs ({clickable_ratio:.2f} ratio)")
                
                if clickable_ratio > 0.8:  # At least 80% should be in different areas
                    print(f"   ✅ Good visual separation")
                    return True
                else:
                    print(f"   ❌ Poor visual separation - likely stacked")
                    return False
                    
        return True
        
    def toggle_border_highlighting(self, enabled):
        """Toggle border highlighting for visual debugging"""
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
                    pictograph.setStyleSheet(pictograph.styleSheet() + "; border: 3px solid red !important;")
                else:
                    style = pictograph.styleSheet().replace("; border: 3px solid red !important;", "")
                    pictograph.setStyleSheet(style)
                    
    def toggle_measurements(self, enabled):
        """Toggle measurement display"""
        # This would add measurement overlays - simplified for now
        print(f"📐 Measurements display: {'Enabled' if enabled else 'Disabled'}")
        
    def update_results(self, text):
        """Update results display"""
        self.results_label.setText(text)
        print(f"📊 {text}")


def main():
    """Run the visual fixes verification"""
    print("✅ Starting Visual Fixes Verification...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Visual Fixes Verification")
    
    # Create and show verification window
    window = VisualFixesVerificationWindow()
    window.show()
    
    print("✅ Verification tool ready - testing both critical visual fixes")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
