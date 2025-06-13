# V2 Motion Generation Implementation Plan

## 🎯 Objective
Implement V1's data-driven motion generation system in V2 to achieve pixel-perfect functional parity with V1's option picker.

## 📋 Implementation Strategy

### Phase 1: Core Algorithm Implementation (Priority 1)
### Phase 2: Dataset Integration (Priority 2)  
### Phase 3: Object Pooling Optimization (Priority 3)
### Phase 4: Testing & Validation (Priority 4)

---

## 🚀 Phase 1: Core Algorithm Implementation

### Step 1.1: Create Position Matching Service
**File**: `v2/src/application/services/position_matching_service.py`

```python
class PositionMatchingService:
    def __init__(self, pictograph_dataset: dict):
        self.pictograph_dataset = pictograph_dataset
    
    def get_next_options(self, last_beat_end_pos: str) -> List[dict]:
        """V1's core algorithm: find all pictographs where start_pos matches"""
        next_opts = []
        for group in self.pictograph_dataset.values():
            for item in group:
                if item.get('start_pos') == last_beat_end_pos:
                    next_opts.append(item)
        return next_opts
```

### Step 1.2: Implement V1's Letter Type Classification
**File**: `v2/src/domain/models/letter_type_classifier.py`

```python
class LetterTypeClassifier:
    TYPE1_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
                     "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
    TYPE2_LETTERS = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
    TYPE3_LETTERS = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]
    TYPE4_LETTERS = ["Φ", "Ψ", "Λ"]
    TYPE5_LETTERS = ["Φ-", "Ψ-", "Λ-"]
    TYPE6_LETTERS = ["α", "β", "Γ"]
    
    @classmethod
    def get_letter_type(cls, letter: str) -> str:
        if letter in cls.TYPE1_LETTERS: return "Type1"
        elif letter in cls.TYPE2_LETTERS: return "Type2"
        elif letter in cls.TYPE3_LETTERS: return "Type3"
        elif letter in cls.TYPE4_LETTERS: return "Type4"
        elif letter in cls.TYPE5_LETTERS: return "Type5"
        elif letter in cls.TYPE6_LETTERS: return "Type6"
        return "Type1"  # Default fallback
```

### Step 1.3: Update Option Picker to Use Position Matching
**File**: `v2/src/presentation/components/option_picker/__init__.py`

Replace the current `_update_beat_display()` method:

```python
def _update_beat_display(self) -> None:
    """V1-style motion generation using position matching"""
    # Clear existing pictographs
    for section in self._sections.values():
        section.clear_pictographs_v1_style()
    
    # Get last beat's end position
    if not self._beat_options or len(self._beat_options) == 0:
        return
    
    # For start position, use the end_pos as the constraint
    last_beat = self._beat_options[0]  # Assuming first is start position
    last_end_pos = last_beat.end_pos if hasattr(last_beat, 'end_pos') else None
    
    if not last_end_pos:
        print("❌ No end position found in last beat")
        return
    
    # Use position matching service to get next options
    next_options = self.position_matching_service.get_next_options(last_end_pos)
    
    # Convert to BeatData and assign to sections
    for option_data in next_options:
        beat_data = self._convert_v1_data_to_beat_data(option_data)
        letter_type = LetterTypeClassifier.get_letter_type(beat_data.letter)
        
        if letter_type in self._sections:
            section = self._sections[letter_type]
            frame = self._get_or_create_pictograph_frame(beat_data, section)
            section.add_pictograph_from_pool(frame)
```

---

## 🗂️ Phase 2: Dataset Integration

### Step 2.1: Create V1 Dataset Loader
**File**: `v2/src/infrastructure/data/v1_dataset_loader.py`

```python
class V1DatasetLoader:
    def __init__(self, v1_data_path: str = "v1/data"):
        self.v1_data_path = v1_data_path
    
    def load_pictograph_dataset(self) -> dict:
        """Load V1's pictograph dataset"""
        # Implementation to load V1's diamond.json or equivalent
        # Return format: {letter: [pictograph_data_list]}
        pass
    
    def convert_to_v2_format(self, v1_data: dict) -> List[BeatData]:
        """Convert V1 pictograph data to V2 BeatData format"""
        pass
```

### Step 2.2: Create Data Conversion Service
**File**: `v2/src/application/services/data_conversion_service.py`

```python
class DataConversionService:
    def convert_v1_pictograph_to_beat_data(self, v1_data: dict) -> BeatData:
        """Convert V1 pictograph data to V2 BeatData"""
        return BeatData(
            letter=v1_data.get('letter'),
            blue_motion=self._convert_motion_data(v1_data.get('blue_attributes')),
            red_motion=self._convert_motion_data(v1_data.get('red_attributes')),
            start_pos=v1_data.get('start_pos'),
            end_pos=v1_data.get('end_pos')
        )
    
    def _convert_motion_data(self, v1_attrs: dict) -> MotionData:
        """Convert V1 motion attributes to V2 MotionData"""
        return MotionData(
            motion_type=MotionType(v1_attrs.get('motion_type')),
            prop_rot_dir=RotationDirection(v1_attrs.get('prop_rot_dir')),
            start_loc=Location(v1_attrs.get('start_loc')),
            end_loc=Location(v1_attrs.get('end_loc')),
            start_ori=v1_attrs.get('start_ori'),
            end_ori=v1_attrs.get('end_ori')
        )
```

