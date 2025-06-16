from typing import TYPE_CHECKING
from .handlers.beta_prop_positioner import BetaPropPositioner
from .handlers.default_prop_positioner import DefaultPropPositioner

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class PropPlacementManager:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultPropPositioner(self)
        self.beta_positioner = BetaPropPositioner(self)

    def update_prop_positions(self) -> None:
        if self.pictograph.state.letter:
            # Always set props to default locations first
            for prop in self.pictograph.elements.props.values():
                self.default_positioner.set_prop_to_default_loc(prop)

            # Only apply beta positioning if all motions are visible and it's a beta letter
            if self.pictograph.managers.check.ends_with_beta():
                # Check if all motions are visible
                all_motions_visible = self._are_all_motions_visible()

                # Only apply beta positioning if all motions are visible
                if all_motions_visible:
                    self.beta_positioner.reposition_beta_props()

    def _are_all_motions_visible(self) -> bool:
        """
        Check if all motions are currently visible based on visibility settings.
        Returns True if all motions are visible, False otherwise.
        """
        from src.legacy_settings_manager.global_settings.app_context import AppContext

        try:
            settings = AppContext().settings_manager().visibility
            return settings.are_all_motions_visible()
        except (AttributeError, ImportError):
            return True
