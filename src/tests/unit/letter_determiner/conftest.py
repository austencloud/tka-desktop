import pytest
from letter_determination.core import LetterDeterminer
from main_window.main_widget.pictograph_data_loader import PictographDataLoader
from .mocks.widgets import MockMainWidget


@pytest.fixture
def mock_main_widget() -> MockMainWidget:
    """Fixture providing a mocked main widget with loaded pictograph data"""
    widget = MockMainWidget()
    loader = PictographDataLoader(widget)
    widget.pictograph_dataset = loader.load_pictograph_dataset()
    return widget


@pytest.fixture
def letter_determiner(mock_main_widget) -> LetterDeterminer:
    """Fixture providing initialized LetterDeterminer instance"""
    return LetterDeterminer(mock_main_widget)


@pytest.fixture
def pictograph_dataset(mock_main_widget) -> dict:
    """Fixture providing access to the pictograph dataset"""
    return mock_main_widget.pictograph_dataset
