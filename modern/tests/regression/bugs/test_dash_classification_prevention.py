#!/usr/bin/env python3
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent dash classification bug from reoccurring
BUG_REPORT: Type3 letters were not properly classified with dash flags
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


class TestDashClassificationPrevention:
    """Regression test for dash classification bug prevention."""

    @pytest.fixture
    def pictograph_service(self):
        """Create pictograph management service for testing."""
        return PictographManagementService()

    def test_type3_dash_letters_classification(self, pictograph_service):
        """Test that Type3 dash letters are properly classified."""
        type3_dash_letters = ["W-", "X-", "Y-", "Z-"]

        for letter in type3_dash_letters:
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)

            # Verify proper classification
            assert (
                glyph_data is not None
            ), f"Letter '{letter}' should generate glyph data"
            assert (
                glyph_data.letter_type == LetterType.TYPE3
            ), f"Letter '{letter}' should be TYPE3"
            assert (
                glyph_data.has_dash is True
            ), f"Letter '{letter}' should have dash flag set"

    def test_type2_non_dash_letters_classification(self, pictograph_service):
        """Test that Type2 non-dash letters are properly classified."""
        type2_non_dash_letters = ["W", "X", "Y", "Z"]

        for letter in type2_non_dash_letters:
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)

            # Verify proper classification
            assert (
                glyph_data is not None
            ), f"Letter '{letter}' should generate glyph data"
            assert (
                glyph_data.letter_type == LetterType.TYPE2
            ), f"Letter '{letter}' should be TYPE2"
            assert (
                glyph_data.has_dash is False
            ), f"Letter '{letter}' should not have dash flag"

    def test_type1_letters_no_dash_flag(self, pictograph_service):
        """Test that Type1 letters don't get dash flags (regression prevention)."""
        type1_letters = ["A", "B", "C", "D", "E", "F", "G"]

        for letter in type1_letters:
            # Create beat data and generate glyph data
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)

            # Verify proper classification
            if glyph_data:  # Some letters might not generate glyph data
                assert (
                    glyph_data.letter_type == LetterType.TYPE1
                ), f"Letter '{letter}' should be TYPE1"
                assert (
                    glyph_data.has_dash is False
                ), f"Letter '{letter}' should not have dash flag"

    def test_dash_detection_logic(self, pictograph_service):
        """Test that dash detection logic works correctly."""
        test_cases = [
            ("A", False),  # No dash
            ("A-", True),  # Has dash
            ("W", False),  # No dash
            ("W-", True),  # Has dash
            ("Σ", False),  # No dash
            ("Σ-", True),  # Has dash (if supported)
        ]

        for letter, expected_has_dash in test_cases:
            beat_data = BeatData(letter=letter)
            glyph_data = pictograph_service._generate_glyph_data(beat_data)

            if glyph_data:
                assert (
                    glyph_data.has_dash == expected_has_dash
                ), f"Letter '{letter}' dash detection incorrect"

    def test_letter_type_dash_transformation(self, pictograph_service):
        """Test that dash transforms letter types correctly."""
        # Test that dash versions get different classification (TYPE2 -> TYPE3)
        base_letters = ["W", "X", "Y", "Z"]

        for base_letter in base_letters:
            # Test base letter (should be TYPE2)
            beat_data_base = BeatData(letter=base_letter)
            glyph_data_base = pictograph_service._generate_glyph_data(beat_data_base)

            # Test dash version (should be TYPE3)
            dash_letter = f"{base_letter}-"
            beat_data_dash = BeatData(letter=dash_letter)
            glyph_data_dash = pictograph_service._generate_glyph_data(beat_data_dash)

            # Verify transformation
            if glyph_data_base and glyph_data_dash:
                assert (
                    glyph_data_base.letter_type == LetterType.TYPE2
                ), f"Base letter '{base_letter}' should be TYPE2"
                assert (
                    glyph_data_dash.letter_type == LetterType.TYPE3
                ), f"Dash letter '{dash_letter}' should be TYPE3"
                assert (
                    glyph_data_base.has_dash is False
                ), f"Base letter '{base_letter}' should not have dash flag"
                assert (
                    glyph_data_dash.has_dash is True
                ), f"Dash letter '{dash_letter}' should have dash flag"

    def test_glyph_data_generation_robustness(self, pictograph_service):
        """Test that glyph data generation doesn't crash for dash letters."""
        all_dash_letters = [
            "A-",
            "B-",
            "C-",
            "D-",
            "E-",
            "F-",
            "G-",
            "H-",
            "I-",
            "J-",
            "K-",
            "L-",
            "M-",
            "N-",
            "O-",
            "P-",
            "Q-",
            "R-",
            "S-",
            "T-",
            "U-",
            "V-",
            "W-",
            "X-",
            "Y-",
            "Z-",
        ]

        for letter in all_dash_letters:
            beat_data = BeatData(letter=letter)
            # Should not raise an exception
            glyph_data = pictograph_service._generate_glyph_data(beat_data)
            # Glyph data can be None or a valid object, but should not crash

            if glyph_data:
                # If glyph data is generated, dash flag should be set
                assert (
                    glyph_data.has_dash is True
                ), f"Dash letter '{letter}' should have dash flag"
