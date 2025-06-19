#!/usr/bin/env python3
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent VTG and elemental glyph visibility bug from reoccurring  
BUG_REPORT: VTG and elemental glyphs were showing for Type 2 letters when they shouldn't
FIXED_DATE: 2025-06-19
AUTHOR: @austencloud
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

import pytest
from application.services.core.pictograph_management_service import (
    PictographManagementService,
)
from domain.models.core_models import LetterType, BeatData


class TestGlyphVisibilityType2Prevention:
    """Regression test for glyph visibility bug prevention."""
    
    @pytest.fixture
    def pictograph_service(self):
        """Create pictograph management service for testing."""
        return PictographManagementService()
    
    def test_type2_letters_hide_vtg_glyphs(self, pictograph_service):
        """Test that Type 2 letters do not show VTG glyphs."""
        type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
        
        for letter in type2_letters:
            # Verify letter is classified as Type 2
            letter_type = pictograph_service._determine_letter_type(letter)
            assert letter_type == LetterType.TYPE2, f"Letter '{letter}' should be TYPE2"
            
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            
            # Verify VTG glyph is hidden
            if glyph_data:
                assert not glyph_data.show_vtg, f"Letter '{letter}' should not show VTG glyph"
    
    def test_type2_letters_hide_elemental_glyphs(self, pictograph_service):
        """Test that Type 2 letters do not show elemental glyphs."""
        type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
        
        for letter in type2_letters:
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            
            # Verify elemental glyph is hidden
            if glyph_data:
                assert not glyph_data.show_elemental, f"Letter '{letter}' should not show elemental glyph"
    
    def test_type1_letters_show_vtg_glyphs(self, pictograph_service):
        """Test that Type 1 letters still show VTG glyphs (regression prevention)."""
        type1_letters = ["A", "B", "D", "G"]
        
        for letter in type1_letters:
            # Verify letter is classified as Type 1
            letter_type = pictograph_service._determine_letter_type(letter)
            assert letter_type == LetterType.TYPE1, f"Letter '{letter}' should be TYPE1"
            
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            
            # Verify VTG glyph is shown
            if glyph_data:
                assert glyph_data.show_vtg, f"Letter '{letter}' should show VTG glyph"
    
    def test_type1_letters_show_elemental_glyphs(self, pictograph_service):
        """Test that Type 1 letters still show elemental glyphs (regression prevention)."""
        type1_letters = ["A", "B", "D", "G"]
        
        for letter in type1_letters:
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            
            # Verify elemental glyph is shown
            if glyph_data:
                assert glyph_data.show_elemental, f"Letter '{letter}' should show elemental glyph"
    
    def test_letter_type_classification_consistency(self, pictograph_service):
        """Test that letter type classification is consistent."""
        # Type 2 letters
        type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
        for letter in type2_letters:
            letter_type = pictograph_service._determine_letter_type(letter)
            assert letter_type == LetterType.TYPE2, f"Letter '{letter}' classification inconsistent"
        
        # Type 1 letters
        type1_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
        for letter in type1_letters:
            letter_type = pictograph_service._determine_letter_type(letter)
            assert letter_type == LetterType.TYPE1, f"Letter '{letter}' classification inconsistent"
    
    def test_glyph_data_generation_robustness(self, pictograph_service):
        """Test that glyph data generation doesn't crash for any letter."""
        all_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
        
        for letter in all_letters:
            beat_data = BeatData(letter=letter)
            # Should not raise an exception
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            # Glyph data can be None or a valid object, but should not crash
