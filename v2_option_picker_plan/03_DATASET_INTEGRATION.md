# V1 Dataset Integration Guide

## 🎯 Objective

Integrate V1's pictograph dataset into V2 to enable data-driven motion generation using V1's proven dataset.

## 📊 V1 Dataset Structure Analysis

### V1 Dataset Location

```
v1/data/
├── diamond.json          # Main pictograph dataset
├── dictionary/           # Sequence data
└── other_data_files/     # Additional data
```

### V1 Pictograph Data Format

```python
# Example V1 pictograph entry
{
    "letter": "D",
    "start_pos": "alpha1",
    "end_pos": "beta2",
    "blue_attributes": {
        "motion_type": "pro",
        "prop_rot_dir": "cw",
        "start_loc": "n",
        "end_loc": "e",
        "start_ori": "in",
        "end_ori": "clock"
    },
    "red_attributes": {
        "motion_type": "pro",
        "prop_rot_dir": "ccw",
        "start_loc": "s",
        "end_loc": "w",
        "start_ori": "out",
        "end_ori": "counter"
    }
}
```

### V1 Dataset Organization

```python
# V1 dataset structure: {Letter: [pictograph_data_list]}
{
    "A": [pictograph_data_1, pictograph_data_2, ...],
    "B": [pictograph_data_1, pictograph_data_2, ...],
    "D": [pictograph_data_1, pictograph_data_2, ...],
    ...
}
```

## 🔧 Implementation Steps

### Step 1: Create V1 Dataset Loader

**File**: `v2/src/infrastructure/data/v1_dataset_loader.py`

```python
import json
from pathlib import Path
from typing import Dict, List, Any

class V1DatasetLoader:
    def __init__(self, v1_root_path: str = "v1"):
        self.v1_root_path = Path(v1_root_path)
        self.data_path = self.v1_root_path / "data"

    def load_pictograph_dataset(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load V1's main pictograph dataset"""
        diamond_file = self.data_path / "diamond.json"

        if not diamond_file.exists():
            raise FileNotFoundError(f"V1 dataset not found: {diamond_file}")

        with open(diamond_file, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        print(f"✅ Loaded V1 dataset: {len(dataset)} letter groups")

        # Log dataset statistics
        total_pictographs = sum(len(group) for group in dataset.values())
        print(f"📊 Total pictographs: {total_pictographs}")

        return dataset

    def get_dataset_statistics(self, dataset: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analyze V1 dataset structure"""
        stats = {
            "total_letters": len(dataset),
            "total_pictographs": sum(len(group) for group in dataset.values()),
            "letters_by_type": {},
            "start_positions": set(),
            "end_positions": set()
        }

        # Analyze by letter type
        from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier

        for letter, pictographs in dataset.items():
            letter_type = LetterTypeClassifier.get_letter_type(letter)
            if letter_type not in stats["letters_by_type"]:
                stats["letters_by_type"][letter_type] = []
            stats["letters_by_type"][letter_type].append(letter)

            # Collect position data
            for pictograph in pictographs:
                stats["start_positions"].add(pictograph.get("start_pos"))
                stats["end_positions"].add(pictograph.get("end_pos"))

        # Convert sets to sorted lists
        stats["start_positions"] = sorted(list(stats["start_positions"]))
        stats["end_positions"] = sorted(list(stats["end_positions"]))

        return stats
```

### Step 2: Create Data Conversion Service

**File**: `v2/src/application/services/data_conversion_service.py`

