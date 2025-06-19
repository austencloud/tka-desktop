#!/usr/bin/env python3
"""
Domain Model Test Fixtures
==========================

Provides reusable domain model fixtures for testing.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


@pytest.fixture
def sample_beat_data():
    """Provide sample beat data for testing."""
    try:
        from domain.models.core_models import BeatData
        
        beat = BeatData(
            beat_number=1,
            letter="A",
            duration=1.0
        )
        
        return beat
        
    except ImportError:
        pytest.skip("Core domain models not available")


@pytest.fixture
def sample_sequence_data():
    """Provide sample sequence data for testing."""
    try:
        from domain.models.core_models import SequenceData, BeatData
        
        beats = [
            BeatData(beat_number=1, letter="A", duration=1.0),
            BeatData(beat_number=2, letter="B", duration=1.0)
        ]
        
        sequence = SequenceData(
            name="Test Sequence",
            word="AB",
            beats=beats,
            start_position="alpha1"
        )
        
        return sequence
        
    except ImportError:
        pytest.skip("Core domain models not available")


@pytest.fixture
def empty_sequence_data():
    """Provide empty sequence data for testing."""
    try:
        from domain.models.core_models import SequenceData
        
        return SequenceData.empty()
        
    except ImportError:
        pytest.skip("Core domain models not available")


@pytest.fixture
def sample_motion_data():
    """Provide sample motion data for testing."""
    try:
        from domain.models.core_models import (
            MotionData, MotionType, RotationDirection, Location
        )
        
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            start_ori="in",
            end_ori="out"
        )
        
        return motion
        
    except ImportError:
        pytest.skip("Motion domain models not available")


@pytest.fixture
def sample_pictograph_data():
    """Provide sample pictograph data for testing."""
    try:
        from domain.models.pictograph_models import (
            PictographData, GridData, GridMode, ArrowData
        )
        from domain.models.core_models import (
            MotionData, MotionType, RotationDirection, Location
        )
        
        # Create motion data
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0
        )
        
        # Create arrow data
        arrow = ArrowData(
            color="blue",
            motion_data=motion,
            is_visible=True
        )
        
        # Create grid data
        grid = GridData(
            grid_mode=GridMode.DIAMOND,
            center_x=475.0,
            center_y=475.0,
            radius=100.0
        )
        
        # Create pictograph
        pictograph = PictographData(
            grid_data=grid,
            arrows={"blue": arrow},
            is_blank=False
        )
        
        return pictograph
        
    except ImportError:
        pytest.skip("Pictograph domain models not available")


@pytest.fixture
def type1_letters():
    """Provide Type 1 letters for testing."""
    return ["A", "B", "D", "G"]


@pytest.fixture
def type2_letters():
    """Provide Type 2 letters for testing."""
    return ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]


@pytest.fixture
def valid_start_positions():
    """Provide valid start positions for testing."""
    return [
        "alpha1", "alpha2", "alpha3", "alpha4",
        "alpha5", "alpha6", "alpha7", "alpha8",
        "beta1", "beta2", "beta3", "beta4",
        "beta5", "beta6", "beta7", "beta8"
    ]
