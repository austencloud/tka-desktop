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
from src.presentation.components.sequence_workbench.modern_button_panel import (
    ModernSequenceWorkbenchButtonPanel,
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

        # UI components
        self._beat_frame: Optional[ModernBeatFrame] = None
        self._button_panel: Optional[ModernSequenceWorkbenchButtonPanel] = None
        self._graph_editor: Optional[ModernGraphEditor] = (
            None  # Add graph editor component
        )

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the UI layout matching V1's sequence workbench structure"""
        # Main layout for the workbench content
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Top section: Indicator and difficulty labels
        self._setup_indicator_section(main_layout)

        # Middle section: Beat frame + button panel (horizontal layout like V1)
        self._setup_beat_frame_with_button_panel(main_layout)

        # Bottom section: Graph editor placeholder (collapsible)
        self._setup_graph_section(main_layout)

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

    def _setup_beat_frame_with_button_panel(self, parent_layout: QVBoxLayout):
        """Setup beat frame + button panel layout matching V1's beat_frame_layout"""
        # Create horizontal layout for beat frame + button panel (like V1)
        beat_frame_layout = QHBoxLayout()
        beat_frame_layout.setSpacing(12)
        beat_frame_layout.setContentsMargins(0, 0, 0, 0)

        # Create beat frame layout service
        beat_frame_layout_service = BeatFrameLayoutService()

        # Create the actual ModernBeatFrame component (left side)
        self._beat_frame = ModernBeatFrame(
            layout_service=beat_frame_layout_service, parent=self
        )
        self._beat_frame.setMinimumHeight(400)

        # Connect beat frame signals to workbench
        self._beat_frame.beat_selected.connect(self._on_beat_selected)
        self._beat_frame.beat_modified.connect(self._on_beat_modified)
        self._beat_frame.sequence_modified.connect(self._on_sequence_modified)
        self._beat_frame.layout_changed.connect(self._on_layout_changed)

        # Create button panel (right side, between beat frame and option picker)
        self._button_panel = ModernSequenceWorkbenchButtonPanel(self)

        # Add to horizontal layout with proper proportions (like V1's 10:1 ratio)
        beat_frame_layout.addWidget(self._beat_frame, 10)  # Beat frame takes most space
        beat_frame_layout.addWidget(
            self._button_panel, 1
        )  # Button panel takes small space

        parent_layout.addLayout(beat_frame_layout)

    def _setup_graph_section(self, parent_layout: QVBoxLayout):
        """Setup graph editor section"""
        # Create the actual ModernGraphEditor component (replaces placeholder)
        from .sequence_workbench.graph_editor.modern_graph_editor import (
            ModernGraphEditor,
        )

        self._graph_editor = ModernGraphEditor(
            graph_service=self._graph_service, parent=self
        )

        # Connect graph editor signals to workbench
        self._graph_editor.beat_modified.connect(self._on_graph_beat_modified)
        self._graph_editor.arrow_selected.connect(self._on_graph_arrow_selected)
        self._graph_editor.visibility_changed.connect(self._on_graph_visibility_changed)

        # Position graph editor at bottom of workbench (like v1)
        # Note: ModernGraphEditor handles its own positioning and animations
        parent_layout.addWidget(self._graph_editor)

    def _connect_signals(self):
        """Connect button panel signals to service operations"""
        if not self._button_panel:
            return

        # Dictionary & Export operations
        self._button_panel.add_to_dictionary_requested.connect(
            self._handle_add_to_dictionary
        )
        self._button_panel.save_image_requested.connect(self._handle_save_image)
        self._button_panel.view_fullscreen_requested.connect(self._handle_fullscreen)

        # Transform operations
        self._button_panel.mirror_sequence_requested.connect(self._handle_reflection)
        self._button_panel.swap_colors_requested.connect(self._handle_color_swap)
        self._button_panel.rotate_sequence_requested.connect(self._handle_rotation)

        # Sequence management operations
        self._button_panel.copy_json_requested.connect(self._handle_copy_json)
        self._button_panel.delete_beat_requested.connect(self._handle_delete_beat)
        self._button_panel.clear_sequence_requested.connect(self._handle_clear)

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

    # Enhanced event handlers using modern button panel
    def _handle_add_to_dictionary(self):
        """Handle add to dictionary button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback(
                "add_to_dictionary", "No sequence to add to dictionary"
            )
            return

        try:
            result = self._dictionary_service.add_sequence_to_dictionary(
                self._current_sequence
            )
            if result:
                self._show_success_with_button_feedback(
                    "add_to_dictionary", "Added to dictionary!"
                )
            else:
                self._show_error_with_button_feedback(
                    "add_to_dictionary", "Sequence already in dictionary"
                )
        except Exception as e:
            self._show_error_with_button_feedback(
                "add_to_dictionary", f"Failed to add to dictionary: {e}"
            )

    def _handle_save_image(self):
        """Handle save image button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback("save_image", "No sequence to export")
            return

        try:
            success = self._workbench_service.export_sequence_image(
                self._current_sequence
            )
            if success:
                self._show_success_with_button_feedback("save_image", "Image saved!")
            else:
                self._show_error_with_button_feedback(
                    "save_image", "Image export failed"
                )
        except Exception as e:
            self._show_error_with_button_feedback("save_image", f"Export failed: {e}")

    def _handle_delete_beat(self):
        """Handle delete beat button click"""
        if not self._current_sequence or self._current_sequence.length == 0:
            self._show_error_with_button_feedback("delete_beat", "No beats to delete")
            return

        try:
            # Get selected beat index from beat frame
            selected_index = (
                self._beat_frame.get_selected_beat_index() if self._beat_frame else None
            )

            if selected_index is None:
                self._show_error_with_button_feedback("delete_beat", "No beat selected")
                return

            # Use deletion service to remove beat
            updated_sequence = self._deletion_service.delete_beat(
                self._current_sequence, selected_index
            )
            self._current_sequence = updated_sequence
            self._update_display()
            self.sequence_modified.emit(updated_sequence)
            self._show_success_with_button_feedback("delete_beat", "Beat deleted!")
        except Exception as e:
            self._show_error_with_button_feedback("delete_beat", f"Delete failed: {e}")

    def _handle_color_swap(self):
        """Handle color swap button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback(
                "swap_colors", "No sequence to swap colors"
            )
            return

        try:
            swapped_sequence = self._workbench_service.swap_colors(
                self._current_sequence
            )
            self._current_sequence = swapped_sequence
            self._update_display()
            self.sequence_modified.emit(swapped_sequence)
            self._show_success_with_button_feedback("swap_colors", "Colors swapped!")
        except Exception as e:
            self._show_error_with_button_feedback(
                "swap_colors", f"Color swap failed: {e}"
            )

    def _handle_reflection(self):
        """Handle reflection button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback(
                "mirror_sequence", "No sequence to reflect"
            )
            return

        try:
            reflected_sequence = self._workbench_service.reflect_sequence(
                self._current_sequence
            )
            self._current_sequence = reflected_sequence
            self._update_display()
            self.sequence_modified.emit(reflected_sequence)
            self._show_success_with_button_feedback(
                "mirror_sequence", "Sequence reflected!"
            )
        except Exception as e:
            self._show_error_with_button_feedback(
                "mirror_sequence", f"Reflection failed: {e}"
            )

    def _handle_rotation(self):
        """Handle rotation button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback(
                "rotate_sequence", "No sequence to rotate"
            )
            return

        try:
            rotated_sequence = self._workbench_service.rotate_sequence(
                self._current_sequence
            )
            self._current_sequence = rotated_sequence
            self._update_display()
            self.sequence_modified.emit(rotated_sequence)
            self._show_success_with_button_feedback(
                "rotate_sequence", "Sequence rotated!"
            )
        except Exception as e:
            self._show_error_with_button_feedback(
                "rotate_sequence", f"Rotation failed: {e}"
            )

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
            self._show_success_with_button_feedback(
                "clear_sequence", "Sequence cleared!"
            )

        except Exception as e:
            self._show_error_with_button_feedback(
                "clear_sequence", f"Clear failed: {e}"
            )

    def _handle_fullscreen(self):
        """Handle full screen view button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback(
                "view_fullscreen", "No sequence to view"
            )
            return

        try:
            self._fullscreen_service.show_full_screen_view(self._current_sequence)
            self._show_success_with_button_feedback(
                "view_fullscreen", "Opening full screen view..."
            )
        except Exception as e:
            self._show_error_with_button_feedback(
                "view_fullscreen", f"Full screen view failed: {e}"
            )

    def _handle_copy_json(self):
        """Handle copy JSON button click"""
        if not self._current_sequence:
            self._show_error_with_button_feedback("copy_json", "No sequence to copy")
            return

        try:
            json_data = self._workbench_service.export_sequence_json(
                self._current_sequence
            )

            # Copy to clipboard
            from PyQt6.QtWidgets import QApplication

            clipboard = QApplication.clipboard()
            clipboard.setText(json_data)

            self._show_success_with_button_feedback(
                "copy_json", "JSON copied to clipboard!"
            )
        except Exception as e:
            self._show_error_with_button_feedback(
                "copy_json", f"JSON export failed: {e}"
            )

    def _show_success_with_button_feedback(self, button_name: str, message: str):
        """Show success message with button tooltip feedback"""
        self.operation_completed.emit(message)
        if self._button_panel:
            self._button_panel.show_message_tooltip(button_name, message, 2000)

    def _show_error_with_button_feedback(self, button_name: str, message: str):
        """Show error message with button tooltip feedback"""
        self.error_occurred.emit(message)
        if self._button_panel:
            self._button_panel.show_message_tooltip(button_name, f"❌ {message}", 3000)

    def _update_display(self):
        """Update all display elements based on current sequence"""
        if not self._current_sequence:
            self._indicator_label.setText("No sequence loaded")
            self._difficulty_label.setText("Difficulty: -")
            self._current_word_label.setText("Word: -")

            # Disable relevant buttons when no sequence
            if self._button_panel:
                buttons_to_disable = [
                    "save_image",
                    "mirror_sequence",
                    "swap_colors",
                    "rotate_sequence",
                    "copy_json",
                    "clear_sequence",
                ]
                for button_name in buttons_to_disable:
                    self._button_panel.set_button_enabled(button_name, False)

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

        # Enable buttons when sequence is available
        if self._button_panel:
            buttons_to_enable = [
                "save_image",
                "mirror_sequence",
                "swap_colors",
                "rotate_sequence",
                "copy_json",
                "clear_sequence",
            ]
            for button_name in buttons_to_enable:
                self._button_panel.set_button_enabled(button_name, True)

        # Update beat frame with sequence data
        if self._beat_frame:
            self._beat_frame.set_sequence(self._current_sequence)

        # Update graph editor
        self._graph_service.update_graph_display(self._current_sequence)

    # Beat frame signal handlers
    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from beat frame"""
        # Enable/disable delete button based on selection
        if self._button_panel:
            self._button_panel.set_button_enabled("delete_beat", beat_index is not None)

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

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor"""
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

    def _on_graph_arrow_selected(self, arrow_data):
        """Handle arrow selection in graph editor"""
        # Implement arrow selection handling if needed
        pass

    def _on_graph_visibility_changed(self, visible: bool):
        """Handle graph visibility changes"""
        if visible:
            # Graph became visible, update its display
            self._graph_service.update_graph_display(self._current_sequence)
        else:
            # Graph is hidden, handle accordingly (e.g., pause updates)
            pass

    def resizeEvent(self, event):
        """Handle resize events for responsive design"""
        super().resizeEvent(event)

        # Update button panel sizes
        if self._button_panel:
            self._button_panel.update_button_sizes(self.height())
