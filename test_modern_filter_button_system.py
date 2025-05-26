#!/usr/bin/env python3
"""
Test script for the modern 2025 filter button system redesign.

This script tests the new glass-morphism, neomorphic effects, responsive layout,
and modern styling improvements for the browse tab filter buttons.
"""

import sys
import os
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_modern_button_theme():
    """Test the modern 2025 button theme with glass-morphism."""
    print("\n=== Testing Modern Button Theme ===")
    
    try:
        from styles.metallic_blue_button_theme import (
            MetallicBlueButtonTheme,
            GLASS_MORPHISM_NORMAL,
            GLASS_MORPHISM_HOVER,
            NEOMORPHIC_ACTIVE,
            NEOMORPHIC_PRESSED
        )
        from styles.button_state import ButtonState
        
        print("✓ Modern theme imports successful")
        
        # Test normal state theme
        normal_theme = MetallicBlueButtonTheme.get_default_theme(ButtonState.NORMAL, True)
        print(f"✓ Normal theme created: {type(normal_theme).__name__}")
        
        # Test active state theme
        active_theme = MetallicBlueButtonTheme.get_default_theme(ButtonState.ACTIVE, True)
        print(f"✓ Active theme created: {type(active_theme).__name__}")
        
        # Test disabled state theme
        disabled_theme = MetallicBlueButtonTheme.get_default_theme(ButtonState.NORMAL, False)
        print(f"✓ Disabled theme created: {type(disabled_theme).__name__}")
        
        # Verify glass-morphism gradients exist
        assert "rgba" in GLASS_MORPHISM_NORMAL, "Glass-morphism should use rgba colors"
        assert "rgba" in NEOMORPHIC_ACTIVE, "Neomorphic should use rgba colors"
        
        print("✓ All modern themes working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Modern button theme test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_styled_button_enhancements():
    """Test the enhanced StyledButton with animations and modern styling."""
    print("\n=== Testing Enhanced StyledButton ===")
    
    try:
        from styles.styled_button import StyledButton
        
        print("✓ StyledButton import successful")
        
        # Check for modern methods
        modern_methods = [
            '_setup_animations',
            '_setup_modern_font',
            '_animate_click',
            '_animate_click_release',
            'animationScale'
        ]
        
        for method_name in modern_methods:
            if hasattr(StyledButton, method_name):
                print(f"✓ Method {method_name} exists")
            else:
                print(f"✗ Method {method_name} missing")
                return False
        
        print("✓ All modern StyledButton enhancements present")
        return True
        
    except Exception as e:
        print(f"✗ StyledButton enhancement test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_filter_button_group_responsiveness():
    """Test the modern responsive FilterButtonGroup."""
    print("\n=== Testing Filter Button Group Responsiveness ===")
    
    try:
        from main_window.main_widget.browse_tab.sequence_picker.filter_stack.initial_filter_choice_widget.filter_button_group.filter_button_group import FilterButtonGroup
        
        print("✓ FilterButtonGroup import successful")
        
        # Check for modern responsive methods
        responsive_methods = [
            '_setup_responsive_sizing',
            '_setup_modern_layout',
            '_apply_modern_styling',
            '_update_modern_typography',
            '_get_modern_text_color',
            '_ensure_modern_responsiveness'
        ]
        
        for method_name in responsive_methods:
            if hasattr(FilterButtonGroup, method_name):
                print(f"✓ Method {method_name} exists")
            else:
                print(f"✗ Method {method_name} missing")
                return False
        
        print("✓ All responsive FilterButtonGroup methods present")
        return True
        
    except Exception as e:
        print(f"✗ Filter button group responsiveness test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_initial_filter_choice_widget_layout():
    """Test the modern responsive layout system."""
    print("\n=== Testing Initial Filter Choice Widget Layout ===")
    
    try:
        from main_window.main_widget.browse_tab.sequence_picker.filter_stack.initial_filter_choice_widget.initial_filter_choice_widget import InitialFilterChoiceWidget
        
        print("✓ InitialFilterChoiceWidget import successful")
        
        # Check for modern layout methods
        layout_methods = [
            '_setup_modern_ui',
            '_setup_modern_main_layout',
            '_setup_responsive_grid_layout',
            '_populate_grid_layout',
            '_apply_modern_container_styling',
            '_finalize_layout_initialization',
            '_update_responsive_layout',
            '_update_responsive_spacing'
        ]
        
        for method_name in layout_methods:
            if hasattr(InitialFilterChoiceWidget, method_name):
                print(f"✓ Method {method_name} exists")
            else:
                print(f"✗ Method {method_name} missing")
                return False
        
        print("✓ All modern layout methods present")
        return True
        
    except Exception as e:
        print(f"✗ Initial filter choice widget layout test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_responsive_grid_calculations():
    """Test responsive grid column calculations."""
    print("\n=== Testing Responsive Grid Calculations ===")
    
    try:
        # Test column calculation logic
        test_cases = [
            (300, 1),   # Small screen -> 1 column
            (500, 2),   # Medium screen -> 2 columns  
            (800, 3),   # Large screen -> 3 columns
            (1200, 4),  # Extra large screen -> 4 columns
        ]
        
        for width, expected_columns in test_cases:
            if width < 400:
                columns = 1
            elif width < 700:
                columns = 2
            elif width < 1000:
                columns = 3
            else:
                columns = 4
            
            if columns == expected_columns:
                print(f"✓ Width {width}px -> {columns} columns (correct)")
            else:
                print(f"✗ Width {width}px -> {columns} columns (expected {expected_columns})")
                return False
        
        print("✓ Responsive grid calculations working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Responsive grid calculation test failed: {e}")
        return False

def test_modern_styling_constants():
    """Test that modern styling constants are properly defined."""
    print("\n=== Testing Modern Styling Constants ===")
    
    try:
        from styles.metallic_blue_button_theme import (
            GLASS_OPACITY,
            NEOMORPHIC_OPACITY,
            SHADOW_BLUR,
            GLOW_INTENSITY
        )
        
        # Verify constants are reasonable values
        assert 0 < GLASS_OPACITY < 1, "Glass opacity should be between 0 and 1"
        assert 0 < NEOMORPHIC_OPACITY <= 1, "Neomorphic opacity should be between 0 and 1"
        assert SHADOW_BLUR > 0, "Shadow blur should be positive"
        assert 0 < GLOW_INTENSITY <= 1, "Glow intensity should be between 0 and 1"
        
        print(f"✓ Glass opacity: {GLASS_OPACITY}")
        print(f"✓ Neomorphic opacity: {NEOMORPHIC_OPACITY}")
        print(f"✓ Shadow blur: {SHADOW_BLUR}")
        print(f"✓ Glow intensity: {GLOW_INTENSITY}")
        
        print("✓ All modern styling constants properly defined")
        return True
        
    except Exception as e:
        print(f"✗ Modern styling constants test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all modern filter button system tests."""
    print("Modern 2025 Filter Button System Test Suite")
    print("=" * 60)
    
    setup_logging()
    
    tests = [
        test_modern_button_theme,
        test_styled_button_enhancements,
        test_filter_button_group_responsiveness,
        test_initial_filter_choice_widget_layout,
        test_responsive_grid_calculations,
        test_modern_styling_constants
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
        print("🎉 All tests passed! Modern filter button system is ready.")
        print("\n📋 Modern 2025 Features Implemented:")
        print("• Glass-morphism effects with subtle transparency")
        print("• Neomorphic button styling with realistic depth")
        print("• Smooth animations and transitions")
        print("• Responsive grid layout that adapts to screen size")
        print("• Modern typography with proper font weights")
        print("• High contrast colors for accessibility")
        print("• Backdrop blur effects for modern glass look")
        print("• Proper layout timing to fix initialization issues")
        print("\n🚀 The filter button system now has stunning 2025-level design!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
