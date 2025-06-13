# Troubleshooting Guide - V1 Motion Generation in V2

## 🚨 Common Issues and Solutions

### Issue 1: "V1 dataset not found" Error

**Symptoms:**
```
FileNotFoundError: V1 dataset not found: v1/data/diamond.json
```

**Causes:**
- V1 dataset file doesn't exist
- Incorrect path to V1 directory
- File permissions issue

**Solutions:**
```python
# Check if V1 directory exists
import os
v1_path = "v1/data/diamond.json"
if not os.path.exists(v1_path):
    print(f"❌ File not found: {v1_path}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir('.')}")

# Try alternative paths
alternative_paths = [
    "v1/data/diamond.json",
    "../v1/data/diamond.json", 
    "../../v1/data/diamond.json",
    "the-kinetic-constructor-desktop/v1/data/diamond.json"
]

for path in alternative_paths:
    if os.path.exists(path):
        print(f"✅ Found dataset at: {path}")
        break
```

**Fix:**
```python
# Update V1DatasetLoader with correct path
class V1DatasetLoader:
    def __init__(self, v1_root_path: str = "../../v1"):  # Adjust path
        self.v1_root_path = Path(v1_root_path)
```

---

### Issue 2: "No options found for alpha1" Error

**Symptoms:**
```
🎯 Alpha 1 found 0 options
❌ No options found for position: alpha1
```

**Causes:**
- Dataset doesn't contain alpha1 start position
- Position string mismatch (case sensitivity)
- Dataset structure different than expected

**Debugging:**
```python
def debug_dataset_positions():
    """Debug available positions in dataset"""
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    all_start_positions = set()
    all_end_positions = set()
    
    for letter, pictographs in dataset.items():
        for pictograph in pictographs:
            start_pos = pictograph.get("start_pos")
            end_pos = pictograph.get("end_pos")
            if start_pos:
                all_start_positions.add(start_pos)
            if end_pos:
                all_end_positions.add(end_pos)
    
    print(f"Available start positions: {sorted(all_start_positions)}")
    print(f"Available end positions: {sorted(all_end_positions)}")
    
    # Check for alpha1 variations
    alpha_positions = [pos for pos in all_start_positions if "alpha" in pos.lower()]
    print(f"Alpha positions: {alpha_positions}")
```

**Solutions:**
- Use correct position string (check actual dataset)
- Try alternative position names: "Alpha1", "ALPHA1", "alpha_1"
- Use a known working position for testing

---

### Issue 3: "Conversion failed" Errors

**Symptoms:**
```
❌ Conversion failed: 'NoneType' object has no attribute 'get'
❌ Failed to convert option: KeyError: 'motion_type'
```

**Causes:**
- Missing required fields in V1 data
- Unexpected data structure
- Enum mapping failures

**Debugging:**
```python
def debug_v1_data_structure():
    """Debug V1 data structure"""
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    # Examine first few entries
    for letter, pictographs in list(dataset.items())[:3]:
        print(f"\nLetter: {letter}")
        for i, pictograph in enumerate(pictographs[:2]):
            print(f"  Pictograph {i}: {pictograph}")
            
            # Check required fields
            required_fields = ["letter", "start_pos", "end_pos", "blue_attributes", "red_attributes"]
            for field in required_fields:
                if field not in pictograph:
                    print(f"    ❌ Missing field: {field}")
                else:
                    print(f"    ✅ Has field: {field}")
```

**Solutions:**
```python
# Add defensive programming to conversion
def _convert_motion_attributes(self, v1_attrs: dict) -> MotionData:
    if not v1_attrs:
        v1_attrs = {}
    
    # Provide defaults for missing fields
    motion_type = self.MOTION_TYPE_MAP.get(
        v1_attrs.get("motion_type", "static"), 
        MotionType.STATIC
    )
    
    # Handle missing or invalid values gracefully
    try:
        return MotionData(
            motion_type=motion_type,
            prop_rot_dir=self.ROTATION_DIR_MAP.get(v1_attrs.get("prop_rot_dir", "no_rot"), RotationDirection.NO_ROTATION),
            start_loc=self.LOCATION_MAP.get(v1_attrs.get("start_loc", "n"), Location.NORTH),
            end_loc=self.LOCATION_MAP.get(v1_attrs.get("end_loc", "n"), Location.NORTH),
            start_ori=v1_attrs.get("start_ori", "in"),
            end_ori=v1_attrs.get("end_ori", "in")
        )
    except Exception as e:
        print(f"❌ Motion conversion error: {e}")
        print(f"   Data: {v1_attrs}")
        raise
```

