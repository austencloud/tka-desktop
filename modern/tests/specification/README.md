# 📋 Specification Tests - PERMANENT Behavioral Contracts

## Purpose

Specification tests define and enforce the **permanent behavioral contracts** of your system. These tests should **NEVER** be deleted unless the feature itself is completely removed.

## Categories

### 🏛️ Domain (`domain/`)

- **Purpose**: Core business rules and domain logic
- **Lifecycle**: Permanent - only delete when business rule changes
- **Example**: `test_sequence_immutability_contract.py`

### 🔧 Application (`application/`)

- **Purpose**: Service layer contracts and workflows
- **Lifecycle**: Permanent - only delete when service is removed
- **Example**: `test_pictograph_dataset_service_contract.py`

### 🖥️ Presentation (`presentation/`)

- **Purpose**: UI behavior contracts and user interactions
- **Lifecycle**: Permanent - only delete when UI component is removed
- **Example**: `test_beat_frame_layout_contract.py`

## What Belongs Here

### ✅ Specification Test Criteria

- **Business rules**: Core domain logic that must never change
- **API contracts**: Service interfaces that other components depend on
- **User workflows**: Critical user interactions that must be preserved
- **Data integrity**: Immutability, validation, and consistency rules
- **Performance contracts**: Critical performance requirements
- **Legacy parity**: Essential Legacy behaviors that must be maintained

### ❌ Does NOT Belong Here

- Debugging tests (use scaffolding/)
- Implementation details (use unit tests)
- Temporary explorations (use scaffolding/)
- Bug reproductions (use regression/)

## Required Metadata

Every specification test MUST include:

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce [specific behavioral contract]
PERMANENT: [Why this behavior must be preserved]
AUTHOR: @username
"""
```

## Test Patterns

### Domain Specification Example

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce sequence data immutability contract
PERMANENT: Core business rule - sequence operations must return new instances
AUTHOR: @austencloud
"""

@pytest.mark.specification
@pytest.mark.critical
class TestSequenceDataContract:
    """Permanent specification - NEVER DELETE"""

    def test_sequence_operations_return_new_instances(self):
        """PERMANENT: Sequence must be immutable"""
        original = SequenceData(beats=[beat1])
        modified = original.add_beat(beat2)

        assert original is not modified
        assert original.length == 1
        assert modified.length == 2
```

### Application Service Contract Example

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce pictograph dataset service contract
PERMANENT: Other components depend on this interface
AUTHOR: @austencloud
"""

@pytest.mark.specification
@pytest.mark.critical
class TestPictographDatasetServiceContract:
    """Permanent service contract - NEVER DELETE"""

    def test_get_start_position_returns_valid_beat_or_none(self):
        """PERMANENT: Service contract for start position loading"""
        service = PictographDatasetService()
        result = service.get_start_position_pictograph("alpha1_alpha1", "diamond")

        assert result is None or isinstance(result, BeatData)
        if result:
            assert result.letter in ["A", "B", "C", "D"]
```

## AI Agent Instructions

**For VS Code Copilot & Other AI Agents:**

1. **Never suggest deletion** of specification tests
2. **Focus on contracts** not implementation details
3. **Ensure critical marking** for essential behaviors
4. **Verify permanence** - ask "Will this behavior always be required?"
