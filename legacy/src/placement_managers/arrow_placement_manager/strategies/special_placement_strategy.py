from typing import TYPE_CHECKING, Any
from PyQt6.QtCore import QPointF
from src.legacy_settings_manager.global_settings.app_context import AppContext
from placement_managers.arrow_placement_manager.arrow_placement_context import (
    ArrowPlacementContext,
)
from placement_managers.attr_key_generator import (
    AttrKeyGenerator,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.hotkey_graph_adjuster.data_updater.ori_key_generator import (
        OriKeyGenerator,
    )


class SpecialPlacementStrategy:
    def __init__(self, ori_key_generator: "OriKeyGenerator") -> None:
        self.special_placement_loader = AppContext.special_placement_loader()
        self.ori_key_generator = ori_key_generator
        self.special_placements: dict[str, dict[str, dict[str, Any]]] = (
            self.special_placement_loader.load_or_return_special_placements()
        )
        self.attr_key_generator = AttrKeyGenerator()

    def get_special_placements(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns the loaded special placements for reference."""
        return self.special_placements

    def compute_adjustment(self, context: ArrowPlacementContext) -> QPointF:
        """Computes special placement adjustment based on grid mode, motion type, letter, and orientation key."""
        ori_key = self.ori_key_generator.generate_ori_key_from_context(context)

        letter_data = (
            self.special_placements.get(context.grid_mode, {})
            .get(ori_key, {})
            .get(context.letter.value, None)
        )

        if letter_data:
            first_key = next(
                iter(letter_data), None
            )  # Get the first key (e.g., '(0,0)')
            if first_key and isinstance(letter_data[first_key], dict):
                # Determine the correct color to use
                color_key = (
                    context.arrow_color.lower()
                )  # Assuming color is stored in lowercase

                if color_key in letter_data[first_key]:  # Ensure the color exists
                    return QPointF(
                        *letter_data[first_key][color_key]
                    )  # ✅ Unpack list into QPointF

        return QPointF(0, 0)  # Default adjustment if no data found
