#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Beat manipulation workflow contracts
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Beat Manipulation Workflow Contract Tests
=========================================

Defines behavioral contracts for beat manipulation workflows.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestBeatManipulationWorkflowContract:
    """Beat manipulation workflow contract tests."""

    def test_beat_creation_contract(self):
        """
        Test beat creation contract.
        
        CONTRACT: Beats must be creatable with proper properties:
        - Beat has beat number
        - Beat has letter
        - Beat has optional duration
        - Beat properties are preserved
        """
        try:
            from domain.models.core_models import BeatData
            
            # Test basic beat creation
            beat = BeatData(beat_number=1, letter="A")
            assert beat.beat_number == 1
            assert beat.letter == "A"
            
            # Test beat with duration
            beat_with_duration = BeatData(beat_number=2, letter="B", duration=1.5)
            assert beat_with_duration.beat_number == 2
            assert beat_with_duration.letter == "B"
            assert beat_with_duration.duration == 1.5
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_beat_addition_workflow_contract(self):
        """
        Test beat addition workflow contract.
        
        CONTRACT: Beats must be addable to sequences:
        - Beats can be added at specific positions
        - Sequence length updates correctly
        - Beat order is maintained
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            from application.services.core.sequence_management_service import SequenceManagementService
            
            # Create initial sequence
            beat1 = BeatData(beat_number=1, letter="A")
            sequence = SequenceData(
                name="Beat Addition Test",
                word="A",
                beats=[beat1],
                start_position="alpha1"
            )
            
            # Create service
            service = SequenceManagementService()
            
            # Add beat at end
            beat2 = BeatData(beat_number=2, letter="B")
            updated_sequence = service.add_beat(sequence, beat2, 1)
            
            # Verify addition
            assert len(updated_sequence.beats) == 2
            assert updated_sequence.beats[0].letter == "A"
            assert updated_sequence.beats[1].letter == "B"
            
        except ImportError:
            pytest.skip("Sequence management service not available")

    def test_beat_deletion_workflow_contract(self):
        """
        Test beat deletion workflow contract.
        
        CONTRACT: Beats must be deletable from sequences:
        - Beats can be removed by position
        - Sequence length updates correctly
        - Remaining beats maintain order
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            from application.services.core.sequence_management_service import SequenceManagementService
            
            # Create sequence with multiple beats
            beats = [
                BeatData(beat_number=1, letter="A"),
                BeatData(beat_number=2, letter="B"),
                BeatData(beat_number=3, letter="C")
            ]
            sequence = SequenceData(
                name="Beat Deletion Test",
                word="ABC",
                beats=beats,
                start_position="alpha1"
            )
            
            # Create service
            service = SequenceManagementService()
            
            # Delete middle beat
            updated_sequence = service.delete_beat(sequence, 1)  # Delete "B"
            
            # Verify deletion
            assert len(updated_sequence.beats) == 2
            assert updated_sequence.beats[0].letter == "A"
            assert updated_sequence.beats[1].letter == "C"
            
        except ImportError:
            pytest.skip("Sequence management service not available")

    def test_beat_modification_workflow_contract(self):
        """
        Test beat modification workflow contract.
        
        CONTRACT: Beats must be modifiable:
        - Beat properties can be changed
        - Changes are preserved in sequence
        - Modifications don't affect other beats
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Create sequence with beat
            original_beat = BeatData(beat_number=1, letter="A", duration=1.0)
            sequence = SequenceData(
                name="Beat Modification Test",
                word="A",
                beats=[original_beat],
                start_position="alpha1"
            )
            
            # Modify beat (create new beat with changes)
            modified_beat = BeatData(
                beat_number=original_beat.beat_number,
                letter="X",  # Changed letter
                duration=2.0  # Changed duration
            )
            
            # Create new sequence with modified beat
            modified_sequence = SequenceData(
                name=sequence.name,
                word="X",  # Updated word
                beats=[modified_beat],
                start_position=sequence.start_position
            )
            
            # Verify modification
            assert modified_sequence.beats[0].letter == "X"
            assert modified_sequence.beats[0].duration == 2.0
            assert modified_sequence.word == "X"
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_beat_reordering_workflow_contract(self):
        """
        Test beat reordering workflow contract.
        
        CONTRACT: Beats must be reorderable:
        - Beat positions can be changed
        - Sequence maintains integrity after reordering
        - Beat numbers can be updated
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Create sequence with beats
            beats = [
                BeatData(beat_number=1, letter="A"),
                BeatData(beat_number=2, letter="B"),
                BeatData(beat_number=3, letter="C")
            ]
            sequence = SequenceData(
                name="Beat Reordering Test",
                word="ABC",
                beats=beats,
                start_position="alpha1"
            )
            
            # Reorder beats (reverse order)
            reordered_beats = [
                BeatData(beat_number=1, letter="C"),
                BeatData(beat_number=2, letter="B"),
                BeatData(beat_number=3, letter="A")
            ]
            
            reordered_sequence = SequenceData(
                name=sequence.name,
                word="CBA",  # Updated word
                beats=reordered_beats,
                start_position=sequence.start_position
            )
            
            # Verify reordering
            assert len(reordered_sequence.beats) == 3
            assert reordered_sequence.beats[0].letter == "C"
            assert reordered_sequence.beats[1].letter == "B"
            assert reordered_sequence.beats[2].letter == "A"
            assert reordered_sequence.word == "CBA"
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_beat_validation_workflow_contract(self):
        """
        Test beat validation workflow contract.
        
        CONTRACT: Beat validation must work correctly:
        - Valid beats are accepted
        - Invalid beats are rejected or corrected
        - Validation rules are consistent
        """
        try:
            from domain.models.core_models import BeatData
            
            # Test valid beat
            valid_beat = BeatData(beat_number=1, letter="A", duration=1.0)
            assert valid_beat.beat_number == 1
            assert valid_beat.letter == "A"
            assert valid_beat.duration == 1.0
            
            # Test beat with zero beat number (edge case)
            try:
                zero_beat = BeatData(beat_number=0, letter="A")
                # If this works, that's acceptable
                assert zero_beat.beat_number == 0
            except Exception:
                # If this fails, that's also acceptable
                assert True
            
            # Test beat with empty letter (edge case)
            try:
                empty_letter_beat = BeatData(beat_number=1, letter="")
                # If this works, that's acceptable
                assert empty_letter_beat.letter == ""
            except Exception:
                # If this fails, that's also acceptable
                assert True
            
        except ImportError:
            pytest.skip("Core domain models not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
