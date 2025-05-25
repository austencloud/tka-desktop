"""
Automated Browse Tab Layout Testing System

This module provides comprehensive automated testing for the Browse Tab layout
regression issue, monitoring sequence viewer width and simulating user interactions.
"""

import logging
import time
from typing import Optional, Dict, List, Tuple
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt


class BrowseTabLayoutMonitor(QObject):
    """Monitors Browse Tab layout dimensions and detects regressions."""
    
    layout_violation_detected = pyqtSignal(str, dict)
    
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.logger = logging.getLogger(__name__)
        self.measurements: List[Dict] = []
        self.monitoring_active = False
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def start_monitoring(self):
        """Start continuous monitoring of layout dimensions."""
        self.monitoring_active = True
        self.logger.info("🔍 Starting Browse Tab layout monitoring...")
        
    def stop_monitoring(self):
        """Stop monitoring and generate report."""
        self.monitoring_active = False
        self.logger.info("⏹️ Stopping Browse Tab layout monitoring...")
        self._generate_report()
        
    def measure_layout(self, event_name: str = "measurement") -> Dict:
        """Measure current layout dimensions and detect violations."""
        try:
            # Get Browse Tab components
            browse_tab = self._get_browse_tab()
            if not browse_tab:
                return {"error": "Browse Tab not available"}
                
            # Get main widget dimensions
            main_width = self.main_widget.width()
            main_height = self.main_widget.height()
            
            # Get left and right stack dimensions
            left_stack_width = getattr(self.main_widget, 'left_stack', None)
            right_stack_width = getattr(self.main_widget, 'right_stack', None)
            
            left_width = left_stack_width.width() if left_stack_width else 0
            right_width = right_stack_width.width() if right_stack_width else 0
            
            # Get sequence viewer dimensions
            sequence_viewer = browse_tab.sequence_viewer
            viewer_width = sequence_viewer.width()
            viewer_height = sequence_viewer.height()
            
            # Calculate ratios
            expected_right_width = main_width / 3
            expected_left_width = main_width * 2 / 3
            
            # Detect violations
            width_violation = abs(viewer_width - expected_right_width) > 50  # 50px tolerance
            ratio_violation = abs(left_width / right_width - 2.0) > 0.3 if right_width > 0 else True
            
            measurement = {
                "timestamp": time.time(),
                "event": event_name,
                "main_width": main_width,
                "main_height": main_height,
                "left_stack_width": left_width,
                "right_stack_width": right_width,
                "sequence_viewer_width": viewer_width,
                "sequence_viewer_height": viewer_height,
                "expected_right_width": expected_right_width,
                "expected_left_width": expected_left_width,
                "width_violation": width_violation,
                "ratio_violation": ratio_violation,
                "actual_ratio": left_width / right_width if right_width > 0 else 0,
                "expected_ratio": 2.0
            }
            
            self.measurements.append(measurement)
            
            # Log violations
            if width_violation or ratio_violation:
                self.logger.warning(
                    f"🚨 LAYOUT VIOLATION at {event_name}: "
                    f"Viewer width: {viewer_width}px (expected: {expected_right_width:.0f}px), "
                    f"Ratio: {measurement['actual_ratio']:.2f} (expected: 2.0)"
                )
                self.layout_violation_detected.emit(event_name, measurement)
            else:
                self.logger.info(
                    f"✅ Layout OK at {event_name}: "
                    f"Viewer width: {viewer_width}px, Ratio: {measurement['actual_ratio']:.2f}"
                )
                
            return measurement
            
        except Exception as e:
            error_msg = f"Error measuring layout: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def _get_browse_tab(self):
        """Get the Browse Tab widget."""
        try:
            return self.main_widget.get_tab_widget("browse")
        except:
            try:
                return getattr(self.main_widget, 'browse_tab', None)
            except:
                return None
    
    def _generate_report(self):
        """Generate a comprehensive report of all measurements."""
        if not self.measurements:
            self.logger.info("No measurements recorded.")
            return
            
        violations = [m for m in self.measurements if m.get('width_violation') or m.get('ratio_violation')]
        
        self.logger.info(f"\n📊 BROWSE TAB LAYOUT REPORT")
        self.logger.info(f"Total measurements: {len(self.measurements)}")
        self.logger.info(f"Layout violations: {len(violations)}")
        
        if violations:
            self.logger.warning("🚨 VIOLATIONS DETECTED:")
            for v in violations:
                self.logger.warning(
                    f"  - {v['event']}: Viewer {v['sequence_viewer_width']}px "
                    f"(expected {v['expected_right_width']:.0f}px), "
                    f"Ratio {v['actual_ratio']:.2f}"
                )


