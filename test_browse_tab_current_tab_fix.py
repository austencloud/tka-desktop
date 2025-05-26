#!/usr/bin/env python3
"""
Test script for the browse tab current tab detection fix.

This script tests the fix for the issue where the filter controller
incorrectly detects the current tab as "construct" when it's actually "browse".
"""

import sys
import os
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def test_current_tab_detection_methods():
    """Test that the current tab detection methods exist."""
    print("\n=== Testing Current Tab Detection Methods ===")

    try:
        from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
            BrowseTabFilterController,
        )

        print("✓ BrowseTabFilterController import successful")

        # Check if the new methods exist
        methods_to_check = [
            "_get_actual_current_tab",
            "_is_browse_tab_currently_active",
        ]

        for method_name in methods_to_check:
            if hasattr(BrowseTabFilterController, method_name):
                print(f"✓ Method {method_name} exists")
            else:
                print(f"✗ Method {method_name} missing")
                return False

        print("✓ All current tab detection methods present")
        return True

    except Exception as e:
        print(f"✗ Current tab detection test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_mock_current_tab_scenario():
    """Test a mock scenario of the current tab detection."""
    print("\n=== Testing Mock Current Tab Scenario ===")

    try:
        # Create a mock browse tab and filter controller
        class MockBrowseTab:
            def __init__(self):
                self.main_widget = MockMainWidget()
                self.filter_manager = None
                self.ui_updater = None
                self.metadata_extractor = None
                self.browse_settings = MockBrowseSettings()

            def isVisible(self):
                return True  # Simulate browse tab being visible

        class MockMainWidget:
            def __init__(self):
                self.left_stack = MockStack()
                self.coordinator = MockCoordinator()
                self.tab_switcher = MockTabSwitcher()

            def get_widget(self, name):
                return None  # Mock fade manager not available

        class MockStack:
            def __init__(self):
                self.current_widget = None

            def currentWidget(self):
                return self.current_widget

        class MockCoordinator:
            def get_current_tab(self):
                return "browse"  # Simulate coordinator returning browse

        class MockTabSwitcher:
            def _get_current_tab(self):
                return "browse"  # Simulate tab switcher returning browse

        class MockBrowseSettings:
            def set_current_filter(self, criteria):
                pass

            def set_current_section(self, section):
                pass

        # Test the filter controller with mock objects
        from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
            BrowseTabFilterController,
        )

        mock_browse_tab = MockBrowseTab()

        # This should work without crashing
        filter_controller = BrowseTabFilterController(mock_browse_tab)

        # Test the current tab detection
        current_tab = filter_controller._get_actual_current_tab()
        print(f"Detected current tab: {current_tab}")

        # Should detect browse tab as active
        is_active = filter_controller._is_browse_tab_currently_active()
        print(f"Browse tab detected as active: {is_active}")

        if current_tab == "browse" and is_active:
            print("✓ Mock current tab detection working correctly")
            return True
        else:
            print(
                f"✗ Mock current tab detection failed: tab={current_tab}, active={is_active}"
            )
            return False

    except Exception as e:
        print(f"✗ Mock current tab scenario failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_fallback_behavior():
    """Test the fallback behavior when detection methods fail."""
    print("\n=== Testing Fallback Behavior ===")

    try:
        # Create a mock browse tab with minimal functionality
        class MinimalMockBrowseTab:
            def __init__(self):
                self.filter_manager = None
                self.ui_updater = None
                self.metadata_extractor = None
                self.browse_settings = MockBrowseSettings()
                self.main_widget = MockMainWidgetMinimal()  # Minimal main widget

        class MockMainWidgetMinimal:
            def get_widget(self, name):
                return None  # No fade manager available

        class MockBrowseSettings:
            def set_current_filter(self, criteria):
                pass

            def set_current_section(self, section):
                pass

        from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
            BrowseTabFilterController,
        )

        mock_browse_tab = MinimalMockBrowseTab()
        filter_controller = BrowseTabFilterController(mock_browse_tab)

        # Test fallback behavior
        current_tab = filter_controller._get_actual_current_tab()
        print(f"Fallback current tab: {current_tab}")

        # Should fallback to "browse" since this is the browse tab filter controller
        if current_tab == "browse":
            print("✓ Fallback behavior working correctly")
            return True
        else:
            print(f"✗ Fallback behavior failed: expected 'browse', got '{current_tab}'")
            return False

    except Exception as e:
        print(f"✗ Fallback behavior test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_import_compatibility():
    """Test that imports work correctly."""
    print("\n=== Testing Import Compatibility ===")

    try:
        # Test that we can import the required modules
        from src.settings_manager.global_settings.app_context import AppContext

        print("✓ AppContext import successful")

        from main_window.main_widget.browse_tab.browse_tab_filter_controller import (
            BrowseTabFilterController,
        )

        print("✓ BrowseTabFilterController import successful")

        print("✓ All imports working correctly")
        return True

    except Exception as e:
        print(f"✗ Import compatibility test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all current tab detection tests."""
    print("Browse Tab Current Tab Detection Fix Test Suite")
    print("=" * 60)

    setup_logging()

    tests = [
        test_current_tab_detection_methods,
        test_mock_current_tab_scenario,
        test_fallback_behavior,
        test_import_compatibility,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Current tab detection fix is working.")
        print("\n📋 What was fixed:")
        print("• Added _get_actual_current_tab() method to check multiple sources")
        print("• Added _is_browse_tab_currently_active() to detect browse tab state")
        print(
            "• Fixed filter controller to use actual tab state instead of just settings"
        )
        print("• Added fallback logic when detection methods fail")
        print("• Ensured filter buttons work immediately when browse tab is active")
        print(
            "\n🚀 The fix should resolve the 'current_tab == \"browse\"' condition issue!"
        )
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
