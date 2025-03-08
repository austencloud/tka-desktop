import sys
import winsound
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if sys.platform == "win32":
    SND_APPLICATION = 128
    SND_FILENAME = 131072
    SND_ALIAS = 65536
    SND_LOOP = 8
    SND_MEMORY = 4
    SND_PURGE = 64
    SND_ASYNC = 1
    SND_NODEFAULT = 2
    SND_NOSTOP = 16
    SND_NOWAIT = 8192

    MB_ICONASTERISK = 64
    MB_ICONEXCLAMATION = 48
    MB_ICONHAND = 16
    MB_ICONQUESTION = 32
    MB_OK = 0

class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows System Sounds")
        self.setGeometry(100, 100, 350, 600)
        self.setStyleSheet(
            """
            QWidget { background-color: #2E2E2E; }
            QLabel { color: white; font-size: 18px; }
            QPushButton {
                background-color: #555; color: white; font-size: 16px;
                border-radius: 8px; padding: 10px;
            }
            QPushButton:hover { background-color: #777; }
            QPushButton:pressed { background-color: #999; }
            """
        )

        layout = QVBoxLayout()
        title_label = QLabel("Click a button to play a sound")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)

        self.sounds = {
            "Asterisk": MB_ICONASTERISK,
            "Exclamation": MB_ICONEXCLAMATION,
            "Hand (Error)": MB_ICONHAND,
            "Question": MB_ICONQUESTION,
            "Default Beep": 0,
        }

        for name, sound in self.sounds.items():
            button = QPushButton(name)
            button.clicked.connect(lambda _, s=sound: winsound.MessageBeep(s))
            layout.addWidget(button)

        self.sound_flags = {
            "Async": SND_ASYNC,
            "Memory": SND_MEMORY,
            "Purge": SND_PURGE,
            "Nodefault": SND_NODEFAULT,
            "Nostop": SND_NOSTOP,
            "Nowait": SND_NOWAIT,
            "Alias": SND_ALIAS,
            "Filename": SND_FILENAME,
            "Application": SND_APPLICATION,
            "Loop": SND_LOOP,
        }

        for name, flag in self.sound_flags.items():
            button = QPushButton(f"Flag: {name}")
            button.clicked.connect(lambda _, f=flag: winsound.PlaySound(b"SystemExclamation", f))
            layout.addWidget(button)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SoundPlayer()
    window.show()
    sys.exit(app.exec())
