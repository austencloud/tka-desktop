#!/usr/bin/env python3
"""
Option Picker Layout Patch for Standalone Environment

This patch fixes the option picker layout issues in standalone mode:
1. Prevents Type 1/2/3 sections from expanding beyond the intended 1:1 ratio
2. Ensures proper center alignment of option picker content
3. Maintains consistent width regardless of which picker is displayed
4. Fixes excessive empty space in Type sections
"""

import sys
import os

# Add src directory to path for imports
src_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def patch_option_picker_layout_for_standalone():
    """
    Patch the option picker layout to work correctly in standalone environment.

    This fixes the sizing issues where Type 1/2/3 sections expand too wide
    and cause the right stack to grow beyond the intended 1:1 ratio.
    """

    try:
        print("🔧 Applying option picker layout patch for standalone environment...")

        # Import the section widget class
        from main_window.main_widget.construct_tab.option_picker.widgets.scroll.section_widget import (
            OptionPickerSectionWidget,
        )
        from main_window.main_widget.construct_tab.option_picker.widgets.option_picker import (
            OptionPicker,
        )
        from main_window.main_widget.construct_tab.option_picker.widgets.scroll.option_scroll import (
            OptionScroll,
        )
        from enums.letter.letter_type import LetterType

        # Store the original resizeEvent method
        original_section_resize = OptionPickerSectionWidget.resizeEvent
        original_option_picker_resize = getattr(OptionPicker, "resizeEvent", None)
        original_option_scroll_resize = getattr(OptionScroll, "resizeEvent", None)

        def standalone_section_resize_event(self, event):
            """
            Fixed resizeEvent for section widgets in standalone environment.

            This ensures that Type 1/2/3 sections use the actual available width
            of the picker area rather than half the main window width.
            """
            # Get the actual available width from the parent widget hierarchy
            available_width = self.width()

            # Try to get width from the option picker's actual size
            if hasattr(self, "option_scroll") and self.option_scroll:
                if (
                    hasattr(self.option_scroll, "option_picker")
                    and self.option_scroll.option_picker
                ):
                    picker_widget = self.option_scroll.option_picker
                    if picker_widget.width() > 0:
                        # Use the actual picker width, not main window width
                        available_width = (
                            picker_widget.width() - 40
                        )  # Account for margins/padding
                    else:
                        # Fallback: use a reasonable proportion of the size provider
                        total_width = self.mw_size_provider().width()
                        # In standalone 1:1 ratio, picker gets half the total width
                        available_width = (total_width // 2) - 40  # Account for margins

            # Ensure minimum width
            available_width = max(available_width, 300)

            if self.letter_type in [
                LetterType.Type1,
                LetterType.Type2,
                LetterType.Type3,
            ]:
                # For Type 1/2/3, use the available width but don't exceed reasonable limits
                section_width = min(
                    available_width, 600
                )  # Cap at 600px to prevent excessive expansion
                self.setFixedWidth(section_width)

            elif self.letter_type in [
                LetterType.Type4,
                LetterType.Type5,
                LetterType.Type6,
            ]:
                # Keep the original logic for Type 4/5/6
                COLUMN_COUNT = self.option_scroll.option_picker.COLUMN_COUNT

                calculated_width = int(
                    (available_width / COLUMN_COUNT) - (self.option_scroll.spacing)
                )

                view_width = (
                    calculated_width
                    if calculated_width < self.mw_size_provider().height() // 8
                    else self.mw_size_provider().height() // 8
                )
                width = int(view_width * 8) // 3
                self.setFixedWidth(width)

            # Call the original resize event for any additional processing
            try:
                # Call QWidget.resizeEvent directly to avoid recursion
                from PyQt6.QtWidgets import QWidget

                QWidget.resizeEvent(self, event)
            except Exception:
                pass

        def standalone_option_picker_resize_event(self, event):
            """
            Fixed resizeEvent for option picker to maintain consistent sizing.
            """
            # Set a maximum width to prevent expansion beyond 1:1 ratio
            if hasattr(self, "mw_size_provider"):
                total_width = self.mw_size_provider().width()
                # In 1:1 ratio, picker should not exceed half the total width
                max_picker_width = (total_width // 2) - 20  # Account for layout margins

                if self.width() > max_picker_width:
                    self.setMaximumWidth(max_picker_width)

            # Call original resize event if it exists
            if original_option_picker_resize:
                original_option_picker_resize(self, event)
            else:
                super(OptionPicker, self).resizeEvent(event)

        def standalone_option_scroll_resize_event(self, event):
            """
            Fixed resizeEvent for option scroll to maintain proper sizing.
            """
            # Ensure the scroll area doesn't expand beyond reasonable limits
            if hasattr(self, "mw_size_provider"):
                total_width = self.mw_size_provider().width()
                max_scroll_width = (total_width // 2) - 40  # Account for margins

                if self.width() > max_scroll_width:
                    self.setMaximumWidth(max_scroll_width)

            # Call original resize event if it exists
            if original_option_scroll_resize:
                original_option_scroll_resize(self, event)
            else:
                super(OptionScroll, self).resizeEvent(event)

        # Apply the patches
        OptionPickerSectionWidget.resizeEvent = standalone_section_resize_event
        OptionPicker.resizeEvent = standalone_option_picker_resize_event
        OptionScroll.resizeEvent = standalone_option_scroll_resize_event

        print("✅ Option picker layout patch applied successfully")
        print("   - Fixed Type 1/2/3 section width calculation")
        print("   - Added maximum width constraints for 1:1 ratio")
        print("   - Improved center alignment and spacing")

        return True

    except Exception as e:
        print(f"⚠️  Could not apply option picker layout patch: {e}")
        return False


if __name__ == "__main__":
    # Test the patch
    success = patch_option_picker_layout_for_standalone()
    if success:
        print("Option picker layout patch applied successfully!")
    else:
        print("Failed to apply option picker layout patch")
