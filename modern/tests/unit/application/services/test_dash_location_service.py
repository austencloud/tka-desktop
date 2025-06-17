"""
Unit tests for DashLocationService

Tests for Type 3 detection, dash location calculation, and compatibility with legacy logic.
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
    ArrowColor,
    GridMode,
)
from application.services.positioning.dash_location_service import DashLocationService


class TestDashLocationService:
    """Test suite for DashLocationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = DashLocationService()

    def test_type3_detection_canonical_letters(self):
        """Test Type 3 detection using canonical Type 3 letters."""
        type3_letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]

        for letter in type3_letters:
            # Create Type 3 beat data: one dash motion + one shift motion
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
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=1.0,
                ),
            )

            # Test letter info extraction
            letter_info = self.service.analysis_service.get_letter_info(beat_data)
            assert (
                letter_info["letter_type"] == LetterType.TYPE3
            ), f"Failed for letter {letter}"

    def test_type3_dash_arrow_positioning_with_shift_avoidance(self):
        """Test that Type 3 dash arrows avoid shift arrow locations."""
        # Type 3 scenario: shift from NORTH to EAST (shift at NORTHEAST)
        # Dash from NORTH to SOUTH should avoid NORTHEAST

        beat_data = BeatData(
            letter="θ-",  # Type 3 letter
            blue_motion=MotionData(  # Shift motion
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            ),
            red_motion=MotionData(  # Dash motion
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=0.0,
            ),
        )

        # Calculate dash location for red arrow (should avoid shift location)
        dash_location = self.service.calculate_dash_location_from_beat(
            beat_data, is_blue_arrow=False
        )

        # The shift location should be NORTHEAST (north+east)
        grid_info = self.service.analysis_service.get_grid_info(beat_data)
        shift_location = grid_info["shift_location"]

        assert (
            shift_location == Location.NORTHEAST
        ), "Shift location should be NORTHEAST"
        assert (
            dash_location != shift_location
        ), "Dash location should avoid shift location"

    def test_detailed_dash_calculation_parameters(self):
        """Test detailed dash calculation with all parameters."""
        beat_data = BeatData(
            letter="W-",
            blue_motion=MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.EAST,
                end_loc=Location.WEST,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=1.0,
            ),
        )

        # Test detailed calculation method
        letter_info = self.service.analysis_service.get_letter_info(beat_data)
        grid_info = self.service.analysis_service.get_grid_info(beat_data)
        arrow_color = self.service.analysis_service.get_arrow_color(is_blue_arrow=True)
        # Blue arrow is the dash motion
        dash_motion = beat_data.blue_motion
        assert dash_motion is not None, "Blue motion should not be None"

        dash_location = self.service.calculate_dash_location(
            motion=dash_motion,
            letter_type=letter_info["letter_type"],
            is_phi_dash=letter_info["is_phi_dash"],
            is_psi_dash=letter_info["is_psi_dash"],
            is_lambda=letter_info["is_lambda"],
            grid_mode=grid_info["grid_mode"],
            arrow_color=arrow_color,
            shift_location=grid_info["shift_location"],
        )

        assert dash_location is not None
        assert isinstance(dash_location, Location)

    def test_phi_dash_special_case(self):
        """Test Φ_DASH special case handling."""
        beat_data = BeatData(
            letter="Φ-",
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

        letter_info = self.service.analysis_service.get_letter_info(beat_data)
        assert letter_info["is_phi_dash"] is True
        assert letter_info["is_psi_dash"] is False
        assert letter_info["is_lambda"] is False

    def test_psi_dash_special_case(self):
        """Test Ψ- special case handling."""
        beat_data = BeatData(
            letter="Ψ-",
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

        letter_info = self.service.analysis_service.get_letter_info(beat_data)
        assert letter_info["is_phi_dash"] is False
        assert letter_info["is_psi_dash"] is True
        assert letter_info["is_lambda"] is False

    def test_lambda_zero_turns_special_case(self):
        """Test Λ (Lambda) zero turns special case."""
        beat_data = BeatData(
            letter="Λ",
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

        letter_info = self.service.analysis_service.get_letter_info(beat_data)
        assert letter_info["is_lambda"] is True

    def test_grid_mode_diamond_vs_box(self):
        """Test different grid modes (Diamond vs Box)."""
        beat_data = BeatData(
            letter="X-",
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
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                turns=1.0,
            ),
        )

        grid_info = self.service.analysis_service.get_grid_info(beat_data)
        # Default should be Diamond for now
        assert grid_info["grid_mode"] == GridMode.DIAMOND

    def test_arrow_color_determination(self):
        """Test arrow color determination."""
        blue_color = self.service.analysis_service.get_arrow_color(is_blue_arrow=True)
        red_color = self.service.analysis_service.get_arrow_color(is_blue_arrow=False)

        assert blue_color == ArrowColor.BLUE
        assert red_color == ArrowColor.RED

    def test_multiple_type3_scenarios(self):
        """Test multiple Type 3 scenarios with different motion combinations."""
        scenarios = [
            {
                "name": "Dash blue, Pro red",
                "letter": "Y-",
                "blue_motion": MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    turns=0.0,
                ),
                "red_motion": MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.SOUTH,
                    turns=1.0,
                ),
            },
            {
                "name": "Pro blue, Dash red",
                "letter": "Z-",
                "blue_motion": MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.WEST,
                    end_loc=Location.NORTH,
                    turns=1.0,
                ),
                "red_motion": MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                    turns=0.0,
                ),
            },
            {
                "name": "Dash blue, Anti red",
                "letter": "Σ-",
                "blue_motion": MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.NORTH,
                    turns=0.0,
                ),
                "red_motion": MotionData(
                    motion_type=MotionType.ANTI,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.WEST,
                    end_loc=Location.NORTH,
                    turns=1.0,
                ),
            },
        ]

        for scenario in scenarios:
            beat_data = BeatData(
                letter=scenario["letter"],
                blue_motion=scenario["blue_motion"],
                red_motion=scenario["red_motion"],
            )

            # Verify Type 3 detection
            letter_info = self.service.analysis_service.get_letter_info(beat_data)
            assert (
                letter_info["letter_type"] == LetterType.TYPE3
            ), f"Failed Type 3 detection for {scenario['name']}"

            # Verify dash location calculation works
            dash_location_blue = self.service.calculate_dash_location_from_beat(
                beat_data, is_blue_arrow=True
            )
            dash_location_red = self.service.calculate_dash_location_from_beat(
                beat_data, is_blue_arrow=False
            )

            assert (
                dash_location_blue is not None
            ), f"Blue dash location failed for {scenario['name']}"
            assert (
                dash_location_red is not None
            ), f"Red dash location failed for {scenario['name']}"

    def test_non_type3_scenarios(self):
        """Test non-Type 3 scenarios for comparison."""
        # Type 1 scenario (dual shift)
        beat_data_type1 = BeatData(
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=1.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=1.0,
            ),
        )

        letter_info = self.service.analysis_service.get_letter_info(beat_data_type1)
        assert letter_info["letter_type"] != LetterType.TYPE3

        # Type 4 scenario (dash letters)
        beat_data_type4 = BeatData(
            letter="Φ",
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

        letter_info = self.service.analysis_service.get_letter_info(beat_data_type4)
        assert letter_info["letter_type"] != LetterType.TYPE3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
