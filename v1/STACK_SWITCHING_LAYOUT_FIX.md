# Stack Switching Layout Fix - Browse Tab Filter Navigation

## Problem Description

The browse tab's 2:1 aspect ratio was being disrupted specifically when using the filter selector and back button navigation. The issue was that stack switching operations in the browse tab were bypassing the layout ratio management system, causing the window to resize wider and lose the intended 2:1 ratio.

## Root Cause Analysis

The problem was identified in the browse tab's filter navigation system:

### 1. **Direct Stack Switching Without Layout Preservation**
- **Filter Controller**: `browse_tab_filter_controller.py` was calling `setCurrentWidget()` directly on the left stack
- **Go Back Button**: `sequence_picker_go_back_button.py` was using stack fading without preserving layout ratios
- **Filter Stack**: `sequence_picker_filter_stack.py` was switching between filter sections without layout preservation

### 2. **Bypassing Layout Management**
These operations were completely bypassing the layout ratio management system:
```python
# PROBLEMATIC CODE:
self.browse_tab.main_widget.left_stack.setCurrentWidget(self.browse_tab.sequence_picker)
```

This direct stack manipulation would trigger Qt's layout system to recalculate widget sizes without respecting the intended 2:1 stretch factors.

### 3. **Missing Constraint Clearing**
The stack switching operations weren't clearing fixed width constraints that might have been set by previous operations, allowing old constraints to interfere with the intended layout.

## Solution Implemented

### 1. **Browse Tab Filter Controller Fix**

**File**: `src/main_window/main_widget/browse_tab/browse_tab_filter_controller.py`

**Problem**: Direct `setCurrentWidget()` call bypassed layout management.

**Solution**: Replaced direct stack switching with layout-preserving method:

**Before**:
```python
self.browse_tab.main_widget.left_stack.setCurrentWidget(
    self.browse_tab.sequence_picker
)
```

**After**:
```python
# Use layout-preserving stack switching instead of direct setCurrentWidget
self._switch_to_sequence_picker_with_layout_preservation()
```

**Added Method**: `_switch_to_sequence_picker_with_layout_preservation()`
- Sets browse tab's 2:1 stretch ratio before stack switching
- Clears any fixed width constraints that might interfere
- Performs the stack switch
- Forces layout update to ensure changes take effect

### 2. **Go Back Button Fix**

**File**: `src/main_window/main_widget/browse_tab/sequence_picker/control_panel/sequence_picker_go_back_button.py`

**Problem**: Stack fading without layout preservation.

**Solution**: Added layout preservation before stack switching:

**Before**:
```python
def switch_to_initial_filter_selection(self):
    self.main_widget.fade_manager.stack_fader.fade_stack(
        self.main_widget.left_stack, LeftStackIndex.FILTER_SELECTOR, 300
    )
```

**After**:
```python
def switch_to_initial_filter_selection(self):
    # Preserve browse tab layout ratios before stack switching
    self._preserve_browse_tab_layout()
    
    # Use fade stack switching with layout preservation
    self.main_widget.fade_manager.stack_fader.fade_stack(
        self.main_widget.left_stack, LeftStackIndex.FILTER_SELECTOR, 300
    )
```

**Added Method**: `_preserve_browse_tab_layout()`
- Ensures 2:1 stretch ratio is maintained during fade operations
- Clears conflicting width constraints
- Provides error handling with graceful fallback

### 3. **Filter Stack Navigation Fix**

**File**: `src/main_window/main_widget/browse_tab/sequence_picker/filter_stack/sequence_picker_filter_stack.py`

**Problem**: Filter section switching without layout preservation.

**Solution**: Added layout preservation before filter section changes:

**Before**:
```python
self.sequence_picker.main_widget.fade_manager.stack_fader.fade_stack(
    self.sequence_picker.filter_stack, index
)
```

**After**:
```python
# Preserve browse tab layout before stack switching
self._preserve_browse_tab_layout()

self.sequence_picker.main_widget.fade_manager.stack_fader.fade_stack(
    self.sequence_picker.filter_stack, index
)
```

