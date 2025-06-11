# music_player_widget.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtCore import QTimer, Qt
import pygame


class MusicPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._initialize_player()

    def _setup_ui(self):
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_label = QLabel("0:00")

        layout = QHBoxLayout(self)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.position_slider)
        layout.addWidget(self.time_label)
        self.setLayout(layout)

        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)

    def _initialize_player(self):
        pygame.mixer.init()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)

    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)
        self.position_slider.setValue(0)
        self.position_slider.setMaximum(int(pygame.mixer.Sound(file_path).get_length()))

    def play(self):
        pygame.mixer.music.play()
        self.timer.start(1000)

    def pause(self):
        pygame.mixer.music.pause()
        self.timer.stop()

    def stop(self):
        pygame.mixer.music.stop()
        self.timer.stop()
        self.position_slider.setValue(0)

    def update_position(self):
        position = pygame.mixer.music.get_pos() // 1000
        self.position_slider.setValue(position)
        minutes = position // 60
        seconds = position % 60
        self.time_label.setText(f"{minutes}:{seconds:02}")
