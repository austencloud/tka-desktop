"""
Pytest configuration and shared fixtures for TKA V2 test suite.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
from PyQt6.QtCore import QTimer

# Add v2 src to path for imports
v2_src_path = Path(__file__).parent.parent / "src"
if str(v2_src_path) not in sys.path:
    sys.path.insert(0, str(v2_src_path))

# Test markers
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Fast unit tests")
    config.addinivalue_line("markers", "integration: Component integration tests")
    config.addinivalue_line(
        "markers", "ui: User interface tests (now with pytest-qt)"
    )  # Updated marker description
    config.addinivalue_line("markers", "parity: V1 functionality parity tests")
    config.addinivalue_line("markers", "slow: Tests that take >5 seconds")


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
def construct_tab_widget(qtbot, mock_container):
    """Factory for creating ConstructTabWidget in tests."""

    def _create_construct_tab():
        from src.presentation.tabs.construct_tab_widget import ConstructTabWidget

        widget = ConstructTabWidget(mock_container)
        qtbot.addWidget(widget)  # Auto-cleanup
        return widget

    return _create_construct_tab


@pytest.fixture
def mock_sequence_data():
    """Real sequence data for testing using PictographDatasetService."""
    from src.domain.models.core_models import SequenceData
    from src.application.services.pictograph_dataset_service import (
        PictographDatasetService,
    )

    dataset_service = PictographDatasetService()

    # Get real start position beats
    beat1 = dataset_service.get_start_position_pictograph("alpha1_alpha1", "diamond")
    beat2 = dataset_service.get_start_position_pictograph("beta5_beta5", "diamond")

    # Fallback to empty sequence if dataset unavailable
    if not beat1 or not beat2:
        return SequenceData.empty()

    return SequenceData(beats=[beat1, beat2], start_position=beat1)


@pytest.fixture
def mock_beat_data():
    """Real beat data for testing using PictographDatasetService."""
    from src.application.services.pictograph_dataset_service import (
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
def mock_graph_editor_service():
    """Mock graph editor service."""
    from src.core.interfaces.workbench_services import IGraphEditorService

    service = Mock(spec=IGraphEditorService)
    service.update_graph_display = Mock()
    service.toggle_graph_visibility = Mock(return_value=True)
    service.set_selected_beat = Mock()
    service.get_selected_beat = Mock()
    service.update_beat_adjustments = Mock()
    service.is_visible = Mock(return_value=False)
    service.set_arrow_selection = Mock()
    service.get_selected_arrow = Mock()
    service.apply_turn_adjustment = Mock(return_value=True)
    service.apply_orientation_adjustment = Mock(return_value=True)

    return service


@pytest.fixture
def mock_layout_service():
    """Mock layout service."""
    from src.application.services.beat_frame_layout_service import (
        BeatFrameLayoutService,
    )

    service = Mock(spec=BeatFrameLayoutService)
    service.calculate_grid_dimensions = Mock(return_value=(4, 4))
    service.get_beat_position = Mock(return_value=(0, 0))
    service.get_grid_cell_size = Mock(return_value=(100, 100))
    service.calculate_scroll_position = Mock(return_value=0)

    return service


@pytest.fixture
def temp_test_data(tmp_path):
    """Create temporary test data directory."""
    test_data_dir = tmp_path / "test_data"
    test_data_dir.mkdir()

    # Create sample test files
    (test_data_dir / "sample_sequence.json").write_text('{"beats": [], "length": 0}')
    (test_data_dir / "sample_image.png").touch()

    return test_data_dir


class TestTimer:
    """Test utility for Qt timer operations."""

    @staticmethod
    def process_events(app, timeout_ms=100):
        """Process Qt events with timeout."""
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(app.quit)
        timer.start(timeout_ms)
        app.exec()


@pytest.fixture
def test_timer():
    """Test timer utility."""
    return TestTimer()


# Auto-use fixtures for common setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for each test."""
    # Reset any global state
    yield
    # Cleanup after test
    pass


@pytest.fixture
def dummy_conftest_fixture():
    """A simple fixture to test conftest loading."""
    return "hello_from_conftest"
