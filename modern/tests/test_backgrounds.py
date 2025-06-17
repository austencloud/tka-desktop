import pytest
from src.presentation.components.backgrounds.background_factory import BackgroundFactory


def test_all_backgrounds_create_successfully():
    """Test that all registered backgrounds can be created without errors."""
    for bg_type in BackgroundFactory.get_available_backgrounds():
        background = BackgroundFactory.create_background(bg_type)
        assert background is not None
        assert hasattr(background, "animate_background")
        assert hasattr(background, "paint_background")


def test_background_factory_invalid_type():
    """Test that factory raises error for unknown background types."""
    with pytest.raises(ValueError, match="Unknown background type"):
        BackgroundFactory.create_background("InvalidType")


def test_available_backgrounds_list():
    """Test that factory returns expected background types."""
    available = BackgroundFactory.get_available_backgrounds()
    expected_types = ["Aurora", "Bubbles", "Snowfall", "Starfield"]

    for expected_type in expected_types:
        assert expected_type in available
