"""
Pictograph Context Configurator for V2.

This service configures V2 pictograph components to match V1's context-specific
behavior for different usage scenarios (option view, start pos picker, etc.).
"""

from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize

from application.services.context_aware_scaling_service import ScalingContext
from domain.models.core_models import LetterType


class PictographContextConfigurator:
    """
    Configures V2 pictograph components to match V1's context-specific behavior.
    
    This service encapsulates the knowledge of how different V1 views configure
    their pictographs and applies the same configuration to V2 components.
    """
    
    @staticmethod
    def configure_for_option_view(
        pictograph_component,
        main_window_width: int,
        option_picker_width: int,
        spacing: int = 8,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for option view context.
        
        Matches V1's OptionView behavior:
        - size = max(mw_width//16, option_picker.width//8)
        - border_width = max(1, int(size * 0.015))
        - size -= 2 * border_width + spacing
        """
        context_params = {
            'main_window_width': main_window_width,
            'option_picker_width': option_picker_width,
            'spacing': spacing
        }
        
        pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for option view
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_start_pos_picker(
        pictograph_component,
        size_provider_width: int,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for start position picker context.
        
        Matches V1's StartPosPicker behavior:
        - size = size_provider.width//10
        - border_width = max(1, int(size * 0.015))
        - size -= 2 * border_width
        """
        context_params = {
            'size_provider_width': size_provider_width
        }
        
        pictograph_component.set_scaling_context(ScalingContext.START_POS_PICKER, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for start pos picker
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_advanced_start_pos(
        pictograph_component,
        size_provider_width: int,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for advanced start position context.
        
        Matches V1's AdvancedStartPos behavior:
        - size = size_provider.width//12
        - border_width = max(1, int(size * 0.015))
        - size -= 2 * border_width
        """
        context_params = {
            'size_provider_width': size_provider_width
        }
        
        pictograph_component.set_scaling_context(ScalingContext.ADVANCED_START_POS, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for advanced start pos
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_codex_view(
        pictograph_component,
        main_widget_width: int,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for codex view context.
        
        Matches V1's CodexView behavior:
        - size = codex.main_widget.width//16
        """
        context_params = {
            'main_widget_width': main_widget_width
        }
        
        pictograph_component.set_scaling_context(ScalingContext.CODEX_VIEW, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for codex view
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_beat_view(
        pictograph_component,
        enhancement_factor: float = 1.1,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for beat view context.
        
        Matches V1's BeatView behavior:
        - view_scale = min(view_size/beat_scene_size)
        - Enhanced scaling for better visibility
        """
        context_params = {
            'enhancement_factor': enhancement_factor
        }
        
        pictograph_component.set_scaling_context(ScalingContext.BEAT_VIEW, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for beat view
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_graph_editor(
        pictograph_component,
        ge_enhancement_factor: float = 1.05,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for graph editor context.
        
        Matches V1's GE_View behavior:
        - scale_factor = min(view_size/scene_size)
        - Graph editor specific enhancements
        """
        context_params = {
            'ge_enhancement_factor': ge_enhancement_factor
        }
        
        pictograph_component.set_scaling_context(ScalingContext.GRAPH_EDITOR_VIEW, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Enable borders for graph editor
        pictograph_component.enable_borders()
    
    @staticmethod
    def configure_for_visibility_view(
        pictograph_component,
        available_height: int,
        size_factor: float = 0.55,
        letter_type: Optional[LetterType] = None
    ) -> None:
        """
        Configure pictograph component for visibility view context.
        
        Matches V1's VisibilityPictographView behavior:
        - size = int(available_height * 0.55)
        """
        target_size = int(available_height * size_factor)
        
        # Use default context but with specific size
        context_params = {
            'target_size': target_size
        }
        
        pictograph_component.set_scaling_context(ScalingContext.DEFAULT, **context_params)
        
        if letter_type:
            pictograph_component.update_border_colors_for_letter_type(letter_type)
        
        # Set fixed size for visibility view
        pictograph_component.setFixedSize(target_size, target_size)
        
        # Enable borders with black border style
        pictograph_component.enable_borders()
        pictograph_component.border_manager.set_custom_border_colors("#000000", "#000000")
    
    @staticmethod
    def configure_hover_effects(pictograph_component, enable_gold_hover: bool = True) -> None:
        """
        Configure hover effects for pictograph component.
        
        Args:
            pictograph_component: The pictograph component to configure
            enable_gold_hover: Whether to enable gold border on hover
        """
        if enable_gold_hover:
            # Connect hover events to gold border
            def on_enter():
                pictograph_component.set_gold_border()
            
            def on_leave():
                pictograph_component.reset_border_colors()
            
            # Store the functions as attributes so they don't get garbage collected
            pictograph_component._hover_enter_func = on_enter
            pictograph_component._hover_leave_func = on_leave
            
            # Connect to events (this would need to be implemented in the component)
            if hasattr(pictograph_component, 'enterEvent'):
                original_enter = pictograph_component.enterEvent
                original_leave = pictograph_component.leaveEvent
                
                def new_enter_event(event):
                    original_enter(event)
                    on_enter()
                
                def new_leave_event(event):
                    original_leave(event)
                    on_leave()
                
                pictograph_component.enterEvent = new_enter_event
                pictograph_component.leaveEvent = new_leave_event
    
    @staticmethod
    def get_context_specific_size_calculation(
        context: ScalingContext,
        container_size: QSize,
        **context_params
    ) -> int:
        """
        Get the target size for a specific context before scaling calculations.
        
        This matches V1's size calculation logic for each context.
        """
        if context == ScalingContext.OPTION_VIEW:
            main_window_width = context_params.get('main_window_width', container_size.width() * 4)
            option_picker_width = context_params.get('option_picker_width', container_size.width() * 2)
            return max(main_window_width // 16, option_picker_width // 8)
        
        elif context == ScalingContext.START_POS_PICKER:
            size_provider_width = context_params.get('size_provider_width', container_size.width())
            return size_provider_width // 10
        
        elif context == ScalingContext.ADVANCED_START_POS:
            size_provider_width = context_params.get('size_provider_width', container_size.width())
            return size_provider_width // 12
        
        elif context == ScalingContext.CODEX_VIEW:
            main_widget_width = context_params.get('main_widget_width', container_size.width() * 2)
            return main_widget_width // 16
        
        elif context == ScalingContext.VISIBILITY_VIEW:
            available_height = context_params.get('available_height', container_size.height())
            size_factor = context_params.get('size_factor', 0.55)
            return int(available_height * size_factor)
        
        else:
            # Default: use container size
            return min(container_size.width(), container_size.height())
