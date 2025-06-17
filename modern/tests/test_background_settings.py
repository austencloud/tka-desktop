"""
Test background settings functionality.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add modern src to path
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

# Mock PyQt6 to avoid import issues in tests
sys.modules["PyQt6"] = Mock()
sys.modules["PyQt6.QtCore"] = Mock()
sys.modules["PyQt6.QtWidgets"] = Mock()
sys.modules["PyQt6.QtGui"] = Mock()

from src.application.services.settings.background_service import BackgroundService


class TestBackgroundService:
    """Test the background service functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.ui_state_service = Mock()
        self.background_service = BackgroundService(self.ui_state_service)

    def test_get_available_backgrounds(self):
        """Test getting available background types."""
        backgrounds = self.background_service.get_available_backgrounds()

        assert isinstance(backgrounds, list)
        assert len(backgrounds) > 0
        assert "Aurora" in backgrounds
        assert "Starfield" in backgrounds
        assert "Snowfall" in backgrounds
        assert "Bubbles" in backgrounds

    def test_get_current_background_default(self):
        """Test getting current background with default value."""
        self.ui_state_service.get_setting.return_value = "Aurora"

        current = self.background_service.get_current_background()

        assert current == "Aurora"
        self.ui_state_service.get_setting.assert_called_once_with(
            "background_type", "Aurora"
        )

    def test_set_valid_background(self):
        """Test setting a valid background type."""
        result = self.background_service.set_background("Starfield")

        assert result is True
        self.ui_state_service.set_setting.assert_called_once_with(
            "background_type", "Starfield"
        )

    def test_set_invalid_background(self):
        """Test setting an invalid background type."""
        result = self.background_service.set_background("InvalidBackground")

        assert result is False
        self.ui_state_service.set_setting.assert_not_called()

    def test_is_valid_background(self):
        """Test background validation."""
        assert self.background_service.is_valid_background("Aurora") is True
        assert self.background_service.is_valid_background("Starfield") is True
        assert self.background_service.is_valid_background("InvalidBackground") is False


def test_background_service_integration():
    """Test basic background service functionality."""
    ui_state_service = Mock()
    ui_state_service.get_setting.return_value = "Bubbles"

    background_service = BackgroundService(ui_state_service)

    # Test setting and getting
    result = background_service.set_background("Bubbles")
    assert result is True

    current = background_service.get_current_background()
    assert current == "Bubbles"


if __name__ == "__main__":
    pytest.main([__file__])
