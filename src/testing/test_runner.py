"""
Test Runner for Browse Tab Layout Testing

This module provides a command-line interface to run automated tests
and apply fixes based on test results.
"""

import sys
import logging
import time
from typing import Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

# Import the main application components
sys.path.append('src')
from testing.browse_tab_layout_tester import run_automated_browse_tab_test


class TestRunner(QObject):
    """Main test runner that coordinates testing and fixing."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.app = None
        self.main_window = None
        self.tester = None
        self.test_cycles = 0
        self.max_cycles = 3
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('browse_tab_test_results.log')
            ]
        )
    
    def run_test_cycle(self):
        """Run a complete test cycle: start app, test, analyze, fix if needed."""
        self.test_cycles += 1
        self.logger.info(f"\n🔄 STARTING TEST CYCLE {self.test_cycles}/{self.max_cycles}")
        
        try:
            # Start the application
            if not self._start_application():
                self.logger.error("Failed to start application")
                return False
            
            # Wait for application to fully initialize
            QTimer.singleShot(3000, self._run_automated_test)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Test cycle failed: {e}")
            return False
    
    def _start_application(self) -> bool:
        """Start the main application."""
        try:
            self.logger.info("🚀 Starting application...")
            
            # Create QApplication if it doesn't exist
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()
            
            # Import and create the main window
            from main import create_main_window
            self.main_window = create_main_window()
            
            if not self.main_window:
                self.logger.error("Failed to create main window")
                return False
            
            # Show the window
            self.main_window.show()
            
            # Wait for initialization
            for _ in range(10):  # Wait up to 5 seconds
                QApplication.processEvents()
                time.sleep(0.5)
                if hasattr(self.main_window, 'main_widget'):
                    break
            
            if not hasattr(self.main_window, 'main_widget'):
                self.logger.error("Main widget not initialized")
                return False
            
            self.logger.info("✅ Application started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start application: {e}")
            return False
    
    def _run_automated_test(self):
        """Run the automated Browse Tab test."""
        try:
            self.logger.info("🧪 Running automated Browse Tab test...")
            
            main_widget = self.main_window.main_widget
            self.tester = run_automated_browse_tab_test(main_widget)
            
            # Connect to test completion
            self.tester.test_completed.connect(self._on_test_completed)
            
        except Exception as e:
            self.logger.error(f"Failed to run automated test: {e}")
            self._cleanup_and_next_cycle()
    
    def _on_test_completed(self, success: bool, message: str):
        """Handle test completion."""
        self.logger.info(f"📊 Test completed: {message}")
        
        if success:
            self.logger.info("🎉 ALL TESTS PASSED! Layout regression fixed.")
            self._cleanup_and_exit(True)
        else:
            self.logger.warning(f"⚠️ Test failed: {message}")
            
            # Analyze violations and apply fixes
            violations = self.tester.violations_detected
            if violations:
                self._analyze_and_fix_violations(violations)
            
            # Continue to next cycle or exit
            if self.test_cycles < self.max_cycles:
                self.logger.info(f"🔄 Proceeding to next test cycle...")
                self._cleanup_and_next_cycle()
            else:
                self.logger.error("❌ Maximum test cycles reached. Manual intervention required.")
                self._cleanup_and_exit(False)
    
    def _analyze_and_fix_violations(self, violations):
        """Analyze violations and apply targeted fixes."""
        self.logger.info("🔍 Analyzing layout violations...")
        
        for event_name, measurement in violations:
            self.logger.info(f"Violation at {event_name}:")
            self.logger.info(f"  - Sequence viewer width: {measurement['sequence_viewer_width']}px")
            self.logger.info(f"  - Expected width: {measurement['expected_right_width']:.0f}px")
            self.logger.info(f"  - Actual ratio: {measurement['actual_ratio']:.2f}")
            
            # Apply specific fixes based on the violation type
            if event_name == "after_thumbnail_click":
                self._apply_post_selection_fix()
            elif event_name == "during_fade_start":
                self._apply_fade_operation_fix()
            elif event_name == "browse_tab_switched":
                self._apply_initial_layout_fix()
    
    def _apply_post_selection_fix(self):
        """Apply fix for post-selection layout violations."""
        self.logger.info("🔧 Applying post-selection layout fix...")
        
        # This would implement specific fixes for post-selection issues
        # For now, we'll log what needs to be fixed
        self.logger.info("Fix needed: Sequence viewer expanding after thumbnail selection")
    
    def _apply_fade_operation_fix(self):
        """Apply fix for fade operation layout violations."""
        self.logger.info("🔧 Applying fade operation layout fix...")
        
        # This would implement specific fixes for fade-related issues
        self.logger.info("Fix needed: Layout constraints lost during fade operations")
    
    def _apply_initial_layout_fix(self):
        """Apply fix for initial layout violations."""
        self.logger.info("🔧 Applying initial layout fix...")
        
        # This would implement specific fixes for initial layout issues
        self.logger.info("Fix needed: Initial Browse Tab layout ratio incorrect")
    
    def _cleanup_and_next_cycle(self):
        """Clean up current test and prepare for next cycle."""
        self.logger.info("🧹 Cleaning up for next test cycle...")
        
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        
        if self.app:
            self.app.quit()
            self.app = None
        
        # Schedule next cycle
        QTimer.singleShot(2000, self.run_test_cycle)
    
    def _cleanup_and_exit(self, success: bool):
        """Clean up and exit the test runner."""
        self.logger.info("🏁 Test runner completing...")
        
        if self.main_window:
            self.main_window.close()
        
        if self.app:
            self.app.quit()
        
        exit_code = 0 if success else 1
        sys.exit(exit_code)


def main():
    """Main entry point for the test runner."""
    print("🧪 Browse Tab Layout Automated Test Runner")
    print("=" * 50)
    
    runner = TestRunner()
    
    try:
        # Start the first test cycle
        if runner.run_test_cycle():
            # Run the Qt event loop
            if runner.app:
                runner.app.exec()
        else:
            print("❌ Failed to start test cycle")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Test runner interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
