# **Task 1.1: Systematic V1 Code Identification**

**Timeline**: Day 1-2  
**Priority**: CRITICAL  
**Goal**: Find and catalog all V1 compatibility code for removal

---

## **What to do:**

```bash
# Step 1: Find all V1 references
cd TKA/tka-desktop/v2/src/application/services
grep -r "V1\|v1" . --include="*.py" > v1_references.txt
grep -r "# V1\|# v1" . --include="*.py" >> v1_references.txt
grep -r "old\|Old\|OLD" . --include="*.py" >> v1_references.txt
grep -r "legacy\|Legacy" . --include="*.py" >> v1_references.txt

# Step 2: Find V1-style comments
grep -r "V1-style\|v1-style" . --include="*.py" >> v1_references.txt
grep -r "V1 approach\|v1 approach" . --include="*.py" >> v1_references.txt
```

---

## **Expected Issues Found:**

### **EXAMPLE 1: arrow_management_service.py**

```python
def create_sections(self) -> None:
    """V1-style: Create sections with single-row layout for sections 4,5,6"""
    # V1-style: Create transparent horizontal container for sections 4, 5, 6
    # V1 approach: no finalization needed, QVBoxLayout just works!
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
# V1 version references
grep -r "V1\|v1" . --include="*.py"

# Legacy/old references
grep -r "old\|Old\|OLD\|legacy\|Legacy" . --include="*.py"

# V1-style comments
grep -r "V1-style\|v1-style\|V1 style\|v1 style" . --include="*.py"

# V1 approach references
grep -r "V1 approach\|v1 approach\|V1 method\|v1 method" . --include="*.py"

# Working service references (usually V1)
grep -r "working service\|old working\|legacy working" . --include="*.py"

# Temporary compatibility
grep -r "compatibility\|compat\|temp\|temporary" . --include="*.py"

# TODO comments related to V1
grep -r "TODO.*V1\|TODO.*v1\|TODO.*old\|TODO.*legacy" . --include="*.py"
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

Create a comprehensive report of all V1 references:

### **v1_references.txt Format**

```
FILE: src/application/services/motion/arrow_management_service.py
LINE 45: # V1-style: Create transparent horizontal container for sections 4, 5, 6
LINE 67: """V1-style: Create sections with single-row layout for sections 4,5,6"""
LINE 89: # V1 approach: no finalization needed, QVBoxLayout just works!

FILE: src/application/services/motion/motion_management_service.py
LINE 23: # Using DIAMOND layer2 points from circle_coords.json (old working service)
LINE 156: # Hand point coordinates (for STATIC/DASH arrows) - old V1 system

FILE: src/application/services/core/sequence_management_service.py
LINE 78: # V1 compatibility path for legacy sequences
LINE 234: # TODO: Remove V1 compatibility after migration complete
```

---

## **Priority Classification**

### **High Priority (Remove Immediately)**

- Direct V1 references in active code
- V1-style comments in function signatures
- V1 approach explanations in core logic

### **Medium Priority (Review and Clean)**

- V1 references in TODO comments
- Legacy compatibility code paths
- Old working service references

### **Low Priority (Safe to Clean)**

- Historical comments about V1
- Documentation references to V1
- Variable names with V1 references

---

## **Validation Commands**

After identification, validate findings:

```bash
# Count total V1 references
cat v1_references.txt | wc -l

# Group by file for prioritization
cat v1_references.txt | cut -d: -f1 | sort | uniq -c | sort -nr

# Find the most problematic files
grep -c "V1\|v1\|old\|legacy" src/application/services/**/*.py | sort -t: -k2 -nr
```

---

## **Expected Output**

You should find approximately **15-25 V1 references** across these files:

- `arrow_management_service.py` (5-8 references)
- `motion_management_service.py` (3-5 references)
- `sequence_management_service.py` (2-4 references)
- Various positioning services (5-8 references)

---

## **Next Step**

After completing identification, proceed to: [Task 1.2: Clean V1 References](03_v1_code_cleanup.md)