```python
from typing import Dict, Any
from v2.src.domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location

class DataConversionService:
    """Convert V1 pictograph data to V2 BeatData format"""

    # V1 to V2 mapping tables
    MOTION_TYPE_MAP = {
        "pro": MotionType.PRO,
        "anti": MotionType.ANTI,
        "float": MotionType.FLOAT,
        "dash": MotionType.DASH,
        "static": MotionType.STATIC,
    }

    ROTATION_DIR_MAP = {
        "cw": RotationDirection.CLOCKWISE,
        "ccw": RotationDirection.COUNTER_CLOCKWISE,
        "no_rot": RotationDirection.NO_ROTATION
    }

    LOCATION_MAP = {
        "n": Location.NORTH,
        "ne": Location.NORTHEAST,
        "e": Location.EAST,
        "se": Location.SOUTHEAST,
        "s": Location.SOUTH,
        "sw": Location.SOUTHWEST,
        "w": Location.WEST,
        "nw": Location.NORTHWEST
    }

    def convert_v1_pictograph_to_beat_data(self, v1_data: Dict[str, Any]) -> BeatData:
        """Convert single V1 pictograph to V2 BeatData"""
        try:
            blue_motion = self._convert_motion_attributes(v1_data.get("blue_attributes", {}))
            red_motion = self._convert_motion_attributes(v1_data.get("red_attributes", {}))

            return BeatData(
                letter=v1_data.get("letter"),
                blue_motion=blue_motion,
                red_motion=red_motion,
                start_pos=v1_data.get("start_pos"),
                end_pos=v1_data.get("end_pos")
            )
        except Exception as e:
            print(f"❌ Failed to convert V1 data: {e}")
            print(f"   Data: {v1_data}")
            raise

    def _convert_motion_attributes(self, v1_attrs: Dict[str, Any]) -> MotionData:
        """Convert V1 motion attributes to V2 MotionData"""
        motion_type = self.MOTION_TYPE_MAP.get(
            v1_attrs.get("motion_type"),
            MotionType.STATIC
        )

        prop_rot_dir = self.ROTATION_DIR_MAP.get(
            v1_attrs.get("prop_rot_dir"),
            RotationDirection.NO_ROTATION
        )

        start_loc = self.LOCATION_MAP.get(
            v1_attrs.get("start_loc"),
            Location.NORTH
        )

        end_loc = self.LOCATION_MAP.get(
            v1_attrs.get("end_loc"),
            Location.NORTH
        )

        return MotionData(
            motion_type=motion_type,
            prop_rot_dir=prop_rot_dir,
            start_loc=start_loc,
            end_loc=end_loc,
            start_ori=v1_attrs.get("start_ori", "in"),
            end_ori=v1_attrs.get("end_ori", "in")
        )

    def validate_conversion(self, v1_data: Dict[str, Any], v2_data: BeatData) -> bool:
        """Validate that conversion preserved essential data"""
        checks = [
            v1_data.get("letter") == v2_data.letter,
            v1_data.get("start_pos") == v2_data.start_pos,
            v1_data.get("end_pos") == v2_data.end_pos,
            v2_data.blue_motion is not None,
            v2_data.red_motion is not None
        ]

        return all(checks)
```

### Step 3: Create Position Matching Service

**File**: `v2/src/application/services/position_matching_service.py`

```python
from typing import Dict, List, Any
from v2.src.infrastructure.data.v1_dataset_loader import V1DatasetLoader
from v2.src.application.services.data_conversion_service import DataConversionService
from v2.src.domain.models.core_models import BeatData

class PositionMatchingService:
    """V1-style position matching for motion generation"""

    def __init__(self):
        self.dataset_loader = V1DatasetLoader()
        self.conversion_service = DataConversionService()
        self.pictograph_dataset = None
        self._load_dataset()

    def _load_dataset(self):
        """Load V1 dataset on initialization"""
        try:
            self.pictograph_dataset = self.dataset_loader.load_pictograph_dataset()
            stats = self.dataset_loader.get_dataset_statistics(self.pictograph_dataset)
            print(f"📊 Dataset loaded: {stats['total_pictographs']} pictographs across {stats['total_letters']} letters")
        except Exception as e:
            print(f"❌ Failed to load V1 dataset: {e}")
            self.pictograph_dataset = {}

    def get_next_options(self, last_beat_end_pos: str) -> List[BeatData]:
        """V1's core algorithm: find all pictographs where start_pos matches"""
        if not self.pictograph_dataset:
            print("❌ No dataset loaded")
            return []

        print(f"🔍 Searching for options with start_pos = '{last_beat_end_pos}'")

        next_opts = []
        total_checked = 0
        matches_found = 0

        # V1's exact algorithm (lines 120-131 in option_getter.py)
        for letter_group, pictographs in self.pictograph_dataset.items():
            for pictograph_data in pictographs:
                total_checked += 1
                if pictograph_data.get("start_pos") == last_beat_end_pos:
                    try:
                        # Convert V1 data to V2 format
                        beat_data = self.conversion_service.convert_v1_pictograph_to_beat_data(pictograph_data)
                        next_opts.append(beat_data)
                        matches_found += 1
                        print(f"   ✅ Match {matches_found}: Letter {beat_data.letter}, {last_beat_end_pos} → {beat_data.end_pos}")
                    except Exception as e:
                        print(f"   ❌ Failed to convert pictograph: {e}")

        print(f"📊 Search complete: {matches_found} matches found from {total_checked} pictographs")
        return next_opts

    def get_available_start_positions(self) -> List[str]:
        """Get all available start positions from dataset"""
        if not self.pictograph_dataset:
            return []

        start_positions = set()
        for pictographs in self.pictograph_dataset.values():
            for pictograph in pictographs:
                start_pos = pictograph.get("start_pos")
                if start_pos:
                    start_positions.add(start_pos)

        return sorted(list(start_positions))

    def get_available_end_positions(self) -> List[str]:
        """Get all available end positions from dataset"""
        if not self.pictograph_dataset:
            return []

        end_positions = set()
        for pictographs in self.pictograph_dataset.values():
            for pictograph in pictographs:
                end_pos = pictograph.get("end_pos")
                if end_pos:
                    end_positions.add(end_pos)

        return sorted(list(end_positions))
```

