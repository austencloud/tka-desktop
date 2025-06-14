"""
Unit tests for BeatFrameLayoutService.

Tests the core layout calculation logic in isolation.
"""

import pytest
from unittest.mock import Mock, patch

from src.application.services.beat_frame_layout_service import BeatFrameLayoutService


@pytest.mark.unit
class TestBeatFrameLayoutService:
    """Test beat frame layout calculations."""

    def setup_method(self):
        """Setup for each test."""
        self.service = BeatFrameLayoutService()

    def test_calculate_optimal_layout_standard_sequences(self):
        """Test layout calculations for standard sequence lengths."""
        # Test known configurations from service
        test_cases = [
            (2, {"rows": 1, "columns": 8}),  # 2 beats -> 1x8 grid
            (4, {"rows": 1, "columns": 8}),  # 4 beats -> 1x8 grid
            (8, {"rows": 1, "columns": 8}),  # 8 beats -> 1x8 grid
            (16, {"rows": 2, "columns": 8}),  # 16 beats -> 2x8 grid
        ]

        for sequence_length, expected_layout in test_cases:
            layout = self.service.calculate_optimal_layout(sequence_length)
            assert layout == expected_layout, f"Failed for length {sequence_length}"

    def test_calculate_optimal_layout_edge_cases(self):
        """Test layout calculations for edge cases."""
        # Empty sequence
        layout = self.service.calculate_optimal_layout(0)
        assert layout["rows"] >= 1 and layout["columns"] >= 1

        # Single beat
        layout = self.service.calculate_optimal_layout(1)
        assert layout["rows"] >= 1 and layout["columns"] >= 1

        # Large sequence
        layout = self.service.calculate_optimal_layout(64)
        assert layout["rows"] * layout["columns"] >= 64

    def test_get_beat_position_valid_indices(self):
        """Test beat position calculations for valid indices."""
        # Setup layout for 16 beats
        layout = self.service.calculate_optimal_layout(16)

        # Test corner positions
        assert self.service.get_beat_position(0, layout) == (
            0,
            1,
        )  # First beat (after start pos)
        assert self.service.get_beat_position(7, layout) == (0, 8)  # End of first row

        # Test second row positions
        assert self.service.get_beat_position(8, layout) == (
            1,
            1,
        )  # Start of second row

    def test_get_beat_position_invalid_indices(self):
        """Test beat position calculations for invalid indices."""
        layout = self.service.calculate_optimal_layout(16)

        # Negative index - should still work but return valid position
        row, col = self.service.get_beat_position(-1, layout)
        assert isinstance(row, int) and isinstance(col, int)

        # Large index - should still work
        row, col = self.service.get_beat_position(100, layout)
        assert isinstance(row, int) and isinstance(col, int)

    def test_get_grid_dimensions_responsive(self):
        """Test grid dimension calculations are responsive."""
        # Test different layouts
        test_cases = [
            {"rows": 1, "columns": 8},  # Single row
            {"rows": 2, "columns": 8},  # Two rows
            {"rows": 4, "columns": 8},  # Four rows
        ]

        for layout in test_cases:
            width, height = self.service.get_grid_dimensions(layout)

            # Dimensions should be positive
            assert width > 0
            assert height > 0

            # Should scale with layout size
            expected_width = (layout["columns"] + 1) * 128 - 8  # Approximate
            expected_height = layout["rows"] * 128 - 8

            # Allow some tolerance for spacing calculations
            assert abs(width - expected_width) < 50
            assert abs(height - expected_height) < 50

    def test_calculate_scroll_position(self):
        """Test scroll position calculations."""
        # Setup layout
        layout = self.service.calculate_optimal_layout(16)

        # Test scroll to specific beat
        x, y = self.service.calculate_scroll_position(8, layout)
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert x >= 0 and y >= 0

    def test_layout_consistency(self):
        """Test that layout calculations are consistent."""
        # First calculation
        result1 = self.service.calculate_optimal_layout(16)

        # Second calculation should be identical
        result2 = self.service.calculate_optimal_layout(16)

        assert result1 == result2

        # Verify consistent results for same input
        assert result1 == result2

    def test_layout_validation(self):
        """Test layout validation logic."""
        # Valid layouts should pass
        assert self.service.validate_layout(16, 4, 4) == True

        # Invalid layouts should fail
        assert self.service.validate_layout(16, 2, 2) == False  # Too small
        assert self.service.validate_layout(16, 0, 4) == False  # Zero dimension

    def test_performance_requirements(self):
        """Test that layout calculations meet performance requirements."""
        import time

        # Large sequence calculation should be fast
        start_time = time.time()

        layout = self.service.calculate_optimal_layout(64)
        for i in range(100):
            self.service.calculate_optimal_layout(64)
            self.service.get_beat_position(i % 64, layout)

        duration = time.time() - start_time

        # Should complete 100 calculations in under 0.1 seconds
        assert duration < 0.1, f"Layout calculations too slow: {duration}s"
