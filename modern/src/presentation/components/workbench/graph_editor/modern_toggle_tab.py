from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import (
    pyqtSignal,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QEvent,
    Qt,
)
from PyQt6.QtGui import QFont


class ModernToggleTab(QWidget):
    toggle_requested = pyqtSignal()

    def __init__(self, parent, positioning_style="center"):
        super().__init__(parent)
        self._graph_editor = parent
        self._animating = False
        self._positioning_style = positioning_style  # "center" or "left"

        self._setup_ui()
        self._setup_animation()
        # Defer initial positioning until parent is fully initialized
        QTimer.singleShot(0, self._position_tab)

    def _setup_ui(self):
        """Setup the toggle button UI with proper styling and sizing"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create toggle button with proper text and styling
        self._toggle_btn = QPushButton("Graph Editor ▲")
        self._toggle_btn.clicked.connect(self.toggle_requested.emit)
        self._toggle_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set initial visual state (disconnected)
        self._update_visual_state()

        layout.addWidget(self._toggle_btn)

        # Set proper size - larger than the original small version
        self.setMinimumSize(140, 35)
        self.setMaximumSize(200, 50)

    def _setup_animation(self):
        """Setup smooth position animation system"""
        from PyQt6.QtCore import QPoint

        # Position animation for smooth movement
        self._position_animation = QPropertyAnimation(self, b"pos")
        self._position_animation.setDuration(300)  # Smooth 300ms animation
        self._position_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Connect animation events
        self._position_animation.finished.connect(self._on_animation_finished)

    def _on_animation_finished(self):
        """Handle animation completion"""
        self._animating = False

    def _update_visual_state(self):
        """Update visual styling based on connection state"""
        is_connected = (
            self._graph_editor.is_visible()
            if hasattr(self._graph_editor, "is_visible")
            else False
        )

        if is_connected:
            # Connected state: solid blue styling to avoid transparency artifacts
            self._toggle_btn.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(100, 150, 255, 0.90),
                        stop: 0.5 rgba(80, 130, 235, 0.85),
                        stop: 1 rgba(60, 110, 215, 0.80)
                    );
                    border: 2px solid rgba(100, 150, 255, 0.95);
                    border-bottom: 3px solid rgba(100, 150, 255, 1.0);
                    border-radius: 12px 12px 0px 0px;
                    color: rgba(255, 255, 255, 1.0);
                    padding: 10px 20px;
                    font-weight: bold;
                    min-width: 140px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(120, 170, 255, 0.95),
                        stop: 0.5 rgba(100, 150, 255, 0.90),
                        stop: 1 rgba(80, 130, 235, 0.85)
                    );
                    border: 2px solid rgba(120, 170, 255, 1.0);
                    border-bottom: 3px solid rgba(120, 170, 255, 1.0);
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(80, 130, 235, 0.95),
                        stop: 0.5 rgba(60, 110, 215, 0.90),
                        stop: 1 rgba(40, 90, 195, 0.85)
                    );
                    border: 2px solid rgba(80, 130, 235, 1.0);
                    border-bottom: 2px solid rgba(80, 130, 235, 1.0);
                }
            """
            )
        else:
            # Disconnected state: more opaque to avoid artifacts over card boundaries
            self._toggle_btn.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(255, 255, 255, 0.80),
                        stop: 0.5 rgba(235, 235, 235, 0.75),
                        stop: 1 rgba(215, 215, 215, 0.70)
                    );
                    border: 2px solid rgba(255, 255, 255, 0.85);
                    border-bottom: none;
                    border-radius: 12px 12px 0px 0px;
                    color: rgba(50, 50, 50, 1.0);
                    padding: 10px 20px;
                    font-weight: bold;
                    min-width: 140px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(255, 255, 255, 0.90),
                        stop: 0.5 rgba(245, 245, 245, 0.85),
                        stop: 1 rgba(225, 225, 225, 0.80)
                    );
                    border: 2px solid rgba(255, 255, 255, 0.95);
                    color: rgba(30, 30, 30, 1.0);
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 rgba(235, 235, 235, 0.85),
                        stop: 0.5 rgba(215, 215, 215, 0.80),
                        stop: 1 rgba(195, 195, 195, 0.75)
                    );                    border: 2px solid rgba(235, 235, 235, 0.90);
                    color: rgba(20, 20, 20, 1.0);
                }
            """
            )

    def _position_tab(self):
        """Position the toggle tab initially at the bottom center of workbench"""
        # Find the right parent - should be the workbench
        workbench_parent = self._graph_editor.parent()
        if workbench_parent:
            # Go up to find the actual workbench (graph_section -> workbench)
            while workbench_parent and not hasattr(
                workbench_parent, "_beat_frame_section"
            ):
                workbench_parent = workbench_parent.parent()

        if not workbench_parent:
            # Defer positioning until parent is available
            QTimer.singleShot(100, self._position_tab)
            return

        self.setParent(workbench_parent)

        # Ensure parent has valid dimensions before positioning
        if workbench_parent.width() <= 0 or workbench_parent.height() <= 0:
            # Defer positioning until parent has valid size
            QTimer.singleShot(100, self._position_tab)
            return

        # Initial position based on positioning style
        if self._positioning_style == "left":
            # Legacy-style left positioning
            x = 20  # 20px margin from left edge
        else:
            # Default center positioning
            x = (workbench_parent.width() - self.width()) // 2

        y = workbench_parent.height() - self.height() - 10  # 10px margin from bottom

        self.move(x, y)
        self.raise_()

        # Ensure button is visible
        self.show()
        print(
            f"🎯 Toggle tab positioned at ({x}, {y}) in parent {type(workbench_parent).__name__}"
        )

    def update_position(self, animate=True):
        """Update position to hug the top of graph editor frame (Legacy-exact behavior)"""
        if not self._graph_editor._parent_workbench:
            return

        # Prevent multiple animations
        if self._animating and animate:
            return

        parent = self._graph_editor._parent_workbench

        # Calculate horizontal position based on positioning style
        if self._positioning_style == "left":
            # Legacy-style left positioning
            x = 20  # 20px margin from left edge
        else:
            # Default center positioning
            x = (parent.width() - self.width()) // 2

        if self._graph_editor.is_visible():
            # Graph editor is open: position at top of graph editor frame
            graph_editor_height = self._graph_editor.get_preferred_height()
            y = parent.height() - graph_editor_height - self.height()
            self._toggle_btn.setText("Graph Editor ▼")
        else:
            # Graph editor is closed: position at bottom of workbench
            y = parent.height() - self.height() - 10  # 10px margin from bottom
            self._toggle_btn.setText("Graph Editor ▲")

        # Update visual state to show connection
        self._update_visual_state()

        if animate and not self._animating:
            # Animate to new position
            self._animating = True
            from PyQt6.QtCore import QPoint

            self._position_animation.setStartValue(self.pos())
            self._position_animation.setEndValue(QPoint(x, y))
            self._position_animation.start()
        else:
            # Move immediately without animation
            self.move(x, y)

        self.raise_()

    def resizeEvent(self, event):
        """Handle resize events like Legacy toggle tab"""
        super().resizeEvent(event)
        # Update position when the tab itself is resized (no animation during resize)
        self.update_position(animate=False)

    def eventFilter(self, obj, event):
        """Filter events to catch parent window resize"""
        if (
            event.type() == QEvent.Type.Resize
            and obj == self._graph_editor._parent_workbench
        ):
            # Parent window resized, update our position
            QTimer.singleShot(0, lambda: self.update_position(animate=False))
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        """Handle show events to install event filter"""
        super().showEvent(event)
        if self._graph_editor._parent_workbench:
            # Install event filter to catch parent resize events
            self._graph_editor._parent_workbench.installEventFilter(self)

    def hideEvent(self, event):
        """Handle hide events to remove event filter"""
        super().hideEvent(event)
        if self._graph_editor._parent_workbench:
            # Remove event filter when hiding
            self._graph_editor._parent_workbench.removeEventFilter(self)
