from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class SequenceShareSettings:
    DEFAULT_SEQUENCE_SHARING_SETTINGS = {"recipients": []}

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager

    def get_saved_recipients(self):
        return self.settings_manager.settings["sequence_sharing"].get("recipients", [])

    def add_recipient(self, name, email):
        recipients: list = self.get_saved_recipients()
        # Check if recipient already exists
        if not any(recipient["email"] == email for recipient in recipients):
            recipients.append({"name": name, "email": email})
            self.save_recipients(recipients)

    def save_recipients(self, recipients):
        self.settings_manager.settings["sequence_sharing"]["recipients"] = recipients
        self.settings_manager.save_settings()
