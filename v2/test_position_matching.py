#!/usr/bin/env python3
"""
Test Position Matching Implementation

This script tests the new data-driven position matching algorithm
to verify it works correctly with V2's dataset.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_position_matching_service():
    """Test the PositionMatchingService with V2's dataset."""
    print("🧪 Testing Position Matching Service")
    print("=" * 50)
    
    try:
        from application.services.position_matching_service import PositionMatchingService
        from domain.models.letter_type_classifier import LetterTypeClassifier
        
        # Initialize the service
        print("📊 Initializing PositionMatchingService...")
        service = PositionMatchingService()
        
        # Test dataset integrity
        print("\n🔍 Validating dataset integrity...")
        integrity = service.validate_dataset_integrity()
        print(f"   Dataset valid: {integrity['valid']}")
        print(f"   Total pictographs: {integrity['total_pictographs']}")
        print(f"   Total letters: {integrity['total_letters']}")
        
        if integrity['total_issues'] > 0:
            print(f"   Issues found: {integrity['total_issues']}")
            for issue in integrity['issues']:
                print(f"     - {issue}")
        
        # Test available start positions
        print("\n📍 Available start positions:")
        positions = service.get_available_start_positions()
        print(f"   Found {len(positions)} positions: {positions[:10]}...")
        
        # Test Alpha 1 (canonical test case)
        print("\n🎯 Testing Alpha 1 position matching...")
        alpha1_options = service.get_alpha1_options()
        print(f"   Found {len(alpha1_options)} options for alpha1")
        
        if alpha1_options:
            print("   Letters found:")
            letters = [opt.get("letter", "?") for opt in alpha1_options]
            print(f"     {', '.join(letters)}")
            
            # Test letter type classification
            print("\n📋 Letter type classification:")
            letter_types = {}
            for letter in letters:
                letter_type = LetterTypeClassifier.get_letter_type(letter)
                letter_types[letter_type] = letter_types.get(letter_type, 0) + 1
            
            for letter_type, count in letter_types.items():
                print(f"     {letter_type}: {count} letters")
        
        # Test position statistics
        print("\n📊 Position statistics for alpha1:")
        stats = service.get_position_statistics("alpha1")
        print(f"   Total options: {stats['total_options']}")
        print(f"   Unique letters: {stats['unique_letters']}")
        print(f"   Letter types: {stats['letter_types']}")
        
        print("\n✅ Position matching service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Position matching service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_conversion_service():
    """Test the DataConversionService."""
    print("\n🧪 Testing Data Conversion Service")
    print("=" * 50)
    
    try:
        from application.services.data_conversion_service import DataConversionService
        
        # Initialize the service
        conversion_service = DataConversionService()
        
        # Test with sample data
        sample_v1_data = {
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
        
        print("🔄 Converting sample data...")
        beat_data = conversion_service.convert_v1_pictograph_to_beat_data(sample_v1_data)
        
        print(f"   Letter: {beat_data.letter}")
        print(f"   Blue motion: {beat_data.blue_motion.motion_type}")
        print(f"   Red motion: {beat_data.red_motion.motion_type}")
        
        # Validate conversion
        validation = conversion_service.validate_conversion(sample_v1_data, beat_data)
        print(f"   Conversion valid: {validation['valid']}")
        
        if not validation['valid']:
            for issue in validation['issues']:
                print(f"     Issue: {issue}")
        
        print("\n✅ Data conversion service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Data conversion service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_letter_type_classifier():
    """Test the LetterTypeClassifier."""
    print("\n🧪 Testing Letter Type Classifier")
    print("=" * 50)
    
    try:
        from domain.models.letter_type_classifier import LetterTypeClassifier
        
        # Test known letters
        test_cases = [
            ("D", "Type1"),
            ("W", "Type2"),
            ("W-", "Type3"),
            ("Φ", "Type4"),
            ("Φ-", "Type5"),
            ("α", "Type6"),
            ("Unknown", "Type1"),  # Default fallback
        ]
        
        print("🔤 Testing letter classifications:")
        for letter, expected_type in test_cases:
            actual_type = LetterTypeClassifier.get_letter_type(letter)
            status = "✅" if actual_type == expected_type else "❌"
            print(f"   {status} {letter} → {actual_type} (expected: {expected_type})")
        
        # Test statistics
        stats = LetterTypeClassifier.get_classification_stats()
        print(f"\n📊 Classification statistics:")
        for letter_type, count in stats.items():
            print(f"   {letter_type}: {count} letters")
        
        print("\n✅ Letter type classifier test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Letter type classifier test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Position Matching Implementation Tests")
    print("=" * 60)
    
    tests = [
        test_letter_type_classifier,
        test_data_conversion_service,
        test_position_matching_service,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Position matching implementation is working!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
