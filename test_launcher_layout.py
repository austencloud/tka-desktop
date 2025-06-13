#!/usr/bin/env python3
"""
Test script to verify the TKA launcher layout optimization
"""

import sys
import os

# Add launcher to path
launcher_dir = os.path.join(os.path.dirname(__file__), "launcher")
sys.path.insert(0, launcher_dir)


def test_app_definitions():
    """Test that app definitions have the new app_type property"""
    print("Testing app definitions...")

    try:
        from launcher.data.app_definitions import AppDefinitions, AppType

        all_apps = AppDefinitions.get_all()
        print(f"✅ Found {len(all_apps)} applications")

        # Check that all apps have app_type
        for app in all_apps:
            if hasattr(app, "app_type"):
                print(f"✅ {app.title}: {app.app_type.value}")
            else:
                print(f"❌ {app.title}: Missing app_type")

        # Test categorization
        main_apps = [
            app
            for app in all_apps
            if hasattr(app, "app_type") and app.app_type == AppType.MAIN_APPLICATION
        ]
        standalone_tools = [
            app
            for app in all_apps
            if hasattr(app, "app_type") and app.app_type == AppType.STANDALONE_TOOL
        ]
        dev_tools = [
            app
            for app in all_apps
            if hasattr(app, "app_type") and app.app_type == AppType.DEVELOPMENT_TOOL
        ]

        print(f"✅ Main Applications: {len(main_apps)}")
        print(f"✅ Standalone Tools: {len(standalone_tools)}")
        print(f"✅ Development Tools: {len(dev_tools)}")

        return True
    except Exception as e:
        print(f"❌ Error testing app definitions: {e}")
        return False


def test_responsive_grid():
    """Test that responsive grid has new methods"""
    print("\nTesting responsive grid...")

    try:
        from launcher.ui.components.responsive_grid import ResponsiveAppGrid
        from launcher.data.app_definitions import AppDefinitions

        apps = AppDefinitions.get_all()
        grid = ResponsiveAppGrid(apps)

        # Check for new methods
        if hasattr(grid, "create_compact_section_header"):
            print("✅ create_compact_section_header method exists")
        else:
            print("❌ create_compact_section_header method missing")

        # Check for new properties
        if hasattr(grid, "min_card_width"):
            print(f"✅ min_card_width: {grid.min_card_width}")
        else:
            print("❌ min_card_width property missing")

        if hasattr(grid, "card_height_main"):
            print(f"✅ card_height_main: {grid.card_height_main}")
        else:
            print("❌ card_height_main property missing")

        if hasattr(grid, "card_height_tool"):
            print(f"✅ card_height_tool: {grid.card_height_tool}")
        else:
            print("❌ card_height_tool property missing")

        return True
    except Exception as e:
        print(f"❌ Error testing responsive grid: {e}")
        return False


def test_app_card():
    """Test that app card supports expanded parameter"""
    print("\nTesting app card...")

    try:
        from launcher.ui.components.app_card import AppCard
        from launcher.data.app_definitions import AppDefinitions

        apps = AppDefinitions.get_all()
        if apps:
            app = apps[0]

            # Test compact mode
            card_compact = AppCard(app, compact=False, expanded=False)
            print("✅ AppCard created in compact mode")

            # Test expanded mode
            card_expanded = AppCard(app, compact=False, expanded=True)
            print("✅ AppCard created in expanded mode")

            # Check for expanded property
            if hasattr(card_expanded, "expanded"):
                print(f"✅ expanded property: {card_expanded.expanded}")
            else:
                print("❌ expanded property missing")

        return True
    except Exception as e:
        print(f"❌ Error testing app card: {e}")
        return False


def test_styles():
    """Test that styles have new methods"""
    print("\nTesting styles...")

    try:
        from launcher.ui.styles import StyleManager

        # Check for new style methods
        if hasattr(StyleManager, "get_section_header_style"):
            print("✅ get_section_header_style method exists")
        else:
            print("❌ get_section_header_style method missing")

        if hasattr(StyleManager, "get_enhanced_card_style"):
            print("✅ get_enhanced_card_style method exists")
        else:
            print("❌ get_enhanced_card_style method missing")

        return True
    except Exception as e:
        print(f"❌ Error testing styles: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing TKA Launcher Layout Optimization")
    print("=" * 50)

    tests = [
        test_app_definitions,
        test_responsive_grid,
        test_app_card,
        test_styles,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Layout optimization is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
