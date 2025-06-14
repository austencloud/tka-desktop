"""
Modern action buttons for the settings dialog.

Provides Apply, OK, and Cancel buttons with modern styling and state management.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

if TYPE_CHECKING:
    from src.core.application_context import ApplicationContext


class ModernActionButtons(QWidget):
    """
    Modern action buttons with glassmorphism styling and proper state management.
    
    Responsibilities:
    - Provide Apply, OK, Cancel buttons
    - Handle button state management
    - Apply modern styling
    - Emit appropriate signals
    """

    # Signals - only essential buttons
    apply_requested = pyqtSignal()
    ok_requested = pyqtSignal()
    cancel_requested = pyqtSignal()

    def __init__(self, app_context: "ApplicationContext" = None):
        super().__init__()
        self.app_context = app_context
        self._has_changes = False
        
        self._setup_ui()
        self._setup_connections()
        self._update_button_states()

    def _setup_ui(self):
        """Setup the button layout and create buttons."""
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

    def _setup_connections(self):
        """Setup signal connections."""
        self.apply_btn.clicked.connect(self.apply_requested.emit)
        self.ok_btn.clicked.connect(self.ok_requested.emit)
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)

    def _create_modern_button(self, text: str, style_type: str = "primary") -> QPushButton:
        """Create a modern button with glassmorphism styling."""
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

        # Apply modern styling
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

    def set_has_changes(self, has_changes: bool):
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

    def set_apply_success(self, success: bool):
        """Handle apply operation result."""
        if success:
            # Reset changes state after successful apply
            self.set_has_changes(False)
