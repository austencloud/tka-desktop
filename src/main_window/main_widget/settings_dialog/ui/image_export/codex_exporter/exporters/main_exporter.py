"""
Main exporter class for the codex pictograph exporter.
"""
from typing import TYPE_CHECKING, List, Tuple
import os

from .base_exporter import BaseExporter
from .non_hybrid_exporter import NonHybridExporter
from .hybrid_exporter import HybridExporter

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import ImageExportTab
    from ..pictograph_data_manager import PictographDataManager
    from ..pictograph_factory import PictographFactory
    from ..pictograph_renderer import PictographRenderer
    from ..turn_configuration import TurnConfiguration


class MainExporter(BaseExporter):
    """Main exporter class for the codex pictograph exporter."""

    def __init__(
        self, 
        image_export_tab: "ImageExportTab",
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration"
    ):
        """Initialize the exporter.
        
        Args:
            image_export_tab: The parent image export tab
            data_manager: The pictograph data manager
            factory: The pictograph factory
            renderer: The pictograph renderer
            turn_configuration: The turn configuration
        """
        super().__init__(image_export_tab)
        self.data_manager = data_manager
        self.factory = factory
        self.renderer = renderer
        self.turn_configuration = turn_configuration
        
        # Create the specialized exporters
        self.non_hybrid_exporter = NonHybridExporter(
            data_manager, factory, renderer, turn_configuration
        )
        self.hybrid_exporter = HybridExporter(
            data_manager, factory, renderer, turn_configuration
        )
        
    def export_pictographs(
        self, selected_types: List[str], red_turns: int, blue_turns: int, generate_all: bool = False
    ) -> int:
        """Export pictographs with the specified turns.
        
        Args:
            selected_types: The letters to export
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            generate_all: Whether to generate all turn combinations
            
        Returns:
            The number of exported pictographs
        """
        # Ask the user for a directory to save the images
        main_directory = self._get_export_directory()
        if not main_directory:
            return 0  # User canceled
            
        # Determine turn combinations
        if generate_all:
            turn_combinations = self.turn_configuration.get_turn_combinations()
        else:
            turn_combinations = [(red_turns, blue_turns)]
            
        # Calculate total count for progress bar
        total_count = self._calculate_total_count(selected_types, turn_combinations)
        
        # Create and configure progress dialog
        progress = self._create_progress_dialog(total_count)
        
        exported_count = 0
        
        try:
            # Process each selected pictograph type
            for letter in selected_types:
                if progress.wasCanceled():
                    break
                    
                # Process each turn combination for this letter
                for red_turns, blue_turns in turn_combinations:
                    if progress.wasCanceled():
                        break
                        
                    # Create a subdirectory for this turn combination
                    turn_dir_name = self.turn_configuration.get_turn_directory_name(red_turns, blue_turns)
                    turn_directory = os.path.join(main_directory, turn_dir_name)
                    os.makedirs(turn_directory, exist_ok=True)
                    
                    # Handle different pictograph types
                    if self.turn_configuration.is_hybrid_letter(letter):
                        # Hybrid types: one or two versions depending on turns
                        exported = self.hybrid_exporter.export_pictograph(
                            letter, turn_directory, red_turns, blue_turns
                        )
                        exported_count += exported
                    else:
                        # Non-hybrid types: apply the specified turns
                        exported = self.non_hybrid_exporter.export_pictograph(
                            letter, turn_directory, red_turns, blue_turns
                        )
                        exported_count += exported
                        
                    # Update progress
                    progress.setValue(exported_count)
        finally:
            progress.close()
            
        # Show completion message
        self._show_completion_message(exported_count, main_directory, turn_combinations)
        
        return exported_count
        
    def _calculate_total_count(
        self, selected_types: List[str], turn_combinations: List[Tuple[int, int]]
    ) -> int:
        """Calculate the total number of pictographs to export.
        
        Args:
            selected_types: The letters to export
            turn_combinations: The turn combinations to export
            
        Returns:
            The total number of pictographs
        """
        total_count = len(selected_types) * len(turn_combinations)
        
        # Add extra for hybrid letters which need two versions for some combinations
        # Count how many hybrid letters are selected
        hybrid_letter_count = sum(
            1 for letter in selected_types if self.turn_configuration.is_hybrid_letter(letter)
        )
        
        # Count how many combinations need two versions
        # Only combinations where red_turns != blue_turns need two versions
        extra_versions_per_letter = sum(
            1 for red, blue in turn_combinations if red != blue
        )
        
        # Add the extra versions to the total count
        total_count += hybrid_letter_count * extra_versions_per_letter
        
        return total_count
