# 🐛 Regression Tests - BUG Prevention

## Purpose
Regression tests prevent **specific bugs** from reoccurring. They should only be deleted when the feature they protect is completely removed from the system.

## Categories

### 🐛 Bugs (`bugs/`)
- **Purpose**: Prevent specific bugs from reoccurring
- **Lifecycle**: Permanent until feature is removed
- **Example**: `test_issue_47_option_picker_crash.py`

### ⚡ Performance (`performance/`)
- **Purpose**: Prevent performance regressions
- **Lifecycle**: Permanent until feature is removed
- **Example**: `test_sequence_loading_performance.py`

## What Belongs Here

### ✅ Regression Test Criteria
- **Specific bug reproduction**: Test that reproduces the exact bug scenario
- **Performance benchmarks**: Tests that ensure performance doesn't degrade
- **Edge cases**: Unusual scenarios that previously caused issues
- **Integration failures**: Cross-component issues that were fixed

### ❌ Does NOT Belong Here
- General functionality tests (use specification/)
- Debugging tests (use scaffolding/)
- New feature tests (use specification/)

## Required Metadata

Every regression test MUST include:

```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent [specific bug] from reoccurring
BUG_REPORT: #123 or description
FIXED_DATE: YYYY-MM-DD
AUTHOR: @username
"""
```

## Test Patterns

### Bug Regression Example
```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent option picker crash when clearing sequence
BUG_REPORT: #47 - Program crashes when clearing sequence after option selection
FIXED_DATE: 2025-01-15
AUTHOR: @austencloud
"""

@pytest.mark.regression
@pytest.mark.critical
class TestIssue47OptionPickerCrash:
    """Prevent option picker crash regression - DELETE only if feature removed"""
    
    def test_clear_sequence_after_option_selection_no_crash(self):
        """REGRESSION: Clearing sequence after option selection must not crash"""
        # Reproduce the exact scenario that caused the crash
        sequence = SequenceData(beats=[beat1])
        
        # This used to crash
        cleared = SequenceData.empty()
        
        # Should complete without exception
        assert cleared.length == 0
        assert cleared.is_empty
```

### Performance Regression Example
```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent sequence loading performance regression
BUG_REPORT: Sequence loading became 10x slower in Sprint 2
FIXED_DATE: 2025-01-20
AUTHOR: @austencloud
"""

@pytest.mark.regression
@pytest.mark.performance
class TestSequenceLoadingPerformance:
    """Prevent sequence loading performance regression"""
    
    def test_sequence_loading_under_100ms(self):
        """REGRESSION: Sequence loading must complete under 100ms"""
        import time
        
        start = time.time()
        service = PictographDatasetService()
        beat = service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        end = time.time()
        
        duration_ms = (end - start) * 1000
        assert duration_ms < 100, f"Sequence loading took {duration_ms}ms (limit: 100ms)"
```

## Lifecycle Management

### ✅ When to Create Regression Tests
- After fixing any bug
- After performance optimization
- After resolving integration issues
- When edge cases are discovered

### 🗑️ When to Delete Regression Tests
- **ONLY** when the entire feature is removed
- When the component being tested no longer exists
- When the bug scenario is impossible due to architectural changes

### ⚠️ Never Delete For These Reasons
- Test is old
- Test seems redundant
- Test is slow
- Code has been refactored

## AI Agent Instructions

**For VS Code Copilot & Other AI Agents:**

1. **Suggest regression tests** after any bug fix
2. **Never suggest deletion** unless feature is completely removed
3. **Link to bug reports** when creating regression tests
4. **Focus on exact reproduction** of the original bug scenario
