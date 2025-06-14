from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal
from domain.models.core_models import SequenceData
from core.interfaces.workbench_services import IDictionaryService


class WorkbenchIndicatorSection(QWidget):
    """Indicator section component for sequence workbench status display"""

    def __init__(
        self, dictionary_service: IDictionaryService, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._dictionary_service = dictionary_service
        self._current_sequence: Optional[SequenceData] = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup indicator labels layout"""
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        self._indicator_label = QLabel("Ready")
        self._indicator_label.setStyleSheet(
            """
            QLabel {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                padding: 5px 10px;
                color: white;
                font-weight: bold;
            }
        """
        )

        self._difficulty_label = QLabel("Difficulty: -")
        self._difficulty_label.setStyleSheet("color: white; font-size: 12px;")

        self._current_word_label = QLabel("Word: -")
        self._current_word_label.setStyleSheet("color: white; font-size: 12px;")

        self._circular_indicator = QLabel("")
        self._circular_indicator.setFixedSize(20, 20)

        layout.addWidget(self._indicator_label)
        layout.addStretch()
        layout.addWidget(self._difficulty_label)
        layout.addWidget(self._current_word_label)
        layout.addWidget(self._circular_indicator)

    def update_sequence(self, sequence: Optional[SequenceData]):
        """Update display based on current sequence"""
        self._current_sequence = sequence

        if not sequence:
            self._indicator_label.setText("No sequence loaded")
            self._difficulty_label.setText("Difficulty: -")
            self._current_word_label.setText("Word: -")
            self._set_circular_indicator_state("empty")
            return

        # Update status
        self._indicator_label.setText(f"Sequence: {sequence.length} beats")

        # Update difficulty
        try:
            difficulty = self._dictionary_service.calculate_difficulty(sequence)
            self._difficulty_label.setText(f"Difficulty: {difficulty}")
        except Exception:
            self._difficulty_label.setText("Difficulty: -")

        # Update word
        try:
            word = self._dictionary_service.get_word_for_sequence(sequence)
            self._current_word_label.setText(f"Word: {word or '-'}")
        except Exception:
            self._current_word_label.setText("Word: -")

        self._set_circular_indicator_state("loaded")

    def _set_circular_indicator_state(self, state: str):
        """Set circular indicator visual state"""
        colors = {
            "empty": "gray",
            "loaded": "green",
            "modified": "orange",
            "error": "red",
        }

        color = colors.get(state, "gray")
        self._circular_indicator.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 10px;
                border: 2px solid white;
            }}
        """
        )

    def set_status(self, message: str, state: str = "loaded"):
        """Set custom status message"""
        self._indicator_label.setText(message)
        self._set_circular_indicator_state(state)
