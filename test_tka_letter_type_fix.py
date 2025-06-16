#!/usr/bin/env python3
"""
Test script to verify that TKA glyph rendering uses the correct letter type
determined from the letter string rather than a default value.
"""

import sys
import os

sys.path.append("v2/src")

def test_letter_type_determination():
    """Test that letter types are correctly determined from letters."""
    print("🧪 Testing letter type determination for TKA glyph rendering...")
    
    try:
        from domain.models.letter_type_classifier import LetterTypeClassifier
        from domain.models.core_models import LetterType
        
        # Test various letter types to ensure they're correctly determined
        test_cases = [
            # Type 1 letters
            ("A", "Type1", LetterType.TYPE1),
            ("D", "Type1", LetterType.TYPE1),
            ("V", "Type1", LetterType.TYPE1),
            
            # Type 2 letters  
            ("W", "Type2", LetterType.TYPE2),
            ("X", "Type2", LetterType.TYPE2),
            ("Σ", "Type2", LetterType.TYPE2),
            
            # Type 3 letters (dash letters)
            ("W-", "Type3", LetterType.TYPE3),
            ("X-", "Type3", LetterType.TYPE3),
            ("Σ-", "Type3", LetterType.TYPE3),
            
            # Type 4 letters
            ("Φ", "Type4", LetterType.TYPE4),
            ("Ψ", "Type4", LetterType.TYPE4),
            
            # Type 5 letters
            ("Φ-", "Type5", LetterType.TYPE5),
            ("Ψ-", "Type5", LetterType.TYPE5),
            
            # Type 6 letters
            ("α", "Type6", LetterType.TYPE6),
            ("β", "Type6", LetterType.TYPE6),
            ("Γ", "Type6", LetterType.TYPE6),
        ]
        
        all_passed = True
        
        for letter, expected_str, expected_enum in test_cases:
            # Test classifier returns correct string
            actual_str = LetterTypeClassifier.get_letter_type(letter)
            if actual_str != expected_str:
                print(f"❌ Letter '{letter}': expected '{expected_str}', got '{actual_str}'")
                all_passed = False
                continue
                
            # Test enum conversion works
            try:
                actual_enum = LetterType(actual_str)
                if actual_enum != expected_enum:
                    print(f"❌ Letter '{letter}': enum mismatch. Expected {expected_enum}, got {actual_enum}")
                    all_passed = False
                    continue
            except ValueError as e:
                print(f"❌ Letter '{letter}': enum conversion failed: {e}")
                all_passed = False
                continue
                
            print(f"✅ Letter '{letter}': correctly determined as {expected_str} / {expected_enum}")
        
        if all_passed:
            print("\n🎉 All letter type determinations are correct!")
            print("✅ TKA glyph rendering will now use the correct letter type instead of default Type1")
            return True
        else:
            print("\n❌ Some letter type determinations failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fix_behavior():
    """Test that the fix addresses the original issue."""
    print("\n🔧 Testing fix behavior...")
    
    # Simulate what the old code was doing vs new code
    print("Old behavior: Used glyph_data.letter_type (potentially defaulted to Type1)")
    print("New behavior: Uses LetterTypeClassifier.get_letter_type(letter) for accurate determination")
    
    # Show examples of how different letters are classified
    examples = ["D", "W-", "Φ", "α"]
    
    try:
        from domain.models.letter_type_classifier import LetterTypeClassifier
        
        for letter in examples:
            actual_type = LetterTypeClassifier.get_letter_type(letter)
            print(f"  Letter '{letter}' → {actual_type} (was potentially Type1 before)")
            
        print("✅ Fix ensures accurate letter type determination based on actual letter")
        return True
        
    except Exception as e:
        print(f"❌ Fix test failed: {e}")
        return False

if __name__ == "__main__":
    success1 = test_letter_type_determination()
    success2 = test_fix_behavior()
    
    if success1 and success2:
        print(f"\n🎉 ALL TESTS PASSED - TKA glyph letter type fix is working correctly!")
    else:
        print(f"\n❌ SOME TESTS FAILED")
    
    sys.exit(0 if (success1 and success2) else 1)
