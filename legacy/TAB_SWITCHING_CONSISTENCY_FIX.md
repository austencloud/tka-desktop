# Tab Switching Consistency Fix - Browse Tab 2:1 Aspect Ratio

## Problem Description

The browse tab's 2:1 aspect ratio (left panel 2/3 width, right panel 1/3 width) was not being maintained consistently during tab switching. The layout would sometimes correctly preserve the intended dimensions, but other times the panels would immediately revert to an equal 50/50 width distribution.

## Root Cause Analysis

The inconsistency was caused by multiple conflicting tab switching systems and missing constraint clearing:

### 1. **Dual Tab Switching Systems**
- **MainWidgetTabSwitcher** (old system) vs **TabManager** (new dependency injection system)
- Both systems were setting stretch factors but with different timing and constraint handling
- The TabManager was missing the crucial constraint clearing code

### 2. **Missing Initial Layout Setup**
- **MainWidgetCoordinator** wasn't setting initial stretch factors like the old MainWidget
- This caused inconsistent startup behavior depending on which tab was loaded first

### 3. **Incomplete Constraint Clearing**
- **TabManager** was setting stretch factors but not clearing existing fixed width constraints
- Fixed width constraints from previous operations would override the stretch factors

### 4. **Direct Widget Access Issues**
- **MainWidgetTabSwitcher** was still using direct widget access (`self.mw.browse_tab`)
- This could cause AttributeError during the dependency injection transition

## Solution Implemented

### 1. **Fixed TabManager Constraint Clearing**

**File**: `src/main_window/main_widget/core/tab_manager.py`

**Problem**: TabManager was setting stretch factors but not clearing fixed width constraints.

**Solution**: Added comprehensive constraint clearing for both new coordinator and old main widget systems:

```python
# Clear any fixed width constraints that might interfere with stretch factors
if hasattr(self.coordinator, "left_stack"):
    self.coordinator.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
    self.coordinator.left_stack.setMinimumWidth(0)
if hasattr(self.coordinator, "right_stack"):
    self.coordinator.right_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
    self.coordinator.right_stack.setMinimumWidth(0)
```

### 2. **Added Initial Layout Setup to MainWidgetCoordinator**

**File**: `src/main_window/main_widget/core/main_widget_coordinator.py`

**Problem**: MainWidgetCoordinator wasn't setting initial stretch factors.

**Solution**: Added initial 2:1 stretch ratio during layout creation:

```python
# Add widgets with initial 2:1 stretch ratio (browse tab default)
# This ensures consistent layout from startup
self.content_layout.addWidget(self.left_stack, 2)  # 2/3 width for left stack
self.content_layout.addWidget(self.right_stack, 1)  # 1/3 width for right stack
```

### 3. **Fixed Direct Widget Access in MainWidgetTabSwitcher**

**File**: `src/main_window/main_widget/main_widget_tab_switcher.py`

**Problem**: Direct access to `self.mw.browse_tab` and `self.mw.sequence_card_tab` could cause AttributeError.

**Solution**: Implemented dependency injection pattern with graceful fallbacks:

**Before**:
```python
self.mw.browse_tab.sequence_viewer.thumbnail_box.image_label._resize_pixmap_to_fit()
```

**After**:
```python
browse_tab = self._get_browse_tab()
if browse_tab and hasattr(browse_tab, 'sequence_viewer'):
    sequence_viewer = browse_tab.sequence_viewer
    if hasattr(sequence_viewer, 'thumbnail_box') and hasattr(sequence_viewer.thumbnail_box, 'image_label'):
        sequence_viewer.thumbnail_box.image_label._resize_pixmap_to_fit()
```

**Added Methods**:
- `_get_browse_tab()`: Get browse tab with graceful fallbacks
- `_get_sequence_card_tab()`: Get sequence card tab with graceful fallbacks

## Key Improvements

### 1. **Consistent Constraint Management**
- **Unified Approach**: Both TabManager and MainWidgetTabSwitcher now use the same constraint clearing pattern
- **Complete Clearing**: All fixed width constraints are properly cleared before setting stretch factors
- **System Compatibility**: Works with both new coordinator and old main widget systems

### 2. **Predictable Startup Behavior**
- **Initial Ratios**: MainWidgetCoordinator sets initial 2:1 stretch factors
- **Consistent Defaults**: Browse tab ratio is the default, ensuring predictable behavior
- **No Race Conditions**: Layout is established before any tab switching occurs

### 3. **Robust Widget Access**
- **Dependency Injection**: Uses proper `get_tab_widget()` methods instead of direct access
- **Graceful Fallbacks**: Three levels of fallback for maximum compatibility
- **Error Prevention**: Prevents AttributeError during transition period

### 4. **Layout Stability**
- **Stretch Factor Priority**: Stretch factors take precedence over fixed widths
- **Constraint Clearing**: Removes conflicting layout constraints consistently
- **Animation Compatibility**: Works properly with fade animations and transitions

## Files Modified

1. **`src/main_window/main_widget/core/tab_manager.py`**
   - Added constraint clearing for both coordinator and main widget systems
   - Enhanced layout ratio application with proper constraint management

2. **`src/main_window/main_widget/core/main_widget_coordinator.py`**
   - Added initial 2:1 stretch factors during layout creation
   - Ensures consistent startup behavior

3. **`src/main_window/main_widget/main_widget_tab_switcher.py`**
   - Fixed direct widget access using dependency injection pattern
   - Added `_get_browse_tab()` and `_get_sequence_card_tab()` methods
   - Enhanced error handling and graceful fallbacks

## Testing

### Comprehensive Test Suite
Created `src/testing/tab_switching_consistency_test.py` with the following test scenarios:

1. **Initial Browse Tab Layout**: Verify correct 2:1 ratio on startup
2. **Tab Switching Sequence**: Test switching through all tabs and back to browse
3. **Fast Consecutive Switches**: Test rapid tab switching behavior
4. **Window Resize During Switches**: Test layout stability during window resizing
5. **Browse Tab Return Consistency**: Test that returning to browse always maintains ratio

### Manual Testing Checklist
- [ ] Switch to browse tab from startup - verify 2:1 ratio
- [ ] Switch between all tabs multiple times - verify browse tab ratio is preserved
- [ ] Resize window while on browse tab - verify ratio is maintained
- [ ] Fast consecutive tab switches - verify no layout regression
- [ ] Application restart - verify consistent initial layout

## Expected Results

### Browse Tab Layout
- **Left Panel (Sequence Picker)**: ~66.7% of total content width (2/3)
- **Right Panel (Sequence Viewer)**: ~33.3% of total content width (1/3)
- **Aspect Ratio**: 2:1 (±30% tolerance for animations and transitions)

### Consistency Guarantees
- **Startup**: Browse tab always starts with correct 2:1 ratio
- **Tab Switching**: Ratio is preserved when switching away and back to browse tab
- **Window Resizing**: Ratio is maintained during window resize operations
- **Fast Switching**: No layout regression during rapid tab changes

## Benefits

1. **Predictable Layout**: Browse tab consistently maintains 2:1 aspect ratio
2. **Smooth Transitions**: No jarring layout changes during tab switching
3. **Robust Error Handling**: Graceful handling of missing components during transition
4. **Performance**: Efficient constraint management without layout thrashing
5. **Maintainability**: Consistent patterns across both old and new systems

## Backward Compatibility

All changes maintain backward compatibility:
- **Legacy Support**: Old direct access patterns still work as fallbacks
- **Gradual Migration**: Supports smooth transition to new dependency injection system
- **No Breaking Changes**: Existing functionality is preserved and enhanced