---

### Issue 4: "Qt object deleted" Errors

**Symptoms:**
```
RuntimeError: wrapped C/C++ object of type ClickablePictographFrame has been deleted
```

**Causes:**
- Calling deleteLater() on pictograph objects
- Parent-child relationship issues
- Object lifecycle management problems

**Solutions:**
```python
# V1-style clear (NO DELETION)
def clear_pictographs_v1_style(self):
    """V1-style clear: hide and remove from layout, DON'T delete"""
    for pictograph in self.pictographs:
        if pictograph is not None:
            try:
                # Remove from layout but don't delete
                if hasattr(self, 'pictograph_layout') and self.pictograph_layout:
                    self.pictograph_layout.removeWidget(pictograph)
                
                # Hide the widget
                pictograph.setVisible(False)
                
                # DO NOT call deleteLater() - this is the key!
                # pictograph.deleteLater()  # ← NEVER DO THIS
                
            except RuntimeError as e:
                print(f"⚠️ Widget already deleted: {e}")
    
    self.pictographs.clear()

# Object pooling approach
class PictographPool:
    def __init__(self, max_size=36):
        self.pool = []
        self.available = []
        self.in_use = []
        
        # Pre-create objects
        for i in range(max_size):
            frame = ClickablePictographFrame(dummy_data)
            frame.setVisible(False)
            self.pool.append(frame)
            self.available.append(frame)
    
    def get_frame(self):
        if self.available:
            frame = self.available.pop()
            self.in_use.append(frame)
            return frame
        return None
    
    def return_frame(self, frame):
        if frame in self.in_use:
            self.in_use.remove(frame)
            self.available.append(frame)
            frame.setVisible(False)
```

---

### Issue 5: "Section not found" Errors

**Symptoms:**
```
❌ No section found for Letter D (type: Type1)
```

**Causes:**
- Section not initialized in option picker
- Letter type classification mismatch
- Section dictionary key mismatch

**Debugging:**
```python
def debug_sections():
    """Debug section availability"""
    # Check available sections
    print(f"Available sections: {list(self._sections.keys())}")
    
    # Check letter type classification
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    test_letters = ["A", "D", "W", "X", "Φ", "α"]
    
    for letter in test_letters:
        letter_type = LetterTypeClassifier.get_letter_type(letter)
        section_exists = letter_type in self._sections
        print(f"Letter {letter} → {letter_type} → Section exists: {section_exists}")
```

**Solutions:**
```python
# Ensure all sections are initialized
def _initialize_sections(self):
    """Initialize all required sections"""
    required_sections = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]
    
    for section_type in required_sections:
        if section_type not in self._sections:
            section = OptionPickerSection(section_type, self)
            self._sections[section_type] = section
            print(f"✅ Initialized section: {section_type}")

# Fallback section assignment
def _assign_to_section_with_fallback(self, option, letter_type):
    """Assign to section with fallback to Type1"""
    if letter_type in self._sections:
        section = self._sections[letter_type]
    else:
        print(f"⚠️ Section {letter_type} not found, using Type1 fallback")
        section = self._sections.get("Type1")
    
    if section:
        frame = self._create_frame(option, section)
        section.add_pictograph_from_pool(frame)
        return True
    
    print(f"❌ No section available for {option.letter}")
    return False
```

---

### Issue 6: Performance Issues

**Symptoms:**
- Slow option loading (>1 second)
- High memory usage
- UI freezing during operations

**Causes:**
- Inefficient dataset queries
- Creating too many objects
- Synchronous operations blocking UI

