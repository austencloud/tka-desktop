from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal


class OptionPickerFilter(QWidget):
    filter_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = self._create_widget()

    def _create_widget(self) -> QWidget:
        filter_widget = QWidget()
        layout = QHBoxLayout(filter_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        filter_label = QLabel("Filter:")
        filter_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        filter_label.setStyleSheet("QLabel { color: #2d3748; }")
        layout.addWidget(filter_label)

        self.reversal_combo = QComboBox()
        self.reversal_combo.addItems(["All", "Same", "Opposite"])
        self.reversal_combo.setCurrentText("All")
        self.reversal_combo.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
        """
        )
        self.reversal_combo.currentTextChanged.connect(self.filter_changed.emit)
        layout.addWidget(self.reversal_combo)

        layout.addStretch()

        filter_widget.setStyleSheet(
            """
            QWidget {
                background-color: rgba(248, 249, 250, 150);
                border: 1px solid rgba(222, 226, 230, 150);
                border-radius: 4px;
                margin: 2px;
            }
        """
        )

        return filter_widget
