# **Task 1.2: Clean V1 References**

**Timeline**: Day 1-2  
**Priority**: CRITICAL  
**Goal**: Remove all V1 compatibility code and replace with clean V2 patterns

---

## **Action Plan:**

### **BEFORE (V1 cruft):**

```python
def create_sections(self) -> None:
    """V1-style: Create sections with single-row layout for sections 4,5,6"""
    # V1-style: Create transparent horizontal container for sections 4, 5, 6
    # V1 approach: no finalization needed, QVBoxLayout just works!
```

### **AFTER (Clean V2):**

```python
def create_sections(self) -> None:
    """Create responsive section layout for option picker components."""
    # Implementation with modern responsive design patterns
```

---

## **Files to Clean**

### **1. arrow_management_service.py** - Remove V1 positioning comments

**Find and Replace Patterns:**

```python
# REMOVE THESE PATTERNS:
# V1-style: Create sections with single-row layout for sections 4,5,6
# V1-style: Create transparent horizontal container for sections 4, 5, 6
# V1 approach: no finalization needed, QVBoxLayout just works!

# REPLACE WITH:
# Create responsive section layout for option picker components
# Modern container management with proper lifecycle
# Responsive layout that adapts to content
```

**Specific Changes:**

```python
# BEFORE:
def create_sections(self) -> None:
    """V1-style: Create sections with single-row layout for sections 4,5,6"""
    # V1-style: Create transparent horizontal container for sections 4, 5, 6
    self.sections = {}
    # V1 approach: no finalization needed, QVBoxLayout just works!

# AFTER:
def create_sections(self) -> None:
    """Create responsive section layout for option picker components."""
    # Initialize section containers with modern layout management
    self.sections = {}
    # Modern approach: explicit lifecycle management for optimal performance
```

### **2. motion_management_service.py** - Remove V1 algorithm references

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

### **3. sequence_management_service.py** - Clean up V1 compatibility paths

**Find and Replace Patterns:**

```python
# REMOVE:
# V1 compatibility path for legacy sequences
# TODO: Remove V1 compatibility after migration complete

# REPLACE WITH:
# Standard sequence processing path
# Validated sequence handling workflow
```

**Specific Changes:**

```python
# BEFORE:
def process_sequence(self, sequence_data):
    """Process sequence with V1 compatibility."""
    # V1 compatibility path for legacy sequences
    if hasattr(sequence_data, 'v1_format'):
        return self._process_v1_sequence(sequence_data)
    # TODO: Remove V1 compatibility after migration complete
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
"""V1-style: [description]"""
# New pattern documentation
"""[Clean description without V1 reference]"""

# Old implementation comments
# V1 approach: [explanation]
# Modern approach: [explanation]

# Old working service references
# old working service
# validated service implementation

# Legacy compatibility notes
# V1 compatibility [note]
# Standard implementation [note]
```

---

## **Specific File Changes**

### **arrow_management_service.py**

```python
# Lines to change (approximate):
# Line 45: Remove "V1-style:" from docstring
# Line 67: Remove "V1 approach:" comment
# Line 89: Replace with modern explanation
# Line 123: Update "old working service" reference
```

### **motion_management_service.py**

```python
# Lines to change (approximate):
# Line 23: Update coordinate system comment
# Line 156: Modernize hand point coordinate comment
# Line 189: Remove V1 algorithm reference
# Line 245: Clean up legacy compatibility note
```

### **sequence_management_service.py**

```python
# Lines to change (approximate):
# Line 78: Remove V1 compatibility path
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
# Verify no V1 references remain in cleaned files
grep -n "V1\|v1\|old\|legacy" src/application/services/motion/arrow_management_service.py

# Should return zero results after cleanup
```

---

## **Post-Cleanup Verification**

After cleaning all files, run this comprehensive check:

```bash
# After cleanup, this should return zero results:
grep -r "V1\|v1\|old\|legacy" src/application/services/ --include="*.py"

# Verify specific patterns are gone:
grep -r "V1-style\|v1-style" src/application/services/ --include="*.py"
grep -r "V1 approach\|v1 approach" src/application/services/ --include="*.py"
grep -r "old working service" src/application/services/ --include="*.py"
```

**Expected Result**: All commands should return **zero matches**.

---

## **Quality Checks**

### **Before Proceeding to Task 1.3**

1. ✅ **All V1 references removed** from service files
2. ✅ **All services compile** without syntax errors
3. ✅ **Existing tests pass** after cleanup
4. ✅ **No functionality regression** observed
5. ✅ **Code is more readable** without V1 cruft

---

## **Common Pitfalls to Avoid**

### **❌ Don't Do This:**

- Remove comments that explain **why** something is done a certain way
- Delete functional code that happens to mention V1
- Change variable names that work fine (unless they're confusing)

### **✅ Do This:**

- Remove references to **V1 implementation approaches**
- Clean up **V1-style documentation**
- Replace **V1 compatibility paths** with standard implementations
- Update **TODO comments** to be actionable or remove them

---

## **Next Step**

After completing V1 cleanup, proceed to: [Task 1.3: Complete Auto-Injection Implementation](04_di_container_enhancement.md)
