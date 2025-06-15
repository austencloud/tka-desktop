"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Contract testing for MotionManagementService consolidation
SCOPE: Unified motion validation, combination, and orientation operations
EXPECTED_DURATION: permanent
"""

import pytest
from typing import List, Tuple

from application.services.motion.motion_management_service import (
    MotionManagementService,
    IMotionManagementService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
    BeatData,
)


@pytest.fixture
def motion_service():
    """Provide MotionManagementService instance for testing."""
    return MotionManagementService()


@pytest.fixture
def sample_pro_motion():
    """Provide sample PRO motion for testing."""
    return MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=1.0,
    )


@pytest.fixture
def sample_anti_motion():
    """Provide sample ANTI motion for testing."""
    return MotionData(
        motion_type=MotionType.ANTI,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.EAST,
        end_loc=Location.WEST,
        turns=1.0,
    )


@pytest.fixture
def sample_static_motion():
    """Provide sample STATIC motion for testing."""
    return MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        start_loc=Location.NORTHEAST,
        end_loc=Location.NORTHEAST,
        turns=0.0,
    )


class TestMotionManagementServiceInterface:
    """Test that MotionManagementService implements the interface correctly."""
    
    def test_implements_interface(self, motion_service):
        """Test that service implements IMotionManagementService."""
        # Note: Python Protocols don't work with isinstance, check methods instead
        interface_methods = [
            'validate_motion_combination',
            'get_valid_motion_combinations',
            'calculate_motion_orientation',
            'get_motion_validation_errors',
            'generate_motion_combinations_for_letter',
        ]
        
        for method_name in interface_methods:
            assert hasattr(motion_service, method_name), f"Should have {method_name} method"
            assert callable(getattr(motion_service, method_name)), f"{method_name} should be callable"


class TestMotionValidation:
    """Test motion combination validation."""
    
    def test_validate_motion_combination_valid(
        self, motion_service, sample_pro_motion, sample_anti_motion
    ):
        """Test validation of valid motion combination."""
        is_valid = motion_service.validate_motion_combination(
            sample_pro_motion, sample_anti_motion
        )
        
        assert isinstance(is_valid, bool), "Should return boolean"
        # Most combinations should be valid unless specifically invalid
        assert is_valid is True, "PRO + ANTI should be valid combination"
    
    def test_validate_motion_combination_invalid(self, motion_service):
        """Test validation of invalid motion combination."""
        # Create potentially invalid combination (same location pattern)
        motion1 = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )
        
        motion2 = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )
        
        is_valid = motion_service.validate_motion_combination(motion1, motion2)
        
        assert isinstance(is_valid, bool), "Should return boolean"
        # This specific combination might be invalid due to identical patterns
    
    def test_get_motion_validation_errors_valid(
        self, motion_service, sample_pro_motion, sample_anti_motion
    ):
        """Test getting validation errors for valid combination."""
        errors = motion_service.get_motion_validation_errors(
            sample_pro_motion, sample_anti_motion
        )
        
        assert isinstance(errors, list), "Should return list of errors"
        assert len(errors) == 0, "Valid combination should have no errors"
    
    def test_get_motion_validation_errors_invalid(self, motion_service):
        """Test getting validation errors for invalid combination."""
        # Create combination with invalid rotation (both NO_ROTATION)
        motion1 = MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            turns=0.0,
        )
        
        motion2 = MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.SOUTH,
            end_loc=Location.SOUTH,
            turns=0.0,
        )
        
        errors = motion_service.get_motion_validation_errors(motion1, motion2)
        
        assert isinstance(errors, list), "Should return list of errors"
        # This combination might have rotation validation errors


class TestMotionCombinationGeneration:
    """Test motion combination generation."""
    
    def test_get_valid_motion_combinations(self, motion_service):
        """Test getting valid motion combinations for type and location."""
        combinations = motion_service.get_valid_motion_combinations(
            MotionType.PRO, Location.NORTH
        )
        
        assert isinstance(combinations, list), "Should return list"
        assert len(combinations) > 0, "Should generate some combinations"
        
        # Check that all returned motions are valid
        for motion in combinations:
            assert isinstance(motion, MotionData), "Should return MotionData objects"
            assert motion.motion_type == MotionType.PRO, "Should match requested type"
            assert motion.start_loc == Location.NORTH, "Should match requested location"
    
    def test_get_valid_motion_combinations_static(self, motion_service):
        """Test getting valid combinations for STATIC motion type."""
        combinations = motion_service.get_valid_motion_combinations(
            MotionType.STATIC, Location.EAST
        )
        
        assert isinstance(combinations, list), "Should return list"
        
        # STATIC motions should have 0 turns
        for motion in combinations:
            assert motion.motion_type == MotionType.STATIC
            assert motion.turns == 0.0, "STATIC motions should have 0 turns"
            assert motion.start_loc == motion.end_loc, "STATIC motions don't move"
    
    def test_generate_motion_combinations_for_letter(self, motion_service):
        """Test generating motion combinations for specific letter."""
        combinations = motion_service.generate_motion_combinations_for_letter("A")
        
        assert isinstance(combinations, list), "Should return list"
        assert len(combinations) <= 50, "Should limit combinations to prevent explosion"
        
        # Check that all combinations are tuples of two motions
        for combination in combinations:
            assert isinstance(combination, tuple), "Should return tuples"
            assert len(combination) == 2, "Should have blue and red motion"
            
            blue_motion, red_motion = combination
            assert isinstance(blue_motion, MotionData), "Blue should be MotionData"
            assert isinstance(red_motion, MotionData), "Red should be MotionData"
            
            # Verify the combination is valid
            is_valid = motion_service.validate_motion_combination(blue_motion, red_motion)
            assert is_valid, "Generated combinations should be valid"


class TestMotionOrientation:
    """Test motion orientation calculations."""
    
    def test_calculate_motion_orientation_pro_even_turns(self, motion_service):
        """Test orientation calculation for PRO motion with even turns."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2.0,  # Even turns
        )
        
        end_orientation = motion_service.calculate_motion_orientation(
            motion, Orientation.IN
        )
        
        assert isinstance(end_orientation, Orientation), "Should return Orientation"
        # PRO with even turns should maintain orientation
        assert end_orientation == Orientation.IN, "Even turns should maintain orientation"
    
    def test_calculate_motion_orientation_pro_odd_turns(self, motion_service):
        """Test orientation calculation for PRO motion with odd turns."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,  # Odd turns
        )
        
        end_orientation = motion_service.calculate_motion_orientation(
            motion, Orientation.IN
        )
        
        assert isinstance(end_orientation, Orientation), "Should return Orientation"
        # PRO with odd turns should flip orientation
        assert end_orientation == Orientation.OUT, "Odd turns should flip orientation"
    
    def test_calculate_motion_orientation_anti_even_turns(self, motion_service):
        """Test orientation calculation for ANTI motion with even turns."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2.0,  # Even turns
        )
        
        end_orientation = motion_service.calculate_motion_orientation(
            motion, Orientation.IN
        )
        
        assert isinstance(end_orientation, Orientation), "Should return Orientation"
        # ANTI with even turns should flip orientation
        assert end_orientation == Orientation.OUT, "ANTI even turns should flip orientation"
    
    def test_calculate_motion_orientation_half_turns(self, motion_service):
        """Test orientation calculation for half turns."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            turns=0.5,  # Half turn
        )
        
        end_orientation = motion_service.calculate_motion_orientation(
            motion, Orientation.IN
        )
        
        assert isinstance(end_orientation, Orientation), "Should return Orientation"
        # Half turns always flip orientation
        assert end_orientation == Orientation.OUT, "Half turns should always flip orientation"
    
    def test_calculate_motion_orientation_default_start(self, motion_service):
        """Test orientation calculation with default start orientation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )
        
        # Test with default start orientation (should be IN)
        end_orientation = motion_service.calculate_motion_orientation(motion)
        
        assert isinstance(end_orientation, Orientation), "Should return Orientation"
        # Should work with default start orientation


class TestMotionManagementIntegration:
    """Test integration between different motion management features."""
    
    def test_validation_and_generation_consistency(self, motion_service):
        """Test that generated combinations pass validation."""
        # Generate combinations for a letter
        combinations = motion_service.generate_motion_combinations_for_letter("A")
        
        # Verify all generated combinations are valid
        for blue_motion, red_motion in combinations:
            is_valid = motion_service.validate_motion_combination(blue_motion, red_motion)
            assert is_valid, "Generated combinations should pass validation"
            
            errors = motion_service.get_motion_validation_errors(blue_motion, red_motion)
            assert len(errors) == 0, "Generated combinations should have no validation errors"
    
    def test_orientation_calculation_consistency(self, motion_service):
        """Test that orientation calculations are consistent."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )
        
        # Calculate orientation multiple times - should be consistent
        orientation1 = motion_service.calculate_motion_orientation(motion, Orientation.IN)
        orientation2 = motion_service.calculate_motion_orientation(motion, Orientation.IN)
        
        assert orientation1 == orientation2, "Orientation calculation should be deterministic"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
