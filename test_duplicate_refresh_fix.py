#!/usr/bin/env python3
"""
Test script to verify the duplicate refresh fix works
"""

import sys
import os
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, "v2/src")

def test_duplicate_refresh_fix():
    """Test that option picker refresh only happens once per beat addition"""
    print("🧪 Testing duplicate refresh fix...")
    
    try:
        # Simple test: check that the construct tab code no longer has duplicate refresh calls
        construct_tab_file = "v2/src/presentation/tabs/construct_tab_widget.py"
        
        with open(construct_tab_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences of _refresh_option_picker_from_sequence calls
        refresh_calls = content.count('self._refresh_option_picker_from_sequence(')
        
        print(f"📊 Found {refresh_calls} calls to _refresh_option_picker_from_sequence")
        
        # Check that there's only one call (in _on_workbench_modified)
        if refresh_calls == 1:
            print("✅ Exactly one refresh call found - this is correct!")
            
            # Verify the call is in the right place
            if '_on_workbench_modified' in content:
                lines = content.split('\n')
                refresh_line = None
                workbench_modified_line = None
                
                for i, line in enumerate(lines):
                    if 'def _on_workbench_modified' in line:
                        workbench_modified_line = i
                    if 'self._refresh_option_picker_from_sequence(' in line:
                        refresh_line = i
                        
                if refresh_line and workbench_modified_line and refresh_line > workbench_modified_line:
                    print("✅ Refresh call is in _on_workbench_modified method - correct placement!")
                    
                    # Check that there's no refresh call in _handle_beat_data_selected
                    handle_beat_section = ""
                    in_handle_beat = False
                    for line in lines:
                        if 'def _handle_beat_data_selected' in line:
                            in_handle_beat = True
                        elif in_handle_beat and (line.strip().startswith('def ') and '_handle_beat_data_selected' not in line):
                            break
                        elif in_handle_beat:
                            handle_beat_section += line + '\n'
                    
                    if 'self._refresh_option_picker_from_sequence(' not in handle_beat_section:
                        print("✅ No refresh call in _handle_beat_data_selected - duplicate removed!")
                        return True
                    else:
                        print("❌ Still found refresh call in _handle_beat_data_selected")
                        return False
                else:
                    print("❌ Refresh call not found in _on_workbench_modified method")
                    return False
            else:
                print("❌ _on_workbench_modified method not found")
                return False
        else:
            print(f"❌ Expected exactly 1 refresh call, found {refresh_calls}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_duplicate_refresh_fix()
    print(f"\n{'🎉 SUCCESS' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1)
