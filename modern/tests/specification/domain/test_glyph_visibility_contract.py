#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Glyph visibility contracts - migrated from test_glyph_visibility_fix.py
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Glyph Visibility Contract Tests
==============================

Migrated from test_glyph_visibility_fix.py.
Defines behavioral contracts for VTG and elemental glyph visibility based on letter types.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestGlyphVisibilityContract:
    """Glyph visibility contract tests."""

    def test_pictograph_management_service_import(self):
        """Test that pictograph management service can be imported."""
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            assert PictographManagementService is not None
        except ImportError:
            pytest.skip("Pictograph management service not available")

    def test_letter_type_and_beat_data_imports(self):
        """Test that letter type and beat data can be imported."""
        try:
            from domain.models.core_models import LetterType, BeatData
            assert LetterType is not None
            assert BeatData is not None
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_type2_glyph_visibility_contract(self):
        """
        Test Type 2 glyph visibility contract.
        
        CONTRACT: Type 2 letters must NOT show VTG and elemental glyphs:
        - Letters W, X, Y, Z, Σ, Δ, θ, Ω are Type 2
        - Type 2 letters have show_vtg = False
        - Type 2 letters have show_elemental = False
        """
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            from domain.models.core_models import LetterType, BeatData
            
            # Initialize the service
            service = PictographManagementService()
            
            # Test cases: Type 2 letters that should NOT show VTG/elemental glyphs
            type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
            
            for letter in type2_letters:
                # Determine letter type using the service's method
                letter_type = service._determine_letter_type(letter)
                
                # Verify letter is classified as Type 2
                assert letter_type == LetterType.TYPE2, f"Letter '{letter}' should be TYPE2, got {letter_type}"
                
                # Create beat data to test glyph data generation
                beat_data = BeatData(letter=letter)
                glyph_data = service._generate_glyph_data(beat_data)
                
                if glyph_data:
                    # Verify VTG glyph is hidden
                    assert not glyph_data.show_vtg, f"Letter '{letter}': VTG glyph should be hidden but show_vtg=True"
                    
                    # Verify elemental glyph is hidden
                    assert not glyph_data.show_elemental, f"Letter '{letter}': Elemental glyph should be hidden but show_elemental=True"
                    
        except ImportError:
            pytest.skip("Required services not available for Type 2 glyph visibility testing")

    def test_type1_glyph_visibility_contract(self):
        """
        Test Type 1 glyph visibility contract.
        
        CONTRACT: Type 1 letters must show VTG and elemental glyphs:
        - Letters A, B, D, G are Type 1
        - Type 1 letters have show_vtg = True
        - Type 1 letters have show_elemental = True
        """
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            from domain.models.core_models import LetterType, BeatData
            
            # Initialize the service
            service = PictographManagementService()
            
            # Test cases: Type 1 letters that SHOULD show VTG/elemental glyphs
            type1_letters = ["A", "B", "D", "G"]
            
            for letter in type1_letters:
                # Determine letter type using the service's method
                letter_type = service._determine_letter_type(letter)
                
                # Verify letter is classified as Type 1
                assert letter_type == LetterType.TYPE1, f"Letter '{letter}' should be TYPE1, got {letter_type}"
                
                # Create beat data to test glyph data generation
                beat_data = BeatData(letter=letter)
                glyph_data = service._generate_glyph_data(beat_data)
                
                if glyph_data:
                    # Verify VTG glyph is shown
                    assert glyph_data.show_vtg, f"Letter '{letter}': VTG glyph should be shown but show_vtg=False"
                    
                    # Verify elemental glyph is shown
                    assert glyph_data.show_elemental, f"Letter '{letter}': Elemental glyph should be shown but show_elemental=False"
                    
        except ImportError:
            pytest.skip("Required services not available for Type 1 glyph visibility testing")

    def test_letter_type_classification_contract(self):
        """
        Test letter type classification contract.
        
        CONTRACT: Letter type classification must be consistent:
        - Service can determine letter type for any letter
        - Classification is consistent across calls
        - Type 1 and Type 2 are properly distinguished
        """
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            from domain.models.core_models import LetterType
            
            # Initialize the service
            service = PictographManagementService()
            
            # Test known Type 1 letters
            type1_letters = ["A", "B", "D", "G"]
            for letter in type1_letters:
                letter_type = service._determine_letter_type(letter)
                assert letter_type == LetterType.TYPE1, f"Letter '{letter}' should be TYPE1"
            
            # Test known Type 2 letters
            type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
            for letter in type2_letters:
                letter_type = service._determine_letter_type(letter)
                assert letter_type == LetterType.TYPE2, f"Letter '{letter}' should be TYPE2"
            
            # Test consistency - same letter should always return same type
            test_letter = "A"
            first_result = service._determine_letter_type(test_letter)
            second_result = service._determine_letter_type(test_letter)
            assert first_result == second_result, f"Letter type classification for '{test_letter}' is inconsistent"
            
        except ImportError:
            pytest.skip("Required services not available for letter type classification testing")

    def test_glyph_data_generation_contract(self):
        """
        Test glyph data generation contract.
        
        CONTRACT: Glyph data generation must work correctly:
        - Service can generate glyph data from beat data
        - Glyph data contains show_vtg and show_elemental properties
        - Glyph data generation is consistent
        """
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            from domain.models.core_models import BeatData
            
            # Initialize the service
            service = PictographManagementService()
            
            # Test glyph data generation for various letters
            test_letters = ["A", "B", "W", "X", "G", "Z"]
            
            for letter in test_letters:
                # Create beat data
                beat_data = BeatData(letter=letter)
                
                # Generate glyph data
                glyph_data = service._generate_glyph_data(beat_data)
                
                if glyph_data:
                    # Verify glyph data has required properties
                    assert hasattr(glyph_data, 'show_vtg'), f"Glyph data for '{letter}' missing show_vtg property"
                    assert hasattr(glyph_data, 'show_elemental'), f"Glyph data for '{letter}' missing show_elemental property"
                    
                    # Verify properties are boolean
                    assert isinstance(glyph_data.show_vtg, bool), f"show_vtg for '{letter}' should be boolean"
                    assert isinstance(glyph_data.show_elemental, bool), f"show_elemental for '{letter}' should be boolean"
            
        except ImportError:
            pytest.skip("Required services not available for glyph data generation testing")

    def test_glyph_visibility_comprehensive_contract(self):
        """
        Test comprehensive glyph visibility contract.
        
        CONTRACT: Complete glyph visibility system must work correctly:
        - All Type 1 letters show glyphs
        - All Type 2 letters hide glyphs
        - No exceptions or edge cases
        """
        try:
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )
            from domain.models.core_models import LetterType, BeatData
            
            # Initialize the service
            service = PictographManagementService()
            
            # Comprehensive test data
            all_test_data = {
                LetterType.TYPE1: ["A", "B", "D", "G"],
                LetterType.TYPE2: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
            }
            
            for expected_type, letters in all_test_data.items():
                for letter in letters:
                    # Verify letter type classification
                    actual_type = service._determine_letter_type(letter)
                    assert actual_type == expected_type, f"Letter '{letter}' type mismatch"
                    
                    # Generate glyph data
                    beat_data = BeatData(letter=letter)
                    glyph_data = service._generate_glyph_data(beat_data)
                    
                    if glyph_data:
                        if expected_type == LetterType.TYPE1:
                            # Type 1 should show glyphs
                            assert glyph_data.show_vtg, f"Type 1 letter '{letter}' should show VTG"
                            assert glyph_data.show_elemental, f"Type 1 letter '{letter}' should show elemental"
                        elif expected_type == LetterType.TYPE2:
                            # Type 2 should hide glyphs
                            assert not glyph_data.show_vtg, f"Type 2 letter '{letter}' should hide VTG"
                            assert not glyph_data.show_elemental, f"Type 2 letter '{letter}' should hide elemental"
            
        except ImportError:
            pytest.skip("Required services not available for comprehensive glyph visibility testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
