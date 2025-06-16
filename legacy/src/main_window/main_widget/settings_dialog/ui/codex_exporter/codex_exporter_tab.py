"""
Tab for exporting pictographs with turns.
Modern 2025 UI design with glass-morphism and gradient effects.
"""

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)

from PyQt6.QtGui import QFont, QColor


from main_window.main_widget.settings_dialog.ui.codex_exporter.codex_exporter import (
    CodexExporter,
)
from main_window.main_widget.settings_dialog.ui.codex_exporter.components.turn_config_container import (
    TurnConfigContainer,
)
from main_window.main_widget.settings_dialog.ui.codex_exporter.widgets import (
    ModernButton,
)

from .theme import Colors, Sizing

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
        LegacySettingsDialog,
    )


class CodexExporterTab(QWidget):
    """Tab for exporting pictographs with turns."""

    def __init__(self, settings_dialog: "LegacySettingsDialog"):
        """Initialize the tab.

        Args:
            settings_dialog: The parent settings dialog
        """
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget

        # Get settings_manager from dependency injection system
        try:
            self.settings_manager = self.main_widget.app_context.settings_manager
        except AttributeError:
            # Fallback for cases where app_context is not available during initialization
            self.settings_manager = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during CodexExporterTab initialization"
            )

        self.codex_exporter = CodexExporter(self)

        # Create components
        self.turn_configuration = TurnConfigContainer(self)
        self.export_button = ModernButton("Export All Pictographs", primary=True)
        self.export_button.clicked.connect(self._export_pictographs)

        # Set up the UI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the tab UI with modern 2025 styling."""
        # Create sizing instance for responsive UI
        sizing = Sizing(self)

        # Set the background gradient for the entire tab
        self.setStyleSheet(f"background: {Colors.BACKGROUND_GRADIENT};")

        # Use proportional layout with relative spacing
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(sizing.spacing_lg)
        main_layout.setContentsMargins(
            sizing.margin_lg, sizing.margin_lg, sizing.margin_lg, sizing.margin_lg
        )

        # Create a main card for the codex exporter
        main_card = QFrame(self)
        main_card.setObjectName("mainCard")
        # Set a minimum height to ensure the card takes up more vertical space
        main_card.setMinimumHeight(500)  # Adjust this value as needed
        main_card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        main_card.setStyleSheet(
            f"""
            #mainCard {{
                background: {Colors.CARD_GRADIENT};
                border-radius: {sizing.border_radius_lg}px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """
        )

        # Add shadow effect to the main card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        main_card.setGraphicsEffect(shadow)

        # Create card layout with proportional spacing
        card_layout = QVBoxLayout(main_card)
        card_layout.setSpacing(sizing.spacing_md)
        card_layout.setContentsMargins(
            sizing.margin_md, sizing.margin_md, sizing.margin_md, sizing.margin_md
        )

        # Add title to the card with responsive font size
        title_label = QLabel("Codex Exporter", main_card)
        title_label.setObjectName("cardTitle")

        # Set font using theme sizing
        title_font = QFont()
        title_font.setPointSize(sizing.font_xlarge)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)

        # The styling for the title is included in the card style
        card_layout.addWidget(title_label)

        # Add separator
        separator = QFrame(main_card)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background: {Colors.SEPARATOR_GRADIENT};")
        card_layout.addWidget(separator)
        card_layout.addSpacing(sizing.spacing_sm)

        # Modify the turn configuration component
        # Remove the title from the turn configuration component
        self.turn_configuration.findChild(QLabel, "cardTitle").setVisible(False)

        # Apply glass-morphism effect to the turn configuration component
        self.turn_configuration.setStyleSheet(
            f"""
            QFrame[cssClass="card"] {{
                background-color: rgba(30, 30, 46, 0.7);
                border-radius: {sizing.border_radius_lg}px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }}
        """
        )

        # Make the turn configuration expand to fill available space
        self.turn_configuration.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Add the turn configuration to the card layout
        card_layout.addWidget(
            self.turn_configuration, 1
        )  # Give it a stretch factor of 1

        # Add the main card to the main layout with a stretch factor
        main_layout.addWidget(main_card, 1)  # Give it a stretch factor of 1

        # Style the export button with modern gradient
        self.export_button.setMinimumHeight(sizing.button_height)
        self.export_button.setMinimumWidth(sizing.button_height * 4)
        self.export_button.setStyleSheet(
            f"""
            QPushButton {{
                background: {Colors.BUTTON_GRADIENT};
                color: #121212;
                border: none;
                border-radius: {sizing.border_radius_md}px;
                padding: {sizing.spacing_sm}px {sizing.spacing_lg}px;
                font-weight: bold;
                font-size: {sizing.font_medium}px;
            }}
            QPushButton:hover {{
                background: {Colors.BUTTON_HOVER_GRADIENT};
            }}
            QPushButton:pressed {{
                background: {Colors.BUTTON_PRESSED_GRADIENT};
            }}
        """
        )

        # Add button shadow
        button_shadow = QGraphicsDropShadowEffect(self)
        button_shadow.setBlurRadius(20)
        button_shadow.setColor(QColor(79, 255, 143, 100))
        button_shadow.setOffset(0, 4)
        self.export_button.setGraphicsEffect(button_shadow)

        # Export button layout with improved spacing
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.export_button)
        main_layout.addLayout(button_layout)

    def get_selected_letters(self):
        """Get the selected letters to export.

        Returns:
            A list of letters to export
        """
        # Include all letters (A-V, W, X, Y, Z, Σ, Δ, θ, Ω)
        all_letters = (
            list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            + ["Σ", "Δ", "θ", "Ω"]
            + [
                "W-",
                "X-",
                "Y-",
                "Z-",
                "Σ-",
                "Δ-",
                "θ-",
                "Ω-",
            ]
        )
        return all_letters

    def _export_pictographs(self):
        """Export all pictographs with the configured turns."""
        # Get all letters to export
        all_letters = self.get_selected_letters()

        # Get the turn configuration
        turn_config = self.turn_configuration.get_turn_values()
        red_turns = turn_config["red_turns"]
        blue_turns = turn_config["blue_turns"]
        generate_all = turn_config["generate_all"]
        grid_mode = turn_config["grid_mode"]

        # Save the settings for next time
        self.settings_manager.codex_exporter.set_last_red_turns(red_turns)
        self.settings_manager.codex_exporter.set_last_blue_turns(blue_turns)
        self.settings_manager.codex_exporter.set_grid_mode(grid_mode)

        # Export the pictographs
        self.codex_exporter.export_pictographs(
            all_letters, red_turns, blue_turns, generate_all, grid_mode
        )

    def update_codex_exporter_tab_from_settings(self):
        """Update the tab from settings.

        This method is called when the tab is shown or when settings are changed.
        The turn configuration components already load their settings when initialized,
        so we don't need to do anything here.
        """
