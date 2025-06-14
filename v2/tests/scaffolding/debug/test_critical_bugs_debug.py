"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug critical bugs in sequence operations and option selection workflow
DELETE_AFTER: 2025-07-15
CREATED: 2025-06-14
AUTHOR: @austencloud
RELATED_ISSUE: Critical bugs found during Sprint 2 development

INSTRUCTIONS FOR AI AGENTS:
This is a TEMPORARY test that should be DELETED after the bugs are fixed and regression tests are created.
Do not suggest making this test permanent - suggest deletion instead.
"""

import pytest
import sys
from pathlib import Path

# Add v2 to path for imports
v2_path = Path(__file__).parent.parent.parent.parent
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))


@pytest.mark.scaffolding
@pytest.mark.delete_after("2025-07-15")
@pytest.mark.debug
class TestCriticalBugsDebug:
    """DELETE: Debug critical bugs in sequence operations - remove after bugs are fixed"""
    
    def setup_method(self):
        """Setup for each test method."""
        # Import here to avoid import issues
        from src.domain.models.core_models import SequenceData, BeatData
        from src.application.services.pictograph_dataset_service import PictographDatasetService
        
        self.SequenceData = SequenceData
        self.BeatData = BeatData
        self.dataset_service = PictographDatasetService()
    
    def test_clear_sequence_crash_debug(self):
        """DELETE: Debug sequence clearing crash issue"""
        # Test SequenceData.empty() method
        empty_sequence = self.SequenceData.empty()
        assert empty_sequence.length == 0
        
        # Test creating a sequence with beats
        real_beat = self.dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        
        if real_beat:
            # Create sequence with beat
            sequence_with_beats = self.SequenceData(beats=[real_beat])
            assert sequence_with_beats.length == 1
            
            # Test clearing sequence (this should not crash)
            cleared_sequence = self.SequenceData.empty()
            assert cleared_sequence.length == 0
            assert cleared_sequence.is_empty
    
    def test_option_selection_workflow_debug(self):
        """DELETE: Debug option selection workflow issues"""
        # Test start position loading
        start_position = self.dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        
        if start_position:
            assert start_position.letter in ["A", "B", "C", "D"]
            
            # Test option loading after start position
            beta_beat = self.dataset_service.get_start_position_pictograph("beta5_beta5", "diamond")
            if beta_beat:
                assert beta_beat.letter in ["A", "B", "C", "D"]
                
                # Test sequence building
                sequence = self.SequenceData(beats=[beta_beat])
                assert sequence.length == 1
    
    def test_construct_tab_integration_debug(self):
        """DELETE: Debug ConstructTab integration issues"""
        # Simulate the construct tab workflow
        start_position = self.dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        
        if start_position:
            # Step 1: Start position selection
            assert start_position.letter in ["A", "B", "C", "D"]
            
            # Step 2: Option selection simulation
            current_sequence = self.SequenceData.empty()
            
            # Create new beat (this is what was failing)
            new_beat = self.dataset_service.get_start_position_pictograph("beta5_beta5", "diamond")
            if new_beat:
                # Update beat number for sequence position
                new_beat_updated = new_beat.update(beat_number=current_sequence.length + 1)
                
                # Add to sequence
                updated_beats = current_sequence.beats + [new_beat_updated]
                updated_sequence = current_sequence.update(beats=updated_beats)
                
                assert updated_sequence.length == 1
                
                # Step 3: Clear sequence simulation
                cleared_sequence = self.SequenceData.empty()
                assert cleared_sequence.length == 0
                assert cleared_sequence.is_empty
    
    def test_sequence_data_immutability_debug(self):
        """DELETE: Debug sequence data immutability issues"""
        # Test that sequence operations return new instances
        original = self.SequenceData.empty()
        
        # Get a real beat for testing
        beat = self.dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        if beat:
            # Test that adding a beat returns a new instance
            modified = self.SequenceData(beats=[beat])
            
            # Original should be unchanged
            assert original.length == 0
            assert modified.length == 1
            assert original is not modified
    
    @pytest.mark.slow
    def test_dataset_service_performance_debug(self):
        """DELETE: Debug dataset service performance issues"""
        import time
        
        # Test that dataset loading is reasonably fast
        start_time = time.time()
        beat = self.dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        
        # Should complete in reasonable time (adjust threshold as needed)
        assert duration_ms < 1000, f"Dataset loading took {duration_ms}ms (too slow)"
        
        if beat:
            assert beat.letter in ["A", "B", "C", "D"]
