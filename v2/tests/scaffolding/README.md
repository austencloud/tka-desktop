# 🏗️ Scaffolding Tests - TEMPORARY Development Aids

## Purpose

Scaffolding tests are **temporary** tests created to aid development, debugging, and exploration. They should be **actively removed** when they've served their purpose.

## Categories

### 🐛 Debug (`debug/`)

- **Purpose**: Reproduce and fix specific bugs
- **Lifecycle**: Delete after bug is fixed and regression test is added
- **Example**: `test_option_picker_crash_debug.py`

### 🔍 Exploration (`exploration/`)

- **Purpose**: Understand existing code or explore new approaches
- **Lifecycle**: Delete after understanding is achieved
- **Example**: `test_legacy_behavior_exploration.py`

### ⚡ Spike (`spike/`)

- **Purpose**: Proof of concept for new features
- **Lifecycle**: Delete after spike is complete and real implementation begins
- **Example**: `test_graph_editor_animation_spike.py`

## Lifecycle Rules

### ✅ When to Create Scaffolding Tests

- Debugging a specific issue
- Exploring unfamiliar code
- Prototyping new functionality
- Understanding Legacy behavior for parity
- Testing layout/sizing issues

### 🗑️ When to Delete Scaffolding Tests

- Bug is fixed and regression test exists
- Understanding is achieved and documented
- Spike is complete and real implementation started
- Layout/sizing issue is resolved
- Test has reached its DELETE_BY date

### ⚠️ Red Flags (Delete Immediately)

- Test older than 30 days without clear purpose
- Test duplicating specification coverage
- Test with no DELETE_BY date
- Test that always passes/fails
- Test with unclear purpose documentation

## Required Metadata

Every scaffolding test MUST include:

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: One-line description of why this test exists
DELETE_AFTER: YYYY-MM-DD (required)
CREATED: YYYY-MM-DD
AUTHOR: @username
RELATED_ISSUE: #123 (if applicable)
"""
```

## AI Agent Instructions

**For VS Code Copilot & Other AI Agents:**

1. **Always ask about lifecycle** when creating tests in this directory
2. **Suggest deletion** when purpose appears achieved
3. **Warn about missing metadata** in scaffolding tests
4. **Recommend migration** to specification/ when behavior becomes permanent

## Examples

### Good Scaffolding Test

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug option picker layout crash during Sprint 2
DELETE_AFTER: 2025-02-01
CREATED: 2025-01-15
AUTHOR: @austencloud
RELATED_ISSUE: #47
"""

@pytest.mark.scaffolding
@pytest.mark.delete_after("2025-02-01")
@pytest.mark.debug
class TestOptionPickerLayoutDebug:
    """DELETE: Debugging option picker layout issues"""

    def test_widget_sizing_crash(self):
        """DELETE: Reproduce widget sizing crash"""
        # Temporary debugging code
        pass
```

### Bad Scaffolding Test (Delete Immediately)

```python
# No metadata, unclear purpose, old
def test_something():
    assert True  # Always passes
```