class BrowseTabMockInteractor(QObject):
    """Simulates user interactions with the Browse Tab."""
    
    interaction_completed = pyqtSignal(str)
    
    def __init__(self, main_widget, monitor: BrowseTabLayoutMonitor):
        super().__init__()
        self.main_widget = main_widget
        self.monitor = monitor
        self.logger = logging.getLogger(__name__)
        
    def switch_to_browse_tab(self) -> bool:
        """Programmatically switch to the Browse Tab."""
        try:
            self.logger.info("🔄 Switching to Browse Tab...")
            
            # Try multiple methods to switch to Browse Tab
            tab_manager = getattr(self.main_widget, 'tab_manager', None)
            if tab_manager:
                tab_manager.switch_to_tab("browse")
                self.monitor.measure_layout("browse_tab_switched")
                QApplication.processEvents()
                time.sleep(0.5)  # Allow UI to settle
                return True
            else:
                self.logger.error("Tab manager not available")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to switch to Browse Tab: {e}")
            return False
    
    def simulate_thumbnail_click(self, thumbnail_index: int = 0) -> bool:
        """Simulate clicking on a thumbnail in the browser scroll area."""
        try:
            self.logger.info(f"🖱️ Simulating thumbnail click (index: {thumbnail_index})...")
            
            # Measure before click
            self.monitor.measure_layout("before_thumbnail_click")
            
            # Get Browse Tab
            browse_tab = self.monitor._get_browse_tab()
            if not browse_tab:
                self.logger.error("Browse Tab not available")
                return False
            
            # Get thumbnail boxes
            scroll_widget = browse_tab.sequence_picker.scroll_widget
            thumbnail_boxes = getattr(scroll_widget, 'thumbnail_boxes', {})
            
            if not thumbnail_boxes:
                self.logger.error("No thumbnail boxes available")
                return False
            
            # Get the first available thumbnail box
            box_names = list(thumbnail_boxes.keys())
            if thumbnail_index >= len(box_names):
                thumbnail_index = 0
                
            if not box_names:
                self.logger.error("No thumbnail boxes found")
                return False
                
            selected_box = thumbnail_boxes[box_names[thumbnail_index]]
            image_label = selected_box.image_label
            
            self.logger.info(f"Clicking thumbnail: {box_names[thumbnail_index]}")
            
            # Measure during fade operation
            self.monitor.measure_layout("during_fade_start")
            
            # Simulate the click
            browse_tab.selection_handler.on_thumbnail_clicked(image_label)
            
            # Allow fade operation to complete
            QApplication.processEvents()
            time.sleep(0.5)  # Wait for fade
            
            # Measure after click
            self.monitor.measure_layout("after_thumbnail_click")
            
            self.interaction_completed.emit(f"thumbnail_click_{thumbnail_index}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to simulate thumbnail click: {e}")
            return False


class BrowseTabAutomatedTester(QObject):
    """Main automated testing controller."""
    
    test_completed = pyqtSignal(bool, str)
    
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.monitor = BrowseTabLayoutMonitor(main_widget)
        self.interactor = BrowseTabMockInteractor(main_widget, self.monitor)
        self.logger = logging.getLogger(__name__)
        
        # Test configuration
        self.test_thumbnails = [0, 1, 2]  # Test first 3 thumbnails
        self.current_test_index = 0
        self.violations_detected = []
        
        # Connect signals
        self.monitor.layout_violation_detected.connect(self._on_violation_detected)
        self.interactor.interaction_completed.connect(self._on_interaction_completed)
        
    def start_automated_test(self):
        """Start the automated test cycle."""
        self.logger.info("🚀 Starting automated Browse Tab layout test...")
        
        # Start monitoring
        self.monitor.start_monitoring()
        
        # Initial measurement
        self.monitor.measure_layout("test_start")
        
        # Switch to Browse Tab
        if self.interactor.switch_to_browse_tab():
            # Start thumbnail testing
            QTimer.singleShot(1000, self._test_next_thumbnail)
        else:
            self._complete_test(False, "Failed to switch to Browse Tab")
    
    def _test_next_thumbnail(self):
        """Test the next thumbnail in the sequence."""
        if self.current_test_index >= len(self.test_thumbnails):
            self._complete_test(len(self.violations_detected) == 0, "All tests completed")
            return
            
        thumbnail_index = self.test_thumbnails[self.current_test_index]
        self.logger.info(f"Testing thumbnail {thumbnail_index + 1}/{len(self.test_thumbnails)}")
        
        if self.interactor.simulate_thumbnail_click(thumbnail_index):
            self.current_test_index += 1
            # Schedule next test
            QTimer.singleShot(2000, self._test_next_thumbnail)
        else:
            self._complete_test(False, f"Failed to test thumbnail {thumbnail_index}")
    
    def _on_violation_detected(self, event_name: str, measurement: dict):
        """Handle layout violation detection."""
        self.violations_detected.append((event_name, measurement))
        self.logger.error(f"🚨 Violation detected during: {event_name}")
    
    def _on_interaction_completed(self, interaction_name: str):
        """Handle interaction completion."""
        self.logger.info(f"✅ Interaction completed: {interaction_name}")
    
    def _complete_test(self, success: bool, message: str):
        """Complete the automated test and generate report."""
        self.monitor.stop_monitoring()
        
        if success:
            self.logger.info(f"✅ TEST PASSED: {message}")
        else:
            self.logger.error(f"❌ TEST FAILED: {message}")
            
        self.test_completed.emit(success, message)


def run_automated_browse_tab_test(main_widget):
    """Run the automated Browse Tab layout test."""
    tester = BrowseTabAutomatedTester(main_widget)
    tester.start_automated_test()
    return tester
