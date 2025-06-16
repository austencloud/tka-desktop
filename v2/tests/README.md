# TKA Modern Test Suite - Lifecycle-Based Testing

## 🎯 Philosophy: Tests as Temporary Scaffolding

**Revolutionary Approach**: Most tests are temporary scaffolding that should be deliberately removed when they've served their purpose. Only behavioral contracts and bug prevention tests should be permanent.

## 🚀 Quick Start

```bash
# Run all tests with health check
python tests/test_runner.py

# Run specific lifecycle categories
python tests/test_runner.py scaffolding specification
python tests/test_runner.py regression integration

# Check test suite health
python tests/test_runner.py --health

# Show expired scaffolding tests
python tests/test_runner.py --expired

# Generate lifecycle report
python tests/scripts/test_lifecycle_manager.py --report

# Run with pytest directly
python -m pytest tests/scaffolding/     # Temporary development aids
python -m pytest tests/specification/   # Permanent behavioral contracts
python -m pytest tests/regression/      # Bug prevention tests
python -m pytest tests/integration/     # Cross-component workflows

# Skip slow tests
python -m pytest -m "not slow"
```

## 📁 Lifecycle-Based Test Categories

### 🏗️ Scaffolding Tests (`tests/scaffolding/`) - TEMPORARY

- **Purpose**: Development aids, debugging, exploration
- **Lifecycle**: DELETE after purpose is achieved
- **Target**: <30 seconds total
- **Subdirectories**:
  - `debug/` - Bug reproduction and debugging
  - `exploration/` - Code understanding and Legacy behavior exploration
  - `spike/` - Proof of concepts and prototypes

**Required Metadata**: DELETE_AFTER date, PURPOSE, AUTHOR

### 📋 Specification Tests (`tests/specification/`) - PERMANENT

- **Purpose**: Behavioral contracts and business rules
- **Lifecycle**: NEVER delete unless feature removed
- **Target**: <60 seconds total
- **Subdirectories**:
  - `domain/` - Core business rules and domain logic
  - `application/` - Service layer contracts
  - `presentation/` - UI behavior contracts

**Required Metadata**: PERMANENT justification, PURPOSE, AUTHOR

### 🐛 Regression Tests (`tests/regression/`) - PERMANENT

- **Purpose**: Prevent specific bugs from reoccurring
- **Lifecycle**: DELETE only when feature removed
- **Target**: <120 seconds total
- **Subdirectories**:
  - `bugs/` - Specific bug prevention
  - `performance/` - Performance regression prevention

**Required Metadata**: BUG_REPORT, FIXED_DATE, PURPOSE, AUTHOR

### 🔗 Integration Tests (`tests/integration/`) - MINIMAL

- **Purpose**: Cross-component workflows
- **Lifecycle**: Keep minimal essential set
- **Target**: <180 seconds total
- **Subdirectories**:
  - `workflows/` - Complete user journeys

## Test Management Workflow

### 1. Creating New Tests

```bash
# Use test templates
cp tests/templates/unit_test_template.py tests/unit/services/test_new_service.py
cp tests/templates/integration_test_template.py tests/integration/test_new_integration.py

# Follow naming conventions
test_[component]_[functionality].py
test_[service]_[operation].py
test_[workflow]_[scenario].py
```

### 2. Test Quality Maintenance

```bash
# Check for outdated tests
python tests/test_runner.py --outdated

# Clean obsolete tests (dry run)
python tests/test_runner.py --clean

# Run performance monitoring
python tests/test_runner.py --profile
```

### 3. Continuous Integration

```bash
# Pre-commit hook
python tests/test_runner.py unit integration

# Full test suite
python tests/test_runner.py

# Coverage reporting
python -m pytest --cov=src --cov-report=html
```

## Test Organization

```
tests/
├── __init__.py                 # Test suite configuration
├── conftest.py                 # Shared fixtures and setup
├── pytest.ini                 # Pytest configuration
├── test_runner.py              # Advanced test runner
├── README.md                   # This file
├── templates/                  # Test templates
│   ├── unit_test_template.py
│   ├── integration_test_template.py
│   ├── ui_test_template.py
│   └── parity_test_template.py
├── unit/                       # Fast service layer tests
│   ├── __init__.py
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/                # Component communication tests
│   ├── __init__.py
│   ├── components/
│   ├── services/
│   └── workflows/
├── ui/                         # User interface tests
│   ├── __init__.py
│   ├── components/
│   ├── layouts/
│   └── interactions/
├── parity/                     # Legacy functionality parity tests
│   ├── __init__.py
│   ├── graph_editor/
│   ├── sequence_operations/
│   └── workflows/
└── results/                    # Test execution results
    ├── test_results_*.json
    ├── coverage_reports/
    └── performance_profiles/
```

## Best Practices

### Test Writing Guidelines

1. **One Concept Per Test**: Each test should verify one specific behavior
2. **Clear Test Names**: Use descriptive names that explain what is being tested
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Fast Execution**: Keep tests fast, especially unit tests
5. **Deterministic**: Tests should always produce the same result

### Fixture Usage

```python
# Use provided fixtures for common setup
def test_service_operation(mock_sequence_data, mock_container):
    service = MyService(container=mock_container)
    result = service.process(mock_sequence_data)
    assert result is not None

# Create custom fixtures for specific needs
@pytest.fixture
def custom_test_data():
    return create_specific_test_scenario()
```

### Performance Requirements

- **Unit tests**: Individual test <0.01s, category total <1s
- **Integration tests**: Individual test <1s, category total <10s
- **UI tests**: Individual test <5s, category total <30s
- **Parity tests**: Individual test <10s, category total <60s

### Error Handling

```python
# Test both success and failure cases
def test_service_success_case():
    # Test normal operation
    pass

def test_service_error_handling():
    # Test error conditions
    with pytest.raises(SpecificException):
        service.operation_that_should_fail()
```

## Advanced Features

### Automatic Test Discovery

The test runner automatically discovers and categorizes tests based on:

- File location (`tests/unit/`, `tests/integration/`, etc.)
- Test markers (`@pytest.mark.unit`, `@pytest.mark.integration`)
- Naming conventions (`test_*.py`, `Test*` classes)

### Outdated Test Detection

Tests are flagged as potentially outdated if:

- Source code has been modified more recently than the test
- Test hasn't been updated in >30 days while related code changed
- Test references deprecated APIs or patterns

### Self-Cleaning Mechanism

Obsolete tests are identified and can be safely removed when:

- Referenced code no longer exists
- Test duplicates functionality of newer tests
- Test is no longer relevant to current architecture

### Performance Monitoring

Test execution is monitored for:

- Individual test duration
- Category time limits
- Memory usage patterns
- Regression detection

## Troubleshooting

### Common Issues

1. **Qt Application Errors**: Use `qapp` fixture for UI tests
2. **Signal/Slot Testing**: Use `QSignalSpy` for signal verification
3. **Mock Setup**: Use provided mock fixtures for consistent behavior
4. **Timeout Issues**: Check test performance requirements

### Debug Mode

```bash
# Run with verbose output
python tests/test_runner.py -v

# Run specific test with debugging
python -m pytest tests/unit/services/test_specific.py::test_method -v -s

# Use pdb for debugging
python -m pytest --pdb tests/unit/services/test_specific.py
```
