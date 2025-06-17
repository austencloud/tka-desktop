from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from typing import Optional


class AccessibilityManager:
    """Singleton helper to keep widgets keyboard‑ and screen‑reader‑friendly."""

    _instance: Optional["AccessibilityManager"] = None

    def __init__(self) -> None:
        if AccessibilityManager._instance is not None:
            raise RuntimeError("AccessibilityManager is a singleton")
        AccessibilityManager._instance = self

    @classmethod
    def instance(cls) -> "AccessibilityManager":
        if cls._instance is None:
            cls._instance = AccessibilityManager()
        return cls._instance

    def configure(self, widget: QWidget, name: str, desc: str = "") -> None:
        widget.setAccessibleName(name)
        widget.setAccessibleDescription(desc)
        widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
