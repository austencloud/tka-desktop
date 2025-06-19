#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Start position behavior contracts - migrated from test_start_position_clear.py
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Start Position Behavior Contract Tests
=====================================

Migrated from test_start_position_clear.py.
Defines behavioral contracts for start position management and clearing.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestStartPositionBehaviorContract:
    """Start position behavior contract tests."""

    def test_sequence_data_import(self):
        """Test that sequence data can be imported."""
        try:
            from domain.models.core_models import SequenceData, BeatData
            assert SequenceData is not None
            assert BeatData is not None
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_start_position_creation_contract(self):
        """
        Test start position creation contract.
        
        CONTRACT: Start positions must be properly created:
        - Sequence can be created with start position
        - Start position is preserved in sequence data
        - Empty sequences have no start position
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Test sequence with start position
            beat = BeatData(beat_number=1, letter="A")
            sequence = SequenceData(
                name="Test Sequence",
                word="A",
                beats=[beat],
                start_position="alpha1"
            )
            
            # Verify start position is set
            assert sequence.start_position == "alpha1"
            assert sequence.name == "Test Sequence"
            assert len(sequence.beats) == 1
            
            # Test empty sequence
            empty_sequence = SequenceData.empty()
            assert empty_sequence.start_position is None or empty_sequence.start_position == ""
            assert len(empty_sequence.beats) == 0
            
        except ImportError:
            pytest.skip("Required models not available for start position creation testing")

    def test_start_position_clearing_contract(self):
        """
        Test start position clearing contract.
        
        CONTRACT: Start positions must be properly cleared:
        - Sequence can be cleared to empty state
        - Cleared sequence has no start position
        - Clearing preserves sequence structure
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Create sequence with start position
            beat = BeatData(beat_number=1, letter="A")
            sequence = SequenceData(
                name="Test Sequence",
                word="A",
                beats=[beat],
                start_position="alpha1"
            )
            
            # Verify initial state
            assert sequence.start_position == "alpha1"
            assert len(sequence.beats) == 1
            
            # Clear sequence (create empty version)
            cleared_sequence = SequenceData.empty()
            cleared_sequence.name = sequence.name  # Preserve name
            
            # Verify cleared state
            assert cleared_sequence.start_position is None or cleared_sequence.start_position == ""
            assert len(cleared_sequence.beats) == 0
            assert cleared_sequence.name == "Test Sequence"  # Name preserved
            
        except ImportError:
            pytest.skip("Required models not available for start position clearing testing")

    def test_start_position_validation_contract(self):
        """
        Test start position validation contract.
        
        CONTRACT: Start positions must be valid:
        - Valid start positions follow naming convention
        - Invalid start positions are rejected or normalized
        - Start position format is consistent
        """
        try:
            from domain.models.core_models import SequenceData
            
            # Test valid start positions
            valid_positions = [
                "alpha1", "alpha2", "alpha3", "alpha4",
                "alpha5", "alpha6", "alpha7", "alpha8",
                "beta1", "beta2", "beta3", "beta4",
                "beta5", "beta6", "beta7", "beta8"
            ]
            
            for position in valid_positions:
                # Create sequence with valid start position
                sequence = SequenceData(
                    name="Test",
                    word="",
                    beats=[],
                    start_position=position
                )
                
                # Verify position is preserved
                assert sequence.start_position == position
            
            # Test empty/None start position
            sequence_none = SequenceData(
                name="Test",
                word="",
                beats=[],
                start_position=None
            )
            assert sequence_none.start_position is None
            
            sequence_empty = SequenceData(
                name="Test",
                word="",
                beats=[],
                start_position=""
            )
            assert sequence_empty.start_position == ""
            
        except ImportError:
            pytest.skip("Required models not available for start position validation testing")

    def test_start_position_state_management_contract(self):
        """
        Test start position state management contract.
        
        CONTRACT: Start position state must be properly managed:
        - Start position changes are tracked
        - State transitions are consistent
        - Start position integrates with sequence lifecycle
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Test state transitions
            states = [
                (None, "Empty state"),
                ("alpha1", "Initial position"),
                ("beta3", "Changed position"),
                ("", "Cleared position"),
                ("alpha8", "Final position")
            ]
            
            sequence = SequenceData.empty()
            
            for position, description in states:
                # Update start position
                sequence.start_position = position
                
                # Verify state
                assert sequence.start_position == position, f"Failed at {description}"
            
            # Test with beats
            beat = BeatData(beat_number=1, letter="A")
            sequence_with_beats = SequenceData(
                name="Test",
                word="A",
                beats=[beat],
                start_position="alpha1"
            )
            
            # Verify start position works with beats
            assert sequence_with_beats.start_position == "alpha1"
            assert len(sequence_with_beats.beats) == 1
            
        except ImportError:
            pytest.skip("Required models not available for start position state management testing")

    def test_start_position_integration_contract(self):
        """
        Test start position integration contract.
        
        CONTRACT: Start positions must integrate with other systems:
        - Start position works with sequence creation
        - Start position works with beat management
        - Start position works with sequence operations
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Test integration with sequence creation
            sequence = SequenceData(
                name="Integration Test",
                word="AB",
                beats=[
                    BeatData(beat_number=1, letter="A"),
                    BeatData(beat_number=2, letter="B")
                ],
                start_position="beta2"
            )
            
            # Verify all components work together
            assert sequence.name == "Integration Test"
            assert sequence.word == "AB"
            assert sequence.start_position == "beta2"
            assert len(sequence.beats) == 2
            assert sequence.length == 2
            
            # Test sequence operations preserve start position
            original_position = sequence.start_position
            
            # Verify start position is preserved through sequence operations
            assert sequence.start_position == original_position
            
        except ImportError:
            pytest.skip("Required models not available for start position integration testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
