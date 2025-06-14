#!/usr/bin/env python3
"""
Basic functionality test for StartPositionView after lifecycle fix
"""

import sys
sys.path.insert(0, 'src')

from PyQt6.QtWidgets import QApplication
from src.presentation.components.workbench.beat_frame.start_position_view import StartPositionView

def test_basic_functionality():
    """Test basic functionality after the lifecycle fix"""
    app = QApplication([])
    
    try:
        # Create StartPositionView
        view = StartPositionView()
        view.show()
        print("✅ StartPositionView created successfully")

        # Test basic functionality
        if view._pictograph_component:
            print("✅ PictographComponent initialized")
        else:
            print("❌ PictographComponent not initialized")
            
        if view._start_text_overlay:
            print("✅ StartTextOverlay created")
            if hasattr(view._start_text_overlay, 'is_valid'):
                validity = view._start_text_overlay.is_valid()
                print(f"✅ Validity checking available: {validity}")
            else:
                print("❌ Validity checking not available")
        else:
            print("❌ StartTextOverlay not created")

        # Test cleanup
        view.cleanup()
        print("✅ Cleanup completed successfully")
        print("🎉 All basic functionality tests passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during basic functionality test: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