---

## 🏊 Phase 3: Object Pooling Optimization

### Step 3.1: Implement V1-Style Object Pool
**File**: `v2/src/presentation/components/option_picker/pictograph_pool.py`

```python
class PictographPool:
    MAX_PICTOGRAPHS = 36  # V1's pool size
    
    def __init__(self, parent_container):
        self.parent_container = parent_container
        self.pool = []
        self.available_indices = set(range(self.MAX_PICTOGRAPHS))
        self.used_indices = set()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Create pool of reusable pictograph frames"""
        for i in range(self.MAX_PICTOGRAPHS):
            frame = ClickablePictographFrame(
                dummy_beat_data, 
                parent=self.parent_container
            )
            frame.setVisible(False)
            self.pool.append(frame)
    
    def get_frame(self) -> ClickablePictographFrame:
        """Get available frame from pool"""
        if self.available_indices:
            index = self.available_indices.pop()
            self.used_indices.add(index)
            return self.pool[index]
        return None
    
    def return_frame(self, frame: ClickablePictographFrame):
        """Return frame to pool (V1-style hide, don't delete)"""
        frame.setVisible(False)
        # Find index and return to available pool
        index = self.pool.index(frame)
        if index in self.used_indices:
            self.used_indices.remove(index)
            self.available_indices.add(index)
```

---

## 🧪 Phase 4: Testing & Validation

### Step 4.1: Create Alpha 1 Test
**File**: `v2/test_alpha1_motion_generation.py`

```python
def test_alpha1_motion_generation():
    """Test that Alpha 1 generates identical results to V1"""
    # Load V1 dataset
    dataset_loader = V1DatasetLoader()
    dataset = dataset_loader.load_pictograph_dataset()
    
    # Create position matching service
    position_service = PositionMatchingService(dataset)
    
    # Test Alpha 1 (end_pos = "alpha1")
    alpha1_options = position_service.get_next_options("alpha1")
    
    # Verify expected letters
    expected_letters = ["A", "B", "C", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]  # Update based on V1 results
    actual_letters = [opt.get('letter') for opt in alpha1_options]
    
    assert set(actual_letters) == set(expected_letters), f"Expected {expected_letters}, got {actual_letters}"
    
    # Verify sectional assignment
    for letter in actual_letters:
        letter_type = LetterTypeClassifier.get_letter_type(letter)
        assert letter_type in ["Type1", "Type2"], f"Unexpected letter type for {letter}: {letter_type}"
    
    print("✅ Alpha 1 motion generation test passed!")
```

### Step 4.2: Integration Test
**File**: `v2/test_option_picker_integration.py`

```python
def test_option_picker_integration():
    """Test full option picker with V1 data"""
    # Create option picker with V1 dataset
    option_picker = ModernOptionPicker(container)
    option_picker.initialize_with_v1_dataset()
    
    # Simulate Alpha 1 selection
    alpha1_beat = create_alpha1_start_position()
    option_picker.load_motion_combinations([alpha1_beat])
    
    # Verify sections populated correctly
    assert len(option_picker._sections["Type1"]) > 0
    assert len(option_picker._sections["Type2"]) > 0
    
    print("✅ Option picker integration test passed!")
```

---

## 📊 Implementation Checklist

### Phase 1: Core Algorithm ✅
- [ ] Create PositionMatchingService
- [ ] Implement LetterTypeClassifier  
- [ ] Update option picker to use position matching
- [ ] Test with hardcoded Alpha 1 data

### Phase 2: Dataset Integration ✅
- [ ] Create V1DatasetLoader
- [ ] Implement DataConversionService
- [ ] Load actual V1 pictograph dataset
- [ ] Test data conversion accuracy

### Phase 3: Object Pooling ✅
- [ ] Implement PictographPool
- [ ] Update option picker to use pool
- [ ] Verify no Qt object deletion issues
- [ ] Performance testing

### Phase 4: Testing & Validation ✅
- [ ] Alpha 1 motion generation test
- [ ] Full option picker integration test
- [ ] Visual comparison with V1
- [ ] Performance benchmarking

---

## 🎯 Success Criteria

1. **Functional Parity**: Alpha 1 generates identical letters to V1
2. **Visual Parity**: Pictographs render identically to V1
3. **Performance Parity**: No slower than V1
4. **Stability**: No Qt object deletion cascade issues

## 🔗 Next Steps

1. **Start with Phase 1** - implement core position matching algorithm
2. **Test incrementally** - verify each step before proceeding
3. **Use Alpha 1 as benchmark** - it's the simplest test case
4. **Expand gradually** - add more start positions once Alpha 1 works

Ready to implement V1's proven data-driven approach! 🚀
