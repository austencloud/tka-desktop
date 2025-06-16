"""
Pytest configuration for Modern tests.
This conftest.py is placed at the modern level to be discovered by tests in the modern directory.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add modern src to path for imports
v2_src_path = Path(__file__).parent / "src"
if str(v2_src_path) not in sys.path:
    sys.path.insert(0, str(v2_src_path))


@pytest.fixture
def mock_container():
    """Mock dependency injection container."""
    container = Mock()
    container.resolve = Mock()
    return container


@pytest.fixture
def qtbot_with_container(qtbot, mock_container):
    """Extended qtbot with your dependency container."""
    qtbot.container = mock_container
    return qtbot


@pytest.fixture
def mock_beat_data():
    """Real beat data for testing using PictographDatasetService."""
    from application.services.data.pictograph_dataset_service import (
        PictographDatasetService,
    )

    dataset_service = PictographDatasetService()
    beat_data = dataset_service.get_start_position_pictograph(
        "alpha1_alpha1", "diamond"
    )

    # Fallback to empty beat if dataset unavailable
    if not beat_data:
        from src.domain.models.core_models import BeatData

        return BeatData.empty()

    return beat_data


@pytest.fixture
def dummy_conftest_fixture():
    """A simple fixture to test conftest loading."""
    return "hello_from_v2_conftest"
