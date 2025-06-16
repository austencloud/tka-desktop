"""
Tab Switching Consistency Test

This script tests the tab switching functionality to ensure the browse tab's 2:1 aspect ratio
is maintained consistently across all tab switching scenarios.
"""

import logging
import time
from typing import Dict, List, Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


class TabSwitchingConsistencyTester:
    """Tests tab switching consistency and browse tab aspect ratio preservation."""
    
    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.test_results = []
        
    def setup_logging(self):
        """Setup logging for the test."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def run_comprehensive_test(self) -> bool:
        """Run comprehensive tab switching consistency tests."""
        self.logger.info("🧪 Starting Comprehensive Tab Switching Consistency Test...")
        
        all_tests_passed = True
        
        # Test 1: Initial browse tab layout
        if not self._test_initial_browse_tab_layout():
            all_tests_passed = False
            
        # Test 2: Tab switching sequence
        if not self._test_tab_switching_sequence():
            all_tests_passed = False
            
        # Test 3: Fast consecutive switches
        if not self._test_fast_consecutive_switches():
            all_tests_passed = False
            
        # Test 4: Window resize during tab switches
        if not self._test_window_resize_during_switches():
            all_tests_passed = False
            
        # Test 5: Browse tab return consistency
        if not self._test_browse_tab_return_consistency():
            all_tests_passed = False
            
        # Print summary
        self._print_test_summary()
        
        if all_tests_passed:
            self.logger.info("✅ All tab switching consistency tests passed!")
        else:
            self.logger.error("❌ Some tab switching consistency tests failed!")
            
        return all_tests_passed
        
    def _test_initial_browse_tab_layout(self) -> bool:
        """Test that the initial browse tab layout has correct 2:1 ratio."""
        self.logger.info("🔍 Testing initial browse tab layout...")
        
        # Switch to browse tab
        if not self._switch_to_tab("browse"):
            self._record_test_result("Initial Browse Tab Layout", False, "Failed to switch to browse tab")
            return False
            
        # Allow UI to settle
        self._wait_for_ui_settle()
        
        # Measure layout
        measurement = self._measure_layout("initial_browse_tab")
        is_valid = self._validate_browse_tab_ratio(measurement)
        
        self._record_test_result(
            "Initial Browse Tab Layout", 
            is_valid, 
            f"Ratio: {measurement.get('aspect_ratio', 0):.2f}" if measurement else "No measurement"
        )
        
        return is_valid
        
    def _test_tab_switching_sequence(self) -> bool:
        """Test switching through all tabs and back to browse."""
        self.logger.info("🔄 Testing tab switching sequence...")
        
        tabs_to_test = ["construct", "generate", "learn", "browse", "sequence_card", "browse"]
        all_valid = True
        
        for i, tab_name in enumerate(tabs_to_test):
            self.logger.info(f"  Switching to {tab_name} (step {i+1}/{len(tabs_to_test)})")
            
            if not self._switch_to_tab(tab_name):
                self._record_test_result(f"Switch to {tab_name}", False, "Failed to switch")
                all_valid = False
                continue
                
            self._wait_for_ui_settle()
            
            # If it's browse tab, validate the ratio
            if tab_name == "browse":
                measurement = self._measure_layout(f"switch_to_browse_step_{i}")
                is_valid = self._validate_browse_tab_ratio(measurement)
                
                self._record_test_result(
                    f"Browse Tab Ratio (step {i+1})", 
                    is_valid, 
                    f"Ratio: {measurement.get('aspect_ratio', 0):.2f}" if measurement else "No measurement"
                )
                
                if not is_valid:
                    all_valid = False
                    
        return all_valid
        
    def _test_fast_consecutive_switches(self) -> bool:
        """Test fast consecutive tab switches."""
        self.logger.info("⚡ Testing fast consecutive tab switches...")
        
        tabs = ["browse", "construct", "browse", "generate", "browse", "learn", "browse"]
        all_valid = True
        
        for i, tab_name in enumerate(tabs):
            if not self._switch_to_tab(tab_name):
                self._record_test_result(f"Fast switch to {tab_name}", False, "Failed to switch")
                all_valid = False
                continue
                
            # Minimal wait for fast switching
            QApplication.processEvents()
            time.sleep(0.1)
            
            # Only validate browse tab ratios
            if tab_name == "browse":
                measurement = self._measure_layout(f"fast_switch_{i}")
                is_valid = self._validate_browse_tab_ratio(measurement)
                
                self._record_test_result(
                    f"Fast Switch Browse Ratio #{i+1}", 
                    is_valid, 
                    f"Ratio: {measurement.get('aspect_ratio', 0):.2f}" if measurement else "No measurement"
                )
                
                if not is_valid:
                    all_valid = False
                    
        return all_valid
        
    def _test_window_resize_during_switches(self) -> bool:
        """Test window resizing during tab switches."""
        self.logger.info("📏 Testing window resize during tab switches...")
        
        # Switch to browse tab
        if not self._switch_to_tab("browse"):
            self._record_test_result("Resize Test Setup", False, "Failed to switch to browse tab")
            return False
            
        self._wait_for_ui_settle()
        
        # Resize window
        original_size = self.main_widget.size()
        new_width = int(original_size.width() * 1.3)
        new_height = int(original_size.height() * 1.1)
        
        self.logger.info(f"  Resizing window to {new_width}x{new_height}")
        self.main_widget.resize(new_width, new_height)
        self._wait_for_ui_settle()
        
        # Measure after resize
        measurement = self._measure_layout("after_resize")
        is_valid = self._validate_browse_tab_ratio(measurement)
        
        # Switch to another tab and back
        self._switch_to_tab("construct")
        self._wait_for_ui_settle()
        self._switch_to_tab("browse")
        self._wait_for_ui_settle()
        
        # Measure after tab switch with resized window
        measurement2 = self._measure_layout("after_resize_and_switch")
        is_valid2 = self._validate_browse_tab_ratio(measurement2)
        
        # Restore original size
        self.main_widget.resize(original_size)
        self._wait_for_ui_settle()
        
        self._record_test_result(
            "Resize During Switch", 
            is_valid and is_valid2, 
            f"After resize: {measurement.get('aspect_ratio', 0):.2f}, After switch: {measurement2.get('aspect_ratio', 0):.2f}"
        )
        
        return is_valid and is_valid2
        
    def _test_browse_tab_return_consistency(self) -> bool:
        """Test that returning to browse tab always maintains correct ratio."""
        self.logger.info("🔄 Testing browse tab return consistency...")
        
        other_tabs = ["construct", "generate", "learn", "sequence_card"]
        all_valid = True
        
        for tab_name in other_tabs:
            # Switch away from browse
            if not self._switch_to_tab(tab_name):
                continue
                
            self._wait_for_ui_settle()
            
            # Switch back to browse
            if not self._switch_to_tab("browse"):
                self._record_test_result(f"Return from {tab_name}", False, "Failed to return to browse")
                all_valid = False
                continue
                
            self._wait_for_ui_settle()
            
            # Validate ratio
            measurement = self._measure_layout(f"return_from_{tab_name}")
            is_valid = self._validate_browse_tab_ratio(measurement)
            
            self._record_test_result(
                f"Return from {tab_name}", 
                is_valid, 
                f"Ratio: {measurement.get('aspect_ratio', 0):.2f}" if measurement else "No measurement"
            )
            
            if not is_valid:
                all_valid = False
                
        return all_valid
        
    def _switch_to_tab(self, tab_name: str) -> bool:
        """Switch to a specific tab."""
        try:
            # Try using tab manager (new system)
            if hasattr(self.main_widget, 'tab_manager'):
                self.main_widget.tab_manager.switch_to_tab(tab_name)
                return True
            # Try using tab switcher (old system)
            elif hasattr(self.main_widget, 'tab_switcher'):
                from src.main_window.main_widget.main_widget_tab_switcher import TabName
                tab_enum = getattr(TabName, tab_name.upper(), None)
                if tab_enum:
                    self.main_widget.tab_switcher.switch_tab(tab_enum)
                    return True
            # Try direct method call
            elif hasattr(self.main_widget, 'switch_to_tab'):
                self.main_widget.switch_to_tab(tab_name)
                return True
        except Exception as e:
            self.logger.error(f"Error switching to {tab_name}: {e}")
            
        return False
        
    def _measure_layout(self, context: str) -> Dict:
        """Measure the current layout dimensions."""
        try:
            main_width = self.main_widget.width()
            main_height = self.main_widget.height()
            
            left_width = self.main_widget.left_stack.width() if hasattr(self.main_widget, 'left_stack') else 0
            right_width = self.main_widget.right_stack.width() if hasattr(self.main_widget, 'right_stack') else 0
            
            # Calculate ratios
            total_content_width = left_width + right_width
            left_ratio = left_width / total_content_width if total_content_width > 0 else 0
            right_ratio = right_width / total_content_width if total_content_width > 0 else 0
            aspect_ratio = left_width / right_width if right_width > 0 else 0
            
            return {
                'context': context,
                'main_width': main_width,
                'main_height': main_height,
                'left_width': left_width,
                'right_width': right_width,
                'total_content_width': total_content_width,
                'left_ratio': left_ratio,
                'right_ratio': right_ratio,
                'aspect_ratio': aspect_ratio,
                'expected_aspect_ratio': 2.0
            }
            
        except Exception as e:
            self.logger.error(f"Error measuring layout: {e}")
            return {}
            
    def _validate_browse_tab_ratio(self, measurement: Dict) -> bool:
        """Validate that the aspect ratio is close to 2:1."""
        if not measurement:
            return False
            
        aspect_ratio = measurement.get('aspect_ratio', 0)
        expected_ratio = 2.0
        tolerance = 0.3  # Allow 30% tolerance for tab switching tests
        
        return abs(aspect_ratio - expected_ratio) <= tolerance
        
    def _wait_for_ui_settle(self):
        """Wait for UI to settle after changes."""
        QApplication.processEvents()
        time.sleep(0.3)  # Allow time for animations and layout updates
        
    def _record_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Record a test result."""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        
        status = "✅ PASS" if passed else "❌ FAIL"
        self.logger.info(f"  {status}: {test_name} - {details}")
        
    def _print_test_summary(self):
        """Print a summary of all test results."""
        self.logger.info("\n" + "="*60)
        self.logger.info("TAB SWITCHING CONSISTENCY TEST SUMMARY")
        self.logger.info("="*60)
        
        passed_count = sum(1 for result in self.test_results if result['passed'])
        total_count = len(self.test_results)
        
        for result in self.test_results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            self.logger.info(f"{status}: {result['test']} - {result['details']}")
            
        self.logger.info("-"*60)
        self.logger.info(f"TOTAL: {passed_count}/{total_count} tests passed")
        self.logger.info("="*60)


def run_tab_switching_consistency_test(main_widget) -> bool:
    """Run the comprehensive tab switching consistency test."""
    tester = TabSwitchingConsistencyTester(main_widget)
    return tester.run_comprehensive_test()


if __name__ == "__main__":
    print("This test requires a running main widget instance.")
    print("Import and call run_tab_switching_consistency_test(main_widget) from your application.")