**Added Method**: `_preserve_browse_tab_layout()`
- Same layout preservation pattern as other components
- Ensures consistency across all filter navigation operations

## Layout Preservation Pattern

All fixes implement the same consistent layout preservation pattern:

```python
def _preserve_browse_tab_layout(self):
    """Preserve the browse tab's 2:1 layout ratio during stack switching."""
    try:
        main_widget = self.main_widget  # or self.sequence_picker.main_widget
        
        # Ensure browse tab layout ratios are preserved during stack switching
        if hasattr(main_widget, "content_layout"):
            # Set browse tab's 2:1 stretch ratio
            main_widget.content_layout.setStretch(0, 2)  # Left stack: 2 parts
            main_widget.content_layout.setStretch(1, 1)  # Right stack: 1 part
            
            # Clear any fixed width constraints that might interfere
            if hasattr(main_widget, "left_stack"):
                main_widget.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.left_stack.setMinimumWidth(0)
            if hasattr(main_widget, "right_stack"):
                main_widget.right_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                main_widget.right_stack.setMinimumWidth(0)
                
    except Exception as e:
        # Log the error but don't fail the operation
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to preserve browse tab layout: {e}")
```

## Key Improvements

### 1. **Consistent Layout Preservation**
- **Unified Pattern**: All stack switching operations now use the same layout preservation pattern
- **Proactive Approach**: Layout ratios are set BEFORE stack switching, not after
- **Constraint Clearing**: Fixed width constraints are cleared to prevent interference

### 2. **Robust Error Handling**
- **Graceful Fallback**: If layout preservation fails, operations continue with logging
- **Non-Breaking**: Errors in layout preservation don't break filter navigation
- **Debugging Support**: Clear logging messages for troubleshooting

### 3. **Comprehensive Coverage**
- **Filter Application**: Layout preserved when applying filters and switching to sequence picker
- **Back Navigation**: Layout preserved when going back to filter selector
- **Filter Section Navigation**: Layout preserved when switching between filter sections

## Files Modified

1. **`src/main_window/main_widget/browse_tab/browse_tab_filter_controller.py`**
   - Replaced direct `setCurrentWidget()` with layout-preserving method
   - Added `_switch_to_sequence_picker_with_layout_preservation()` method

2. **`src/main_window/main_widget/browse_tab/sequence_picker/control_panel/sequence_picker_go_back_button.py`**
   - Added layout preservation before stack fading
   - Added `_preserve_browse_tab_layout()` method

3. **`src/main_window/main_widget/browse_tab/sequence_picker/filter_stack/sequence_picker_filter_stack.py`**
   - Added layout preservation before filter section switching
   - Added `_preserve_browse_tab_layout()` method

## Testing Scenarios

### Manual Testing
1. **Filter Application**: Apply various filters and verify 2:1 ratio is maintained
2. **Back Button Navigation**: Use go back button and verify layout stability
3. **Filter Section Navigation**: Navigate through different filter sections
4. **Combined Operations**: Mix filter application with back navigation
5. **Window Resizing**: Test all operations with window resizing

### Expected Results
- **Consistent Layout**: Browse tab maintains 2:1 ratio during all filter navigation
- **No Window Expansion**: Window doesn't unexpectedly resize wider during navigation
- **Smooth Transitions**: All fade animations work properly with preserved layout
- **Stable Behavior**: Layout remains stable across all filter operations

## Benefits

1. **Layout Stability**: Browse tab consistently maintains 2:1 aspect ratio during filter navigation
2. **User Experience**: No jarring layout changes or unexpected window resizing
3. **Predictable Behavior**: All filter navigation operations behave consistently
4. **Maintainable Code**: Unified pattern makes future maintenance easier
5. **Robust Operation**: Error handling ensures navigation continues even if layout preservation fails

## Integration with Previous Fixes

This fix complements the previous tab switching consistency fixes:
- **Tab Manager**: Handles layout ratios during tab switching
- **Stack Switching**: Handles layout ratios during internal browse tab navigation
- **Comprehensive Coverage**: Together, they ensure layout stability in all scenarios
