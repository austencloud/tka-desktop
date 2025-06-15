from typing import List, Optional, Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject

from core.dependency_injection.di_container import SimpleContainer
from core.interfaces.core_services import ILayoutService
from domain.models.core_models import BeatData
from .pictograph_pool_manager import PictographPoolManager
from .beat_data_loader import BeatDataLoader
from .display_manager import OptionPickerDisplayManager
from .widget_factory import OptionPickerWidgetFactory
from .dimension_analyzer import OptionPickerDimensionAnalyzer
from .option_picker_filter import OptionPickerFilter


class ModernOptionPicker(QObject):
    option_selected = pyqtSignal(str)
    beat_data_selected = pyqtSignal(object)  # New signal for actual BeatData

    def __init__(self, container: SimpleContainer, progress_callback=None):
        super().__init__()
        self.container = container
        self.progress_callback = progress_callback

        # Core components
        self.widget: Optional[QWidget] = None
        self.sections_container: Optional[QWidget] = None
        self.sections_layout: Optional[QVBoxLayout] = None
        self.filter_widget: Optional[OptionPickerFilter] = None

        # Service components
        self._layout_service: Optional[ILayoutService] = None
        self._pool_manager: Optional[PictographPoolManager] = None
        self._beat_loader: Optional[BeatDataLoader] = None
        self._display_manager: Optional[OptionPickerDisplayManager] = None
        self._widget_factory: Optional[OptionPickerWidgetFactory] = None
        self._dimension_analyzer: Optional[OptionPickerDimensionAnalyzer] = None

    def initialize(self) -> None:
        """Initialize the option picker with all components"""
        if self.progress_callback:
            self.progress_callback("Resolving layout service", 0.1)

        self._layout_service = self.container.resolve(ILayoutService)

        if self.progress_callback:
            self.progress_callback("Creating widget factory", 0.15)

        self._widget_factory = OptionPickerWidgetFactory(self.container)

        if self.progress_callback:
            self.progress_callback("Creating option picker widget", 0.2)

        (
            self.widget,
            self.sections_container,
            self.sections_layout,
            self.filter_widget,
        ) = self._widget_factory.create_widget(self._on_widget_resize)

        if self.progress_callback:
            self.progress_callback("Initializing pool manager", 0.25)

        self._pool_manager = PictographPoolManager(self.widget)
        self._pool_manager.set_click_handler(self._handle_beat_click)
        self._pool_manager.set_beat_data_click_handler(self._handle_beat_data_click)

        if self.progress_callback:
            self.progress_callback("Initializing display manager", 0.3)

        # Create size provider that gives sections the full available width
        def mw_size_provider():
            from PyQt6.QtCore import QSize

            # Get actual available width from the option picker widget hierarchy
            if self.widget and self.widget.width() > 0:
                # In V2, the option picker IS the full available space
                # So sections should use the full widget width, not half
                actual_width = self.widget.width()
                actual_height = self.widget.height()
                # Return the actual size - sections will use full width
                return QSize(actual_width, actual_height)
            else:
                # Fallback for initialization phase
                return QSize(1200, 800)

        self._display_manager = OptionPickerDisplayManager(
            self.sections_container,
            self.sections_layout,
            self._pool_manager,
            mw_size_provider,
        )

        if self.progress_callback:
            self.progress_callback("Initializing beat data loader", 0.35)

        self._beat_loader = BeatDataLoader()

        if self.progress_callback:
            self.progress_callback("Initializing dimension analyzer", 0.4)

        self._dimension_analyzer = OptionPickerDimensionAnalyzer(
            self.widget,
            self.sections_container,
            self.sections_layout,
            self._display_manager.get_sections(),
        )

        if self.progress_callback:
            self.progress_callback("Initializing pictograph pool", 0.45)

        self._pool_manager.initialize_pool(self.progress_callback)

        if self.progress_callback:
            self.progress_callback("Creating sections", 0.85)

        self._display_manager.create_sections()

        if self.progress_callback:
            self.progress_callback("Setting up filter connections", 0.9)

        self.filter_widget.filter_changed.connect(self._on_filter_changed)

        if self.progress_callback:
            self.progress_callback("Loading initial beat options", 0.95)

        self._load_beat_options()

        if self.progress_callback:
            self.progress_callback("Option picker initialization complete", 1.0)

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """Load motion combinations using data-driven position matching"""
        if not self._beat_loader or not self._display_manager:
            print("❌ Components not initialized")
            return

        beat_options = self._beat_loader.load_motion_combinations(sequence_data)
        self._display_manager.update_beat_display(beat_options)
        self._ensure_sections_visible()

    def _load_beat_options(self) -> None:
        """Load initial beat options"""
        if not self._beat_loader or not self._display_manager:
            return

        beat_options = self._beat_loader.refresh_options()
        self._display_manager.update_beat_display(beat_options)

    def _ensure_sections_visible(self) -> None:
        """Ensure sections are visible after loading combinations"""
        if self._display_manager:
            sections = self._display_manager.get_sections()
            for section in sections.values():
                if hasattr(section, "pictograph_container"):
                    section.pictograph_container.setVisible(True)

    def _handle_beat_click(self, beat_id: str) -> None:
        """Handle beat selection clicks (legacy compatibility)"""
        self.option_selected.emit(beat_id)

    def _handle_beat_data_click(self, beat_data: BeatData) -> None:
        """Handle beat data selection clicks (new precise method)"""
        self.beat_data_selected.emit(beat_data)

    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """Get BeatData for a specific option ID (e.g., 'beat_J' -> BeatData with letter='J')"""
        if not self._beat_loader:
            return None

        # Extract letter from option_id (e.g., "beat_J" -> "J")
        if option_id.startswith("beat_"):
            target_letter = option_id[5:]  # Remove "beat_" prefix

            # Search through current beat options for matching letter
            beat_options = self._beat_loader.get_beat_options()
            for beat_data in beat_options:
                if beat_data.letter == target_letter:
                    print(
                        f"✅ Found beat data for option {option_id}: {beat_data.letter}"
                    )
                    return beat_data

            print(
                f"❌ No beat data found for option {option_id} (letter: {target_letter})"
            )
            return None
        else:
            print(f"❌ Invalid option ID format: {option_id}")
            return None

    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options"""
        if self._beat_loader and self._display_manager:
            beat_options = self._beat_loader.refresh_options()
            self._display_manager.update_beat_display(beat_options)
            print(f"🔄 Option picker refreshed with {len(beat_options)} options")

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> None:
        """Refresh options based on sequence state (V1-compatible dynamic updates)"""
        if self._beat_loader and self._display_manager:
            beat_options = self._beat_loader.refresh_options_from_sequence(
                sequence_data
            )
            self._display_manager.update_beat_display(beat_options)
            print(
                f"🔄 Option picker dynamically refreshed with {len(beat_options)} options"
            )

    def _on_widget_resize(self) -> None:
        """Handle widget resize events"""
        if self._pool_manager:
            self._pool_manager.resize_all_frames()

        # CRITICAL: Resize bottom row sections to proper 1/3 width
        if self._display_manager:
            self._display_manager.resize_bottom_row_sections()

    def _on_filter_changed(self, filter_text: str) -> None:
        """Handle filter changes"""
        if self._beat_loader and self._display_manager:
            beat_options = self._beat_loader.get_beat_options()
            self._display_manager.update_beat_display(beat_options)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the widget"""
        if self.widget:
            self.widget.setEnabled(enabled)

    def get_size(self) -> tuple[int, int]:
        """Get widget size"""
        if self._widget_factory:
            return self._widget_factory.get_size()
        return (600, 800)

    def log_dimensions(self, phase: str) -> None:
        """Log comprehensive dimension analysis"""
        if self._dimension_analyzer:
            self._dimension_analyzer.log_all_container_dimensions(phase)
