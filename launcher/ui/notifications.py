from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QPalette


class ToastNotification(QWidget):
    def __init__(self, message, notification_type="info", duration=3000, parent=None):
        super().__init__(parent)
        self.duration = duration
        self.setup_ui(message, notification_type)
        self.setup_animation()

    def setup_ui(self, message, notification_type):
        self.setFixedSize(300, 80)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        styles = {
            "success": "background: rgba(46, 204, 113, 0.9); color: white;",
            "error": "background: rgba(231, 76, 60, 0.9); color: white;",
            "warning": "background: rgba(241, 196, 15, 0.9); color: black;",
            "info": "background: rgba(52, 152, 219, 0.9); color: white;",
        }

        style = styles.get(notification_type, styles["info"])
        self.setStyleSheet(
            f"""
            QWidget {{
                {style}
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }}
        """
        )

        layout.addWidget(self.label)

    def setup_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out.finished.connect(self.close)

    def show_toast(self):
        self.show()
        self.fade_in.start()

        QTimer.singleShot(self.duration, self.start_fade_out)

    def start_fade_out(self):
        self.fade_out.start()


class NotificationManager:
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.notifications = []

    def show_notification(self, message, notification_type="info", duration=3000):
        if self.parent:
            parent_rect = self.parent.geometry()
            x = parent_rect.right() - 320
            y = parent_rect.top() + 20 + (len(self.notifications) * 90)
        else:
            x, y = 100, 100

        toast = ToastNotification(message, notification_type, duration, self.parent)
        toast.move(x, y)
        toast.show_toast()

        self.notifications.append(toast)

        QTimer.singleShot(duration + 500, lambda: self.cleanup_notification(toast))

    def cleanup_notification(self, toast):
        if toast in self.notifications:
            self.notifications.remove(toast)
        toast.deleteLater()
