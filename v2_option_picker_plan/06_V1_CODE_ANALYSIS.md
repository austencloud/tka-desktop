# V1 Code Analysis - Complete Reference

## 🎯 Purpose
Detailed analysis of V1's codebase with exact file paths, line numbers, and code examples for implementing V1's motion generation system in V2.

## 📁 Key V1 Files and Their Roles

### Core Motion Generation Pipeline

#### 1. Start Position Selection
**File**: `v1/src/base_widgets/pictograph/elements/views/start_pos_picker_pictograph_view.py`
**Lines**: 32-40
```python
def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
        self.clicked.emit()  # Triggers start position selection
```

#### 2. Start Position Adder
**File**: `v1/src/main_window/main_widget/sequence_workbench/sequence_beat_frame/start_position_adder.py`
**Lines**: 25-91
```python
def add_start_pos_to_sequence(self, clicked_start_option: "Pictograph") -> None:
    # Sets start position data and triggers option picker update
    self.construct_tab.transition_to_option_picker()
    self.construct_tab.option_picker.updater.update_options()  # ← KEY TRIGGER
```

#### 3. Option Updater (Orchestrator)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/core/option_updater.py`
**Lines**: 37-65
```python
def update_options(self) -> None:
    sequence = self.json_loader.load_current_sequence()
    sequence_without_metdata = sequence[1:]
    
    # Get next options using position matching
    next_options = self.option_picker.option_getter.get_next_options(
        sequence_without_metdata, selected_filter
    )
    
    # Clear existing sections
    for section in self.option_picker.option_scroll.sections.values():
        section.clear_pictographs()  # ← V1's clear pattern
    
    # Assign to sections using letter type classification
    for i, option_data in enumerate(next_options):
        option = self.option_picker.option_pool[i]  # ← Object pooling
        option.managers.updater.update_pictograph(option_data)
        letter_type = LetterType.get_letter_type(option.state.letter)
        section = self.option_picker.option_scroll.sections.get(letter_type)
        if section:
            section.add_pictograph(option)  # ← Add to section
```

#### 4. Option Getter (Core Algorithm)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/core/option_getter.py`
**Lines**: 27-38 (Main method)
```python
def get_next_options(
    self, sequence: list[dict[str, Any]], selected_filter: Optional[str] = None
) -> list[dict[str, Any]]:
    options = self._load_all_next_option_dicts(sequence)  # ← Core algorithm
    if selected_filter is not None:
        options = [
            o for o in options
            if self._determine_reversal_filter(sequence, o) == selected_filter
        ]
    self.update_orientations(sequence, options)
    return options
```

**Lines**: 88-114 (Core Algorithm Implementation)
```python
def _load_all_next_option_dicts(
    self, sequence: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    next_opts: list[dict[str, Any]] = []
    if not sequence:
        return next_opts
    
    # Get last beat's end position
    last = sequence[-1]
    start = last.get(END_POS)  # ← Key: get end position of last beat
    
    if start:
        # V1's CORE ALGORITHM: Position matching
        for group in self.pictograph_dataset.values():
            for item in group:
                if item.get(START_POS) == start:  # ← THE ENTIRE ALGORITHM
                    next_opts.append(item)  # ← Add to valid options
    
    # Update orientations for continuity
    for o in next_opts:
        for color in (BLUE, RED):
            o[f"{color}_attributes"][START_ORI] = last[f"{color}_attributes"][END_ORI]
        self.ori_validation_engine.validate_single_pictograph(o, last)
    
    return next_opts
```

### Letter Type Classification

#### 5. Letter Type Enum
**File**: `v1/src/enums/letter/letter_type.py`
**Lines**: 8-39
```python
class LetterType(Enum):
    Type1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
             "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
    Type2 = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
    Type3 = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]
    Type4 = ["Φ", "Ψ", "Λ"]
    Type5 = ["Φ-", "Ψ-", "Λ-"]
    Type6 = ["α", "β", "Γ"]

    @classmethod
    def get_letter_type(cls, letter: str) -> "LetterType":
        for letter_type in cls:
            if letter in letter_type.value:
                return letter_type
        return cls.Type1  # Default fallback
```

### Object Pooling System

#### 6. Option Factory (Object Pool Creation)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/core/option_factory.py`
**Lines**: 15-25
```python
class OptionFactory:
    MAX_PICTOGRAPHS = 36  # ← Pool size
    
    def create_options(self) -> list[Pictograph]:
        options = []
        for i in range(self.MAX_PICTOGRAPHS):
            option = Pictograph(self.option_picker)  # ← Pre-allocate objects
            options.append(option)
        return options
```

#### 7. Option Picker (Pool Management)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/widgets/option_picker.py`
**Lines**: 53-55
```python
def __init__(self, construct_tab):
    self.option_factory = OptionFactory(self, mw_size_provider)
    self.option_pool = self.option_factory.create_options()  # ← Create pool
```

### Section Management

