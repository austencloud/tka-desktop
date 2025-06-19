#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-07-19
Test script to verify the duplicate refresh fix works

BUG REPORT: Option picker was being refreshed multiple times per beat addition
EXPECTED: Option picker should only refresh once per beat addition
STATUS: NEEDS_TESTING
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_duplicate_refresh_fix():
    """Test that option picker refresh only happens once per beat addition"""
    print("🧪 Testing duplicate refresh fix...")

    try:
        # Check the construct tab code for duplicate refresh calls
        construct_tab_file = (
            modern_src_path
            / "presentation"
            / "tabs"
            / "construct"
            / "construct_tab_widget.py"
        )

        if not construct_tab_file.exists():
            print(f"❌ Construct tab file not found: {construct_tab_file}")
            return False

        with open(construct_tab_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Count occurrences of refresh calls (new method name)
        refresh_calls = content.count("refresh_from_sequence(")
        old_refresh_calls = content.count("self._refresh_option_picker_from_sequence(")

        print(f"📊 Found {refresh_calls} calls to refresh_from_sequence")
        print(
            f"📊 Found {old_refresh_calls} calls to old _refresh_option_picker_from_sequence"
        )

        # Check that there's only one call (in _on_workbench_modified)
        if refresh_calls == 1:
            print("✅ Exactly one refresh call found - this is correct!")

            # Verify the call is in the right place
            if "_on_workbench_modified" in content:
                lines = content.split("\n")
                refresh_line = None
                workbench_modified_line = None

                for i, line in enumerate(lines):
                    if "def _on_workbench_modified" in line:
                        workbench_modified_line = i
                    if "self._refresh_option_picker_from_sequence(" in line:
                        refresh_line = i

                if (
                    refresh_line is not None
                    and workbench_modified_line is not None
                    and refresh_line > workbench_modified_line
                ):
                    print(
                        "✅ Refresh call is in _on_workbench_modified method - correct placement!"
                    )

                    # Check that there's no refresh call in _handle_beat_data_selected
                    handle_beat_section = ""
                    in_handle_beat = False
                    for line in lines:
                        if "def _handle_beat_data_selected" in line:
                            in_handle_beat = True
                        elif in_handle_beat and (
                            line.strip().startswith("def ")
                            and "_handle_beat_data_selected" not in line
                        ):
                            break
                        elif in_handle_beat:
                            handle_beat_section += line + "\n"

                    if (
                        "self._refresh_option_picker_from_sequence("
                        not in handle_beat_section
                    ):
                        print(
                            "✅ No refresh call in _handle_beat_data_selected - duplicate removed!"
                        )
                        return True
                    else:
                        print(
                            "❌ Still found refresh call in _handle_beat_data_selected"
                        )
                        return False
                else:
                    print("❌ Refresh call not found in _on_workbench_modified method")
                    return False
            else:
                print("❌ _on_workbench_modified method not found")
                return False
        elif refresh_calls == 0 and old_refresh_calls == 0:
            print(
                "⚠️  No refresh calls found in construct tab - checking option picker manager..."
            )

            # Check option picker manager for duplicate prevention
            option_picker_file = (
                modern_src_path
                / "presentation"
                / "tabs"
                / "construct"
                / "option_picker_manager.py"
            )

            if option_picker_file.exists():
                with open(option_picker_file, "r", encoding="utf-8") as f:
                    manager_content = f.read()

                # Check for duplicate prevention logic
                if "_last_refresh_sequence_id" in manager_content:
                    print(
                        "✅ Found duplicate prevention logic in option picker manager!"
                    )
                    print(
                        "📋 Duplicate refresh prevention implemented via tracking variables"
                    )

                    # Check for refresh_from_sequence method
                    if "def refresh_from_sequence" in manager_content:
                        print(
                            "✅ Found refresh_from_sequence method in option picker manager"
                        )
                        return True
                    else:
                        print("❌ refresh_from_sequence method not found")
                        return False
                else:
                    print("❌ No duplicate prevention logic found")
                    return False
            else:
                print("❌ Option picker manager file not found")
                return False
        else:
            print(f"❌ Expected exactly 1 refresh call, found {refresh_calls}")
            print(
                "📋 Multiple refresh calls detected - duplicate issue may still exist"
            )
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_duplicate_refresh_fix_pytest():
    """Pytest version of the duplicate refresh fix test."""
    result = test_duplicate_refresh_fix()
    assert result, "Duplicate refresh fix test failed"


if __name__ == "__main__":
    print("🧪 Starting Duplicate Refresh Fix Test")
    print("=" * 50)
    success = test_duplicate_refresh_fix()
    if success:
        print("\n✅ Test completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Test failed")
        sys.exit(1)
