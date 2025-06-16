# **Task 1.2: Clean Legacy References**

**Timeline**: Day 1-2  
**Priority**: CRITICAL  
**Goal**: Remove all Legacy compatibility code and replace with clean V2 patterns

---

## **Action Plan:**

### **BEFORE (Legacy cruft):**

```python
def create_sections(self) -> None:
    """Legacy-style: Create sections with single-row layout for sections 4,5,6"""
    # Legacy-style: Create transparent horizontal container for sections 4, 5, 6
    # Legacy approach: no finalization needed, QVBoxLayout just works!
```

### **AFTER (Clean V2):**

```python
def create_sections(self) -> None:
    """Create responsive section layout for option picker components."""
    # Implementation with modern responsive design patterns
```

---

## **Files to Clean**

### **1. arrow_management_service.py** - Remove Legacy positioning comments

**Find and Replace Patterns:**

```python
# REMOVE THESE PATTERNS:
# Legacy-style: Create sections with single-row layout for sections 4,5,6
# Legacy-style: Create transparent horizontal container for sections 4, 5, 6
# Legacy approach: no finalization needed, QVBoxLayout just works!

# REPLACE WITH:
# Create responsive section layout for option picker components
# Modern container management with proper lifecycle
# Responsive layout that adapts to content
```

**Specific Changes:**

```python
# BEFORE:
def create_sections(self) -> None:
    """Legacy-style: Create sections with single-row layout for sections 4,5,6"""
    # Legacy-style: Create transparent horizontal container for sections 4, 5, 6
    self.sections = {}
    # Legacy approach: no finalization needed, QVBoxLayout just works!

# AFTER:
def create_sections(self) -> None:
    """Create responsive section layout for option picker components."""
    # Initialize section containers with modern layout management
    self.sections = {}
    # Modern approach: explicit lifecycle management for optimal performance
```

### **2. motion_management_service.py** - Remove Legacy algorithm references

**Find and Replace Patterns:**

```python
# REMOVE:
# Using DIAMOND layer2 points from circle_coords.json (old working service)
# Hand point coordinates (for STATIC/DASH arrows) - inner grid positions where props are placed

# REPLACE WITH:
# Using optimized coordinate system from circle_coords.json
# Prop placement coordinates for arrow positioning system
```

**Specific Changes:**

```python
# BEFORE:
def get_diamond_coordinates(self):
    """Get diamond coordinates from old working service."""
    # Using DIAMOND layer2 points from circle_coords.json (old working service)
    return self.coordinate_service.get_diamond_layer2()

# AFTER:
def get_diamond_coordinates(self):
    """Get optimized diamond coordinates for prop positioning."""
    # Using validated coordinate system from circle_coords.json
    return self.coordinate_service.get_diamond_layer2()
```

### **3. sequence_management_service.py** - Clean up Legacy compatibility paths

**Find and Replace Patterns:**

```python
# REMOVE:
# Legacy compatibility path for legacy sequences
# TODO: Remove Legacy compatibility after migration complete

# REPLACE WITH:
# Standard sequence processing path
# Validated sequence handling workflow
```

**Specific Changes:**

```python
# BEFORE:
def process_sequence(self, sequence_data):
    """Process sequence with Legacy compatibility."""
    # Legacy compatibility path for legacy sequences
    if hasattr(sequence_data, 'legacy_format'):
        return self._process_legacy_sequence(sequence_data)
    # TODO: Remove Legacy compatibility after migration complete
    return self._process_v2_sequence(sequence_data)

# AFTER:
def process_sequence(self, sequence_data):
    """Process sequence with validated data structures."""
    # Standard sequence processing with modern validation
    return self._process_sequence(sequence_data)
```

### **4. All services in positioning/, motion/, core/ directories**

**Systematic Cleanup Pattern:**

```python
# FOR EACH FILE, REPLACE:

# Old pattern documentation
"""Legacy-style: [description]"""
# New pattern documentation
"""[Clean description without Legacy reference]"""

# Old implementation comments
# Legacy approach: [explanation]
# Modern approach: [explanation]

# Old working service references
# old working service
# validated service implementation

# Legacy compatibility notes
# Legacy compatibility [note]
# Standard implementation [note]
```

---

## **Specific File Changes**

### **arrow_management_service.py**

```python
# Lines to change (approximate):
# Line 45: Remove "Legacy-style:" from docstring
# Line 67: Remove "Legacy approach:" comment
# Line 89: Replace with modern explanation
# Line 123: Update "old working service" reference
```

### **motion_management_service.py**

```python
# Lines to change (approximate):
# Line 23: Update coordinate system comment
# Line 156: Modernize hand point coordinate comment
# Line 189: Remove Legacy algorithm reference
# Line 245: Clean up legacy compatibility note
```

### **sequence_management_service.py**

```python
# Lines to change (approximate):
# Line 78: Remove Legacy compatibility path
# Line 134: Update TODO comment to be actionable
# Line 234: Remove migration reference
# Line 278: Modernize sequence handling comment
```

---

## **Validation Process**

After each file cleanup:

### **1. Syntax Validation**

```bash
# Check Python syntax
python -m py_compile src/application/services/motion/arrow_management_service.py

# Check imports work
python -c "from src.application.services.motion.arrow_management_service import ArrowManagementService"
```

### **2. Functionality Validation**

```bash
# Run existing tests
python -m pytest tests/application/services/test_arrow_management_service.py -v

# Check service can be instantiated
python -c "
from src.core.dependency_injection.di_container import DIContainer
container = DIContainer()
# Validate service works
"
```

### **3. Reference Validation**

```bash
# Verify no Legacy references remain in cleaned files
grep -n "Legacy\|legacy\|old\|legacy" src/application/services/motion/arrow_management_service.py

# Should return zero results after cleanup
```

---

## **Post-Cleanup Verification**

After cleaning all files, run this comprehensive check:

```bash
# After cleanup, this should return zero results:
grep -r "Legacy\|legacy\|old\|legacy" src/application/services/ --include="*.py"

# Verify specific patterns are gone:
grep -r "Legacy-style\|legacy-style" src/application/services/ --include="*.py"
grep -r "Legacy approach\|legacy approach" src/application/services/ --include="*.py"
grep -r "old working service" src/application/services/ --include="*.py"
```

**Expected Result**: All commands should return **zero matches**.

---

## **Quality Checks**

### **Before Proceeding to Task 1.3**

1. ✅ **All Legacy references removed** from service files
2. ✅ **All services compile** without syntax errors
3. ✅ **Existing tests pass** after cleanup
4. ✅ **No functionality regression** observed
5. ✅ **Code is more readable** without Legacy cruft

---

## **Common Pitfalls to Avoid**

### **❌ Don't Do This:**

- Remove comments that explain **why** something is done a certain way
- Delete functional code that happens to mention Legacy
- Change variable names that work fine (unless they're confusing)

### **✅ Do This:**

- Remove references to **Legacy implementation approaches**
- Clean up **Legacy-style documentation**
- Replace **Legacy compatibility paths** with standard implementations
- Update **TODO comments** to be actionable or remove them

---

## **Next Step**

After completing Legacy cleanup, proceed to: [Task 1.3: Complete Auto-Injection Implementation](04_di_container_enhancement.md)
