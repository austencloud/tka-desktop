from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
from typing import Optional, Callable


class AnimatedCard(QFrame):
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        action_callback: Callable,
        parent: Optional[QFrame] = None,
    ):
        super().__init__(parent)
        self.action_callback = action_callback
        self.is_running = False
        self.setup_ui(title, description, icon)
        self.setup_animations()

    def setup_ui(self, title: str, description: str, icon: str) -> None:
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(
            """
            AnimatedCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.1), stop:1 rgba(255, 255, 255, 0.05));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                margin: 5px;
            }
            AnimatedCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.2), stop:1 rgba(255, 255, 255, 0.1));
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
        """
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        header_layout = QHBoxLayout()

        self.icon_label = QLabel(icon)
        self.icon_label.setFont(QFont("Arial", 16))

        title_layout = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")

        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Arial", 9))
        self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        self.desc_label.setWordWrap(True)

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.desc_label)

        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 12px;")

        header_layout.addWidget(self.icon_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.status_indicator)

        layout.addLayout(header_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 3px;
                background: rgba(0, 0, 0, 0.3);
                height: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 3px;
            }
        """
        )
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.last_run_label = QLabel("")
        self.last_run_label.setFont(QFont("Arial", 8))
        self.last_run_label.setStyleSheet("color: rgba(255, 255, 255, 0.5);")
        layout.addWidget(self.last_run_label)

        self.setMinimumHeight(120)
        self.setMaximumHeight(120)

    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.action_callback()

    def enterEvent(self, event):
        current_rect = self.geometry()
        expanded_rect = QRect(
            current_rect.x() - 2,
            current_rect.y() - 2,
            current_rect.width() + 4,
            current_rect.height() + 4,
        )
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(expanded_rect)
        self.animation.start()

    def leaveEvent(self, event):
        current_rect = self.geometry()
        original_rect = QRect(
            current_rect.x() + 2,
            current_rect.y() + 2,
            current_rect.width() - 4,
            current_rect.height() - 4,
        )
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(original_rect)
        self.animation.start()

    def set_running_state(self, running: bool) -> None:
        self.is_running = running
        if running:
            self.status_indicator.setStyleSheet("color: #f39c12; font-size: 12px;")
            self.progress_bar.show()
            self.progress_bar.setRange(0, 0)
        else:
            self.status_indicator.setStyleSheet("color: #2ecc71; font-size: 12px;")
            self.progress_bar.hide()
            self.last_run_label.setText(
                f"Last run: {datetime.now().strftime('%H:%M:%S')}"
            )

    def set_error_state(self) -> None:
        self.status_indicator.setStyleSheet("color: #e74c3c; font-size: 12px;")
        self.progress_bar.hide()
