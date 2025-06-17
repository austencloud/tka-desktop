# 🤖 AI Agent Instructions for TKA Desktop

## 🚨 CRITICAL: Test Organization Rules

**Before creating ANY test file, you MUST:**

1. **Read the test organization guide**: `modern/tests/TEST_ORGANIZATION_GUIDE.md`
2. **Follow the decision tree**: Ask "Why am I writing this test?"
3. **Use proper lifecycle metadata**: Every test needs lifecycle headers
4. **Validate placement**: Run `python modern/tests/scripts/validate_test_placement.py`

## 📁 Quick Reference - Where Tests Go

```
├── "I'm debugging a bug" → tests/scaffolding/debug/
├── "I'm exploring how Legacy works" → tests/scaffolding/exploration/
├── "I'm prototyping a new idea" → tests/scaffolding/spike/
├── "This behavior must NEVER change" → tests/specification/
├── "This bug must NEVER come back" → tests/regression/
└── "Testing cross-component workflow" → tests/integration/
```

## ⚠️ RED FLAGS - Never Do These

- ❌ Put tests in the root `tests/` directory
- ❌ Create scaffolding tests without DELETE_AFTER dates
- ❌ Create specification tests for implementation details
- ❌ Skip lifecycle metadata
- ❌ Ignore the validation scripts

## 🔧 Required Tools Usage

**Before committing any test changes:**

```bash
# Validate test placement
python modern/tests/scripts/validate_test_placement.py

# Check test health
python modern/tests/test_runner.py --health

# Find expired tests
python modern/tests/test_runner.py --expired
```

## 📝 Required Test Metadata Templates

### Scaffolding (Temporary)

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: [One-line description]
DELETE_AFTER: YYYY-MM-DD (REQUIRED!)
CREATED: YYYY-MM-DD
AUTHOR: @username
RELATED_ISSUE: #123 (if applicable)
"""
```

### Specification (Permanent)

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce [specific behavioral contract]
PERMANENT: [Why this behavior must be preserved]
AUTHOR: @username
"""
```

### Regression (Bug Prevention)

```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent [specific bug] from reoccurring
BUG_REPORT: #123 - Description
FIXED_DATE: YYYY-MM-DD
AUTHOR: @username
"""
```

## 🎯 Success Criteria

Your test changes are correct when:

- ✅ Validation scripts pass
- ✅ Tests are in correct directories
- ✅ All metadata is present
- ✅ DELETE_AFTER dates are set for scaffolding
- ✅ No tests in wrong locations

**Remember**: Most tests should be temporary scaffolding that gets deleted!
