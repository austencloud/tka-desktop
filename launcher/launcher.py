from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QPushButton,
    QMessageBox,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from typing import List
import sys
import subprocess

from .accessibility import AccessibilityManager
from .apps import AppDefinitions, AppDefinition


class LauncherWindow(QMainWindow):
    """A slim, horizontally-oriented launcher bar."""

    HEIGHT = 45  # px, adjusted to better match typical taskbar height
    WIDTH = 420  # px, increased to accommodate Parallel button

    def __init__(self) -> None:
        super().__init__()
        self.a11y = AccessibilityManager.instance()
        self._setup_window()
        self._setup_layout()
        self._setup_shortcuts()
        self.position_overlay_taskbar_secondary_left_fifth()

    def _setup_window(self) -> None:
        self.setWindowTitle("TKA Launcher")
        # Frameless & always on top keeps it minimal and unobtrusive
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        # High‑contrast palette for accessibility; relies on system colors
        self.setStyleSheet("background: palette(window);")

    def _setup_layout(self) -> None:
        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(
            4, 2, 4, 2
        )  # Reduced margins (left, top, right, bottom)
        layout.setSpacing(8)  # Increased spacing between widgets (e.g., from 4 to 8)
        self.setCentralWidget(central)

        # Add TKA Label
        tka_label = QLabel("TKA:")  # Added colon
        tka_label_font = tka_label.font()
        tka_label_font.setFamily("Monotype Corsiva")  # Set font family
        tka_label_font.setPointSize(18)  # Slightly larger for style
        # tka_label_font.setBold(True) # Monotype Corsiva is often better not bold
        tka_label.setFont(tka_label_font)
        tka_label.setStyleSheet(
            "color: palette(text); padding-right: 10px; margin-left: 5px;"
        )  # Style and spacing
        layout.addWidget(tka_label)

        for app in AppDefinitions.all():
            btn = QPushButton(f"{app.icon}  {app.title}")
            btn.clicked.connect(lambda _, a=app: self._launch(a))
            btn.setToolTip(app.description)
            self.a11y.configure(btn, f"Launch {app.title}", app.description)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(
                self.HEIGHT
                - 8  # e.g., 48 - 8 = 40px button height, allowing 4px top/bottom margin within launcher
            )
            btn.setStyleSheet(
                """
                QPushButton {
                    border: 2px solid transparent; /* Reserve space for focus border */
                    padding: 0 10px; 
                    font-size: 14px; 
                    font-weight: 600;
                    color: palette(text);
                    background: palette(base);
                    border-radius: 4px; 
                }
                QPushButton:hover { background: palette(light); }
                QPushButton:focus {
                    border: 2px solid #0078d4; /* Use border for focus to follow radius */
                    /* outline: none; */ /* Optionally remove outline if border is used */
                }
                """
            )
            layout.addWidget(btn)

    def _setup_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("F5"), self, self._refresh)

    def position_overlay_taskbar_secondary_left_fifth(self) -> None:
        """Moves the launcher to overlay the taskbar area on the secondary screen,
        positioned 1/5 from the left edge of the full screen geometry."""
        screens = QApplication.screens()
        if len(screens) > 1:
            secondary_screen = screens[1]  # Assuming the second screen is the target
        else:
            secondary_screen = (
                QApplication.primaryScreen()
            )  # Fallback to primary if no secondary

        screen_geometry = (
            secondary_screen.geometry()
        )  # Use .geometry() to include taskbar area

        # Position 1/5 from the left edge of the full screen area
        x_position = screen_geometry.x() + (screen_geometry.width() // 5)

        # Position at the bottom of the full screen area
        y_position = screen_geometry.y() + screen_geometry.height() - self.HEIGHT

        self.setGeometry(x_position, y_position, self.WIDTH, self.HEIGHT)

    def _launch(self, app: AppDefinition) -> None:
        try:
            if app.script_path:
                subprocess.Popen([sys.executable, app.script_path])
            elif app.command:
                subprocess.Popen(app.command, shell=True)
        except Exception as e:
            QMessageBox.warning(
                self, "Launch Error", f"Failed to launch {app.title}:\n{e}"
            )

    def _refresh(self) -> None:
        self.close()
        new = LauncherWindow()
        new.show()


class LauncherApplication(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        self.setStyle("Fusion")
        self.setApplicationName("Kinetic Constructor Launcher")
        self.setOrganizationName("Kinetic Constructor")

    def run(self) -> int:
        window = LauncherWindow()
        window.show()
        return self.exec()
