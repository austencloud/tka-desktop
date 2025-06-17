#!/usr/bin/env python3
"""
Manual test for background settings functionality.
Run this to verify the background settings work correctly.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

# Add modern src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_background_service():
    """Test the background service functionality."""
    print("🧪 Testing Background Service...")

    try:
        # Mock the UI state service to avoid PyQt6 dependencies
        ui_state_service = Mock()
        ui_state_service.get_setting.return_value = "Aurora"

        # Import and test the background service
        from src.application.services.settings.background_service import (
            BackgroundService,
        )

        background_service = BackgroundService(ui_state_service)

        # Test 1: Get available backgrounds
        backgrounds = background_service.get_available_backgrounds()
        print(f"✅ Available backgrounds: {backgrounds}")
        assert len(backgrounds) == 4
        assert all(
            bg in backgrounds for bg in ["Aurora", "Starfield", "Snowfall", "Bubbles"]
        )

        # Test 2: Get current background
        current = background_service.get_current_background()
        print(f"✅ Current background: {current}")
        assert current == "Aurora"

        # Test 3: Set valid background
        result = background_service.set_background("Starfield")
        print(f"✅ Set background to Starfield: {result}")
        assert result is True

        # Test 4: Set invalid background
        result = background_service.set_background("InvalidBackground")
        print(f"✅ Set invalid background rejected: {not result}")
        assert result is False

        # Test 5: Validate backgrounds
        assert background_service.is_valid_background("Aurora") is True
        assert background_service.is_valid_background("InvalidBackground") is False
        print("✅ Background validation works correctly")

        print("🎉 All background service tests passed!")
        return True

    except Exception as e:
        print(f"❌ Background service test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_background_interfaces():
    """Test that the background interfaces are properly defined."""
    print("\n🧪 Testing Background Interfaces...")

    try:
        from src.core.interfaces.background_interfaces import IBackgroundService

        # Check that the interface has the expected methods
        expected_methods = [
            "get_available_backgrounds",
            "get_current_background",
            "set_background",
            "is_valid_background",
        ]

        for method in expected_methods:
            assert hasattr(IBackgroundService, method), f"Missing method: {method}"

        print("✅ Background interface is properly defined")
        return True

    except Exception as e:
        print(f"❌ Background interface test failed: {e}")
        return False


def test_settings_integration():
    """Test that the settings dialog components exist."""
    print("\n🧪 Testing Settings Integration...")

    try:
        # Test that the background tab exists
        from src.presentation.components.ui.settings.tabs.background_tab import (
            BackgroundTab,
        )

        print("✅ Background tab component exists")

        # Test that the animated tile widget exists
        from src.presentation.components.ui.settings.tabs.background_tab import (
            AnimatedBackgroundTile,
        )

        print("✅ Animated background tile widget exists")

        return True

    except Exception as e:
        print(f"❌ Settings integration test failed: {e}")
        return False


def main():
    """Run all manual tests."""
    print("🚀 Running Background Settings Manual Tests\n")

    tests = [
        test_background_service,
        test_background_interfaces,
        test_settings_integration,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! Background settings functionality is working correctly."
        )
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
