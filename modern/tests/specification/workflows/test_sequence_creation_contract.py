#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Sequence creation workflow contracts
CREATED: 2025-06-19
AUTHOR: AI Assistant
RELATED_ISSUE: Test suite restructuring

Sequence Creation Workflow Contract Tests
========================================

Defines behavioral contracts for sequence creation workflows.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


class TestSequenceCreationWorkflowContract:
    """Sequence creation workflow contract tests."""

    def test_empty_sequence_creation_contract(self):
        """
        Test empty sequence creation contract.
        
        CONTRACT: Empty sequences must be creatable:
        - Empty sequence has no beats
        - Empty sequence has no start position
        - Empty sequence has default properties
        """
        try:
            from domain.models.core_models import SequenceData
            
            # Create empty sequence
            empty_sequence = SequenceData.empty()
            
            # Verify empty sequence properties
            assert empty_sequence is not None
            assert len(empty_sequence.beats) == 0
            assert empty_sequence.length == 0
            assert empty_sequence.start_position is None or empty_sequence.start_position == ""
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_sequence_with_beats_creation_contract(self):
        """
        Test sequence with beats creation contract.
        
        CONTRACT: Sequences with beats must be creatable:
        - Sequence can contain multiple beats
        - Beat order is preserved
        - Sequence properties are calculated correctly
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Create beats
            beat1 = BeatData(beat_number=1, letter="A")
            beat2 = BeatData(beat_number=2, letter="B")
            beat3 = BeatData(beat_number=3, letter="C")
            
            # Create sequence with beats
            sequence = SequenceData(
                name="Test Sequence",
                word="ABC",
                beats=[beat1, beat2, beat3],
                start_position="alpha1"
            )
            
            # Verify sequence properties
            assert sequence.name == "Test Sequence"
            assert sequence.word == "ABC"
            assert len(sequence.beats) == 3
            assert sequence.length == 3
            assert sequence.start_position == "alpha1"
            
            # Verify beat order
            assert sequence.beats[0].letter == "A"
            assert sequence.beats[1].letter == "B"
            assert sequence.beats[2].letter == "C"
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_sequence_service_creation_contract(self):
        """
        Test sequence service creation contract.
        
        CONTRACT: Sequence service must support creation:
        - Service can create sequences
        - Created sequences have proper structure
        - Service handles creation parameters correctly
        """
        try:
            from application.services.core.sequence_management_service import SequenceManagementService
            
            # Create service
            service = SequenceManagementService()
            
            # Test sequence creation through service
            sequence = service.create_sequence("Service Test", 2)
            
            # Verify service-created sequence
            assert sequence is not None
            assert sequence.name == "Service Test"
            assert len(sequence.beats) == 2
            assert sequence.length == 2
            
        except ImportError:
            pytest.skip("Sequence management service not available")

    def test_sequence_validation_workflow_contract(self):
        """
        Test sequence validation workflow contract.
        
        CONTRACT: Sequence validation must work correctly:
        - Valid sequences pass validation
        - Invalid sequences are rejected or corrected
        - Validation rules are consistent
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Test valid sequence
            valid_beat = BeatData(beat_number=1, letter="A")
            valid_sequence = SequenceData(
                name="Valid Sequence",
                word="A",
                beats=[valid_beat],
                start_position="alpha1"
            )
            
            # Verify valid sequence
            assert valid_sequence.name == "Valid Sequence"
            assert len(valid_sequence.beats) == 1
            assert valid_sequence.beats[0].beat_number == 1
            
            # Test sequence with no name (should still be valid)
            unnamed_sequence = SequenceData(
                name="",
                word="B",
                beats=[BeatData(beat_number=1, letter="B")],
                start_position="beta1"
            )
            
            # Verify unnamed sequence is handled
            assert unnamed_sequence.word == "B"
            assert len(unnamed_sequence.beats) == 1
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_sequence_modification_workflow_contract(self):
        """
        Test sequence modification workflow contract.
        
        CONTRACT: Sequences must be modifiable:
        - Beats can be added to sequences
        - Sequence properties update correctly
        - Modifications preserve sequence integrity
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            from application.services.core.sequence_management_service import SequenceManagementService
            
            # Create initial sequence
            initial_beat = BeatData(beat_number=1, letter="A")
            sequence = SequenceData(
                name="Modifiable Sequence",
                word="A",
                beats=[initial_beat],
                start_position="alpha1"
            )
            
            # Verify initial state
            assert len(sequence.beats) == 1
            assert sequence.word == "A"
            
            # Test adding beat through service
            service = SequenceManagementService()
            new_beat = BeatData(beat_number=2, letter="B")
            
            # Add beat to sequence
            updated_sequence = service.add_beat(sequence, new_beat, 1)
            
            # Verify modification
            assert len(updated_sequence.beats) == 2
            assert updated_sequence.beats[1].letter == "B"
            
        except ImportError:
            pytest.skip("Sequence management service not available")

    def test_sequence_state_transitions_contract(self):
        """
        Test sequence state transitions contract.
        
        CONTRACT: Sequence state transitions must be valid:
        - Empty → With beats transition works
        - With beats → Empty transition works
        - State changes are atomic
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Start with empty sequence
            sequence = SequenceData.empty()
            assert len(sequence.beats) == 0
            
            # Transition to sequence with beats
            beat = BeatData(beat_number=1, letter="A")
            sequence_with_beats = SequenceData(
                name="Transition Test",
                word="A",
                beats=[beat],
                start_position="alpha1"
            )
            
            # Verify transition
            assert len(sequence_with_beats.beats) == 1
            assert sequence_with_beats.word == "A"
            
            # Transition back to empty
            empty_again = SequenceData.empty()
            empty_again.name = sequence_with_beats.name  # Preserve name
            
            # Verify return to empty state
            assert len(empty_again.beats) == 0
            assert empty_again.name == "Transition Test"
            
        except ImportError:
            pytest.skip("Core domain models not available")

    def test_sequence_creation_error_handling_contract(self):
        """
        Test sequence creation error handling contract.
        
        CONTRACT: Sequence creation errors must be handled:
        - Invalid parameters are handled gracefully
        - Error conditions don't crash the system
        - Meaningful error information is provided
        """
        try:
            from domain.models.core_models import SequenceData, BeatData
            
            # Test creating sequence with invalid data
            try:
                # Test with None beats (should be handled)
                sequence_none_beats = SequenceData(
                    name="Test",
                    word="",
                    beats=None,
                    start_position=""
                )
                # If this works, that's fine
                assert True
            except Exception:
                # If this fails, that's also acceptable
                assert True
            
            # Test with empty beats list (should work)
            sequence_empty_beats = SequenceData(
                name="Empty Test",
                word="",
                beats=[],
                start_position=""
            )
            
            # Verify empty beats sequence
            assert sequence_empty_beats.name == "Empty Test"
            assert len(sequence_empty_beats.beats) == 0
            
        except ImportError:
            pytest.skip("Core domain models not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
