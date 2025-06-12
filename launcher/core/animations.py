# Animation Manager - Smooth 60fps UI Animations
from PyQt6.QtCore import (
    QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QSequentialAnimationGroup, QTimer, pyqtSignal, QRect, QPoint
)
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtGui import QColor
from typing import Dict, Any, Optional, Callable
import time


class AnimationManager(QObject):
    """
    Central animation management system for smooth UI interactions
    
    Features:
    - 60fps smooth animations
    - Easing curves for natural motion
    - Animation queuing and sequencing
    - Performance monitoring
    - Reduced motion support
    - Launch feedback animations
    """
    
    animation_started = pyqtSignal(str)  # animation_name
    animation_finished = pyqtSignal(str)  # animation_name
    
    def __init__(self):
        super().__init__()
        self.active_animations: Dict[str, QPropertyAnimation] = {}
        self.animation_groups: Dict[str, QParallelAnimationGroup] = {}
        self.reduced_motion = False
        self.animation_duration_multiplier = 1.0
        
    def set_reduced_motion(self, enabled: bool):
        """Enable reduced motion for accessibility"""
        self.reduced_motion = enabled
        self.animation_duration_multiplier = 0.3 if enabled else 1.0
        
    def create_fade_animation(self, widget: QWidget, start_opacity: float = 0.0,
                            end_opacity: float = 1.0, duration: int = 300,
                            easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic) -> QPropertyAnimation:
        """Create a fade in/out animation"""
        if self.reduced_motion:
            duration = int(duration * self.animation_duration_multiplier)
            
        # Create opacity effect if not exists
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
            
        animation = QPropertyAnimation(widget.graphicsEffect(), b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(easing)
        
        return animation
        
    def create_slide_animation(self, widget: QWidget, start_pos: QPoint,
                             end_pos: QPoint, duration: int = 300,
                             easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic) -> QPropertyAnimation:
        """Create a slide animation"""
        if self.reduced_motion:
            duration = int(duration * self.animation_duration_multiplier)
            
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(easing)
        
        return animation
        
    def create_scale_animation(self, widget: QWidget, start_scale: float = 0.8,
                             end_scale: float = 1.0, duration: int = 200,
                             easing: QEasingCurve.Type = QEasingCurve.Type.OutBack) -> QPropertyAnimation:
        """Create a scale animation using geometry"""
        if self.reduced_motion:
            duration = int(duration * self.animation_duration_multiplier)
            
        # Calculate scaled geometries
        original_rect = widget.geometry()
        center = original_rect.center()
        
        start_width = int(original_rect.width() * start_scale)
        start_height = int(original_rect.height() * start_scale)
        start_rect = QRect(
            center.x() - start_width // 2,
            center.y() - start_height // 2,
            start_width,
            start_height
        )
        
        end_width = int(original_rect.width() * end_scale)
        end_height = int(original_rect.height() * end_scale)
        end_rect = QRect(
            center.x() - end_width // 2,
            center.y() - end_height // 2,
            end_width,
            end_height
        )
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(easing)
        
        return animation
        
    def animate_app_launch(self, widget: QWidget, callback: Optional[Callable] = None) -> str:
        """Animate application launch with visual feedback"""
        animation_name = f"launch_{id(widget)}"
        
        if self.reduced_motion:
            # Simple fade for reduced motion
            animation = self.create_fade_animation(widget, 1.0, 0.7, 150)
            fade_back = self.create_fade_animation(widget, 0.7, 1.0, 150)
            
            group = QSequentialAnimationGroup()
            group.addAnimation(animation)
            group.addAnimation(fade_back)
        else:
            # Full launch animation with scale and fade
            scale_down = self.create_scale_animation(widget, 1.0, 0.95, 100)
            fade_out = self.create_fade_animation(widget, 1.0, 0.8, 100)
            
            scale_up = self.create_scale_animation(widget, 0.95, 1.0, 150)
            fade_in = self.create_fade_animation(widget, 0.8, 1.0, 150)
            
            # Parallel animations for press effect
            press_group = QParallelAnimationGroup()
            press_group.addAnimation(scale_down)
            press_group.addAnimation(fade_out)
            
            # Parallel animations for release effect
            release_group = QParallelAnimationGroup()
            release_group.addAnimation(scale_up)
            release_group.addAnimation(fade_in)
            
            # Sequential group for complete animation
            group = QSequentialAnimationGroup()
            group.addAnimation(press_group)
            group.addAnimation(release_group)
            
        # Connect signals
        group.started.connect(lambda: self.animation_started.emit(animation_name))
        group.finished.connect(lambda: self.animation_finished.emit(animation_name))
        group.finished.connect(lambda: self.cleanup_animation(animation_name))
        
        if callback:
            group.finished.connect(callback)
            
        # Store and start animation
        self.animation_groups[animation_name] = group
        group.start()
        
        return animation_name
        
    def animate_command_palette_show(self, widget: QWidget) -> str:
        """Animate command palette appearance"""
        animation_name = f"palette_show_{id(widget)}"
        
        if self.reduced_motion:
            # Simple fade in
            animation = self.create_fade_animation(widget, 0.0, 1.0, 200)
        else:
            # Slide down and fade in
            start_pos = widget.pos()
            slide_start = QPoint(start_pos.x(), start_pos.y() - 50)
            
            slide_animation = self.create_slide_animation(widget, slide_start, start_pos, 300)
            fade_animation = self.create_fade_animation(widget, 0.0, 1.0, 300)
            
            group = QParallelAnimationGroup()
            group.addAnimation(slide_animation)
            group.addAnimation(fade_animation)
            animation = group
            
        # Connect signals
        animation.started.connect(lambda: self.animation_started.emit(animation_name))
        animation.finished.connect(lambda: self.animation_finished.emit(animation_name))
        animation.finished.connect(lambda: self.cleanup_animation(animation_name))
        
        # Store and start
        if isinstance(animation, QParallelAnimationGroup):
            self.animation_groups[animation_name] = animation
        else:
            self.active_animations[animation_name] = animation
            
        animation.start()
        return animation_name
        
    def animate_command_palette_hide(self, widget: QWidget) -> str:
        """Animate command palette disappearance"""
        animation_name = f"palette_hide_{id(widget)}"
        
        if self.reduced_motion:
            # Simple fade out
            animation = self.create_fade_animation(widget, 1.0, 0.0, 150)
        else:
            # Slide up and fade out
            start_pos = widget.pos()
            slide_end = QPoint(start_pos.x(), start_pos.y() - 30)
            
            slide_animation = self.create_slide_animation(widget, start_pos, slide_end, 200)
            fade_animation = self.create_fade_animation(widget, 1.0, 0.0, 200)
            
            group = QParallelAnimationGroup()
            group.addAnimation(slide_animation)
            group.addAnimation(fade_animation)
            animation = group
            
        # Connect signals
        animation.started.connect(lambda: self.animation_started.emit(animation_name))
        animation.finished.connect(lambda: self.animation_finished.emit(animation_name))
        animation.finished.connect(lambda: self.cleanup_animation(animation_name))
        
        # Store and start
        if isinstance(animation, QParallelAnimationGroup):
            self.animation_groups[animation_name] = animation
        else:
            self.active_animations[animation_name] = animation
            
        animation.start()
        return animation_name
        
    def animate_health_status_change(self, widget: QWidget, is_healthy: bool) -> str:
        """Animate health status indicator changes"""
        animation_name = f"health_{id(widget)}"
        
        if self.reduced_motion:
            # Simple color transition (would need custom property)
            animation = self.create_fade_animation(widget, 0.8, 1.0, 200)
        else:
            # Pulse effect for status change
            pulse_out = self.create_scale_animation(widget, 1.0, 1.1, 150)
            pulse_in = self.create_scale_animation(widget, 1.1, 1.0, 150)
            
            group = QSequentialAnimationGroup()
            group.addAnimation(pulse_out)
            group.addAnimation(pulse_in)
            animation = group
            
        # Connect signals
        animation.started.connect(lambda: self.animation_started.emit(animation_name))
        animation.finished.connect(lambda: self.animation_finished.emit(animation_name))
        animation.finished.connect(lambda: self.cleanup_animation(animation_name))
        
        # Store and start
        if isinstance(animation, QSequentialAnimationGroup):
            self.animation_groups[animation_name] = animation
        else:
            self.active_animations[animation_name] = animation
            
        animation.start()
        return animation_name
        
    def animate_hover_effect(self, widget: QWidget, hover_in: bool) -> str:
        """Animate hover effects"""
        animation_name = f"hover_{id(widget)}"
        
        # Cancel existing hover animation
        self.stop_animation(animation_name)
        
        if self.reduced_motion:
            duration = 100
        else:
            duration = 200
            
        if hover_in:
            animation = self.create_scale_animation(widget, 1.0, 1.02, duration)
        else:
            animation = self.create_scale_animation(widget, 1.02, 1.0, duration)
            
        # Connect signals
        animation.finished.connect(lambda: self.cleanup_animation(animation_name))
        
        # Store and start
        self.active_animations[animation_name] = animation
        animation.start()
        
        return animation_name
        
    def stop_animation(self, animation_name: str):
        """Stop a specific animation"""
        if animation_name in self.active_animations:
            self.active_animations[animation_name].stop()
            del self.active_animations[animation_name]
            
        if animation_name in self.animation_groups:
            self.animation_groups[animation_name].stop()
            del self.animation_groups[animation_name]
            
    def stop_all_animations(self):
        """Stop all running animations"""
        for animation in self.active_animations.values():
            animation.stop()
        for group in self.animation_groups.values():
            group.stop()
            
        self.active_animations.clear()
        self.animation_groups.clear()
        
    def cleanup_animation(self, animation_name: str):
        """Clean up finished animation"""
        if animation_name in self.active_animations:
            del self.active_animations[animation_name]
        if animation_name in self.animation_groups:
            del self.animation_groups[animation_name]
            
    def get_animation_stats(self) -> Dict[str, Any]:
        """Get animation performance statistics"""
        return {
            "active_animations": len(self.active_animations),
            "active_groups": len(self.animation_groups),
            "reduced_motion": self.reduced_motion,
            "duration_multiplier": self.animation_duration_multiplier
        }
