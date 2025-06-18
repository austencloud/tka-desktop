from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QGraphicsDropShadowEffect,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QFont,
    QPainter,
    QLinearGradient,
    QColor,
    QPen,
    QBrush,
    QGuiApplication,
)
from presentation.components.backgrounds.background_widget import MainBackgroundWidget


class ModernProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(12)
        self.setTextVisible(False)
        self.setStyleSheet(
            """
            QProgressBar {
                border: none;
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 200, 255, 0.8),
                    stop:0.5 rgba(100, 150, 255, 0.9),
                    stop:1 rgba(200, 100, 255, 0.8));
            }
        """
        )


class GlassmorphContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QWidget {
                background: rgba(20, 20, 30, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
        """
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(50, 50, 80, 240))
        gradient.setColorAt(0.5, QColor(30, 30, 50, 250))
        gradient.setColorAt(1, QColor(20, 20, 40, 255))

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(255, 255, 255, 60), 1))
        painter.drawRoundedRect(rect, 20, 20)


class SplashScreen(QWidget):
    progress_updated = pyqtSignal(int, str)

    def __init__(self, target_screen=None, parent=None):
        super().__init__(parent)
        self.target_screen = target_screen or QGuiApplication.primaryScreen()
        self.current_progress = 0
        self.current_message = "Initializing..."
        self.is_closing = False

        self._setup_window_properties()
        self._setup_background()
        self._setup_ui()
        self._setup_animations()
        self._center_on_target_screen()

        # Start with zero opacity for fade-in animation
        self.setWindowOpacity(0.0)

    def _setup_window_properties(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(700, 500)

    def _setup_background(self):
        self.background_widget = MainBackgroundWidget(self, "Starfield")
        self.background_widget.setGeometry(self.rect())

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(0)

        self.container = GlassmorphContainer()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)

        title_section = QWidget()
        title_section.setMinimumHeight(140)
        title_layout = QVBoxLayout(title_section)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.setSpacing(8)

        self.title_label = QLabel("The Kinetic Constructor")
        title_font = QFont("Monotype Corsiva", 36, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(70)
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """
        )

        self.version_label = QLabel("Version 2.0")
        version_font = QFont("Arial", 16, QFont.Weight.Normal)
        self.version_label.setFont(version_font)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setFixedHeight(40)
        self.version_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }
        """
        )

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.version_label)

        container_layout.addWidget(title_section)
        container_layout.addSpacerItem(
            QSpacerItem(
                20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        progress_section = QWidget()
        progress_section.setMinimumHeight(110)
        progress_layout = QVBoxLayout(progress_section)
        progress_layout.setSpacing(18)

        self.status_label = QLabel(self.current_message)
        status_font = QFont("Arial", 13)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(30)
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """
        )

        self.progress_bar = ModernProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.percentage_label = QLabel("0%")
        percentage_font = QFont("Arial", 11)
        self.percentage_label.setFont(percentage_font)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.percentage_label.setFixedHeight(25)
        self.percentage_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: transparent;
                border: none;
            }
        """
        )

        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.percentage_label)

        container_layout.addWidget(progress_section)

        self.attribution_label = QLabel("Created by Austen Cloud")
        attribution_font = QFont("Arial", 10)
        self.attribution_label.setFont(attribution_font)
        self.attribution_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.attribution_label.setFixedHeight(25)
        self.attribution_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                background: transparent;
                border: none;
            }
        """
        )
        container_layout.addWidget(self.attribution_label)

        layout.addWidget(self.container)

    def _setup_animations(self):
        # Fade-in animation
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(800)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Logo pulsing animation
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self._pulse_logo)
        self.pulse_timer.start(2500)
        self.pulse_scale = 1.0
        self.pulse_direction = 1

    def _pulse_logo(self):
        if self.is_closing:
            return

        self.pulse_scale += 0.08 * self.pulse_direction
        if self.pulse_scale >= 1.15:
            self.pulse_direction = -1
        elif self.pulse_scale <= 1.0:
            self.pulse_direction = 1

        font_size = int(36 * self.pulse_scale)
        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                background: transparent;
                border: none;
                font-family: "Monotype Corsiva";
                font-size: {font_size}px;
                font-weight: bold;
            }}
        """
        )

    def _center_on_target_screen(self):
        if self.target_screen:
            screen_geometry = self.target_screen.geometry()
            x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

    def show_animated(self):
        self.show()
        self.fade_in_animation.start()
        return self.fade_in_animation  # Return animation for callback connection

    def update_progress(self, value: int, message: str = ""):
        if self.is_closing:
            return

        self.current_progress = value
        if message:
            self.current_message = message

        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")
        self.status_label.setText(self.current_message)

        # PERFORMANCE FIX: Only process events in release mode to avoid debug delays
        # In debug mode, QApplication.processEvents() has significant overhead
        import sys

        if not sys.flags.debug and not __debug__:
            from PyQt6.QtWidgets import QApplication

            QApplication.processEvents()

    def hide_animated(self, callback=None):
        if self.is_closing:
            return

        self.is_closing = True
        if hasattr(self, "pulse_timer"):
            self.pulse_timer.stop()

        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(600)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)

        def on_finished():
            self.close()
            if callback:
                callback()

        fade_out.finished.connect(on_finished)
        fade_out.start()

        # Store reference to prevent garbage collection
        self._fade_out_animation = fade_out

    def close(self):
        self.is_closing = True
        if hasattr(self, "pulse_timer"):
            self.pulse_timer.stop()
        super().close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background_widget"):
            self.background_widget.setGeometry(self.rect())

    def paintEvent(self, event):
        super().paintEvent(event)