## 🧪 Testing Dataset Integration

### Test File: `v2/test_dataset_integration.py`

```python
def test_v1_dataset_loading():
    """Test V1 dataset loading"""
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()

    assert len(dataset) > 0, "Dataset should not be empty"
    assert "A" in dataset, "Dataset should contain letter A"
    assert "D" in dataset, "Dataset should contain letter D"

    print("✅ V1 dataset loading test passed")

def test_data_conversion():
    """Test V1 to V2 data conversion"""
    # Sample V1 data
    v1_data = {
        "letter": "D",
        "start_pos": "alpha1",
        "end_pos": "beta2",
        "blue_attributes": {
            "motion_type": "pro",
            "prop_rot_dir": "cw",
            "start_loc": "n",
            "end_loc": "e",
            "start_ori": "in",
            "end_ori": "clock"
        },
        "red_attributes": {
            "motion_type": "pro",
            "prop_rot_dir": "ccw",
            "start_loc": "s",
            "end_loc": "w",
            "start_ori": "out",
            "end_ori": "counter"
        }
    }

    converter = DataConversionService()
    v2_data = converter.convert_v1_pictograph_to_beat_data(v1_data)

    assert v2_data.letter == "D"
    assert v2_data.start_pos == "alpha1"
    assert v2_data.end_pos == "beta2"
    assert v2_data.blue_motion.motion_type == MotionType.PRO

    print("✅ Data conversion test passed")

def test_position_matching():
    """Test position matching service"""
    service = PositionMatchingService()

    # Test Alpha 1 matching
    alpha1_options = service.get_next_options("alpha1")

    assert len(alpha1_options) > 0, "Should find options for alpha1"

    # Verify all results have start_pos = alpha1
    for option in alpha1_options:
        assert option.start_pos == "alpha1", f"Expected start_pos=alpha1, got {option.start_pos}"

    print(f"✅ Position matching test passed: {len(alpha1_options)} options found for alpha1")
```

## 🔗 Integration Points

### Update Option Picker to Use V1 Dataset

**File**: `v2/src/presentation/components/option_picker/__init__.py`

```python
def initialize_with_v1_dataset(self):
    """Initialize option picker with V1 dataset"""
    self.position_matching_service = PositionMatchingService()
    print("✅ Option picker initialized with V1 dataset")

def load_motion_combinations_v1_style(self, sequence_data: List[dict]):
    """Load motion combinations using V1's position matching"""
    if not sequence_data or len(sequence_data) < 2:
        return

    # Get last beat's end position
    last_beat = sequence_data[-1]
    last_end_pos = last_beat.get("end_pos")

    if not last_end_pos:
        print("❌ No end position in last beat")
        return

    # Use V1's position matching algorithm
    next_options = self.position_matching_service.get_next_options(last_end_pos)

    # Clear existing and populate sections
    self._clear_all_sections()
    self._populate_sections_with_options(next_options)
```

## 📊 Success Criteria

1. **Dataset Loading**: Successfully load V1's pictograph dataset
2. **Data Conversion**: Convert V1 format to V2 BeatData without data loss
3. **Position Matching**: Find correct options using V1's algorithm
4. **Alpha 1 Test**: Generate identical letters to V1 for Alpha 1 start position

## 🔗 Next Steps

1. **Implement dataset loader** and test with V1 data
2. **Create conversion service** and validate data integrity
3. **Build position matching service** using V1's algorithm
4. **Test with Alpha 1** to verify identical results to V1

## ⚠️ Critical Orientation Values

**IMPORTANT**: V1 uses string orientation values, not numbers:

- `start_ori` and `end_ori` values are: `"in"`, `"out"`, `"clock"`, `"counter"`
- **NOT** numeric degrees (0, 90, 180, 270)

## 🔗 Next Steps

1. **Implement dataset loader** and test with V1 data
2. **Create conversion service** with correct orientation handling
3. **Build position matching service** using V1's algorithm
4. **Test with Alpha 1** to verify identical results to V1

Ready to integrate V1's proven dataset! 🚀
