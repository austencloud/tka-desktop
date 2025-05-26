"""
Modern Settings Dialog with glassmorphism UI and comprehensive state management.
"""

from typing import TYPE_CHECKING, Dict, Any
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
)
from PyQt6.QtCore import QEvent, pyqtSignal, Qt
from PyQt6.QtGui import QFont
import logging

# Try to import our modern components, fall back to simple versions if they fail
try:
    from .core.settings_state_manager import SettingsStateManager
    from .core.glassmorphism_styler import GlassmorphismStyler
    from .ui.settings_dialog_sidebar import SettingsDialogSidebar
    from .ui.enhanced_general.enhanced_general_tab import EnhancedGeneralTab

    MODERN_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Modern components not available, using fallbacks: {e}")
    MODERN_COMPONENTS_AVAILABLE = False

    # Create simple fallback classes
    class SettingsStateManager:
        def __init__(self, settings_manager):
            self.settings_manager = settings_manager

        def is_modified(self):
            return False

        def apply_changes(self):
            return True

        def revert_changes(self):
            pass

        def reset_to_defaults(self):
            pass

        def create_backup(self):
            return "backup.json"

        def restore_backup(self, path):
            return True

    class GlassmorphismStyler:
        SPACING = {"sm": 4, "md": 8, "lg": 16, "xl": 24}

        @staticmethod
        def create_dialog_style():
            return ""

        @staticmethod
        def create_sidebar_style():
            return ""

        @staticmethod
        def add_shadow_effect(widget, **kwargs):
            pass

    class SettingsDialogSidebar(QListWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self._setup_modern_styling()
            self._setup_enhanced_behavior()

        def _setup_enhanced_behavior(self):
            """Setup enhanced modern behavior for the sidebar."""
            # Enable smooth scrolling
            self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            # Set modern selection behavior
            self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            # Enhanced spacing
            self.setSpacing(2)

        def _setup_modern_styling(self):
            """Apply cutting-edge 2025-level glassmorphism styling to the sidebar."""
            sidebar_style = """
            QListWidget {
                /* Advanced glassmorphism container with depth */
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:0.3 rgba(255, 255, 255, 0.12),
                    stop:0.7 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.05));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 20px;
                padding: 16px 12px;
                outline: none;
                font-family: "Segoe UI", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 15px;
                font-weight: 500;
                selection-background-color: transparent;
            }

            QListWidget::item {
                /* Modern list item with enhanced spacing */
                background: transparent;
                border: none;
                border-radius: 14px;
                padding: 16px 20px;
                margin: 4px 6px;
                color: rgba(255, 255, 255, 0.87);
                font-weight: 500;
                min-height: 28px;
                font-size: 15px;
                letter-spacing: 0.3px;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }

            QListWidget::item:hover {
                /* Sophisticated hover effect with multi-layer glassmorphism */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:0.5 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.15));
                color: rgba(255, 255, 255, 1.0);
                border: 1px solid rgba(255, 255, 255, 0.35);
                font-weight: 600;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }

            QListWidget::item:selected {
                /* Premium selection state with blue accent */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.45),
                    stop:0.3 rgba(59, 130, 246, 0.38),
                    stop:0.7 rgba(59, 130, 246, 0.32),
                    stop:1 rgba(59, 130, 246, 0.28));
                color: rgba(255, 255, 255, 1.0);
                border: 1px solid rgba(59, 130, 246, 0.65);
                font-weight: 700;
                letter-spacing: 0.4px;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
            }

            QListWidget::item:selected:hover {
                /* Enhanced selected hover state */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(59, 130, 246, 0.55),
                    stop:0.3 rgba(59, 130, 246, 0.48),
                    stop:0.7 rgba(59, 130, 246, 0.42),
                    stop:1 rgba(59, 130, 246, 0.38));
                border: 1px solid rgba(59, 130, 246, 0.75);
                box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35);
                transform: translateY(-1px);
            }

            QListWidget::item:focus {
                /* Subtle focus indicator */
                outline: none;
                border: 1px solid rgba(59, 130, 246, 0.5);
            }
            """
            self.setStyleSheet(sidebar_style)

    class EnhancedGeneralTab(QWidget):
        def __init__(self, settings_manager, state_manager, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Enhanced General Tab (Fallback)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)


# Import the actual tab implementations
try:
    from .ui.prop_type.prop_type_tab import PropTypeTab
    from .ui.visibility.visibility_tab import VisibilityTab
    from .ui.beat_layout.beat_layout_tab import BeatLayoutTab
    from .ui.image_export.image_export_tab import ImageExportTab
    from .ui.codex_exporter.codex_exporter_tab import CodexExporterTab

    REAL_TABS_AVAILABLE = True
    print("[DEBUG] Successfully imported real tab implementations")
except ImportError as e:
    print(f"[DEBUG] Could not import real tabs, using placeholders: {e}")
    REAL_TABS_AVAILABLE = False

    # Create placeholder classes for tabs - we'll use the enhanced general tab and placeholders for others
    class PropTypeTab(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Prop Type Tab (Legacy)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    class VisibilityTab(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Visibility Tab (Legacy)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    class BeatLayoutTab(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Beat Layout Tab (Legacy)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    class ImageExportTab(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Image Export Tab (Legacy)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

    class CodexExporterTab(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("Codex Exporter Tab (Legacy)")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)


# Define the simplified ModernActionButtons class (always available)
class ModernActionButtons(QWidget):
    """Simplified modern action buttons without flickering issues."""

    # Signals - only essential buttons
    apply_requested = pyqtSignal()
    ok_requested = pyqtSignal()
    cancel_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._has_changes = False
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 16, 0, 0)

        # Create only essential buttons
        self.apply_btn = self._create_modern_button("Apply", "primary")
        self.ok_btn = self._create_modern_button("OK", "success")
        self.cancel_btn = self._create_modern_button("Cancel", "secondary")

        # Center the buttons
        layout.addStretch()
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)
        layout.addStretch()

        # Connect signals
        self.apply_btn.clicked.connect(self.apply_requested.emit)
        self.ok_btn.clicked.connect(self.ok_requested.emit)
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)

        # Set initial states
        self._update_button_states()

    def _create_modern_button(self, text, style_type="primary"):
        """Create a stable modern button without flickering animations."""
        button = QPushButton(text)
        button.setMinimumSize(120, 40)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Define color schemes for different button types
        colors = {
            "primary": {
                "bg": "rgba(59, 130, 246, 0.85)",  # Blue
                "hover": "rgba(59, 130, 246, 1.0)",
                "text": "rgba(255, 255, 255, 0.95)",
                "border": "rgba(59, 130, 246, 0.4)",
                "disabled_bg": "rgba(59, 130, 246, 0.3)",
                "disabled_text": "rgba(255, 255, 255, 0.4)",
            },
            "success": {
                "bg": "rgba(34, 197, 94, 0.85)",  # Green
                "hover": "rgba(34, 197, 94, 1.0)",
                "text": "rgba(255, 255, 255, 0.95)",
                "border": "rgba(34, 197, 94, 0.4)",
                "disabled_bg": "rgba(34, 197, 94, 0.3)",
                "disabled_text": "rgba(255, 255, 255, 0.4)",
            },
            "secondary": {
                "bg": "rgba(107, 114, 128, 0.85)",  # Gray
                "hover": "rgba(107, 114, 128, 1.0)",
                "text": "rgba(255, 255, 255, 0.95)",
                "border": "rgba(107, 114, 128, 0.4)",
                "disabled_bg": "rgba(107, 114, 128, 0.3)",
                "disabled_text": "rgba(255, 255, 255, 0.4)",
            },
        }

        color_scheme = colors.get(style_type, colors["primary"])

        # Stable button styling without problematic effects
        button_style = f"""
        QPushButton {{
            background: {color_scheme["bg"]};
            border: 1px solid {color_scheme["border"]};
            border-radius: 10px;
            color: {color_scheme["text"]};
            font-weight: 600;
            font-size: 14px;
            padding: 10px 20px;
            font-family: "Segoe UI", Arial, sans-serif;
        }}
        QPushButton:hover {{
            background: {color_scheme["hover"]};
            border: 1px solid {color_scheme["border"]};
        }}
        QPushButton:pressed {{
            background: {color_scheme["bg"]};
            border: 1px solid {color_scheme["border"]};
        }}
        QPushButton:disabled {{
            background: {color_scheme["disabled_bg"]};
            color: {color_scheme["disabled_text"]};
            border: 1px solid rgba(107, 114, 128, 0.2);
        }}
        """

        button.setStyleSheet(button_style)
        return button

    def set_has_changes(self, has_changes):
        """Update button states based on changes."""
        self._has_changes = has_changes
        self._update_button_states()

    def _update_button_states(self):
        """Update button enabled/disabled states."""
        # Apply button only enabled if there are changes
        self.apply_btn.setEnabled(self._has_changes)
        # OK and Cancel always enabled
        self.ok_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)

    def set_apply_success(self, success):
        """Handle apply operation result."""
        if success:
            # Reset changes state after successful apply
            self.set_has_changes(False)


from src.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ModernSettingsDialog(QDialog):
    """
    Modern settings dialog with glassmorphism UI, state management, and enhanced functionality.
    """

    # Signals
    settings_applied = pyqtSignal(bool)  # success
    dialog_closed = pyqtSignal()

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = AppContext.settings_manager()

        # Initialize state manager
        self.state_manager = SettingsStateManager(self.settings_manager)

        # Tab storage
        self.tabs: Dict[str, QWidget] = {}
        self.tab_order = [
            "General",
            "Prop Type",
            "Visibility",
            "Beat Layout",
            "Image Export",
            "Codex Exporter",
        ]

        self._setup_dialog()
        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

        # Initialize drag functionality for frameless window
        self.drag_position = None

        logging.info("Modern Settings Dialog initialized")

    def _setup_dialog(self):
        """Setup modern frameless dialog properties."""
        self.setWindowTitle("Settings")
        self.setModal(True)

        # Remove window frame for modern modal appearance
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        # Set transparent background for glassmorphism effect
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set a larger size for better content accommodation
        self.setFixedSize(1400, 900)

        # Center the dialog properly
        self._center_dialog()

        print("[DEBUG] Modern frameless dialog setup complete")

    def _center_dialog(self):
        """Center the dialog on the screen or parent window."""
        try:
            # Get the main window to center on
            main_window = None

            # Try to get the main window from the main_widget
            if self.main_widget:
                # Try different ways to get the main window
                if hasattr(self.main_widget, "window"):
                    main_window = self.main_widget.window()
                elif hasattr(self.main_widget, "parent") and self.main_widget.parent():
                    main_window = self.main_widget.parent()
                    while main_window and main_window.parent():
                        main_window = main_window.parent()

            if main_window and main_window.isVisible():
                # Center on the main window
                main_geometry = main_window.geometry()
                dialog_width = self.width()
                dialog_height = self.height()

                # Calculate center position relative to main window
                x = main_geometry.x() + (main_geometry.width() - dialog_width) // 2
                y = main_geometry.y() + (main_geometry.height() - dialog_height) // 2

                # Get the screen that contains the main window
                screen = (
                    main_window.screen() if hasattr(main_window, "screen") else None
                )
                if not screen:
                    from PyQt6.QtWidgets import QApplication

                    screen = QApplication.screenAt(main_window.pos())

                if screen:
                    screen_geometry = screen.availableGeometry()
                    # Ensure dialog stays within the screen bounds
                    x = max(
                        screen_geometry.x(),
                        min(
                            x,
                            screen_geometry.x()
                            + screen_geometry.width()
                            - dialog_width,
                        ),
                    )
                    y = max(
                        screen_geometry.y(),
                        min(
                            y,
                            screen_geometry.y()
                            + screen_geometry.height()
                            - dialog_height,
                        ),
                    )

                self.move(x, y)
                print(f"[DEBUG] Centered dialog on main window at ({x}, {y})")
                return

            # Fallback: center on primary screen
            from PyQt6.QtWidgets import QApplication

            screen = QApplication.primaryScreen()
            if screen:
                screen_geometry = screen.availableGeometry()
                dialog_width = self.width()
                dialog_height = self.height()

                x = screen_geometry.x() + (screen_geometry.width() - dialog_width) // 2
                y = (
                    screen_geometry.y()
                    + (screen_geometry.height() - dialog_height) // 2
                )

                self.move(x, y)
                print(f"[DEBUG] Centered dialog on primary screen at ({x}, {y})")
                return

            # Ultimate fallback
            self.move(200, 200)
            print("[DEBUG] Used fallback position (200, 200)")

        except Exception as e:
            print(f"[DEBUG] Error centering dialog: {e}")
            # Fallback position
            self.move(200, 200)

    def _setup_ui(self):
        """Setup the modern UI layout."""
        print("[DEBUG] Setting up modern UI layout...")

        # Main layout with no margins for frameless design
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create main container with glassmorphism background
        self.main_container = QWidget()
        self.main_container.setObjectName("main_container")
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(20)

        # Create modern header with title and close button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title_label = QLabel("Settings")
        title_label.setObjectName("dialog_title")
        title_label.setStyleSheet(
            """
            QLabel#dialog_title {
                font-size: 24px;
                font-weight: 700;
                color: rgba(255, 255, 255, 0.95);
                margin: 0px;
                padding: 0px;
            }
        """
        )
        header_layout.addWidget(title_label)

        # Spacer
        header_layout.addStretch()

        # Custom close button
        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(32, 32)
        self.close_button.setStyleSheet(
            """
            QPushButton#close_button {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#close_button:hover {
                background: rgba(239, 68, 68, 0.8);
                border: 1px solid rgba(239, 68, 68, 0.9);
                color: rgba(255, 255, 255, 1.0);
            }
            QPushButton#close_button:pressed {
                background: rgba(220, 38, 38, 0.9);
            }
        """
        )
        self.close_button.clicked.connect(self._on_cancel_clicked)
        header_layout.addWidget(self.close_button)

        container_layout.addLayout(header_layout)

        # Content area (sidebar + tabs)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Create modern sidebar with enhanced dimensions
        print("[DEBUG] Creating sidebar...")
        self.sidebar = SettingsDialogSidebar(self)
        self.sidebar.setMinimumWidth(240)
        self.sidebar.setMaximumWidth(280)
        self.sidebar.setFixedWidth(260)  # Fixed width for consistent layout
        content_layout.addWidget(self.sidebar)

        # Create stacked widget for tab content
        print("[DEBUG] Creating content area...")
        self.content_area = QStackedWidget()
        self.content_area.setMinimumWidth(500)
        content_layout.addWidget(self.content_area, stretch=1)

        # Create tabs
        print("[DEBUG] Creating tabs...")
        self._create_tabs()

        # Add content to container layout
        container_layout.addLayout(content_layout, stretch=1)

        # Create simplified action buttons (only Apply, OK, Cancel)
        print("[DEBUG] Creating action buttons...")
        self.action_buttons = ModernActionButtons()
        container_layout.addWidget(self.action_buttons)

        # Add container to main layout
        main_layout.addWidget(self.main_container)

        print("[DEBUG] Modern UI layout setup complete")

    def _create_tabs(self):
        """Create all tab widgets."""
        try:
            print("[DEBUG] Creating tab widgets...")

            # Create tabs with enhanced General tab (User Profile tab removed)
            if REAL_TABS_AVAILABLE:
                # Use real tab implementations - they expect a settings_dialog parameter
                self.tabs = {
                    "General": EnhancedGeneralTab(
                        self.settings_manager, self.state_manager, self
                    ),
                    "Prop Type": PropTypeTab(self),
                    "Visibility": VisibilityTab(self),
                    "Beat Layout": BeatLayoutTab(self),
                    "Image Export": ImageExportTab(self),
                    "Codex Exporter": CodexExporterTab(self),
                }
                print("[DEBUG] Created tabs using real implementations")
            else:
                # Use placeholder implementations
                self.tabs = {
                    "General": EnhancedGeneralTab(
                        self.settings_manager, self.state_manager, self
                    ),
                    "Prop Type": PropTypeTab(self),
                    "Visibility": VisibilityTab(self),
                    "Beat Layout": BeatLayoutTab(self),
                    "Image Export": ImageExportTab(self),
                    "Codex Exporter": CodexExporterTab(self),
                }
                print("[DEBUG] Created tabs using placeholder implementations")
            print(f"[DEBUG] Created {len(self.tabs)} tab widgets")

            # Add tabs to sidebar and content area
            for tab_name in self.tab_order:
                if tab_name in self.tabs:
                    tab_widget = self.tabs[tab_name]
                    print(f"[DEBUG] Adding tab: {tab_name}")

                    # Add to sidebar
                    self.sidebar.addItem(tab_name)

                    # Add to content area
                    self.content_area.addWidget(tab_widget)

                    logging.debug(f"Added tab: {tab_name}")

            print(f"[DEBUG] Sidebar has {self.sidebar.count()} items")
            print(f"[DEBUG] Content area has {self.content_area.count()} widgets")

            # Set default selection
            if self.sidebar.count() > 0:
                self.sidebar.setCurrentRow(0)
                self.content_area.setCurrentIndex(0)
                print("[DEBUG] Set default selection to first tab")

        except Exception as e:
            print(f"[DEBUG] Error creating tabs: {e}")
            logging.error(f"Error creating tabs: {e}")
            import traceback

            traceback.print_exc()

    def _setup_connections(self):
        """Setup signal connections."""
        try:
            # Sidebar selection
            self.sidebar.currentRowChanged.connect(self._on_tab_selected)

            # Action button connections (simplified)
            self.action_buttons.apply_requested.connect(self._on_apply_settings)
            self.action_buttons.ok_requested.connect(self._on_ok_clicked)
            self.action_buttons.cancel_requested.connect(self._on_cancel_clicked)

            # State manager connections
            self.state_manager.settings_changed.connect(self._on_setting_changed)
            self.state_manager.validation_failed.connect(self._on_validation_failed)
            self.state_manager.backup_created.connect(self._on_backup_created)
            self.state_manager.backup_restored.connect(self._on_backup_restored)

            # Enhanced General Tab connections
            if "General" in self.tabs and hasattr(
                self.tabs["General"], "setting_changed"
            ):
                self.tabs["General"].setting_changed.connect(
                    self._on_tab_setting_changed
                )

        except Exception as e:
            logging.error(f"Error setting up connections: {e}")

    def _apply_styling(self):
        """Apply glassmorphism styling to the frameless dialog."""
        try:
            # Modern 2025-level glassmorphism dialog styling for frameless design
            dialog_style = """
            /* Main dialog - transparent background for frameless effect */
            QDialog {
                background: transparent;
            }

            /* Main container with glassmorphism background */
            QWidget#main_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 41, 59, 0.95),
                    stop:0.5 rgba(51, 65, 85, 0.95),
                    stop:1 rgba(30, 41, 59, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 24px;
            }

            /* Beautiful Modern Sidebar Styling */
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:0.5 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 12px 8px;
                outline: none;
                font-size: 14px;
                font-weight: 500;
            }

            QListWidget::item {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.8);
                padding: 12px 16px;
                border-radius: 12px;
                margin: 2px 0;
                min-height: 20px;
                font-weight: 500;
            }

            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(99, 102, 241, 0.4),
                    stop:1 rgba(139, 92, 246, 0.3));
                color: rgba(255, 255, 255, 1.0);
                border: 1px solid rgba(99, 102, 241, 0.6);
                font-weight: 600;
            }

            QListWidget::item:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }

            QListWidget::item:focus {
                outline: none;
            }

            /* General label styling */
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
                background: transparent;
            }

            /* Content area styling */
            QStackedWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 8px;
            }

            """

            # Apply the main dialog style
            self.setStyleSheet(dialog_style)

            # Apply unified tab content styling to all tabs
            tab_content_style = GlassmorphismStyler.create_unified_tab_content_style()
            for tab_name, tab_widget in self.tabs.items():
                if tab_widget:
                    # Set object name for styling
                    tab_widget.setObjectName("tab_content")
                    # Apply the unified styling
                    current_style = tab_widget.styleSheet()
                    if current_style:
                        # Preserve existing styles and add new ones
                        combined_style = current_style + "\n" + tab_content_style
                    else:
                        combined_style = tab_content_style
                    tab_widget.setStyleSheet(combined_style)

            # Add shadow effect to main container for depth
            GlassmorphismStyler.add_shadow_effect(
                self.main_container, offset_y=12, blur_radius=32
            )

            # Add shadow effect to sidebar for additional depth
            GlassmorphismStyler.add_shadow_effect(
                self.sidebar, offset_x=2, offset_y=4, blur_radius=12
            )

        except Exception as e:
            logging.error(f"Error applying styling: {e}")

    def _on_tab_selected(self, index: int):
        """Handle tab selection."""
        try:
            if 0 <= index < self.content_area.count():
                self.content_area.setCurrentIndex(index)

                # Save current tab to settings
                tab_name = (
                    self.tab_order[index] if index < len(self.tab_order) else None
                )
                if tab_name and self.settings_manager:
                    self.settings_manager.global_settings.set_current_settings_dialog_tab(
                        tab_name
                    )

                logging.debug(f"Selected tab: {tab_name} (index: {index})")

        except Exception as e:
            logging.error(f"Error selecting tab: {e}")

    def _on_setting_changed(self, setting_key: str, old_value: Any, new_value: Any):
        """Handle setting change from state manager."""
        try:
            # Update action buttons to reflect changes
            has_changes = self.state_manager.is_modified()
            self.action_buttons.set_has_changes(has_changes)

            logging.debug(
                f"Setting changed: {setting_key} = {new_value} (was: {old_value})"
            )

        except Exception as e:
            logging.error(f"Error handling setting change: {e}")

    def _on_tab_setting_changed(self, setting_key: str, old_value: Any, new_value: Any):
        """Handle setting change from tab widgets."""
        # This is already handled by the state manager, but we can add additional logic here if needed
        pass

    def _on_validation_failed(self, setting_key: str, error_message: str):
        """Handle validation failure."""
        logging.warning(f"Validation failed for {setting_key}: {error_message}")
        # Could show a tooltip or status message here

    def _on_apply_settings(self):
        """Apply all pending settings changes."""
        try:
            success = self.state_manager.apply_changes()
            self.action_buttons.set_apply_success(success)
            self.settings_applied.emit(success)

            if success:
                logging.info("Settings applied successfully")
            else:
                logging.warning("Some settings failed to apply")

        except Exception as e:
            logging.error(f"Error applying settings: {e}")
            self.action_buttons.set_apply_success(False)

    def _on_ok_clicked(self):
        """Handle OK button click."""
        try:
            # Apply changes first
            if self.state_manager.is_modified():
                success = self.state_manager.apply_changes()
                self.settings_applied.emit(success)

            # Close dialog
            self.accept()

        except Exception as e:
            logging.error(f"Error in OK action: {e}")

    def _on_cancel_clicked(self):
        """Handle Cancel button click."""
        try:
            # Revert any changes
            self.state_manager.revert_changes()

            # Close dialog
            self.reject()

        except Exception as e:
            logging.error(f"Error in Cancel action: {e}")

    def _on_reset_settings(self):
        """Handle Reset to Defaults."""
        try:
            self.state_manager.reset_to_defaults()

            # Refresh all tabs
            self._refresh_all_tabs()

            logging.info("Settings reset to defaults")

        except Exception as e:
            logging.error(f"Error resetting settings: {e}")

    def _on_safe_settings(self):
        """Handle Save Settings request."""
        try:
            # This would implement a safe configuration
            # For now, just reset to defaults
            self._on_reset_settings()

        except Exception as e:
            logging.error(f"Error applying Save Settings: {e}")

    def _on_create_backup(self):
        """Handle backup creation."""
        try:
            backup_path = self.state_manager.create_backup()
            logging.info(f"Backup created: {backup_path}")

        except Exception as e:
            logging.error(f"Error creating backup: {e}")

    def _on_restore_backup(self, backup_path: str):
        """Handle backup restoration."""
        try:
            success = self.state_manager.restore_backup(backup_path)
            if success:
                self._refresh_all_tabs()
                logging.info(f"Backup restored: {backup_path}")
            else:
                logging.error(f"Failed to restore backup: {backup_path}")

        except Exception as e:
            logging.error(f"Error restoring backup: {e}")

    def _on_backup_created(self, backup_path: str):
        """Handle backup created signal."""
        logging.info(f"Backup created successfully: {backup_path}")

    def _on_backup_restored(self, backup_path: str):
        """Handle backup restored signal."""
        logging.info(f"Backup restored successfully: {backup_path}")

    def _refresh_all_tabs(self):
        """Refresh all tab contents from current settings."""
        try:
            for tab_name, tab_widget in self.tabs.items():
                if hasattr(tab_widget, "refresh_settings"):
                    tab_widget.refresh_settings()

        except Exception as e:
            logging.error(f"Error refreshing tabs: {e}")

    def showEvent(self, event: QEvent):
        """Handle dialog show event."""
        super().showEvent(event)

        try:
            # Center the dialog when shown
            self._center_dialog()

            # Restore last selected tab
            last_tab = None
            if self.settings_manager and hasattr(
                self.settings_manager, "global_settings"
            ):
                last_tab = (
                    self.settings_manager.global_settings.get_current_settings_dialog_tab()
                )

            # Find tab index
            if last_tab and last_tab in self.tab_order:
                tab_index = self.tab_order.index(last_tab)
                self.sidebar.setCurrentRow(tab_index)
                self.content_area.setCurrentIndex(tab_index)

            # Update specific tabs
            self._update_tab_on_show(last_tab or self.tab_order[0])

        except Exception as e:
            logging.error(f"Error in showEvent: {e}")

    def mousePressEvent(self, event):
        """Handle mouse press for dragging frameless dialog."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Store the position where the mouse was pressed
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging frameless dialog."""
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and self.drag_position is not None
        ):
            # Move the dialog to the new position
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def _update_tab_on_show(self, tab_name: str):
        """Update specific tab when dialog is shown."""
        try:
            if tab_name in self.tabs:
                tab_widget = self.tabs[tab_name]

                # Call specific update methods based on tab type
                if tab_name == "Prop Type" and hasattr(
                    tab_widget, "update_active_prop_type_from_settings"
                ):
                    tab_widget.update_active_prop_type_from_settings()
                elif tab_name == "Visibility" and hasattr(tab_widget, "buttons_widget"):
                    tab_widget.buttons_widget.update_visibility_buttons_from_settings()
                elif tab_name == "Beat Layout" and hasattr(
                    tab_widget, "on_sequence_length_changed"
                ):
                    beat_count = (
                        self.main_widget.sequence_workbench.beat_frame.get.beat_count()
                    )
                    tab_widget.on_sequence_length_changed(beat_count)
                    if hasattr(tab_widget, "controls"):
                        tab_widget.controls.length_selector.num_beats_spinbox.setValue(
                            beat_count
                        )
                elif tab_name == "Image Export" and hasattr(
                    tab_widget, "update_image_export_tab_from_settings"
                ):
                    tab_widget.update_image_export_tab_from_settings()
                elif tab_name == "Codex Exporter" and hasattr(
                    tab_widget, "update_codex_exporter_tab_from_settings"
                ):
                    tab_widget.update_codex_exporter_tab_from_settings()
                elif tab_name == "General" and hasattr(tab_widget, "refresh_settings"):
                    tab_widget.refresh_settings()

        except Exception as e:
            logging.error(f"Error updating tab {tab_name} on show: {e}")

    def closeEvent(self, event):
        """Handle dialog close event."""
        try:
            # Check for unsaved changes
            if self.state_manager.is_modified():
                # Changes will be handled by cancel/ok buttons
                pass

            self.dialog_closed.emit()
            super().closeEvent(event)

        except Exception as e:
            logging.error(f"Error in closeEvent: {e}")
            super().closeEvent(event)
