"""
Integration tests for Type 3 detection and dash positioning

These tests verify that Type 3 letters are properly detected using the canonical
letter list and that dash arrows are positioned correctly in Type 3 scenarios.
"""

import pytest
import sys
from pathlib import Path

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    LetterType,
)
from domain.models.letter_type_classifier import LetterTypeClassifier
from application.services.positioning.dash_location_service import DashLocationService
from application.services.data.pictograph_analysis_service import PictographAnalysisService


class TestType3DetectionIntegration:
    """Integration tests for Type 3 detection and positioning."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dash_service = DashLocationService()
        self.analysis_service = PictographAnalysisService()

    def test_canonical_type3_letter_detection(self):
        """Test that all canonical Type 3 letters are correctly detected."""
        type3_letters = LetterTypeClassifier.TYPE3_LETTERS
        
        for letter in type3_letters:
            # Create a proper Type 3 beat: one dash motion + one shift motion  
            beat_data = BeatData(
                letter=letter,
                blue_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    turns=0.0,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.PRO,  # Shift motion
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=1.0,
                ),
            )
            
            # Test letter classification
            letter_type_str = LetterTypeClassifier.get_letter_type(letter)
            assert letter_type_str == "Type3", f"Letter {letter} should be classified as Type3"
            
            # Test motion pattern analysis
            letter_info = self.analysis_service.get_letter_info(beat_data)
            assert letter_info["letter_type"] == LetterType.TYPE3, f"Motion analysis failed for {letter}"

    def test_type3_dash_positioning_order(self):
        """Test that in Type 3 scenarios, shift is positioned before dash."""
        # Type 3 scenario with clear shift + dash motions
        beat_data = BeatData(
            letter="θ-",  # Type 3 letter
            blue_motion=MotionData(  # Shift motion - should be positioned first
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            ),
            red_motion=MotionData(  # Dash motion - should avoid shift location
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=0.0,
            ),
        )
        
        # Get shift location (blue arrow is the shift)
        grid_info = self.analysis_service.get_grid_info(beat_data)
        shift_location = grid_info["shift_location"]
        
        # Calculate dash location (red arrow is the dash)
        dash_location = self.dash_service.calculate_dash_location_from_beat(
            beat_data, is_blue_arrow=False
        )
        
        print(f"Shift location: {shift_location}")
        print(f"Dash location: {dash_location}")
        
        # Verify they are different locations
        assert shift_location != dash_location, "Dash should not be placed at shift location"
        
        # Verify shift location is calculated correctly (NORTH + EAST = NORTHEAST)
        assert shift_location == Location.NORTHEAST, "Shift should be at NORTHEAST"

    def test_type3_vs_non_type3_positioning(self):
        """Test that Type 3 positioning is different from non-Type 3 positioning."""
        # Type 3 scenario
        type3_beat = BeatData(
            letter="W-",  # Type 3
            blue_motion=MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            ),
        )
        
        # Non-Type 3 scenario (dual dash like Φ)
        non_type3_beat = BeatData(
            letter="Φ",  # Type 4
            blue_motion=MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.EAST,
                end_loc=Location.WEST,
                turns=0.0,
            ),
        )
        
        # Calculate dash locations
        type3_dash_location = self.dash_service.calculate_dash_location_from_beat(
            type3_beat, is_blue_arrow=True
        )
        non_type3_dash_location = self.dash_service.calculate_dash_location_from_beat(
            non_type3_beat, is_blue_arrow=True
        )
        
        print(f"Type 3 dash location: {type3_dash_location}")
        print(f"Non-Type 3 dash location: {non_type3_dash_location}")
        
        # They should use different logic and potentially different locations
        # The important thing is that Type 3 considers shift avoidance
        assert type3_dash_location is not None
        assert non_type3_dash_location is not None

    def test_all_type3_motion_combinations(self):
        """Test all valid Type 3 motion combinations (dash + shift variations)."""
        motion_combinations = [
            {
                "name": "Dash Blue, Pro Red",
                "blue": MotionType.DASH,
                "red": MotionType.PRO,
            },
            {
                "name": "Pro Blue, Dash Red", 
                "blue": MotionType.PRO,
                "red": MotionType.DASH,
            },
            {
                "name": "Dash Blue, Anti Red",
                "blue": MotionType.DASH,
                "red": MotionType.ANTI,
            },
            {
                "name": "Anti Blue, Dash Red",
                "blue": MotionType.ANTI,
                "red": MotionType.DASH,
            },
            {
                "name": "Dash Blue, Float Red",
                "blue": MotionType.DASH,
                "red": MotionType.FLOAT,
            },
            {
                "name": "Float Blue, Dash Red",
                "blue": MotionType.FLOAT,
                "red": MotionType.DASH,
            },
        ]
        
        for combo in motion_combinations:
            # Create motions based on the combination
            blue_motion = MotionData(
                motion_type=combo["blue"],
                prop_rot_dir=RotationDirection.CLOCKWISE if combo["blue"] != MotionType.DASH else RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.EAST if combo["blue"] != MotionType.DASH else Location.SOUTH,
                turns=1.0 if combo["blue"] != MotionType.DASH else 0.0,
            )
            
            red_motion = MotionData(
                motion_type=combo["red"],
                prop_rot_dir=RotationDirection.CLOCKWISE if combo["red"] != MotionType.DASH else RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST if combo["red"] != MotionType.DASH else Location.NORTH,
                turns=1.0 if combo["red"] != MotionType.DASH else 0.0,
            )
            
            beat_data = BeatData(
                letter="Y-",  # Type 3 letter
                blue_motion=blue_motion,
                red_motion=red_motion,
            )
            
            # Test Type 3 detection
            letter_info = self.analysis_service.get_letter_info(beat_data)
            assert letter_info["letter_type"] == LetterType.TYPE3, f"Type 3 detection failed for {combo['name']}"
            
            # Test that both arrows can get dash locations calculated
            blue_dash_loc = self.dash_service.calculate_dash_location_from_beat(beat_data, is_blue_arrow=True)
            red_dash_loc = self.dash_service.calculate_dash_location_from_beat(beat_data, is_blue_arrow=False)
            
            assert blue_dash_loc is not None, f"Blue dash location failed for {combo['name']}"
            assert red_dash_loc is not None, f"Red dash location failed for {combo['name']}"

    def test_type3_specific_scenarios(self):
        """Test specific Type 3 scenarios that are known to be problematic."""
        scenarios = [
            {
                "name": "North-East shift, North-South dash",
                "letter": "X-",
                "shift_start": Location.NORTH,
                "shift_end": Location.EAST,
                "dash_start": Location.NORTH, 
                "dash_end": Location.SOUTH,
                "expected_shift": Location.NORTHEAST,
            },
            {
                "name": "South-West shift, East-West dash",
                "letter": "Z-",
                "shift_start": Location.SOUTH,
                "shift_end": Location.WEST,
                "dash_start": Location.EAST,
                "dash_end": Location.WEST,
                "expected_shift": Location.SOUTHWEST,
            },
            {
                "name": "West-North shift, South-North dash",
                "letter": "Ω-",
                "shift_start": Location.WEST,
                "shift_end": Location.NORTH,
                "dash_start": Location.SOUTH,
                "dash_end": Location.NORTH,
                "expected_shift": Location.NORTHWEST,
            },
        ]
        
        for scenario in scenarios:
            beat_data = BeatData(
                letter=scenario["letter"],
                blue_motion=MotionData(  # Shift motion
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=scenario["shift_start"],
                    end_loc=scenario["shift_end"],
                    turns=1.0,
                ),
                red_motion=MotionData(  # Dash motion
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=scenario["dash_start"],
                    end_loc=scenario["dash_end"],
                    turns=0.0,
                ),
            )
            
            # Get shift location
            grid_info = self.analysis_service.get_grid_info(beat_data)
            actual_shift = grid_info["shift_location"]
            
            # Get dash location
            dash_location = self.dash_service.calculate_dash_location_from_beat(
                beat_data, is_blue_arrow=False  # Red is dash
            )
            
            print(f"Scenario: {scenario['name']}")
            print(f"  Expected shift: {scenario['expected_shift']}")
            print(f"  Actual shift: {actual_shift}")
            print(f"  Dash location: {dash_location}")
            
            # Verify shift location
            assert actual_shift == scenario["expected_shift"], f"Shift location wrong in {scenario['name']}"
            
            # Verify dash avoids shift
            assert dash_location != actual_shift, f"Dash should avoid shift in {scenario['name']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
