"""
Glassmorphism Styler for modern UI design with translucent backgrounds and blur effects.
"""

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPalette, QFont, QFontMetrics
from PyQt6.QtWidgets import QWidget, QGraphicsBlurEffect, QGraphicsDropShadowEffect
import logging


class GlassmorphismStyler:
    """
    Provides modern glassmorphism styling for UI components.
    Features translucent backgrounds, blur effects, and elegant borders.
    """

    # Modern color palette
    COLORS = {
        "primary": "#6366f1",  # Indigo
        "primary_light": "#818cf8",  # Light indigo
        "primary_dark": "#4f46e5",  # Dark indigo
        "secondary": "#8b5cf6",  # Purple
        "accent": "#06b6d4",  # Cyan
        "success": "#10b981",  # Emerald
        "warning": "#f59e0b",  # Amber
        "error": "#ef4444",  # Red
        "surface": "#1f2937",  # Dark gray
        "surface_light": "#374151",  # Medium gray
        "surface_lighter": "#4b5563",  # Light gray
        "background": "#111827",  # Very dark gray
        "text_primary": "#f9fafb",  # Almost white
        "text_secondary": "#d1d5db",  # Light gray
        "text_muted": "#9ca3af",  # Medium gray
        "border": "#374151",  # Medium gray
        "border_light": "#4b5563",  # Light gray
    }

    # Typography scale
    FONTS = {
        "heading_large": {"size": 24, "weight": "bold"},
        "heading_medium": {"size": 20, "weight": "bold"},
        "heading_small": {"size": 16, "weight": "bold"},
        "body_large": {"size": 14, "weight": "normal"},
        "body_medium": {"size": 12, "weight": "normal"},
        "body_small": {"size": 10, "weight": "normal"},
        "caption": {"size": 9, "weight": "normal"},
    }

    # Spacing scale
    SPACING = {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
        "xxl": 48,
    }

    # Border radius scale
    RADIUS = {
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16,
        "full": 9999,
    }

    @classmethod
    def get_color(cls, color_name: str, alpha: float = 1.0) -> str:
        """Get color with optional alpha transparency."""
        if color_name not in cls.COLORS:
            logging.warning(f"Unknown color: {color_name}")
            return cls.COLORS["text_primary"]

        color = cls.COLORS[color_name]
        if alpha < 1.0:
            # Convert hex to rgba
            color = color.lstrip("#")
            r, g, b = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
            return f"rgba({r}, {g}, {b}, {alpha})"
        return color

    @classmethod
    def get_font(cls, font_type: str) -> QFont:
        """Get font with specified type."""
        if font_type not in cls.FONTS:
            font_type = "body_medium"

        font_config = cls.FONTS[font_type]
        font = QFont()
        font.setPointSize(font_config["size"])

        if font_config["weight"] == "bold":
            font.setBold(True)

        return font

    @classmethod
    def create_glassmorphism_card(
        cls,
        widget: QWidget,
        blur_radius: int = 10,
        opacity: float = 0.1,
        border_radius: int = 12,
    ) -> str:
        """
        Create glassmorphism card styling for a widget.

        Args:
            widget: The widget to style
            blur_radius: Blur effect radius
            opacity: Background opacity (0.0 - 1.0)
            border_radius: Corner radius

        Returns:
            CSS stylesheet string
        """
        return f"""
        QWidget {{
            background-color: {cls.get_color('surface', opacity)};
            border: 1px solid {cls.get_color('border_light', 0.3)};
            border-radius: {border_radius}px;
            padding: {cls.SPACING['md']}px;
        }}

        QWidget:hover {{
            background-color: {cls.get_color('surface_light', opacity + 0.05)};
            border-color: {cls.get_color('border_light', 0.5)};
        }}
        """

    @classmethod
    def create_modern_button(cls, button_type: str = "primary") -> str:
        """
        Create modern button styling.

        Args:
            button_type: 'primary', 'secondary', 'success', 'warning', 'error'
        """
        base_color = cls.get_color(button_type)
        hover_color = (
            cls.get_color(f"{button_type}_light")
            if f"{button_type}_light" in cls.COLORS
            else base_color
        )

        return f"""
        QPushButton {{
            background-color: {base_color};
            color: {cls.get_color('text_primary')};
            border: none;
            border-radius: {cls.RADIUS['md']}px;
            padding: {cls.SPACING['sm']}px {cls.SPACING['md']}px;
            font-size: {cls.FONTS['body_medium']['size']}px;
            font-weight: 500;
            min-height: 32px;
        }}

        QPushButton:hover {{
            background-color: {hover_color};
            border: 1px solid {cls.get_color('primary_light', 0.5)};
        }}

        QPushButton:pressed {{
            background-color: {cls.get_color(f"{button_type}_dark") if f"{button_type}_dark" in cls.COLORS else base_color};
            border: 1px solid {cls.get_color('primary_dark', 0.7)};
        }}

        QPushButton:disabled {{
            background-color: {cls.get_color('surface_light')};
            color: {cls.get_color('text_muted')};
        }}
        """

    @classmethod
    def create_modern_input(cls) -> str:
        """Create modern input field styling."""
        return f"""
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {cls.get_color('surface', 0.5)};
            border: 1px solid {cls.get_color('border')};
            border-radius: {cls.RADIUS['md']}px;
            padding: {cls.SPACING['sm']}px {cls.SPACING['md']}px;
            color: {cls.get_color('text_primary')};
            font-size: {cls.FONTS['body_medium']['size']}px;
            min-height: 32px;
        }}

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border-color: {cls.get_color('primary')};
            background-color: {cls.get_color('surface', 0.7)};
        }}

        QLineEdit:hover, QTextEdit:hover, QComboBox:hover {{
            border-color: {cls.get_color('border_light')};
        }}
        """

    @classmethod
    def create_modern_toggle(cls) -> str:
        """Create modern toggle switch styling."""
        return f"""
        QCheckBox {{
            color: {cls.get_color('text_primary')};
            font-size: {cls.FONTS['body_medium']['size']}px;
            spacing: {cls.SPACING['sm']}px;
        }}

        QCheckBox::indicator {{
            width: 48px;
            height: 24px;
            border-radius: 12px;
            background-color: {cls.get_color('surface_light')};
            border: 1px solid {cls.get_color('border')};
        }}

        QCheckBox::indicator:checked {{
            background-color: {cls.get_color('primary')};
            border-color: {cls.get_color('primary')};
        }}

        QCheckBox::indicator:hover {{
            border-color: {cls.get_color('border_light')};
        }}
        """

    @classmethod
    def create_modern_slider(cls) -> str:
        """Create modern slider styling."""
        return f"""
        QSlider::groove:horizontal {{
            height: 6px;
            background-color: {cls.get_color('surface_light')};
            border-radius: 3px;
        }}

        QSlider::handle:horizontal {{
            background-color: {cls.get_color('primary')};
            border: 2px solid {cls.get_color('primary')};
            width: 20px;
            height: 20px;
            border-radius: 10px;
            margin: -7px 0;
        }}

        QSlider::handle:horizontal:hover {{
            background-color: {cls.get_color('primary_light')};
            border-color: {cls.get_color('primary_light')};
        }}

        QSlider::sub-page:horizontal {{
            background-color: {cls.get_color('primary')};
            border-radius: 3px;
        }}
        """

    @classmethod
    def create_sidebar_style(cls) -> str:
        """Create modern 2025-level glassmorphism sidebar styling."""
        return f"""
        QListWidget {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.get_color('surface', 0.4)},
                stop:0.5 {cls.get_color('surface_light', 0.3)},
                stop:1 {cls.get_color('surface', 0.4)});
            border: 1px solid {cls.get_color('border', 0.2)};
            border-radius: {cls.RADIUS['lg']}px;
            padding: {cls.SPACING['md']}px {cls.SPACING['sm']}px;
            outline: none;
        }}

        QListWidget::item {{
            background-color: transparent;
            color: {cls.get_color('text_secondary')};
            padding: {cls.SPACING['md']}px {cls.SPACING['lg']}px;
            border-radius: {cls.RADIUS['md']}px;
            margin: {cls.SPACING['xs']}px 0;
            font-size: {cls.FONTS['body_medium']['size']}px;
            font-weight: 500;
            min-height: 32px;
        }}

        QListWidget::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.get_color('primary', 0.3)},
                stop:1 {cls.get_color('primary_light', 0.2)});
            color: {cls.get_color('text_primary')};
            border: 1px solid {cls.get_color('primary', 0.4)};
            font-weight: 600;
        }}

        QListWidget::item:hover:!selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.get_color('surface_light', 0.6)},
                stop:1 {cls.get_color('surface_lighter', 0.4)});
            color: {cls.get_color('text_primary')};
            border: 1px solid {cls.get_color('border_light', 0.3)};
        }}

        QListWidget::item:focus {{
            outline: none;
        }}
        """

    @classmethod
    def create_dialog_style(cls) -> str:
        """Create modern dialog styling."""
        return f"""
        QDialog {{
            background-color: {cls.get_color('background')};
            color: {cls.get_color('text_primary')};
            border-radius: {cls.RADIUS['xl']}px;
        }}

        QTabWidget::pane {{
            background-color: {cls.get_color('surface', 0.1)};
            border: 1px solid {cls.get_color('border', 0.3)};
            border-radius: {cls.RADIUS['lg']}px;
            padding: {cls.SPACING['lg']}px;
        }}

        QScrollArea {{
            background-color: transparent;
            border: none;
        }}

        QScrollBar:vertical {{
            background-color: {cls.get_color('surface')};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {cls.get_color('surface_light')};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {cls.get_color('surface_lighter')};
        }}
        """

    @classmethod
    def add_blur_effect(cls, widget: QWidget, blur_radius: int = 10):
        """Add blur effect to a widget."""
        try:
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(blur_radius)
            widget.setGraphicsEffect(blur_effect)
        except Exception as e:
            logging.warning(f"Could not apply blur effect: {e}")

    @classmethod
    def add_shadow_effect(
        cls,
        widget: QWidget,
        offset_x: int = 0,
        offset_y: int = 4,
        blur_radius: int = 12,
        color: str = None,
    ):
        """Add drop shadow effect to a widget."""
        try:
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setOffset(offset_x, offset_y)
            shadow_effect.setBlurRadius(blur_radius)

            if color:
                shadow_color = QColor(color)
            else:
                shadow_color = QColor(0, 0, 0, 50)  # Semi-transparent black

            shadow_effect.setColor(shadow_color)
            widget.setGraphicsEffect(shadow_effect)
        except Exception as e:
            logging.warning(f"Could not apply shadow effect: {e}")

    @classmethod
    def create_unified_tab_content_style(cls) -> str:
        """Create comprehensive glassmorphism styling for all tab content."""
        return f"""
        /* Base tab content styling */
        QWidget[objectName="tab_content"] {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.get_color('surface', 0.05)},
                stop:0.5 {cls.get_color('surface_light', 0.03)},
                stop:1 {cls.get_color('surface', 0.05)});
            border: 1px solid {cls.get_color('border', 0.15)};
            border-radius: {cls.RADIUS['lg']}px;
            padding: {cls.SPACING['lg']}px;
        }}

        /* Group boxes with glassmorphism */
        QGroupBox {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.get_color('surface', 0.1)},
                stop:1 {cls.get_color('surface_light', 0.08)});
            border: 1px solid {cls.get_color('border_light', 0.3)};
            border-radius: {cls.RADIUS['md']}px;
            padding: {cls.SPACING['lg']}px {cls.SPACING['md']}px;
            margin-top: {cls.SPACING['md']}px;
            font-size: {cls.FONTS['heading_small']['size']}px;
            font-weight: 600;
            color: {cls.get_color('text_primary')};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 {cls.SPACING['sm']}px;
            background: {cls.get_color('primary', 0.8)};
            border-radius: {cls.RADIUS['sm']}px;
            color: {cls.get_color('text_primary')};
            font-weight: 600;
            margin-left: {cls.SPACING['md']}px;
        }}

        /* Modern form elements */
        QLineEdit, QTextEdit, QComboBox, QSpinBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('surface', 0.6)},
                stop:1 {cls.get_color('surface_light', 0.4)});
            border: 1px solid {cls.get_color('border', 0.4)};
            border-radius: {cls.RADIUS['md']}px;
            padding: {cls.SPACING['sm']}px {cls.SPACING['md']}px;
            color: {cls.get_color('text_primary')};
            font-size: {cls.FONTS['body_medium']['size']}px;
            min-height: 32px;
            selection-background-color: {cls.get_color('primary', 0.3)};
        }}

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
            border: 2px solid {cls.get_color('primary', 0.8)};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('surface_light', 0.7)},
                stop:1 {cls.get_color('surface_lighter', 0.5)});
        }}

        QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover {{
            border-color: {cls.get_color('border_light', 0.6)};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('surface_light', 0.6)},
                stop:1 {cls.get_color('surface_lighter', 0.4)});
        }}

        /* Modern buttons */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('primary', 0.9)},
                stop:1 {cls.get_color('primary_dark', 0.8)});
            color: {cls.get_color('text_primary')};
            border: 1px solid {cls.get_color('primary', 0.5)};
            border-radius: {cls.RADIUS['md']}px;
            padding: {cls.SPACING['sm']}px {cls.SPACING['lg']}px;
            font-size: {cls.FONTS['body_medium']['size']}px;
            font-weight: 500;
            min-height: 36px;
            min-width: 80px;
        }}

        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('primary_light', 0.9)},
                stop:1 {cls.get_color('primary', 0.8)});
            border: 1px solid {cls.get_color('primary_light', 0.7)};
            transform: translateY(-1px);
        }}

        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('primary_dark', 0.9)},
                stop:1 {cls.get_color('primary_dark', 0.7)});
            border: 1px solid {cls.get_color('primary_dark', 0.8)};
            transform: translateY(1px);
        }}

        QPushButton:disabled {{
            background: {cls.get_color('surface_light', 0.3)};
            color: {cls.get_color('text_muted')};
            border: 1px solid {cls.get_color('border', 0.2)};
        }}

        /* Modern checkboxes */
        QCheckBox {{
            color: {cls.get_color('text_primary')};
            font-size: {cls.FONTS['body_medium']['size']}px;
            spacing: {cls.SPACING['md']}px;
            padding: {cls.SPACING['sm']}px 0;
        }}

        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: {cls.RADIUS['sm']}px;
            background: {cls.get_color('surface', 0.6)};
            border: 2px solid {cls.get_color('border', 0.5)};
        }}

        QCheckBox::indicator:checked {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.get_color('primary')},
                stop:1 {cls.get_color('primary_light')});
            border: 2px solid {cls.get_color('primary')};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }}

        QCheckBox::indicator:hover {{
            border-color: {cls.get_color('border_light', 0.7)};
            background: {cls.get_color('surface_light', 0.6)};
        }}

        /* Modern labels */
        QLabel {{
            color: {cls.get_color('text_primary')};
            font-size: {cls.FONTS['body_medium']['size']}px;
            padding: {cls.SPACING['xs']}px 0;
        }}

        /* Scroll areas */
        QScrollArea {{
            background: transparent;
            border: none;
            border-radius: {cls.RADIUS['md']}px;
        }}

        QScrollArea > QWidget > QWidget {{
            background: transparent;
        }}

        /* Modern scroll bars */
        QScrollBar:vertical {{
            background: {cls.get_color('surface', 0.3)};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.get_color('surface_light', 0.8)},
                stop:1 {cls.get_color('surface_lighter', 0.6)});
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.get_color('primary', 0.6)},
                stop:1 {cls.get_color('primary_light', 0.4)});
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
            background: transparent;
        }}

        QScrollBar:horizontal {{
            background: {cls.get_color('surface', 0.3)};
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('surface_light', 0.8)},
                stop:1 {cls.get_color('surface_lighter', 0.6)});
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.get_color('primary', 0.6)},
                stop:1 {cls.get_color('primary_light', 0.4)});
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
            background: transparent;
        }}
        """