#### 8. Section Widget (V1's Clear Pattern)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/widgets/scroll/section_widget.py`
**Lines**: 65-75
```python
def clear_pictographs(self):
    """V1's clear pattern: remove from layout, hide, but NEVER delete"""
    for pictograph in self.pictographs:
        if pictograph:
            self.pictograph_layout.removeWidget(pictograph)  # ← Remove from layout
            pictograph.setVisible(False)  # ← Hide widget
            # NOTE: NO deleteLater() call - this is key!
    self.pictographs.clear()
```

#### 9. Section Widget (Add Pattern)
**File**: `v1/src/main_window/main_widget/construct_tab/option_picker/widgets/scroll/section_widget.py`
**Lines**: 45-55
```python
def add_pictograph(self, pictograph):
    """V1's add pattern: reuse existing objects"""
    self.pictographs.append(pictograph)
    
    # Calculate grid position (8 columns)
    COLUMN_COUNT = 8
    count = len(self.pictographs)
    row, col = divmod(count - 1, COLUMN_COUNT)
    
    # Add to layout
    self.pictograph_layout.addWidget(pictograph, row, col)
    pictograph.setVisible(True)  # ← Show reused object
```

## 🔧 V1 Data Structures

### Pictograph Data Format
```python
# V1's pictograph data structure
{
    "letter": "D",
    "start_pos": "alpha1", 
    "end_pos": "beta2",
    "blue_attributes": {
        "motion_type": "pro",
        "prop_rot_dir": "cw",
        "start_loc": "n",
        "end_loc": "e", 
        "start_ori": "in",      # ← String values: "in", "out", "clock", "counter"
        "end_ori": "clock"      # ← NOT numeric degrees
    },
    "red_attributes": {
        "motion_type": "pro",
        "prop_rot_dir": "ccw", 
        "start_loc": "s",
        "end_loc": "w",
        "start_ori": "out",     # ← String orientation values
        "end_ori": "counter"
    }
}
```

### Constants Used in V1
```python
# From v1/src/constants.py
START_POS = "start_pos"
END_POS = "end_pos" 
BLUE = "blue"
RED = "red"
BLUE_ATTRS = "blue_attributes"
RED_ATTRS = "red_attributes"
START_ORI = "start_ori"
END_ORI = "end_ori"
MOTION_TYPE = "motion_type"
```

## 🎯 Key V1 Patterns to Replicate

### 1. Position Matching Algorithm
```python
# V1's core logic (option_getter.py:120-131)
for group in self.pictograph_dataset.values():
    for item in group:
        if item.get(START_POS) == start:  # ← Simple string matching
            next_opts.append(item)
```

### 2. Object Pooling Pattern
```python
# V1's reuse pattern (option_updater.py:58-64)
option = self.option_picker.option_pool[i]  # ← Get from pool
option.managers.updater.update_pictograph(option_data)  # ← Update content
section.add_pictograph(option)  # ← Add to layout
```

### 3. V1's Clear Pattern (NO DELETION)
```python
# V1's safe clear (section_widget.py:65-75)
self.pictograph_layout.removeWidget(pictograph)  # ← Remove from layout
pictograph.setVisible(False)  # ← Hide
# NO deleteLater() call!
```

### 4. Letter Type Classification
```python
# V1's classification (letter_type.py:30-35)
for letter_type in cls:
    if letter in letter_type.value:
        return letter_type
return cls.Type1  # ← Default fallback
```

## 🚨 Critical V1 Insights

### What V1 Does RIGHT:
1. **Simple position matching** - no complex validation
2. **Object pooling** - reuse, never delete
3. **Data-driven** - retrieve from dataset, don't generate
4. **Static classification** - letter types are fixed

### What V1 Avoids:
1. **No deleteLater() calls** on pictograph objects
2. **No motion validation** - dataset is pre-validated
3. **No algorithmic generation** - pure data retrieval
4. **No complex lifecycle management** - simple hide/show

## 🔗 Implementation Mapping

### V1 → V2 File Mapping:
- `option_getter.py` → `v2/src/application/services/position_matching_service.py`
- `letter_type.py` → `v2/src/domain/models/letter_type_classifier.py`
- `option_updater.py` → `v2/src/presentation/components/option_picker/__init__.py`
- `option_factory.py` → `v2/src/presentation/components/option_picker/pictograph_pool.py`
- `section_widget.py` → `v2/src/presentation/components/option_picker/option_picker_section.py`

### V1 → V2 Method Mapping:
- `get_next_options()` → `get_next_options()`
- `_load_all_next_option_dicts()` → `get_next_options()`
- `LetterType.get_letter_type()` → `LetterTypeClassifier.get_letter_type()`
- `clear_pictographs()` → `clear_pictographs_v1_style()`
- `add_pictograph()` → `add_pictograph_from_pool()`

## 📊 Success Criteria

Implementing these V1 patterns should result in:
1. **Identical motion combinations** to V1 (same dataset)
2. **Correct sectional assignment** (same classification)
3. **No Qt object deletion issues** (object pooling)
4. **Pixel-perfect visual parity** (same data source)

The V1 codebase provides the complete blueprint for success! 🎯
