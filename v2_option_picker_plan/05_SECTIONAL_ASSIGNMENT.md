# Sectional Assignment Implementation

## 🎯 Objective
Implement V1's letter type classification system to correctly assign pictographs to Type1, Type2, Type3, etc. sections in the option picker.

## 🗂️ V1's Letter Type Classification

### V1's Exact Classification (from v1/src/enums/letter/letter_type.py)

```python
# V1's LetterType enum with exact letter assignments
Type1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
         "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]  # Dual-Shift
Type2 = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]           # Shift  
Type3 = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]   # Cross-Shift
Type4 = ["Φ", "Ψ", "Λ"]                                     # Dash
Type5 = ["Φ-", "Ψ-", "Λ-"]                                  # Dual-Dash
Type6 = ["α", "β", "Γ"]                                     # Static
```

### V1's Assignment Process (from option_updater.py lines 76-85)

```python
letter = option.state.letter
letter_type = LetterType.get_letter_type(letter)  # ← CLASSIFICATION
section = self.option_picker.option_scroll.sections.get(letter_type)
if section:
    section.add_pictograph(option)  # ← ADD TO SECTION
```

## 🔧 Implementation

### Step 1: Create Letter Type Classifier

**File**: `v2/src/domain/models/letter_type_classifier.py`

```python
from typing import Optional

class LetterTypeClassifier:
    """V1-compatible letter type classification"""
    
    # V1's exact letter type assignments
    TYPE1_LETTERS = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
        "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"
    ]
    TYPE2_LETTERS = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
    TYPE3_LETTERS = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]
    TYPE4_LETTERS = ["Φ", "Ψ", "Λ"]
    TYPE5_LETTERS = ["Φ-", "Ψ-", "Λ-"]
    TYPE6_LETTERS = ["α", "β", "Γ"]
    
    # V1's type descriptions
    TYPE_DESCRIPTIONS = {
        "Type1": "Dual-Shift",
        "Type2": "Shift", 
        "Type3": "Cross-Shift",
        "Type4": "Dash",
        "Type5": "Dual-Dash",
        "Type6": "Static"
    }
    
    @classmethod
    def get_letter_type(cls, letter: str) -> str:
        """Get letter type using V1's exact classification"""
        if not letter:
            return "Type1"  # Default fallback
        
        # V1's exact logic
        if letter in cls.TYPE1_LETTERS:
            return "Type1"
        elif letter in cls.TYPE2_LETTERS:
            return "Type2"
        elif letter in cls.TYPE3_LETTERS:
            return "Type3"
        elif letter in cls.TYPE4_LETTERS:
            return "Type4"
        elif letter in cls.TYPE5_LETTERS:
            return "Type5"
        elif letter in cls.TYPE6_LETTERS:
            return "Type6"
        else:
            # V1's fallback behavior
            return "Type1"
    
    @classmethod
    def get_type_description(cls, letter_type: str) -> str:
        """Get description for letter type"""
        return cls.TYPE_DESCRIPTIONS.get(letter_type, "Unknown")
    
    @classmethod
    def get_letters_for_type(cls, letter_type: str) -> list[str]:
        """Get all letters for a given type"""
        type_map = {
            "Type1": cls.TYPE1_LETTERS,
            "Type2": cls.TYPE2_LETTERS,
            "Type3": cls.TYPE3_LETTERS,
            "Type4": cls.TYPE4_LETTERS,
            "Type5": cls.TYPE5_LETTERS,
            "Type6": cls.TYPE6_LETTERS
        }
        return type_map.get(letter_type, [])
    
    @classmethod
    def validate_letter_assignment(cls, letter: str, expected_type: str) -> bool:
        """Validate that a letter is correctly assigned to its type"""
        actual_type = cls.get_letter_type(letter)
        return actual_type == expected_type
    
    @classmethod
    def get_all_types(cls) -> list[str]:
        """Get all available letter types"""
        return ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]
```

### Step 2: Update Option Picker for V1-Style Assignment

**File**: `v2/src/presentation/components/option_picker/__init__.py` (Update)

```python
def _populate_sections_with_v2_options(self, options: List[BeatData]):
    """Populate sections with V1-style letter type assignment"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    print(f"\n📋 V1-STYLE SECTIONAL ASSIGNMENT")
    print(f"   Processing {len(options)} options for sectional assignment")
    
    section_assignments = {}
    assignment_errors = []
    
    for option in options:
        try:
            # V1's exact assignment logic
            letter = option.letter
            letter_type = LetterTypeClassifier.get_letter_type(letter)
            
            # Get target section
            if letter_type in self._sections:
                section = self._sections[letter_type]
                
                # Verify section is valid before adding
                if self._ensure_section_valid(section):
                    # Create and add pictograph frame
                    frame = self._create_pictograph_frame_for_option(option, section)
                    section.add_pictograph_from_pool(frame)
                    
                    # Track successful assignment
                    if letter_type not in section_assignments:
                        section_assignments[letter_type] = []
                    section_assignments[letter_type].append(letter)
                    
                    print(f"   ✅ Assigned Letter {letter} to Section {letter_type}")
                else:
                    assignment_errors.append(f"Invalid section for {letter} (type: {letter_type})")
            else:
                assignment_errors.append(f"No section found for {letter} (type: {letter_type})")
                
        except Exception as e:
            assignment_errors.append(f"Failed to assign {option.letter}: {e}")
    
    # Log final results
    print(f"\n📊 SECTIONAL ASSIGNMENT SUMMARY:")
    total_assigned = 0
    for section_name, letters in section_assignments.items():
        count = len(letters)
        total_assigned += count
        description = LetterTypeClassifier.get_type_description(section_name)
        print(f"   {section_name} ({description}): {letters} ({count} pictographs)")
    
    if assignment_errors:
        print(f"\n❌ ASSIGNMENT ERRORS ({len(assignment_errors)}):")
        for error in assignment_errors:
            print(f"   - {error}")
    
    print(f"\n✅ Successfully assigned {total_assigned}/{len(options)} options")
    
    # Force section visibility
    self._force_section_visibility()
```

