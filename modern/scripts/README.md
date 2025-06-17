# Scripts Directory

This directory contains utility and maintenance scripts for the TKA Desktop Modern project.

## Available Scripts

### `cleanup_script.sh`

**Purpose:** Organizes project files according to the cleanup audit recommendations.

**Usage:**

```bash
cd modern/
./scripts/cleanup_script.sh
```

**Actions:**

- Moves demo files to `tests/demos/`
- Reports files that need manual review
- Provides status summary

**Dependencies:** None (pure bash script)

## Script Organization

- **Maintenance scripts** (like cleanup) → `scripts/`
- **Test-related scripts** → `tests/scripts/`
- **Build/deployment scripts** → Consider `scripts/build/` or `scripts/deploy/`

## Adding New Scripts

When adding new utility scripts:

1. Place them in this `scripts/` directory
2. Make them executable: `chmod +x script_name.sh`
3. Add documentation to this README
4. Follow the naming convention: `action_description.sh`

## Best Practices

- Use relative paths when possible
- Include error handling and status messages
- Add help text with `--help` flag
- Test scripts in isolation before committing
