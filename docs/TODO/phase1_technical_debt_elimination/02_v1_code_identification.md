# **Task 1.1: Systematic Legacy Code Identification**

**Timeline**: Day 1-2  
**Priority**: CRITICAL  
**Goal**: Find and catalog all Legacy compatibility code for removal

---

## **What to do:**

```bash
# Step 1: Find all Legacy references
cd TKA/tka-desktop/v2/src/application/services
grep -r "Legacy\|legacy" . --include="*.py" > legacy_references.txt
grep -r "# Legacy\|# legacy" . --include="*.py" >> legacy_references.txt
grep -r "old\|Old\|OLD" . --include="*.py" >> legacy_references.txt
grep -r "legacy\|Legacy" . --include="*.py" >> legacy_references.txt

# Step 2: Find Legacy-style comments
grep -r "Legacy-style\|legacy-style" . --include="*.py" >> legacy_references.txt
grep -r "Legacy approach\|legacy approach" . --include="*.py" >> legacy_references.txt
```

---

## **Expected Issues Found:**

### **EXAMPLE 1: arrow_management_service.py**

```python
def create_sections(self) -> None:
    """Legacy-style: Create sections with single-row layout for sections 4,5,6"""
    # Legacy-style: Create transparent horizontal container for sections 4, 5, 6
    # Legacy approach: no finalization needed, QVBoxLayout just works!
```

### **EXAMPLE 2: Various services**

```python
# Using DIAMOND layer2 points from circle_coords.json (old working service)
# Hand point coordinates (for STATIC/DASH arrows) - inner grid positions where props are placed
```

---

## **Comprehensive Search Strategy**

### **Primary Patterns to Find**

```bash
# Legacy version references
grep -r "Legacy\|legacy" . --include="*.py"

# Legacy/old references
grep -r "old\|Old\|OLD\|legacy\|Legacy" . --include="*.py"

# Legacy-style comments
grep -r "Legacy-style\|legacy-style\|Legacy style\|legacy style" . --include="*.py"

# Legacy approach references
grep -r "Legacy approach\|legacy approach\|Legacy method\|legacy method" . --include="*.py"

# Working service references (usually Legacy)
grep -r "working service\|old working\|legacy working" . --include="*.py"

# Temporary compatibility
grep -r "compatibility\|compat\|temp\|temporary" . --include="*.py"

# TODO comments related to Legacy
grep -r "TODO.*Legacy\|TODO.*legacy\|TODO.*old\|TODO.*legacy" . --include="*.py"
```

### **Secondary Patterns**

```bash
# Deprecated patterns
grep -r "deprecated\|Deprecated\|DEPRECATED" . --include="*.py"

# Backup/fallback patterns
grep -r "backup\|fallback\|old_" . --include="*.py"

# Migration-related comments
grep -r "migration\|Migration\|migrate" . --include="*.py"
```

---

## **Documentation of Findings**

Create a comprehensive report of all Legacy references:

### **legacy_references.txt Format**

```
FILE: src/application/services/motion/arrow_management_service.py
LINE 45: # Legacy-style: Create transparent horizontal container for sections 4, 5, 6
LINE 67: """Legacy-style: Create sections with single-row layout for sections 4,5,6"""
LINE 89: # Legacy approach: no finalization needed, QVBoxLayout just works!

FILE: src/application/services/motion/motion_management_service.py
LINE 23: # Using DIAMOND layer2 points from circle_coords.json (old working service)
LINE 156: # Hand point coordinates (for STATIC/DASH arrows) - old Legacy system

FILE: src/application/services/core/sequence_management_service.py
LINE 78: # Legacy compatibility path for legacy sequences
LINE 234: # TODO: Remove Legacy compatibility after migration complete
```

---

## **Priority Classification**

### **High Priority (Remove Immediately)**

- Direct Legacy references in active code
- Legacy-style comments in function signatures
- Legacy approach explanations in core logic

### **Medium Priority (Review and Clean)**

- Legacy references in TODO comments
- Legacy compatibility code paths
- Old working service references

### **Low Priority (Safe to Clean)**

- Historical comments about Legacy
- Documentation references to Legacy
- Variable names with Legacy references

---

## **Validation Commands**

After identification, validate findings:

```bash
# Count total Legacy references
cat legacy_references.txt | wc -l

# Group by file for prioritization
cat legacy_references.txt | cut -d: -f1 | sort | uniq -c | sort -nr

# Find the most problematic files
grep -c "Legacy\|legacy\|old\|legacy" src/application/services/**/*.py | sort -t: -k2 -nr
```

---

## **Expected Output**

You should find approximately **15-25 Legacy references** across these files:

- `arrow_management_service.py` (5-8 references)
- `motion_management_service.py` (3-5 references)
- `sequence_management_service.py` (2-4 references)
- Various positioning services (5-8 references)

---

## **Next Step**

After completing identification, proceed to: [Task 1.2: Clean Legacy References](03_legacy_code_cleanup.md)
