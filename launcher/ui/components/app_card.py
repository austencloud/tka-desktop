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

    def __init__(self, app, compact=False, parent=None):
        super().__init__(parent)
        self.app = app
        self.compact = compact
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.NoFrame)

        # Modern elevated card styling with subtle shadows and gradients
        self.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                color: white;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.12));
                border-color: rgba(74, 144, 226, 0.4);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.4),
                    stop:1 rgba(74, 144, 226, 0.3));
                border: 1px solid rgba(74, 144, 226, 0.6);
                border-radius: 8px;
                color: white;
                font-weight: 600;
                padding: 8px 16px;
                min-height: 28px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.6),
                    stop:1 rgba(74, 144, 226, 0.4));
                border-color: rgba(74, 144, 226, 0.8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 144, 226, 0.7),
                    stop:1 rgba(74, 144, 226, 0.5));
            }
        """
        )

        if self.compact:
            # Enhanced compact mode with dynamic sizing
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            layout = QHBoxLayout(self)
            layout.setSpacing(12)  # Reduced spacing
            layout.setContentsMargins(12, 8, 12, 8)  # Reduced margins

            # Icon with modern styling
            icon_container = QFrame()
            icon_container.setFixedSize(36, 36)  # Smaller icon container
            icon_container.setStyleSheet(
                """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(74, 144, 226, 0.2),
                        stop:1 rgba(142, 68, 173, 0.2));
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                }
            """
            )

            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel(self.app.icon)
            icon_label.setFont(QFont("Segoe UI", 16))  # Smaller icon font
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none;")
            icon_layout.addWidget(icon_label)

            layout.addWidget(icon_container)

            # Text content with enhanced typography
            text_layout = QVBoxLayout()
            text_layout.setSpacing(6)
            text_layout.setContentsMargins(0, 0, 0, 0)

            title_label = QLabel(self.app.title)
            title_label.setFont(
                QFont("Segoe UI", 11, QFont.Weight.Bold)
            )  # Smaller title
            title_label.setStyleSheet(
                """
                color: white; 
                background: transparent; 
                border: none;
                font-weight: 700;
            """
            )
            text_layout.addWidget(title_label)

            desc_label = QLabel(self.app.description)
            desc_label.setFont(QFont("Segoe UI", 9))  # Smaller description
            desc_label.setStyleSheet(
                """
                color: rgba(255, 255, 255, 0.8); 
                background: transparent; 
                border: none;
                font-weight: 400;
            """
            )
            if len(self.app.description) > 40:  # Shorter description limit
                desc_label.setText(self.app.description[:37] + "...")
            text_layout.addWidget(desc_label)

            layout.addLayout(text_layout, 1)

            # Modern keyboard shortcut badge
            if self.app.keyboard_shortcut:
                shortcut_label = QLabel(self.app.keyboard_shortcut)
                shortcut_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))
                shortcut_label.setStyleSheet(
                    """
                    color: rgba(255, 255, 255, 0.9);
                    background: rgba(255, 255, 255, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-weight: 500;
                """
                )
                shortcut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                shortcut_label.setFixedHeight(32)
                layout.addWidget(shortcut_label)

            # Enhanced launch button
            launch_btn = QPushButton("Launch")
            launch_btn.setFixedSize(70, 28)  # Smaller button
            launch_btn.clicked.connect(lambda: self.launch_requested.emit(self.app))
            layout.addWidget(launch_btn)

        else:
            # FULL CARD MODE: dynamic sizing
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            layout = QVBoxLayout(self)
            layout.setSpacing(10)  # Increased spacing between sections
            layout.setContentsMargins(16, 16, 16, 16)  # Better margins

            # Header with icon and title
            header_layout = QHBoxLayout()
            header_layout.setSpacing(12)  # Proper spacing between icon and title
            header_layout.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel(self.app.icon)
            icon_label.setFont(QFont("Segoe UI", 24))  # Larger icon for grid view
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setFixedSize(40, 40)  # Fixed size to prevent layout issues
            icon_label.setStyleSheet("background: transparent; border: none;")

            title_label = QLabel(self.app.title)
            title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            title_label.setWordWrap(True)
            title_label.setStyleSheet(
                "color: white; background: transparent; border: none;"
            )
            # Set minimum height to accommodate 2 lines of text
            title_label.setMinimumHeight(32)
            title_label.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
            )

            header_layout.addWidget(icon_label)
            header_layout.addWidget(title_label, 1)  # Allow title to expand
            layout.addLayout(header_layout)

            # Description with proper height allocation
            desc_label = QLabel(self.app.description)
            desc_label.setFont(QFont("Segoe UI", 9))
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(
                "color: rgba(255, 255, 255, 0.7); background: transparent; border: none;"
            )
            desc_label.setMinimumHeight(40)  # Ensure adequate space for description
            desc_label.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
            )
            # Truncate very long descriptions
            if len(self.app.description) > 100:
                desc_label.setText(self.app.description[:97] + "...")
            layout.addWidget(desc_label)

            # Keyboard shortcut (if available) - positioned above launch button
            if self.app.keyboard_shortcut:
                shortcut_label = QLabel(self.app.keyboard_shortcut)
                shortcut_label.setFont(QFont("Consolas", 9))
                shortcut_label.setStyleSheet(
                    """
                    color: rgba(255, 255, 255, 0.8);
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                    padding: 4px 8px;
                """
                )
                shortcut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                shortcut_label.setFixedHeight(24)
                layout.addWidget(shortcut_label)

            # Add stretch to push launch button to bottom
            layout.addStretch()

            # Launch button at the bottom with proper margins
            launch_btn = QPushButton("Launch")
            launch_btn.setFixedHeight(36)  # Consistent button height
            launch_btn.clicked.connect(lambda: self.launch_requested.emit(self.app))
            layout.addWidget(launch_btn)
