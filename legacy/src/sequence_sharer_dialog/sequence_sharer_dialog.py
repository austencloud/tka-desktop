import os
import time  # Import time for formatting timestamps
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QHBoxLayout,
    QSpacerItem,
    QCheckBox,
    QTextEdit,  # Use QTextEdit for multi-line input
)
from .email_sender import EmailSender
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceSharerDialog(QDialog):
    def __init__(self, main_widget: "MainWidget", image_path: str, word: str):
        super().__init__(main_widget)
        self.image_path = image_path
        self.word = word
        self.main_widget = main_widget

        # Get settings_manager from dependency injection system
        try:
            self.settings_manager = main_widget.app_context.settings_manager
        except AttributeError:
            # Fallback when settings not available
            self.settings_manager = None

        self.checkbox_email_map = {}

        self.setWindowTitle("Share Sequence Image")

        width = int(self.main_widget.width() / 5)
        height = int(self.main_widget.height() / 2)
        self.setFixedSize(width, height)

        self.init_ui()
        self.apply_styling()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.create_recipient_section(layout)
        self.create_subject_section(layout)
        self.create_body_section(layout)
        self.create_add_recipient_section(layout)
        self.create_send_cancel_buttons(layout)

        self.setLayout(layout)

    def create_recipient_section(self, layout: QVBoxLayout):
        """Create the section for selecting recipients."""
        self.recipient_label = QLabel("Select Recipients:")
        layout.addWidget(self.recipient_label)

        self.recipient_checkboxes: list[QCheckBox] = []
        for (
            recipient
        ) in self.settings_manager.sequence_share_settings.get_saved_recipients():
            checkbox = QCheckBox(f"{recipient['name']} ({recipient['email']})")
            layout.addWidget(checkbox)
            self.recipient_checkboxes.append(checkbox)
            self.checkbox_email_map[checkbox] = recipient["email"]

    def create_subject_section(self, layout: QVBoxLayout):
        """Create the section for email subject input."""
        self.subject_label = QLabel("Email Subject:")
        self.subject_input = QLineEdit(f"{self.word}", self)  # Default subject
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)

    def create_body_section(self, layout: QVBoxLayout):
        """Create the section for email body input."""
        creation_time = time.strftime(
            "%m-%d-%Y at %I:%M %p", time.localtime(os.path.getctime(self.image_path))
        )  # Format image creation time

        # Sanitize the month and day to remove leading zeros
        month, day, year = creation_time.split("-")
        month = month.lstrip("0")
        day = day.lstrip("0")
        sanitized_creation_time = f"{month}-{day}-{year}"

        self.body_label = QLabel("Email Body:")
        self.body_input = QTextEdit(self)  # Use QTextEdit for multi-line input
        self.body_input.setText(
            f"Attached is the image for {self.word}.\nIt was created on {sanitized_creation_time}."
        )  # Set default multi-line text
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_input)

    def create_add_recipient_section(self, layout: QVBoxLayout):
        """Create the section for adding a new recipient."""
        self.new_recipient_label = QLabel("Add New Recipient:")
        layout.addWidget(self.new_recipient_label)

        self.new_name_input = QLineEdit(self)
        self.new_name_input.setPlaceholderText("Recipient Name")
        self.new_email_input = QLineEdit(self)
        self.new_email_input.setPlaceholderText("Recipient Email")

        add_recipient_layout = QHBoxLayout()
        add_recipient_layout.addWidget(self.new_name_input)
        add_recipient_layout.addWidget(self.new_email_input)

        self.add_recipient_button = QPushButton("Add Recipient", self)
        self.add_recipient_button.clicked.connect(self.add_recipient)
        self.add_recipient_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addLayout(add_recipient_layout)
        layout.addWidget(self.add_recipient_button)

    def create_send_cancel_buttons(self, layout: QVBoxLayout):
        """Create the section for send and cancel buttons."""
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_email)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # make the button cursors pointed hands
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding))
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.send_button)

        layout.addLayout(button_layout)

    def apply_styling(self):
        """Apply styling to the dialog."""
        self.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                margin-bottom: 10px;
            }
            QLineEdit, QTextEdit, QCheckBox {
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 12px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton#Cancel {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )

    def add_recipient(self):
        """Add a new recipient to the settings."""
        name = self.new_name_input.text().strip()
        email = self.new_email_input.text().strip()

        if name and email:
            self.settings_manager.sequence_share_settings.add_recipient(name, email)
            QMessageBox.information(
                self, "Success", f"Added recipient: {name} ({email})"
            )
            self.new_name_input.clear()
            self.new_email_input.clear()
            self.refresh_dialog()  # Refresh the dialog

    def refresh_dialog(self):
        """Refresh the dialog to update the recipient list."""
        self.close()
        self.__init__(self.main_widget, self.image_path, self.word)
        self.exec()

    def send_email(self):
        """Send the email to selected recipients."""
        selected_emails = [
            self.checkbox_email_map[checkbox]
            for checkbox in self.recipient_checkboxes
            if checkbox.isChecked()
        ]

        if not selected_emails:
            QMessageBox.warning(
                self, "No Recipients", "Please select at least one recipient."
            )
            return

        from_email = os.getenv("GMAIL_USER")
        password = os.getenv("GMAIL_PASS")

        if not from_email or not password:
            QMessageBox.critical(
                self,
                "Email Setup Error",
                "Please set up your Gmail credentials using environment variables.",
            )
            return

        subject = self.subject_input.text()
        body = self.body_input.toPlainText()  # Get multi-line text

        try:
            for recipient_email in selected_emails:
                EmailSender.send_email(
                    self.image_path,
                    recipient_email,
                    from_email,
                    password,
                    subject,
                    body,
                )
                success_message = QMessageBox(self)
                success_message.setIcon(QMessageBox.Icon.Information)
                success_message.setText("Email(s) sent successfully!")
                success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                ok_button = success_message.button(QMessageBox.StandardButton.Ok)
                ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
                success_message.exec()
                self.accept()  # Close the dialog on success
        except Exception as e:
            QMessageBox.critical(self, "Email Error", str(e))
