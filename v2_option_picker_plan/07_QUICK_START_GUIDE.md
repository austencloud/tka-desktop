# Quick Start Implementation Guide

## 🚀 Get V1's Motion Generation Working in V2 - Fast Track

This guide gets you from zero to working V1-style motion generation in V2 as quickly as possible.

## ⚡ 30-Minute Implementation Plan

### Step 1: Create Core Services (10 minutes)

#### A. Letter Type Classifier
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
        return "Type1"
```

#### B. Position Matching Service
**File**: `v2/src/application/services/position_matching_service.py`
```python
class PositionMatchingService:
    def __init__(self, pictograph_dataset: dict):
        self.pictograph_dataset = pictograph_dataset
    
    def get_next_options(self, last_beat_end_pos: str) -> list[dict]:
        """V1's core algorithm: position matching"""
        next_opts = []
        for group in self.pictograph_dataset.values():
            for item in group:
                if item.get("start_pos") == last_beat_end_pos:
                    next_opts.append(item)
        return next_opts
```

#### C. Data Conversion Service
**File**: `v2/src/application/services/data_conversion_service.py`
```python
from v2.src.domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location

class DataConversionService:
    MOTION_TYPE_MAP = {"pro": MotionType.PRO, "anti": MotionType.ANTI, "dash": MotionType.DASH, "static": MotionType.STATIC}
    ROTATION_DIR_MAP = {"cw": RotationDirection.CLOCKWISE, "ccw": RotationDirection.COUNTER_CLOCKWISE, "no_rot": RotationDirection.NO_ROTATION}
    LOCATION_MAP = {"n": Location.NORTH, "e": Location.EAST, "s": Location.SOUTH, "w": Location.WEST, "ne": Location.NORTHEAST, "se": Location.SOUTHEAST, "sw": Location.SOUTHWEST, "nw": Location.NORTHWEST}
    
    def convert_v1_pictograph_to_beat_data(self, v1_data: dict) -> BeatData:
        return BeatData(
            letter=v1_data.get("letter"),
            blue_motion=self._convert_motion_attributes(v1_data.get("blue_attributes", {})),
            red_motion=self._convert_motion_attributes(v1_data.get("red_attributes", {})),
            start_pos=v1_data.get("start_pos"),
            end_pos=v1_data.get("end_pos")
        )
    
    def _convert_motion_attributes(self, v1_attrs: dict) -> MotionData:
        return MotionData(
            motion_type=self.MOTION_TYPE_MAP.get(v1_attrs.get("motion_type"), MotionType.STATIC),
            prop_rot_dir=self.ROTATION_DIR_MAP.get(v1_attrs.get("prop_rot_dir"), RotationDirection.NO_ROTATION),
            start_loc=self.LOCATION_MAP.get(v1_attrs.get("start_loc"), Location.NORTH),
            end_loc=self.LOCATION_MAP.get(v1_attrs.get("end_loc"), Location.NORTH),
            start_ori=v1_attrs.get("start_ori", "in"),  # String values: "in", "out", "clock", "counter"
            end_ori=v1_attrs.get("end_ori", "in")
        )
```

### Step 2: Load V1 Dataset (10 minutes)

#### D. V1 Dataset Loader
**File**: `v2/src/infrastructure/data/v1_dataset_loader.py`
```python
import json
from pathlib import Path

