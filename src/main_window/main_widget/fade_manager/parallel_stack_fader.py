from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QStackedWidget

if TYPE_CHECKING:
    from main_window.main_widget.fade_manager.fade_manager import FadeManager


class ParallelStackFader:
    """Handles parallel fading of two stacked widgets with optional resizing."""

    left_old_widget: Optional[QWidget] = None
    left_new_widget: Optional[QWidget] = None
    right_old_widget: Optional[QWidget] = None
    right_new_widget: Optional[QWidget] = None

    def __init__(self, manager: "FadeManager"):
        self.manager = manager

    def fade_both_stacks(
        self,
        right_stack: QStackedWidget,
        right_new_index: int,
        left_stack: QStackedWidget,
        left_new_index: int,
        width_ratio: tuple[float, float],
        duration: int = 300,
        callback: Optional[callable] = None,
    ):
        """Fades out both stacks in parallel, resizes the layout, and fades in the new widgets."""
        self.right_old_widget = right_stack.currentWidget()
        self.left_old_widget = left_stack.currentWidget()
        self.right_new_widget = right_stack.widget(right_new_index)
        self.left_new_widget = left_stack.widget(left_new_index)

        if not (
            self.right_old_widget
            and self.left_old_widget
            and self.right_new_widget
            and self.left_new_widget
        ):
            return

        def switch_and_resize():
            # Use layout stretch factors instead of fixed widths to prevent layout regression
            main_widget = self.manager.main_widget
            if hasattr(main_widget, "content_layout"):
                # Calculate stretch factors from width ratios
                left_stretch = int(width_ratio[0] * 10)  # Scale up for better precision
                right_stretch = int(width_ratio[1] * 10)

                # Apply stretch factors to the layout
                main_widget.content_layout.setStretch(0, left_stretch)
                main_widget.content_layout.setStretch(1, right_stretch)

                # Clear any fixed widths that might interfere
                left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
                right_stack.setMaximumWidth(16777215)
                left_stack.setMinimumWidth(0)
                right_stack.setMinimumWidth(0)
            else:
                # Fallback to old fixed width method if content_layout not available
                total_width = main_widget.width()
                left_width = int(total_width * width_ratio[0])
                left_stack.setFixedWidth(left_width)
                right_stack.setFixedWidth(total_width - left_width)

            right_stack.setCurrentIndex(right_new_index)
            left_stack.setCurrentIndex(left_new_index)

        def finalize():
            if callback:
                callback()

        fade_enabled = self.manager.fades_enabled()

        if not fade_enabled:
            switch_and_resize()
            finalize()
            return

        def fade_in_new_widgets():
            self.manager.widget_fader.fade_widgets(
                [self.right_new_widget, self.left_new_widget],
                fade_in=True,
                duration=duration,
                callback=finalize,
            )

        self.manager.widget_fader.fade_widgets(
            [self.right_old_widget, self.left_old_widget],
            fade_in=False,
            duration=duration,
            callback=lambda: (switch_and_resize(), fade_in_new_widgets()),
        )
