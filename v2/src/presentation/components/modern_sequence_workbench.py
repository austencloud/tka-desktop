from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from ...core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from ...domain.models.core_models import SequenceData, BeatData
from ...core.interfaces.core_services import ILayoutService
from ...application.services.beat_frame_layout_service import BeatFrameLayoutService
from src.presentation.components.sequence_workbench.beat_frame.modern_beat_frame import (
    ModernBeatFrame,
)


class ModernSequenceWorkbench(QWidget):
    """Modern sequence workbench component following v2 architecture patterns"""

    # Signals for communication with other components
    sequence_modified = pyqtSignal(SequenceData)
    operation_completed = pyqtSignal(str)  # message
    error_occurred = pyqtSignal(str)  # error message

    def __init__(
        self,
        layout_service: ILayoutService,
        workbench_service: ISequenceWorkbenchService,
        fullscreen_service: IFullScreenService,
        deletion_service: IBeatDeletionService,
        graph_service: IGraphEditorService,
        dictionary_service: IDictionaryService,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Store injected dependencies (no global state access!)
        self._layout_service = layout_service
        self._workbench_service = workbench_service
        self._fullscreen_service = fullscreen_service
        self._deletion_service = deletion_service
        self._graph_service = graph_service
        self._dictionary_service = dictionary_service

        # Current sequence state
        self._current_sequence: Optional[SequenceData] = None

        # Start position state (separate from sequence beats like v1)
        self._start_position_data: Optional[BeatData] = None

        # Beat frame component (will be initialized in _setup_ui)
        self._beat_frame: Optional[ModernBeatFrame] = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the UI layout based on v1 workbench structure"""
        layout = QVBoxLayout(self)

        # Top section: Indicator and difficulty labels
        self._setup_indicator_section(layout)

        # Main section: Beat frame area
        self._setup_beat_frame_section(layout)

        # Bottom section: Control buttons
        self._setup_button_panel(layout)

        # Side section: Graph editor (collapsible)
        self._setup_graph_section()

    def _setup_indicator_section(self, parent_layout: QVBoxLayout):
        """Setup indicator labels section"""
        indicator_layout = QHBoxLayout()

        self._indicator_label = QLabel("Ready")
        self._indicator_label.setStyleSheet(
            """
            QLabel {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                padding: 5px 10px;
                color: white;
            }
        """
        )

        self._difficulty_label = QLabel("Difficulty: -")
        self._current_word_label = QLabel("Word: -")
        self._circular_indicator = QLabel("")

        indicator_layout.addWidget(self._indicator_label)
        indicator_layout.addStretch()
        indicator_layout.addWidget(self._difficulty_label)
        indicator_layout.addWidget(self._current_word_label)
        indicator_layout.addWidget(self._circular_indicator)

        parent_layout.addLayout(indicator_layout)

    def _setup_beat_frame_section(self, parent_layout: QVBoxLayout):
        """Setup main beat frame display area with actual ModernBeatFrame"""
        # Create beat frame layout service
        beat_frame_layout_service = BeatFrameLayoutService()

        # Create the actual ModernBeatFrame component
        self._beat_frame = ModernBeatFrame(
            layout_service=beat_frame_layout_service, parent=self
        )

        # Set minimum height for proper display
        self._beat_frame.setMinimumHeight(400)

        # Connect beat frame signals to workbench
        self._beat_frame.beat_selected.connect(self._on_beat_selected)
        self._beat_frame.beat_modified.connect(self._on_beat_modified)
        self._beat_frame.sequence_modified.connect(self._on_sequence_modified)
        self._beat_frame.layout_changed.connect(self._on_layout_changed)

        parent_layout.addWidget(self._beat_frame)

    def _setup_button_panel(self, parent_layout: QVBoxLayout):
        """Setup control buttons panel based on v1 button panel"""
        button_layout = QHBoxLayout()

        # Color swap button
        self._color_swap_btn = QPushButton("Swap Colors")
        self._color_swap_btn.clicked.connect(self._handle_color_swap)

        # Reflection button
        self._reflect_btn = QPushButton("Reflect")
        self._reflect_btn.clicked.connect(self._handle_reflection)

        # Rotation button
        self._rotate_btn = QPushButton("Rotate")
        self._rotate_btn.clicked.connect(self._handle_rotation)

        # Clear button
        self._clear_btn = QPushButton("Clear")
        self._clear_btn.clicked.connect(self._handle_clear)

        # Full screen button
        self._fullscreen_btn = QPushButton("👁️")
        self._fullscreen_btn.clicked.connect(self._handle_fullscreen)

        # Copy JSON button
        self._copy_json_btn = QPushButton("Copy JSON")
        self._copy_json_btn.clicked.connect(self._handle_copy_json)

        button_layout.addWidget(self._color_swap_btn)
        button_layout.addWidget(self._reflect_btn)
        button_layout.addWidget(self._rotate_btn)
        button_layout.addWidget(self._clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self._fullscreen_btn)
        button_layout.addWidget(self._copy_json_btn)

        parent_layout.addLayout(button_layout)

    def _setup_graph_section(self):
        """Setup graph editor section"""
        # Graph editor would be a separate component
        # This maintains the v1 functionality while using modern architecture
        pass

    def _connect_signals(self):
        """Connect internal signals"""
        pass

    # Public API methods
    def set_sequence(self, sequence: SequenceData):
        """Set the current sequence to display/edit"""
        self._current_sequence = sequence
        self._update_display()

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position (separate from sequence beats like v1)"""
        self._start_position_data = start_position_data
        # Update beat frame start position display
        if self._beat_frame:
            self._beat_frame.set_start_position(start_position_data)

    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self._start_position_data

    # Event handlers that use injected services
    def _handle_color_swap(self):
        """Handle color swap button click"""
        if not self._current_sequence:
            self.error_occurred.emit("No sequence to swap colors")
            return

        try:
            swapped_sequence = self._workbench_service.swap_colors(
                self._current_sequence
            )
            self._current_sequence = swapped_sequence
            self._update_display()
            self.sequence_modified.emit(swapped_sequence)
            self.operation_completed.emit("Colors swapped!")
        except Exception as e:
            self.error_occurred.emit(f"Color swap failed: {e}")

    def _handle_reflection(self):
        """Handle reflection button click"""
        if not self._current_sequence:
            self.error_occurred.emit("No sequence to reflect")
            return

        try:
            reflected_sequence = self._workbench_service.reflect_sequence(
                self._current_sequence
            )
            self._current_sequence = reflected_sequence
            self._update_display()
            self.sequence_modified.emit(reflected_sequence)
            self.operation_completed.emit("Sequence reflected!")
        except Exception as e:
            self.error_occurred.emit(f"Reflection failed: {e}")

    def _handle_rotation(self):
        """Handle rotation button click"""
        if not self._current_sequence:
            self.error_occurred.emit("No sequence to rotate")
            return

        try:
            rotated_sequence = self._workbench_service.rotate_sequence(
                self._current_sequence
            )
            self._current_sequence = rotated_sequence
            self._update_display()
            self.sequence_modified.emit(rotated_sequence)
            self.operation_completed.emit("Sequence rotated!")
        except Exception as e:
            self.error_occurred.emit(f"Rotation failed: {e}")

    def _handle_clear(self):
        """Handle clear button click - V1 behavior: clear all beats but preserve start position"""
        try:
            # Clear all sequence beats but preserve start position (V1 behavior)
            empty_sequence = SequenceData.empty()
            self._current_sequence = empty_sequence

            # Update beat frame display - this will show only start position at (0,0)
            if self._beat_frame:
                self._beat_frame.set_sequence(empty_sequence)
                # Start position remains visible and persistent

            self.sequence_modified.emit(empty_sequence)
            self.operation_completed.emit("Sequence cleared!")

            print("🗑️ Sequence cleared - start position preserved at (0,0)")

        except Exception as e:
            self.error_occurred.emit(f"Clear failed: {e}")

    def _handle_fullscreen(self):
        """Handle full screen view button click"""
        if not self._current_sequence:
            self.error_occurred.emit("No sequence to view")
            return

        try:
            self._fullscreen_service.show_full_screen_view(self._current_sequence)
        except Exception as e:
            self.error_occurred.emit(f"Full screen view failed: {e}")

    def _handle_copy_json(self):
        """Handle copy JSON button click"""
        if not self._current_sequence:
            self.error_occurred.emit("No sequence to copy")
            return

        try:
            json_data = self._workbench_service.export_sequence_json(
                self._current_sequence
            )
            # Copy to clipboard logic would go here
            self.operation_completed.emit("Sequence JSON copied to clipboard!")
        except Exception as e:
            self.error_occurred.emit(f"JSON export failed: {e}")

    def _update_display(self):
        """Update all display elements based on current sequence"""
        if not self._current_sequence:
            self._indicator_label.setText("No sequence loaded")
            self._difficulty_label.setText("Difficulty: -")
            self._current_word_label.setText("Word: -")
            # Clear beat frame
            if self._beat_frame:
                self._beat_frame.set_sequence(None)
            return

        # Update indicator
        self._indicator_label.setText(
            f"Sequence: {self._current_sequence.length} beats"
        )

        # Update difficulty
        difficulty = self._dictionary_service.calculate_difficulty(
            self._current_sequence
        )
        self._difficulty_label.setText(f"Difficulty: {difficulty}")

        # Update word
        word = self._dictionary_service.get_word_for_sequence(self._current_sequence)
        self._current_word_label.setText(f"Word: {word or '-'}")

        # Update beat frame with sequence data
        if self._beat_frame:
            self._beat_frame.set_sequence(self._current_sequence)

        # Update graph editor
        self._graph_service.update_graph_display(self._current_sequence)

    # Beat frame signal handlers
    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from beat frame"""
        # Could emit a signal or update UI state based on selection
        pass

    def _on_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from beat frame"""
        if not self._current_sequence:
            return

        # Update the sequence with the modified beat
        new_beats = list(self._current_sequence.beats)
        if beat_index < len(new_beats):
            new_beats[beat_index] = beat_data
            self._current_sequence = SequenceData(
                name=self._current_sequence.name, beats=new_beats
            )
            self.sequence_modified.emit(self._current_sequence)

    def _on_sequence_modified(self, sequence):
        """Handle sequence modification from beat frame"""
        self._current_sequence = sequence
        self._update_display()
        self.sequence_modified.emit(sequence)

    def _on_layout_changed(self, rows: int, columns: int):
        """Handle layout change from beat frame"""
        # Could update UI or emit signals based on layout changes
        pass
