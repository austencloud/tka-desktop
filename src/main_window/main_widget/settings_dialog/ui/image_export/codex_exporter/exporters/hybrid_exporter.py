"""
Hybrid pictograph exporter for the codex pictograph exporter.
"""
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from ..pictograph_data_manager import PictographDataManager
    from ..pictograph_factory import PictographFactory
    from ..pictograph_renderer import PictographRenderer
    from ..turn_configuration import TurnConfiguration


class HybridExporter:
    """Hybrid pictograph exporter for the codex pictograph exporter."""

    def __init__(
        self, 
        data_manager: "PictographDataManager",
        factory: "PictographFactory",
        renderer: "PictographRenderer",
        turn_configuration: "TurnConfiguration"
    ):
        """Initialize the exporter.
        
        Args:
            data_manager: The pictograph data manager
            factory: The pictograph factory
            renderer: The pictograph renderer
            turn_configuration: The turn configuration
        """
        self.data_manager = data_manager
        self.factory = factory
        self.renderer = renderer
        self.turn_configuration = turn_configuration
        
    def export_pictograph(
        self, letter: str, directory: str, red_turns: int, blue_turns: int
    ) -> int:
        """Export a hybrid pictograph with specified turns.
        
        Args:
            letter: The letter to export
            directory: The directory to save to
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            
        Returns:
            The number of exported pictographs (0, 1, or 2)
        """
        # Get the start and end positions for this letter
        start_pos, end_pos = self.turn_configuration.get_letter_positions(letter)
        
        # Get pro version of the pictograph (we'll always use the pro version as base)
        pro_version, _ = self.data_manager.get_hybrid_pictograph_versions(
            letter, start_pos, end_pos
        )
        
        # If we couldn't find pro version, create minimal data
        if not pro_version:
            minimal_data = self.data_manager.create_minimal_data_for_letter(letter)
            
            # Export a single version
            pictograph = self.factory.create_pictograph_from_data(minimal_data, "diamond")
            from ..turn_applier import TurnApplier
            TurnApplier.apply_turns_to_pictograph(
                pictograph, red_turns=red_turns, blue_turns=blue_turns
            )
            
            filename = self.turn_configuration.get_non_hybrid_filename(letter)
            filepath = os.path.join(directory, filename)
            
            image = self.renderer.create_pictograph_image(pictograph)
            image.save(filepath, "PNG", 100)
            print(
                f"Saved hybrid pictograph {letter} with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
            )
            
            return 1
            
        # For hybrid pictographs, we only need both versions if the turns are different
        if red_turns == blue_turns:
            # If turns are the same, just use one version
            pictograph = self.factory.create_pictograph_from_data(pro_version, "diamond")
            from ..turn_applier import TurnApplier
            TurnApplier.apply_turns_to_pictograph(
                pictograph, red_turns=red_turns, blue_turns=blue_turns
            )
            
            # Simple filename without motion type since we only need one version
            filename = self.turn_configuration.get_non_hybrid_filename(letter)
            filepath = os.path.join(directory, filename)
            
            image = self.renderer.create_pictograph_image(pictograph)
            image.save(filepath, "PNG", 100)
            print(
                f"Saved hybrid pictograph {letter} with turns (red:{red_turns}, blue:{blue_turns}) to {filepath}"
            )
            
            return 1
        else:
            # If turns are different, we need two versions:
            # 1. Pro hand has turns, anti hand has 0 turns
            # 2. Pro hand has 0 turns, anti hand has turns
            exported_count = 0
            
            # Get red motion type from the pro version
            # We only need to know if red is pro or anti, as blue will be the opposite
            red_attrs = pro_version.get("red_attributes", {})
            red_motion_type = red_attrs.get("motion_type", "pro")
            
            # Version 1: Pro hand has turns, anti hand has 0 turns
            pictograph1 = self.factory.create_pictograph_from_data(pro_version, "diamond")
            
            # For version 1, we want:
            # - Pro hand: Use the specified turns (red_turns or blue_turns)
            # - Anti hand: Always 0 turns
            
            # Determine which hand gets which turns based on motion type
            if red_motion_type == "pro":
                # Red is pro, blue is anti
                red_turns_to_apply = red_turns  # Pro hand gets specified turns
                blue_turns_to_apply = 0         # Anti hand gets 0 turns
            else:
                # Blue is pro, red is anti
                red_turns_to_apply = 0          # Anti hand gets 0 turns
                blue_turns_to_apply = blue_turns  # Pro hand gets specified turns
                
            from ..turn_applier import TurnApplier
            TurnApplier.apply_turns_to_pictograph(
                pictograph1, 
                red_turns=red_turns_to_apply,
                blue_turns=blue_turns_to_apply,
            )
            
            filename1 = self.turn_configuration.get_hybrid_filename(
                letter, red_turns, blue_turns, "pro_turns"
            )
            filepath1 = os.path.join(directory, filename1)
            
            image1 = self.renderer.create_pictograph_image(pictograph1)
            image1.save(filepath1, "PNG", 100)
            print(
                f"Saved hybrid pictograph {letter} (Pro hand has turns) to {filepath1}"
            )
            
            exported_count += 1
            
            # Version 2: Pro hand has 0 turns, anti hand has turns
            pictograph2 = self.factory.create_pictograph_from_data(pro_version, "diamond")
            
            # For version 2, we want:
            # - Pro hand: Always 0 turns
            # - Anti hand: Use the specified turns (red_turns or blue_turns)
            
            # Determine which hand gets which turns based on motion type
            if red_motion_type == "pro":
                # Red is pro, blue is anti
                red_turns_to_apply = 0          # Pro hand gets 0 turns
                blue_turns_to_apply = blue_turns  # Anti hand gets specified turns
            else:
                # Blue is pro, red is anti
                red_turns_to_apply = red_turns  # Anti hand gets specified turns
                blue_turns_to_apply = 0         # Pro hand gets 0 turns
                
            TurnApplier.apply_turns_to_pictograph(
                pictograph2, 
                red_turns=red_turns_to_apply,
                blue_turns=blue_turns_to_apply,
            )
            
            filename2 = self.turn_configuration.get_hybrid_filename(
                letter, red_turns, blue_turns, "anti_turns"
            )
            filepath2 = os.path.join(directory, filename2)
            
            image2 = self.renderer.create_pictograph_image(pictograph2)
            image2.save(filepath2, "PNG", 100)
            print(
                f"Saved hybrid pictograph {letter} (Anti hand has turns) to {filepath2}"
            )
            
            exported_count += 1
            
            return exported_count
