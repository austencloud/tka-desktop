"""
Settings tab manager for the modern settings dialog.

Handles tab creation, organization, and management.
"""

from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import QWidget, QStackedWidget, QListWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import logging

if TYPE_CHECKING:
    from src.core.application_context import ApplicationContext
    from ..core.settings_state_manager import SettingsStateManager

logger = logging.getLogger(__name__)


class SettingsTabManager:
    """
    Manages settings dialog tabs.
    
    Responsibilities:
    - Create tab widgets
    - Organize tab order
    - Populate sidebar and content area
    - Handle tab imports and fallbacks
    """

    def __init__(
        self, 
        settings_manager, 
        state_manager: "SettingsStateManager",
        app_context: "ApplicationContext" = None,
        parent_dialog=None
    ):
        self.settings_manager = settings_manager
        self.state_manager = state_manager
        self.app_context = app_context
        self.parent_dialog = parent_dialog
        
        # Tab configuration
        self.tab_order = [
            "General",
            "Prop Type", 
            "Visibility",
            "Beat Layout",
            "Image Export",
            "Codex Exporter",
        ]
        
        self.tabs: Dict[str, QWidget] = {}
        self._real_tabs_available = self._check_real_tabs_availability()

    def create_tabs(self, sidebar: QListWidget, content_area: QStackedWidget) -> Dict[str, QWidget]:
        """
        Create all tab widgets and populate sidebar and content area.
        
        Args:
            sidebar: The sidebar list widget
            content_area: The stacked widget for tab content
            
        Returns:
            Dictionary of created tab widgets
        """
        try:
            logger.debug("Creating tab widgets...")

            # Create tab widgets
            self._create_tab_widgets()

            # Populate sidebar and content area
            self._populate_sidebar_and_content(sidebar, content_area)

            logger.debug(f"Created {len(self.tabs)} tab widgets")
            return self.tabs

        except Exception as e:
            logger.error(f"Error creating tabs: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def _create_tab_widgets(self):
        """Create all tab widget instances."""
        if self._real_tabs_available:
            self.tabs = self._create_real_tabs()
            logger.debug("Created tabs using real implementations")
        else:
            self.tabs = self._create_fallback_tabs()
            logger.debug("Created tabs using placeholder implementations")

    def _create_real_tabs(self) -> Dict[str, QWidget]:
        """Create tabs using real implementations."""
        try:
            # Import real tab implementations
            from ..ui.prop_type.prop_type_tab import PropTypeTab
            from ..ui.visibility.visibility_tab import VisibilityTab
            from ..ui.beat_layout.beat_layout_tab import BeatLayoutTab
            from ..ui.image_export.image_export_tab import ImageExportTab
            from ..ui.codex_exporter.codex_exporter_tab import CodexExporterTab
            from ..ui.enhanced_general.enhanced_general_tab import EnhancedGeneralTab

            return {
                "General": EnhancedGeneralTab(
                    self.settings_manager, self.state_manager, self.parent_dialog
                ),
                "Prop Type": PropTypeTab(self.parent_dialog),
                "Visibility": VisibilityTab(self.parent_dialog),
                "Beat Layout": BeatLayoutTab(self.parent_dialog),
                "Image Export": ImageExportTab(self.parent_dialog),
                "Codex Exporter": CodexExporterTab(self.parent_dialog),
            }
        except ImportError as e:
            logger.warning(f"Failed to import real tabs: {e}")
            return self._create_fallback_tabs()

    def _create_fallback_tabs(self) -> Dict[str, QWidget]:
        """Create fallback placeholder tabs."""
        try:
            from ..ui.enhanced_general.enhanced_general_tab import EnhancedGeneralTab
            
            tabs = {
                "General": EnhancedGeneralTab(
                    self.settings_manager, self.state_manager, self.parent_dialog
                ),
            }
            
            # Create placeholder tabs for others
            for tab_name in self.tab_order[1:]:  # Skip "General"
                tabs[tab_name] = self._create_placeholder_tab(tab_name)
                
            return tabs
            
        except ImportError:
            # Ultimate fallback - all placeholder tabs
            return {tab_name: self._create_placeholder_tab(tab_name) for tab_name in self.tab_order}

    def _create_placeholder_tab(self, tab_name: str) -> QWidget:
        """Create a placeholder tab widget."""
        widget = QWidget(self.parent_dialog)
        layout = QVBoxLayout(widget)
        label = QLabel(f"{tab_name} Tab (Legacy)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return widget

    def _populate_sidebar_and_content(self, sidebar: QListWidget, content_area: QStackedWidget):
        """Populate the sidebar and content area with tabs."""
        for tab_name in self.tab_order:
            if tab_name in self.tabs:
                tab_widget = self.tabs[tab_name]
                logger.debug(f"Adding tab: {tab_name}")

                # Add to sidebar
                sidebar.addItem(tab_name)

                # Add to content area
                content_area.addWidget(tab_widget)

        logger.debug(f"Sidebar has {sidebar.count()} items")
        logger.debug(f"Content area has {content_area.count()} widgets")

        # Set default selection
        if sidebar.count() > 0:
            sidebar.setCurrentRow(0)
            content_area.setCurrentIndex(0)
            logger.debug("Set default selection to first tab")

    def _check_real_tabs_availability(self) -> bool:
        """Check if real tab implementations are available."""
        try:
            from ..ui.prop_type.prop_type_tab import PropTypeTab
            from ..ui.visibility.visibility_tab import VisibilityTab
            from ..ui.beat_layout.beat_layout_tab import BeatLayoutTab
            from ..ui.image_export.image_export_tab import ImageExportTab
            from ..ui.codex_exporter.codex_exporter_tab import CodexExporterTab
            return True
        except ImportError:
            return False

    def get_tab_order(self) -> List[str]:
        """Get the tab order list."""
        return self.tab_order.copy()

    def get_tab(self, tab_name: str) -> QWidget:
        """Get a specific tab widget."""
        return self.tabs.get(tab_name)

    def refresh_all_tabs(self):
        """Refresh all tab contents from current settings."""
        try:
            for tab_name, tab_widget in self.tabs.items():
                if hasattr(tab_widget, "refresh_settings"):
                    tab_widget.refresh_settings()
        except Exception as e:
            logger.error(f"Error refreshing tabs: {e}")