**Solutions:**
```python
# Optimize position matching
class OptimizedPositionMatchingService:
    def __init__(self, pictograph_dataset: dict):
        self.pictograph_dataset = pictograph_dataset
        self._build_position_index()
    
    def _build_position_index(self):
        """Build index for fast position lookups"""
        self.position_index = {}
        
        for letter, pictographs in self.pictograph_dataset.items():
            for pictograph in pictographs:
                start_pos = pictograph.get("start_pos")
                if start_pos:
                    if start_pos not in self.position_index:
                        self.position_index[start_pos] = []
                    self.position_index[start_pos].append(pictograph)
        
        print(f"✅ Built position index: {len(self.position_index)} positions")
    
    def get_next_options(self, last_beat_end_pos: str) -> list[dict]:
        """Fast position lookup using index"""
        return self.position_index.get(last_beat_end_pos, [])

# Async loading for large datasets
import asyncio

async def load_options_async(self, end_position: str):
    """Load options asynchronously"""
    loop = asyncio.get_event_loop()
    
    # Run position matching in thread pool
    options = await loop.run_in_executor(
        None, 
        self.position_matching_service.get_next_options, 
        end_position
    )
    
    # Update UI on main thread
    self._populate_sections_v1_style(options)
```

---

### Issue 7: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'v2.src.domain.models.letter_type_classifier'
ImportError: cannot import name 'MotionType' from 'v2.src.domain.models.core_models'
```

**Causes:**
- Incorrect import paths
- Missing __init__.py files
- Circular imports

**Solutions:**
```python
# Add __init__.py files to all directories
# v2/src/__init__.py
# v2/src/domain/__init__.py
# v2/src/domain/models/__init__.py
# v2/src/application/__init__.py
# v2/src/application/services/__init__.py

# Use relative imports within packages
from .letter_type_classifier import LetterTypeClassifier
from ..models.core_models import BeatData, MotionData

# Use absolute imports from outside
import sys
sys.path.append('v2/src')
from domain.models.letter_type_classifier import LetterTypeClassifier
```

---

## 🔧 Debugging Tools

### Dataset Inspector
```python
def inspect_v1_dataset():
    """Comprehensive dataset inspection"""
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    print(f"📊 Dataset Overview:")
    print(f"   Total letters: {len(dataset)}")
    print(f"   Total pictographs: {sum(len(group) for group in dataset.values())}")
    
    # Sample data structure
    first_letter = list(dataset.keys())[0]
    first_pictograph = dataset[first_letter][0]
    print(f"\n📋 Sample Data Structure (Letter {first_letter}):")
    for key, value in first_pictograph.items():
        print(f"   {key}: {value}")
    
    # Position analysis
    all_positions = set()
    for pictographs in dataset.values():
        for pictograph in pictographs:
            all_positions.add(pictograph.get("start_pos"))
            all_positions.add(pictograph.get("end_pos"))
    
    print(f"\n📍 Available Positions: {sorted(all_positions)}")
```

### Performance Profiler
```python
import time
import tracemalloc

def profile_motion_generation():
    """Profile motion generation performance"""
    tracemalloc.start()
    
    start_time = time.time()
    
    # Your motion generation code here
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    service = PositionMatchingService(dataset)
    options = service.get_next_options("alpha1")
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"⏱️ Performance Profile:")
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Memory: {current / 1024 / 1024:.1f} MB current, {peak / 1024 / 1024:.1f} MB peak")
    print(f"   Options: {len(options)}")
```

## 🎯 Quick Fixes Checklist

When things go wrong, try these in order:

1. **Check file paths** - Verify V1 dataset location
2. **Inspect dataset** - Use dataset inspector tool
3. **Test with known data** - Use hardcoded test data first
4. **Check imports** - Verify all modules can be imported
5. **Add defensive programming** - Handle None values and missing fields
6. **Use object pooling** - Avoid Qt object deletion issues
7. **Profile performance** - Identify bottlenecks
8. **Check logs** - Look for error messages and warnings

Most issues stem from incorrect paths, missing data, or Qt object lifecycle problems. The V1 patterns provide the proven solution! 🔧