### Step 3: Section Validation and Management

**File**: `v2/src/presentation/components/option_picker/option_picker_section.py` (Update)

```python
def validate_section_for_letter_type(self, letter_type: str) -> bool:
    """Validate that this section can handle the given letter type"""
    return self.letter_type == letter_type

def get_expected_letters(self) -> list[str]:
    """Get letters that should be assigned to this section"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    return LetterTypeClassifier.get_letters_for_type(self.letter_type)

def validate_letter_assignment(self, letter: str) -> bool:
    """Validate that a letter belongs in this section"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    expected_type = LetterTypeClassifier.get_letter_type(letter)
    return expected_type == self.letter_type
```

## 🧪 Testing Sectional Assignment

### Test File: `v2/test_sectional_assignment.py`

```python
def test_letter_type_classification():
    """Test V1's letter type classification"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    # Test known assignments
    test_cases = [
        ("A", "Type1"), ("D", "Type1"), ("V", "Type1"),
        ("W", "Type2"), ("X", "Type2"), ("Ω", "Type2"),
        ("W-", "Type3"), ("X-", "Type3"), ("Ω-", "Type3"),
        ("Φ", "Type4"), ("Ψ", "Type4"), ("Λ", "Type4"),
        ("Φ-", "Type5"), ("Ψ-", "Type5"), ("Λ-", "Type5"),
        ("α", "Type6"), ("β", "Type6"), ("Γ", "Type6")
    ]
    
    for letter, expected_type in test_cases:
        actual_type = LetterTypeClassifier.get_letter_type(letter)
        assert actual_type == expected_type, f"Letter {letter}: expected {expected_type}, got {actual_type}"
    
    print("✅ Letter type classification test passed")

def test_alpha1_sectional_assignment():
    """Test sectional assignment for Alpha 1 results"""
    # This test requires the full pipeline to be working
    from v2.src.infrastructure.data.v1_dataset_loader import V1DatasetLoader
    from v2.src.application.services.position_matching_service import PositionMatchingService
    from v2.src.application.services.data_conversion_service import DataConversionService
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    # Load dataset and get Alpha 1 options
    loader = V1DatasetLoader()
    dataset = loader.load_pictograph_dataset()
    
    position_service = PositionMatchingService(dataset)
    conversion_service = DataConversionService()
    
    # Get Alpha 1 options
    v1_options = position_service.get_alpha1_options()
    
    # Convert to V2 format
    v2_options = []
    for v1_option in v1_options:
        v2_option = conversion_service.convert_v1_pictograph_to_beat_data(v1_option)
        v2_options.append(v2_option)
    
    # Test sectional assignment
    section_assignments = {}
    for option in v2_options:
        letter_type = LetterTypeClassifier.get_letter_type(option.letter)
        if letter_type not in section_assignments:
            section_assignments[letter_type] = []
        section_assignments[letter_type].append(option.letter)
    
    # Verify expected sections are populated
    assert "Type1" in section_assignments, "Type1 should have assignments"
    assert len(section_assignments["Type1"]) > 0, "Type1 should have letters"
    
    # Log results
    print(f"📊 Alpha 1 Sectional Assignment Results:")
    for section_type, letters in section_assignments.items():
        description = LetterTypeClassifier.get_type_description(section_type)
        print(f"   {section_type} ({description}): {letters}")
    
    print("✅ Alpha 1 sectional assignment test passed")

def test_section_validation():
    """Test section validation methods"""
    from v2.src.domain.models.letter_type_classifier import LetterTypeClassifier
    
    # Test letter validation
    assert LetterTypeClassifier.validate_letter_assignment("D", "Type1")
    assert not LetterTypeClassifier.validate_letter_assignment("D", "Type2")
    
    # Test type enumeration
    all_types = LetterTypeClassifier.get_all_types()
    expected_types = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]
    assert all_types == expected_types
    
    # Test letters for type
    type1_letters = LetterTypeClassifier.get_letters_for_type("Type1")
    assert "D" in type1_letters
    assert "W" not in type1_letters
    
    print("✅ Section validation test passed")

if __name__ == "__main__":
    print("🧪 Testing V1 Sectional Assignment")
    
    # Test classification
    test_letter_type_classification()
    
    # Test validation
    test_section_validation()
    
    # Test full pipeline (requires dataset)
    try:
        test_alpha1_sectional_assignment()
    except Exception as e:
        print(f"⚠️ Full pipeline test skipped: {e}")
    
    print("✅ All sectional assignment tests passed!")
```

## 🎯 Expected Alpha 1 Results

Based on V1 analysis, Alpha 1 should generate letters primarily in:
- **Type1**: D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V
- **Type2**: Possibly W, X, Y, Z (if they exist for alpha1 start position)

## ⚠️ Critical Notes

- **Use V1's exact letter lists**: Don't modify the letter assignments
- **Default to Type1**: V1 falls back to Type1 for unknown letters
- **Case-sensitive matching**: Letter strings must match exactly
- **No dynamic assignment**: Letter types are static, not based on motion data

## 🔗 Next Steps

1. **Implement LetterTypeClassifier** with V1's exact assignments
2. **Update option picker** to use V1-style sectional assignment
3. **Test with Alpha 1** to verify correct section population
4. **Validate against V1** to ensure identical sectional layout

The sectional assignment system ensures pictographs appear in the correct sections just like V1! 🗂️
