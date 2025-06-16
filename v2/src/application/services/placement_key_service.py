"""
Placement Key Service

This service generates placement keys to determine which adjustment
category to use (layer1_alpha, layer2_alpha, etc.).
"""

from domain.models.core_models import MotionData, MotionType, Orientation


class PlacementKeyService:
    """Service that generates placement keys for arrow positioning."""

    def __init__(self):
        pass

    def generate_placement_key(
        self,
        motion_data: MotionData,
        grid_mode: str = "diamond",
        prop_state: str = "alpha",
    ) -> str:
        """
        Generate placement key using proven logic.

        Args:
            motion_data: The motion data
            grid_mode: Grid mode (diamond or box)
            prop_state: Prop state (alpha, beta, gamma)

        Returns:
            Placement key string (e.g., "pro_to_layer1_alpha")
        """
        motion_type = motion_data.motion_type.value

        # Calculate end orientation to determine layer
        end_orientation = self._calculate_end_orientation(motion_data)

        # Determine layer based on end orientation
        if end_orientation in [Orientation.IN, Orientation.OUT]:
            layer = "layer1"
        elif end_orientation in [Orientation.CLOCK, Orientation.COUNTER]:
            layer = "layer2"
        else:
            layer = "layer1"  # Default fallback

        # Generate key: motion_to_layer_propstate
        key = f"{motion_type}_to_{layer}_{prop_state}"

        return key

    def _calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        if turns in {0, 1, 2, 3}:
            if motion_type in [MotionType.PRO, MotionType.STATIC]:
                return (
                    start_orientation
                    if int(turns) % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self._switch_orientation(start_orientation)
                    if int(turns) % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def get_simplified_key(self, motion_data: MotionData) -> str:
        """Get simplified key for basic cases."""
        return self.generate_placement_key(motion_data, "diamond", "alpha")

    def debug_key_generation(self, motion_data: MotionData) -> str:
        """Debug helper to show key generation process."""
        print(f"🔍 Key Generation Debug for {motion_data.motion_type.value} motion:")
        print(
            f"  Start: {motion_data.start_loc.value} → End: {motion_data.end_loc.value}"
        )
        print(f"  Prop Rotation: {motion_data.prop_rot_dir.value}")
        print(f"  Turns: {motion_data.turns}")

        end_orientation = self._calculate_end_orientation(motion_data)
        print(f"  End Orientation: {end_orientation.value}")

        key = self.generate_placement_key(motion_data)
        print(f"  Generated Key: {key}")

        return key
