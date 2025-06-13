from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal


class AppCard(QFrame):
    launch_requested = pyqtSignal(object)

    def __init__(self, app, compact=False, expanded=False, parent=None):
        super().__init__(parent)
        self.app = app
        self.compact = compact
        self.expanded = expanded
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Enhanced card styling with better hover effects
        self.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.15),
                    stop:1 rgba(74, 144, 226, 0.08));
                border: 2px solid rgba(74, 144, 226, 0.5);
            }
        """
        )

        # Main layout with better spacing
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 16, 20, 16)

        # Left side: Icon with background
        icon_size = 56 if self.expanded else 48
        icon_container = QFrame()
        icon_container.setFixedSize(icon_size, icon_size)
        icon_container.setStyleSheet(
            f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(74, 144, 226, 0.2),
                    stop:1 rgba(142, 68, 173, 0.2));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: {icon_size // 4}px;
            }}
        """
        )

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel(self.app.icon)
        icon_font_size = 28 if self.expanded else 24
        icon_label.setFont(QFont("Segoe UI", icon_font_size))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_layout.addWidget(icon_label)

        layout.addWidget(icon_container)

        # Middle: Text content with proper spacing
        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)

        # Title - no truncation, allow wrapping
        title_label = QLabel(self.app.title)
        title_font_size = 16 if self.expanded else 14
        title_label.setFont(QFont("Segoe UI", title_font_size, QFont.Weight.Bold))
        title_label.setWordWrap(True)
        title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                background: transparent;
                border: none;
                line-height: 1.2;
            }
        """
        )
        text_layout.addWidget(title_label)

        # Description - show full text with wrapping
        desc_label = QLabel(self.app.description)
        desc_font_size = 12 if self.expanded else 11
        desc_label.setFont(QFont("Segoe UI", desc_font_size))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
                line-height: 1.4;
            }
        """
        )
        text_layout.addWidget(desc_label)

        # Tags/Keywords (if expanded)
        if self.expanded and hasattr(self.app, "tags") and self.app.tags:
            tags_layout = QHBoxLayout()
            tags_layout.setSpacing(6)
            for tag in self.app.tags[:3]:  # Show first 3 tags
                tag_label = QLabel(tag)
                tag_label.setFont(QFont("Segoe UI", 9))
                tag_label.setStyleSheet(
                    """
                    QLabel {
                        color: rgba(255, 255, 255, 0.9);
                        background: rgba(74, 144, 226, 0.2);
                        border: 1px solid rgba(74, 144, 226, 0.4);
                        border-radius: 4px;
                        padding: 2px 8px;
                    }
                """
                )
                tags_layout.addWidget(tag_label)
            tags_layout.addStretch()
            text_layout.addLayout(tags_layout)

        text_layout.addStretch()
        layout.addLayout(text_layout, 1)

        # Right side: Action area
        action_layout = QVBoxLayout()
        action_layout.setSpacing(8)

        # Keyboard shortcut (if available)
        if self.app.keyboard_shortcut:
            shortcut_label = QLabel(self.app.keyboard_shortcut)
            shortcut_label.setFont(QFont("Consolas", 10, QFont.Weight.Medium))
            shortcut_label.setStyleSheet(
                """
                QLabel {
                    color: rgba(255, 255, 255, 0.9);
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                    padding: 4px 12px;
                }
            """
            )
            shortcut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            action_layout.addWidget(shortcut_label)

        action_layout.addStretch()

        # Launch button - larger and more prominent
        launch_btn = QPushButton("Launch")
        btn_height = 44 if self.expanded else 40
        launch_btn.setFixedHeight(btn_height)
        launch_btn.setMinimumWidth(100)
        launch_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        launch_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.6),
                    stop:1 rgba(74, 144, 226, 0.4));
                border: 1px solid rgba(74, 144, 226, 0.8);
                border-radius: {btn_height // 4}px;
                color: white;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.8),
                    stop:1 rgba(74, 144, 226, 0.6));
                border: 2px solid rgba(74, 144, 226, 1.0);
            }}
            QPushButton:pressed {{
                background: rgba(74, 144, 226, 0.9);
            }}
        """
        )
        launch_btn.clicked.connect(lambda: self.launch_requested.emit(self.app))
        action_layout.addWidget(launch_btn)

        layout.addLayout(action_layout)

    def mousePressEvent(self, event):
        """Make entire card clickable"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.launch_requested.emit(self.app)
        super().mousePressEvent(event)
