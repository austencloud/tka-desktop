#!/usr/bin/env python3
"""
Qt Testing Fixtures
===================

Provides reusable Qt application and widget fixtures for testing.
"""

import sys
import pytest
from pathlib import Path

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))


@pytest.fixture
def qt_app():
    """Provide a Qt application for testing."""
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Create or get existing application
        app = QApplication.instance() or QApplication([])
        
        yield app
        
        # Process events to clean up
        app.processEvents()
        
        # Note: Don't quit the app as it might be shared
        
    except ImportError:
        pytest.skip("PyQt6 not available for Qt testing")


@pytest.fixture
def qt_main_window(qt_app):
    """Provide a main window for testing."""
    try:
        from PyQt6.QtWidgets import QMainWindow
        
        window = QMainWindow()
        window.setGeometry(100, 100, 800, 600)
        
        yield window
        
        # Cleanup
        window.close()
        qt_app.processEvents()
        
    except ImportError:
        pytest.skip("PyQt6 not available for main window testing")


@pytest.fixture
def qt_widget(qt_app):
    """Provide a basic widget for testing."""
    try:
        from PyQt6.QtWidgets import QWidget
        
        widget = QWidget()
        widget.resize(400, 300)
        
        yield widget
        
        # Cleanup
        widget.close()
        qt_app.processEvents()
        
    except ImportError:
        pytest.skip("PyQt6 not available for widget testing")


@pytest.fixture
def construct_tab_widget(qt_app, workbench_di_container):
    """Provide a construct tab widget for testing."""
    try:
        from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
        
        construct_tab = ConstructTabWidget(workbench_di_container)
        construct_tab.resize(800, 600)
        
        yield construct_tab
        
        # Cleanup
        construct_tab.close()
        qt_app.processEvents()
        
    except ImportError:
        pytest.skip("Construct tab widget not available for testing")
