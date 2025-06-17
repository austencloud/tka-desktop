# TKA Parallel Testing Framework

Comprehensive parallel testing system that validates functional equivalence between TKA Legacy and Modern implementations during the migration process.

## Overview

This framework executes identical user actions simultaneously on both Legacy and Modern applications and compares results to ensure Modern maintains exact parity with Legacy's behavior while respecting the existing consolidated service architecture.

**Lifecycle**: SCAFFOLDING  
**Delete After**: Legacy deprecation complete  
**Purpose**: Validate Legacy/Modern functional equivalence during migration

## Architecture

```
tests/parallel/
├── master_test_orchestrator.py     # Main coordination logic
├── master_parallel_test.py         # CLI test runner
├── actions/
│   ├── user_actions.py            # Action abstraction layer
│   └── action_validators.py       # Pre/post-condition validation
├── drivers/
│   ├── driver_base.py             # Common driver interface
│   ├── legacy_driver.py              # Legacy-specific test driver
│   └── modern_driver.py              # Modern-specific test driver
├── comparison/
│   └── result_comparer.py        # Deep comparison engine
├── scenarios/
│   └── basic_workflows.py        # Core TKA workflow scenarios
└── README.md                     # This file
```

## Key Features

### 🎯 Action Mirroring System

- Executes synchronized actions across both Legacy and Modern applications
- Handles timing differences and state synchronization
- Provides rollback capabilities for failed test scenarios

### 🔍 Deep Result Comparison

- **Sequence Data Comparison**: Beat count, motion positions, turn values with exact matching
- **Pictograph Data Comparison**: SVG file paths, arrow positioning, motion-type-specific rendering
- **Arrow Rendering Validation**: Ensures Modern correctly loads motion-type-specific SVG files
- **Numeric Tolerance**: Floating-point comparisons with ±0.001 precision for turn values

### 📊 Comprehensive Reporting

- Step-by-step action execution results with visual pass/fail indicators
- Side-by-side comparison views for Legacy vs Modern outputs
- Detailed difference breakdowns with exact field-level mismatches
- HTML reports with actionable debugging information

## TKA Domain Model Integration

### Verified Motion Type Mappings

Based on codebase analysis, the framework handles:

- **Legacy → Modern Motion Types**: `shift` → `pro`, direct mappings for `anti`, `dash`, `static`, `float`
- **Field Names**: Both versions use `prop_rot_dir` (no mapping needed)
- **Turn Values**: Special handling for float motion (`"fl"` → `-0.5`)

### Data Extraction Patterns

- **Legacy**: Extracts from `beat.state.pictograph_data` with `blue_attributes`/`red_attributes` structure
- **Modern**: Uses `BeatData` with `blue_motion`/`red_motion` MotionData objects
- **Normalization**: Converts enum values to strings for comparison

## Quick Start

### Prerequisites

- Python 3.8+
- TKA Legacy and Modern source code available
- PyQt6 installed

### Basic Usage

```bash
# List available scenarios
python master_parallel_test.py --list

# Run single scenario
python master_parallel_test.py --scenario start_position_selection

# Run all basic scenarios
python master_parallel_test.py --all

# Generate HTML report
python master_parallel_test.py --all --report --output results.html

# Save JSON results
python master_parallel_test.py --all --json results.json
```

### Configuration Options

```bash
# Adjust tolerances
python master_parallel_test.py --all --position-tolerance 1.0 --rotation-tolerance 0.2

# Timeout settings
python master_parallel_test.py --scenario single_beat_creation --timeout 15

# Debugging options
python master_parallel_test.py --all --verbose --no-screenshots
```

## Test Scenarios

### Core Workflow Scenarios

1. **Start Position Selection**

   - Tests alpha, beta, gamma position selection
   - Verifies option picker updates correctly
   - Duration: ~15 seconds

2. **Single Beat Creation**

   - Tests start position → option selection → beat creation workflow
   - Validates pictograph rendering
   - Duration: ~20 seconds

3. **Sequence Building**

   - Tests multi-beat sequence creation with dynamic option updates
   - Verifies sequence state management
   - Duration: ~45 seconds

4. **Motion Modification**

   - Tests turn adjustments and motion type changes
   - Validates motion property updates
   - Duration: ~30 seconds

5. **Graph Editor Toggle**

   - Tests graph editor open/close functionality
   - Verifies layout preservation
   - Duration: ~20 seconds

6. **Sequence Clear**
   - Tests sequence clearing and state reset
   - Validates complete state cleanup
   - Duration: ~25 seconds

## Success Criteria

- **≥95% functional equivalence** across all test scenarios
- **<5% false positive rate** for regression detection
- **100% actionable debugging information** for divergences
- **Preserved arrow rendering quality** (300x300 square aspect ratios)

## Implementation Timeline

### Phase 1 (Weeks 1-2): Infrastructure & Single Action

- ✅ Core action abstraction layer
- ✅ Legacy/Modern application drivers
- ✅ Basic comparison framework
- ✅ Single action (start position) working reliably

### Phase 2 (Weeks 3-4): Core Workflow

- ✅ Start position → option selection → beat addition workflow
- ✅ Arrow rendering validation
- ✅ TKA-specific data normalization
- ✅ Comprehensive test scenarios

### Phase 3 (Weeks 5-6): Advanced Features & Validation

- 🔄 Advanced motion modification scenarios
- 🔄 Graph editor integration testing
- 🔄 Performance optimization
- 🔄 CI/CD integration

## Debugging & Troubleshooting

### Common Issues

1. **Application Startup Failures**

   ```bash
   # Check application paths and dependencies
   python master_parallel_test.py --verbose --scenario start_position_selection
   ```

2. **Timing Issues**

   ```bash
   # Increase timeouts for slower systems
   python master_parallel_test.py --timeout 20 --scenario sequence_building
   ```

3. **False Positives**
   ```bash
   # Adjust tolerances for position/rotation differences
   python master_parallel_test.py --position-tolerance 3.0 --rotation-tolerance 1.0
   ```

### Debug Output

The framework provides detailed logging and debug snapshots:

- **Test logs**: `parallel_test_YYYYMMDD_HHMMSS.log`
- **Screenshots**: `test_data/screenshots/legacy/` and `test_data/screenshots/modern/`
- **Debug snapshots**: `debug_snapshots/` (when enabled)

## Integration with Existing Test Framework

This parallel testing framework integrates with TKA's existing test structure:

- **Lifecycle**: Uses SCAFFOLDING metadata with DELETE_AFTER dates
- **Self-cleaning**: Temporary tests with expiration dates
- **Metadata**: AI-friendly test categorization and purpose documentation

## Contributing

When adding new test scenarios:

1. Create scenario in `scenarios/` directory
2. Add validation rules in scenario validator
3. Update scenario provider to include new scenario
4. Add documentation to this README

## Cost Optimization

- **Efficient batch testing** to minimize $0.05 per message costs
- **Periodic progress confirmations** for long-running test suites
- **Autonomous continuation** without permission requests when making clear progress
- **Focus on high-value scenarios** that catch the most critical regressions
