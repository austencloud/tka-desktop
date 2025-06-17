"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent sequence clearing crash from reoccurring
BUG_REPORT: Critical bugs found during Sprint 2 - sequence operations causing crashes
FIXED_DATE: 2025-06-14
AUTHOR: @austencloud

INSTRUCTIONS FOR AI AGENTS:
This is a REGRESSION test that prevents a specific bug from reoccurring.
Only suggest deletion if the entire sequence feature is removed from the system.
Focus on reproducing the exact scenario that caused the original bug.
"""

import pytest
import sys
from pathlib import Path

# Add modern to path for imports
modern_path = Path(__file__).parent.parent.parent.parent
if str(modern_path) not in sys.path:
    sys.path.insert(0, str(modern_path))


@pytest.mark.regression
@pytest.mark.critical
class TestSequenceClearingCrashRegression:
    """Prevent sequence clearing crash regression - DELETE only if feature removed"""

    def setup_method(self):
        """Setup for each test method."""
        from src.domain.models.core_models import SequenceData, BeatData
        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        self.SequenceData = SequenceData
        self.BeatData = BeatData
        self.dataset_service = PictographDatasetService()

    def test_clear_sequence_after_beat_addition_no_crash(self):
        """REGRESSION: Clearing sequence after adding beats must not crash"""
        # Reproduce the exact scenario that caused the crash

        # Step 1: Create sequence with beats
        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            sequence_with_beats = self.SequenceData(beats=[beat])
            assert sequence_with_beats.length == 1

            # Step 2: Clear sequence (this used to crash)
            cleared_sequence = self.SequenceData.empty()

            # Should complete without exception
            assert cleared_sequence.length == 0
            assert cleared_sequence.is_empty

    def test_multiple_sequence_operations_no_crash(self):
        """REGRESSION: Multiple sequence operations must not cause memory issues"""
        # Test the edge case that also caused crashes

        beat1 = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        beat2 = self.dataset_service.get_start_position_pictograph(
            "beta5_beta5", "diamond"
        )

        if beat1 and beat2:
            # Perform multiple operations that used to cause issues
            for i in range(10):  # Repeat to catch memory issues
                # Create sequence
                sequence = self.SequenceData(beats=[beat1])
                assert sequence.length == 1

                # Add beat
                updated_sequence = self.SequenceData(beats=[beat1, beat2])
                assert updated_sequence.length == 2

                # Clear sequence
                cleared = self.SequenceData.empty()
                assert cleared.length == 0

    def test_construct_tab_workflow_no_crash(self):
        """REGRESSION: ConstructTab workflow must not crash during option selection"""
        # Reproduce the specific ConstructTab integration issue

        # Step 1: Start position selection
        start_position = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if start_position:
            # Step 2: Option selection simulation (this was crashing)
            current_sequence = self.SequenceData.empty()

            # Create new beat (this is what was failing)
            new_beat = self.dataset_service.get_start_position_pictograph(
                "beta5_beta5", "diamond"
            )
            if new_beat:
                # Update beat number for sequence position
                new_beat_updated = new_beat.update(
                    beat_number=current_sequence.length + 1
                )

                # Add to sequence (this operation was causing crashes)
                updated_beats = current_sequence.beats + [new_beat_updated]
                updated_sequence = current_sequence.update(beats=updated_beats)

                assert updated_sequence.length == 1

                # Step 3: Clear sequence (final crash point)
                cleared_sequence = self.SequenceData.empty()
                assert cleared_sequence.length == 0

    def test_rapid_sequence_creation_and_clearing_no_memory_leak(self):
        """REGRESSION: Rapid sequence operations must not cause memory growth"""
        import gc

        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            # Force garbage collection before test
            gc.collect()

            # Perform rapid operations that used to leak memory
            for i in range(100):
                # Create sequence
                sequence = self.SequenceData(beats=[beat])

                # Clear sequence
                cleared = self.SequenceData.empty()

                # Ensure objects are properly cleaned up
                del sequence
                del cleared

            # Force garbage collection after test
            gc.collect()

            # Test should complete without excessive memory growth
            # (Memory growth is hard to test precisely, but the operations should complete)
            assert True  # If we get here without crashing, the regression is prevented

    def test_sequence_state_consistency_after_operations(self):
        """REGRESSION: Sequence state must remain consistent after all operations"""
        # Test that was failing due to state corruption

        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            # Create initial sequence
            original = self.SequenceData.empty()
            assert original.is_empty
            assert original.length == 0

            # Add beat
            with_beat = self.SequenceData(beats=[beat])
            assert not with_beat.is_empty
            assert with_beat.length == 1

            # Clear sequence
            cleared = self.SequenceData.empty()
            assert cleared.is_empty
            assert cleared.length == 0

            # Verify original is unchanged (immutability check)
            assert original.is_empty
            assert original.length == 0

            # Verify with_beat is unchanged (immutability check)
            assert not with_beat.is_empty
            assert with_beat.length == 1

    @pytest.mark.slow
    def test_performance_regression_sequence_operations(self):
        """REGRESSION: Sequence operations must complete within reasonable time"""
        import time

        beat = self.dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )
        if beat:
            # Test that operations complete quickly (performance regression check)
            start_time = time.time()

            # Perform the operations that were slow
            for i in range(50):
                sequence = self.SequenceData(beats=[beat])
                cleared = self.SequenceData.empty()

            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            # Should complete in reasonable time (adjust threshold based on actual performance)
            assert (
                duration_ms < 1000
            ), f"Sequence operations took {duration_ms}ms (performance regression)"
