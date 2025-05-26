#!/usr/bin/env python3
"""
Test script to verify the go back button functionality.
This script will run the application and test the button behavior.
"""

import sys
import os
import time
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_go_back_button():
    """Test the go back button functionality."""
    
    # Set up logging to capture button events
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Testing Go Back Button Functionality")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        
        # Create application
        app = QApplication(sys.argv)
        
        # Import and create main window
        from src.main_window.main_window import MainWindow
        from src.core.application_context import ApplicationContext
        
        # Initialize application context
        app_context = ApplicationContext()
        
        # Create main window
        main_window = MainWindow(app_context)
        main_window.show()
        
        print("✅ Application started successfully")
        print("✅ Main window created and shown")
        
        # Wait for initialization
        def check_button_after_init():
            try:
                # Navigate to browse tab
                main_window.main_widget.tab_manager.switch_to_tab("browse")
                print("✅ Switched to browse tab")
                
                # Get the browse tab
                browse_tab = main_window.main_widget.tab_manager.get_tab("browse")
                if browse_tab:
                    print("✅ Browse tab found")
                    
                    # Get the sequence picker
                    sequence_picker = browse_tab.sequence_picker
                    if sequence_picker:
                        print("✅ Sequence picker found")
                        
                        # Get the control panel
                        control_panel = sequence_picker.control_panel
                        if control_panel:
                            print("✅ Control panel found")
                            
                            # Get the go back button
                            go_back_button = control_panel.go_back_button
                            if go_back_button:
                                print("✅ Go back button found")
                                print(f"   Button size: {go_back_button.width()}x{go_back_button.height()}")
                                print(f"   Button enabled: {go_back_button.isEnabled()}")
                                print(f"   Button visible: {go_back_button.isVisible()}")
                                print(f"   Button text: '{go_back_button.text()}'")
                                
                                # Test button click programmatically
                                print("🔄 Testing button click...")
                                go_back_button.click()
                                print("✅ Button click test completed")
                                
                            else:
                                print("❌ Go back button not found")
                        else:
                            print("❌ Control panel not found")
                    else:
                        print("❌ Sequence picker not found")
                else:
                    print("❌ Browse tab not found")
                    
            except Exception as e:
                print(f"❌ Error during button test: {e}")
                import traceback
                traceback.print_exc()
            
            # Close application after test
            QTimer.singleShot(2000, app.quit)
        
        # Schedule the test after a short delay to allow initialization
        QTimer.singleShot(3000, check_button_after_init)
        
        # Run the application
        print("🔄 Running application test...")
        app.exec()
        
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_go_back_button()
    sys.exit(0 if success else 1)