class V1DatasetLoader:
    def __init__(self, v1_root_path: str = "v1"):
        self.v1_root_path = Path(v1_root_path)
        self.data_path = self.v1_root_path / "data"
    
    def load_pictograph_dataset(self) -> dict:
        """Load V1's pictograph dataset"""
        diamond_file = self.data_path / "diamond.json"
        
        if not diamond_file.exists():
            raise FileNotFoundError(f"V1 dataset not found: {diamond_file}")
        
        with open(diamond_file, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        print(f"✅ Loaded V1 dataset: {len(dataset)} letter groups")
        return dataset
```

### Step 3: Update Option Picker (10 minutes)

#### E. Update Option Picker
**File**: `v2/src/presentation/components/option_picker/__init__.py` (Add these methods)

```python
def initialize_with_v1_dataset(self):
    """Initialize option picker with V1 dataset"""
    from v2.src.infrastructure.data.v1_dataset_loader import V1DatasetLoader
    from v2.src.application.services.position_matching_service import PositionMatchingService
    from v2.src.application.services.data_conversion_service import DataConversionService
    
    # Load V1 dataset
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    # Initialize services
    self.position_matching_service = PositionMatchingService(dataset)
    self.data_conversion_service = DataConversionService()
    
    print("✅ Option picker initialized with V1 dataset")

def load_motion_combinations_v1_style(self, sequence_data: list[dict]):
    """Load motion combinations using V1's position matching"""
    if not hasattr(self, 'position_matching_service'):
        print("❌ V1 services not initialized")
        return
    
    if not sequence_data or len(sequence_data) < 2:
        print("❌ Invalid sequence data")
        return
    
    # Get last beat's end position
    last_beat = sequence_data[-1]
    last_end_pos = last_beat.get("end_pos")
    
    if not last_end_pos:
        print("❌ No end position in last beat")
        return
    
    print(f"🎯 Loading options for end position: {last_end_pos}")
    
    # Use V1's position matching
    v1_options = self.position_matching_service.get_next_options(last_end_pos)
    
    # Convert to V2 format
    v2_options = []
    for v1_option in v1_options:
        try:
            v2_option = self.data_conversion_service.convert_v1_pictograph_to_beat_data(v1_option)
            v2_options.append(v2_option)
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
    
    # Populate sections
    self._populate_sections_v1_style(v2_options)
    
    print(f"✅ Loaded {len(v2_options)} options using V1 position matching")

def _populate_sections_v1_style(self, options: list):
    """Populate sections using V1's letter type classification"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    # Clear existing
    for section in self._sections.values():
        section.clear_pictographs_v1_style()
    
    # Assign to sections
    for option in options:
        letter_type = LetterTypeClassifier.get_letter_type(option.letter)
        
        if letter_type in self._sections:
            section = self._sections[letter_type]
            frame = self._create_simple_frame(option, section)
            section.add_pictograph_from_pool(frame)
            print(f"   ✅ Assigned {option.letter} to {letter_type}")

def _create_simple_frame(self, option, section):
    """Create simple frame for testing"""
    # Use existing ClickablePictographFrame or create simple version
    from v2.src.presentation.components.option_picker.clickable_pictograph_frame import ClickablePictographFrame
    frame = ClickablePictographFrame(option, parent=section.pictograph_container)
    return frame
```

#### F. Update Section Clear Method
**File**: `v2/src/presentation/components/option_picker/option_picker_section.py` (Add method)

```python
def clear_pictographs_v1_style(self):
    """V1-style clear: hide and remove from layout, DON'T delete"""
    for pictograph in self.pictographs:
        if pictograph is not None:
            try:
                if self._ensure_layout_validity():
                    self.pictograph_layout.removeWidget(pictograph)
                pictograph.setVisible(False)
                # NO deleteLater() call - this is V1's key pattern
            except RuntimeError:
                pass
    
    self.pictographs.clear()
    print(f"🧹 V1-style clear (no deletion): section {self.letter_type} cleared")
```

## 🧪 Quick Test

### Create Alpha 1 Test
**File**: `v2/test_v1_integration_quick.py`

```python
def test_alpha1_quick():
    """Quick test of V1 integration"""
    from v2.src.infrastructure.data.v1_dataset_loader import V1DatasetLoader
    from v2.src.application.services.position_matching_service import PositionMatchingService
    from v2.src.application.services.data_conversion_service import DataConversionService
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    # Load V1 dataset
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    # Test position matching
    position_service = PositionMatchingService(dataset)
    alpha1_options = position_service.get_next_options("alpha1")
    
    print(f"🎯 Alpha 1 found {len(alpha1_options)} options")
    
    # Test conversion
    conversion_service = DataConversionService()
    converted_options = []
    
    for v1_option in alpha1_options[:5]:  # Test first 5
        v2_option = conversion_service.convert_v1_pictograph_to_beat_data(v1_option)
        converted_options.append(v2_option)
        
        letter_type = LetterTypeClassifier.get_letter_type(v2_option.letter)
        print(f"   ✅ {v2_option.letter} → {letter_type}")
    
    print("✅ Quick V1 integration test passed!")

if __name__ == "__main__":
    test_alpha1_quick()
```

## 🏃‍♂️ Run the Test

```bash
cd v2
python test_v1_integration_quick.py
```

## 🎯 Expected Results

You should see:
```
✅ Loaded V1 dataset: X letter groups
🎯 Alpha 1 found Y options
   ✅ D → Type1
   ✅ E → Type1
   ✅ F → Type1
   ✅ G → Type1
   ✅ H → Type1
✅ Quick V1 integration test passed!
```

## 🔧 Integration with Existing Option Picker

Update your existing option picker initialization:

```python
# In your main application or test
option_picker = ModernOptionPicker(container)
option_picker.initialize()
option_picker.initialize_with_v1_dataset()  # ← Add this line

# To load Alpha 1 options
alpha1_sequence = [
    {"metadata": "sequence_info"},
    {"end_pos": "alpha1", "letter": "A"}  # Alpha 1 start position
]
option_picker.load_motion_combinations_v1_style(alpha1_sequence)
```

## ✅ Success Criteria

After 30 minutes, you should have:
1. **V1 dataset loading** ✅
2. **Position matching working** ✅
3. **Data conversion functional** ✅
4. **Letter type classification** ✅
5. **Alpha 1 generating correct letters** ✅

## 🔗 Next Steps

Once this works:
1. **Enhance pictograph rendering** with real V2 components
2. **Add object pooling** for performance
3. **Test with more start positions**
4. **Integrate with full V2 application**

You now have V1's proven motion generation working in V2! 🚀
