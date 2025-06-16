from typing import TYPE_CHECKING
from PyQt6.QtCore import QPropertyAnimation, QRect, QPoint, QEasingCurve, QObject

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.graph_editor.legacy_graph_editor import (
        LegacyGraphEditor,
    )


class GraphEditorAnimator(QObject):
    def __init__(self, graph_editor: "LegacyGraphEditor"):
        super().__init__(graph_editor)
        self.sequence_workbench = graph_editor.sequence_workbench
        self.graph_editor = graph_editor
        self.toggle_tab = graph_editor.toggle_tab
        self.graph_editor_placeholder = self.graph_editor.placeholder
        self.button_panel_bottom_placeholder = (
            self.sequence_workbench.button_panel.bottom_placeholder
        )
        self.current_animations = []

    def toggle(self):
        if self.graph_editor.is_toggled:
            self.graph_editor.is_toggled = False
            self.animate_graph_editor(show=False)
        else:
            self.sequence_workbench.layout_manager.main_layout.addWidget(
                self.graph_editor_placeholder
            )
            self.graph_editor.show()
            self.graph_editor.is_toggled = True
            self.animate_graph_editor(show=True)

    def clear_previous_animations(self):
        """Stop all currently running animations and clear effects."""
        for animation in self.current_animations:
            animation.stop()
        self.current_animations.clear()

        # Clear any lingering graphics effects (if used)
        self.graph_editor.setGraphicsEffect(None)
        self.graph_editor_placeholder.setGraphicsEffect(None)
        self.toggle_tab.setGraphicsEffect(None)

    def animate_graph_editor(self, show):
        self.clear_previous_animations()

        parent_height = self.sequence_workbench.height()
        parent_width = self.sequence_workbench.width()
        desired_height = self.sequence_workbench.graph_editor.get_graph_editor_height()

        if show:
            editor_start_rect = QRect(0, parent_height, parent_width, 0)
            editor_end_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            toggle_start_pos = QPoint(0, parent_height - self.toggle_tab.height())
            toggle_end_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            placeholder_start_height = 0
            placeholder_end_height = desired_height
        else:
            editor_start_rect = QRect(
                0, parent_height - desired_height, parent_width, desired_height
            )
            editor_end_rect = QRect(0, parent_height, parent_width, 0)
            toggle_start_pos = QPoint(
                0, parent_height - desired_height - self.toggle_tab.height()
            )
            toggle_end_pos = QPoint(0, parent_height - self.toggle_tab.height())
            placeholder_start_height = desired_height
            placeholder_end_height = 0

        # Animate GraphEditor geometry
        graph_editor_animation = QPropertyAnimation(self.graph_editor, b"geometry")
        graph_editor_animation.setStartValue(editor_start_rect)
        graph_editor_animation.setEndValue(editor_end_rect)
        graph_editor_animation.setDuration(300)
        graph_editor_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(graph_editor_animation)

        # Animate graph editor placeholder height
        placeholder_animation = QPropertyAnimation(
            self.graph_editor_placeholder, b"minimumHeight"
        )
        placeholder_animation.setStartValue(placeholder_start_height)
        placeholder_animation.setEndValue(placeholder_end_height)
        placeholder_animation.setDuration(300)
        placeholder_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(placeholder_animation)

        # Animate toggle tab position
        toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        toggle_tab_animation.setStartValue(toggle_start_pos)
        toggle_tab_animation.setEndValue(toggle_end_pos)
        toggle_tab_animation.setDuration(300)
        toggle_tab_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.current_animations.append(toggle_tab_animation)

        # Handle cleanup on collapse
        if not show:
            graph_editor_animation.finished.connect(
                lambda: self.sequence_workbench.layout_manager.main_layout.removeWidget(
                    self.graph_editor_placeholder
                )
            )
            graph_editor_animation.finished.connect(self.graph_editor.hide)

        # Start all animations
        for animation in self.current_animations:
            animation.start()
