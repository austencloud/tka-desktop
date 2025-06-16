# AI Testing Guidelines for TKA Modern

## For VS Code Copilot, GitHub Copilot, and Other AI Agents

This document teaches AI agents how to work with TKA's lifecycle-based testing strategy.

## 🎯 Core Philosophy

**Tests are temporary scaffolding, not permanent artifacts.**

Most tests should be created, used, and then deliberately deleted when they've served their purpose. Only behavioral contracts and bug prevention tests should be permanent.

## 📁 Test Categories You Must Understand

### 🏗️ SCAFFOLDING (`tests/scaffolding/`) - TEMPORARY

- **Purpose**: Development aids, debugging, exploration
- **Lifecycle**: DELETE after purpose is achieved
- **AI Action**: ALWAYS suggest deletion when purpose appears complete
- **Required**: DELETE_AFTER date in metadata

**When to suggest scaffolding tests:**

- User is debugging a specific issue
- User wants to explore/understand existing code
- User is prototyping new functionality
- User needs to understand Legacy behavior for parity

**When to suggest deletion:**

- Bug is fixed and regression test exists
- Understanding is achieved and documented
- Prototype is complete and real implementation started
- Test has reached DELETE_AFTER date

### 📋 SPECIFICATION (`tests/specification/`) - PERMANENT

- **Purpose**: Behavioral contracts, business rules
- **Lifecycle**: NEVER delete unless feature removed
- **AI Action**: NEVER suggest deletion, focus on contracts
- **Required**: Clear permanent justification

**What belongs here:**

- Core business rules (e.g., sequence immutability)
- Service interface contracts
- Critical user workflow behaviors
- Legacy parity requirements

**What does NOT belong here:**

- Implementation details
- Debugging tests
- Temporary explorations

### 🐛 REGRESSION (`tests/regression/`) - PERMANENT

- **Purpose**: Prevent specific bugs from reoccurring
- **Lifecycle**: DELETE only when feature is removed
- **AI Action**: Suggest after any bug fix
- **Required**: Link to original bug report

## 🤖 AI Agent Decision Tree

### When User Asks for a Test:

1. **Ask: "What is the purpose of this test?"**

   - Debugging/exploring → Suggest `scaffolding/`
   - Enforcing behavior → Suggest `specification/`
   - Preventing bug → Suggest `regression/`

2. **For scaffolding tests, ask: "When should this be deleted?"**

   - Always require DELETE_AFTER date
   - Suggest realistic timeline (1-4 weeks)

3. **For specification tests, ask: "Why must this behavior be permanent?"**
   - Must be core business rule or critical contract
   - If not permanent, suggest scaffolding instead

### When Reviewing Existing Tests:

1. **Check for proper lifecycle metadata**

   - Missing metadata → Warn and suggest adding
   - Scaffolding without DELETE_AFTER → Flag as problem

2. **Identify deletion candidates**

   - Scaffolding tests past DELETE_AFTER date
   - Tests with unclear purpose
   - Tests that duplicate specification coverage

3. **Suggest test migration**
   - Scaffolding that became permanent behavior → Move to specification
   - Debug tests after bug fix → Create regression test

## 📝 Required Metadata Patterns

### Scaffolding Test Metadata:

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug option picker crash during Sprint 2
DELETE_AFTER: 2025-02-01
CREATED: 2025-01-15
AUTHOR: @austencloud
RELATED_ISSUE: #47
"""

@pytest.mark.scaffolding
@pytest.mark.delete_after("2025-02-01")
@pytest.mark.debug
```

### Specification Test Metadata:

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce sequence data immutability contract
PERMANENT: Core business rule - sequence operations must return new instances
AUTHOR: @austencloud
"""

@pytest.mark.specification
@pytest.mark.critical
```

### Regression Test Metadata:

```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent option picker crash from reoccurring
BUG_REPORT: #47 - Program crashes when clearing sequence
FIXED_DATE: 2025-01-15
AUTHOR: @austencloud
"""

@pytest.mark.regression
@pytest.mark.critical
```

## 🚨 Red Flags to Warn About

### Immediate Action Required:

- Scaffolding test without DELETE_AFTER date
- Test older than 30 days in scaffolding/
- Test with no clear purpose documentation
- Specification test that tests implementation details
- Missing lifecycle metadata entirely

### Suggest Review:

- Scaffolding test approaching DELETE_AFTER date
- Test that always passes or always fails
- Test that duplicates existing coverage
- Complex test that could be simplified

## 💬 Suggested AI Responses

### When User Creates Debug Test:

```
"I see you're creating a debug test. This should go in `tests/scaffolding/debug/`
with a DELETE_AFTER date. When do you expect to finish debugging this issue?
I'll set the deletion date accordingly."
```

### When User Creates Permanent Test:

```
"This looks like a behavioral contract. Should this go in `tests/specification/`?
What makes this behavior permanent - is it a core business rule or critical contract?"
```

### When Reviewing Old Scaffolding Test:

```
"This scaffolding test is from [date] and was meant to debug [issue].
Has this issue been resolved? If so, I can help you delete this test
and create a regression test if needed."
```

### When User Wants to Keep Debug Test:

```
"If this test represents permanent behavior, let's move it to `tests/specification/`
with proper contract documentation. Otherwise, let's set a DELETE_AFTER date."
```

## 🔧 Integration with Development Workflow

### During Bug Fixes:

1. Create scaffolding test to reproduce bug
2. Fix the bug
3. Create regression test to prevent recurrence
4. Delete scaffolding test

### During Feature Development:

1. Create scaffolding tests for exploration/prototyping
2. Develop feature with specification tests for contracts
3. Delete scaffolding tests when feature is complete

### During Code Review:

1. Check for proper test lifecycle metadata
2. Suggest test cleanup opportunities
3. Verify new tests are in correct categories

Remember: **Tests are tools to be used and then deliberately removed when no longer needed.**
