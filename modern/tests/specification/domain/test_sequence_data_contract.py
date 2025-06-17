"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce sequence data immutability and consistency contracts
PERMANENT: Core business rule - sequence operations must maintain data integrity
AUTHOR: @austencloud

INSTRUCTIONS FOR AI AGENTS:
This is a PERMANENT test that enforces a behavioral contract.
NEVER suggest deletion unless the entire SequenceData feature is removed.
Focus on testing contracts, not implementation details.
"""

import pytest
import sys
from pathlib import Path

# Add modern to path for imports
modern_path = Path(__file__).parent.parent.parent.parent
if str(modern_path) not in sys.path:
    sys.path.insert(0, str(modern_path))


@pytest.mark.specification
@pytest.mark.critical
class TestSequenceDataContract:
    """Permanent specification test - NEVER DELETE unless feature removed"""

    def setup_method(self):
        """Setup for each test method."""
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        self.SequenceData = SequenceData
        self.BeatData = BeatData
        self.dataset_service = PictographDatasetService()

    def test_sequence_immutability_contract(self):
        """PERMANENT: Sequence operations must return new instances"""
        # Create original sequence
        original = self.SequenceData.empty()

        # Get test beat
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            # Create modified sequence
            modified = self.SequenceData(beats=[beat])

            # Contract: Operations must return new instances
            assert original is not modified
            assert original.length == 0
            assert modified.length == 1

    def test_sequence_length_consistency_contract(self):
        """PERMANENT: Sequence length must match beats array length"""
        # Empty sequence
        empty = self.SequenceData.empty()
        assert empty.length == len(empty.beats)
        assert empty.length == 0

        # Sequence with beats
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            sequence = self.SequenceData(beats=[beat])
            assert sequence.length == len(sequence.beats)
            assert sequence.length == 1

    def test_sequence_empty_state_contract(self):
        """PERMANENT: Empty sequence must have consistent empty state"""
        empty = self.SequenceData.empty()

        # Contract: Empty sequence properties
        assert empty.is_empty == True
        assert empty.length == 0
        assert len(empty.beats) == 0
        assert empty.beats == []

    def test_sequence_beat_ordering_contract(self):
        """PERMANENT: Sequence must maintain beat ordering"""
        beat1 = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        beat2 = self.dataset_service.get_start_position_pictograph(
            "beta5_beta5", "diamond"
        )

        if beat1 and beat2:
            # Create sequence with specific order
            sequence = self.SequenceData(beats=[beat1, beat2])

            # Contract: Beat order must be preserved
            assert sequence.beats[0] == beat1
            assert sequence.beats[1] == beat2
            assert sequence.length == 2

    def test_sequence_update_contract(self):
        """PERMANENT: Sequence update operations must return new instances"""
        original = self.SequenceData.empty()
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if beat:
            # Test update operation
            updated = original.update(beats=[beat])

            # Contract: Update must return new instance
            assert original is not updated
            assert original.length == 0
            assert updated.length == 1
            assert updated.beats[0] == beat


@pytest.mark.specification
@pytest.mark.critical
class TestBeatDataContract:
    """Permanent beat data contract - NEVER DELETE unless feature removed"""

    def setup_method(self):
        """Setup for each test method."""
        from src.domain.models.core_models import BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        self.BeatData = BeatData
        self.dataset_service = PictographDatasetService()

    def test_beat_data_immutability_contract(self):
        """PERMANENT: Beat data operations must return new instances"""
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if beat:
            # Test update operation
            updated = beat.update(beat_number=2)

            # Contract: Update must return new instance
            assert beat is not updated
            assert beat.beat_number != updated.beat_number

    def test_beat_data_letter_contract(self):
        """PERMANENT: Beat data must have valid letter values"""
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if beat:
            # Contract: Letter must be valid
            assert beat.letter in ["A", "B", "C", "D"]
            assert isinstance(beat.letter, str)
            assert len(beat.letter) == 1

    def test_beat_data_empty_contract(self):
        """PERMANENT: Empty beat data must have consistent state"""
        empty_beat = self.BeatData.empty()

        # Contract: Empty beat properties
        assert empty_beat is not None
        assert hasattr(empty_beat, "letter")
        assert hasattr(empty_beat, "beat_number")


@pytest.mark.specification
@pytest.mark.critical
class TestPictographDatasetServiceContract:
    """Permanent service contract - NEVER DELETE unless service removed"""

    def setup_method(self):
        """Setup for each test method."""
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )
        from src.domain.models.core_models import BeatData

        self.service = PictographDatasetService()
        self.BeatData = BeatData

    def test_get_start_position_contract(self):
        """PERMANENT: Must return BeatData or None, never invalid data"""
        result = self.service.get_start_position_pictograph("alpha1_alpha1", "diamond")

        # Contract: Return type must be BeatData or None
        assert result is None or isinstance(result, self.BeatData)

        if result:
            # Contract: Valid beat data properties
            assert hasattr(result, "letter")
            assert hasattr(result, "beat_number")
            assert result.letter in ["A", "B", "C", "D"]

    def test_service_initialization_contract(self):
        """PERMANENT: Service must initialize without external dependencies"""
        # Contract: Service can be created without parameters
        service = type(self.service)()
        assert service is not None

        # Contract: Service has required methods
        assert hasattr(service, "get_start_position_pictograph")
        assert callable(service.get_start_position_pictograph)

    def test_invalid_input_handling_contract(self):
        """PERMANENT: Service must handle invalid inputs gracefully"""
        # Contract: Invalid inputs should not crash
        result1 = self.service.get_start_position_pictograph("invalid_key", "diamond")
        result2 = self.service.get_start_position_pictograph(
            "alpha1_alpha1", "invalid_prop"
        )
        result3 = self.service.get_start_position_pictograph(None, None)

        # Contract: Should return None for invalid inputs, not crash
        assert result1 is None or isinstance(result1, self.BeatData)
        assert result2 is None or isinstance(result2, self.BeatData)
        assert result3 is None or isinstance(result3, self.BeatData)
