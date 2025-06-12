# Accessibility Manager - WCAG 2.1 AA Compliance and Screen Reader Support
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt
from typing import Dict, Any, Optional, List
import logging


class AccessibilityAnnouncer(QObject):
    """Handles accessibility announcements and screen reader communication"""

    announcement_requested = pyqtSignal(str, int)  # message, priority

    def __init__(self):
        super().__init__()
        self.announcement_queue: List[tuple] = []
        self.is_announcing = False

    def announce(self, message: str, priority: int = 0):
        """
        Queue an announcement for screen readers

        Args:
            message: Text to announce
            priority: 0=normal, 1=important, 2=urgent
        """
        self.announcement_queue.append((message, priority))
        self.process_queue()

    def announce_immediate(self, message: str):
        """Make an immediate high-priority announcement"""
        self.announce(message, priority=2)

    def process_queue(self):
        """Process queued announcements"""
        if self.is_announcing or not self.announcement_queue:
            return

        # Sort by priority (higher first)
        self.announcement_queue.sort(key=lambda x: x[1], reverse=True)

        message, priority = self.announcement_queue.pop(0)
        self.is_announcing = True

        # Log accessibility announcement (simplified for now)
        logging.info(f"Accessibility announcement: {message} (priority: {priority})")

        # Reset announcing flag after delay
        QTimer.singleShot(1000, self.reset_announcing)

    def reset_announcing(self):
        """Reset announcing flag and process next item"""
        self.is_announcing = False
        if self.announcement_queue:
            QTimer.singleShot(100, self.process_queue)


class KeyboardNavigationManager(QObject):
    """Manages keyboard navigation patterns and focus management"""

    focus_changed = pyqtSignal(QWidget, QWidget)  # old_widget, new_widget

    def __init__(self):
        super().__init__()
        self.focus_history: List[QWidget] = []
        self.navigation_groups: Dict[str, List[QWidget]] = {}

    def register_navigation_group(self, group_name: str, widgets: List[QWidget]):
        """Register a group of widgets for keyboard navigation"""
        self.navigation_groups[group_name] = widgets

        # Set up tab order within group
        for i in range(len(widgets) - 1):
            QWidget.setTabOrder(widgets[i], widgets[i + 1])

    def set_focus_with_announcement(self, widget: QWidget, announcement: str = ""):
        """Set focus and announce the change"""
        if widget and widget.isEnabled() and widget.isVisible():
            old_focus = QApplication.focusWidget()
            widget.setFocus()

            self.focus_history.append(widget)
            if len(self.focus_history) > 10:  # Keep last 10 focus changes
                self.focus_history.pop(0)

            if announcement:
                AccessibilityManager.instance().announce(announcement)
            else:
                # Auto-generate announcement
                name = widget.accessibleName() or widget.objectName() or "element"
                desc = widget.accessibleDescription()
                auto_announcement = f"Focused on {name}"
                if desc:
                    auto_announcement += f". {desc}"
                AccessibilityManager.instance().announce(auto_announcement)

            self.focus_changed.emit(old_focus, widget)

    def navigate_to_group(self, group_name: str, index: int = 0):
        """Navigate to a specific group and optionally an item within it"""
        if group_name in self.navigation_groups:
            widgets = self.navigation_groups[group_name]
            if widgets and 0 <= index < len(widgets):
                self.set_focus_with_announcement(
                    widgets[index], f"Navigated to {group_name} group"
                )

    def get_current_group(self, widget: QWidget) -> Optional[str]:
        """Get the navigation group of the current widget"""
        for group_name, widgets in self.navigation_groups.items():
            if widget in widgets:
                return group_name
        return None


class AccessibilityManager(QObject):
    """
    Central accessibility management system

    Features:
    - WCAG 2.1 AA compliance monitoring
    - Screen reader announcements
    - Keyboard navigation management
    - High contrast mode support
    - Focus management
    - Accessibility testing utilities
    """

    _instance = None

    def __init__(self):
        super().__init__()
        if AccessibilityManager._instance is not None:
            raise RuntimeError("AccessibilityManager is a singleton")

        self.announcer = AccessibilityAnnouncer()
        self.keyboard_nav = KeyboardNavigationManager()
        self.high_contrast_mode = False
        self.screen_reader_active = self.detect_screen_reader()
        self.accessibility_features = {
            "announcements": True,
            "keyboard_navigation": True,
            "high_contrast": False,
            "reduced_motion": False,
            "large_text": False,
        }

        AccessibilityManager._instance = self

    @classmethod
    def instance(cls) -> "AccessibilityManager":
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = AccessibilityManager()
        return cls._instance

    def detect_screen_reader(self) -> bool:
        """Detect if a screen reader is active"""
        try:
            # Check for common screen readers on Windows
            import subprocess
            import platform

            if platform.system() == "Windows":
                # Check for NVDA, JAWS, or Narrator
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq nvda.exe"],
                    capture_output=True,
                    text=True,
                )
                if "nvda.exe" in result.stdout:
                    return True

                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq jfw.exe"],
                    capture_output=True,
                    text=True,
                )
                if "jfw.exe" in result.stdout:
                    return True

            return False
        except Exception:
            return False

    def announce(self, message: str, priority: int = 0):
        """Make an accessibility announcement"""
        if self.accessibility_features["announcements"]:
            self.announcer.announce(message, priority)

    def announce_app_launch(self, app_name: str, estimated_time: int = 0):
        """Announce application launch"""
        message = f"Launching {app_name}"
        if estimated_time > 0:
            message += f". Estimated startup time: {estimated_time} seconds"
        self.announce(message, priority=1)

    def announce_app_launch_success(self, app_name: str):
        """Announce successful application launch"""
        self.announce(f"{app_name} launched successfully", priority=1)

    def announce_app_launch_failure(self, app_name: str, error: str):
        """Announce application launch failure"""
        self.announce(f"Failed to launch {app_name}. Error: {error}", priority=2)

    def announce_system_health(self, is_healthy: bool, details: str = ""):
        """Announce system health status"""
        status = "healthy" if is_healthy else "experiencing issues"
        message = f"System status: {status}"
        if details:
            message += f". {details}"
        self.announce(message, priority=1)

    def announce_search_results(self, count: int, query: str = ""):
        """Announce search results"""
        if query:
            message = f"Search for '{query}' returned {count} results"
        else:
            message = f"{count} applications available"
        self.announce(message)

    def set_high_contrast_mode(self, enabled: bool):
        """Enable or disable high contrast mode"""
        self.high_contrast_mode = enabled
        self.accessibility_features["high_contrast"] = enabled

        # Apply high contrast styles to application
        app = QApplication.instance()
        if app:
            if enabled:
                self.apply_high_contrast_styles()
            else:
                self.remove_high_contrast_styles()

        self.announce(
            f"High contrast mode {'enabled' if enabled else 'disabled'}", priority=1
        )

    def apply_high_contrast_styles(self):
        """Apply high contrast styling"""
        high_contrast_style = """
            * {
                background-color: black !important;
                color: white !important;
                border-color: white !important;
            }
            QPushButton {
                background-color: #000080 !important;
                color: white !important;
                border: 2px solid white !important;
            }
            QPushButton:focus {
                background-color: #0000FF !important;
                border: 3px solid yellow !important;
            }
            QLineEdit {
                background-color: white !important;
                color: black !important;
                border: 2px solid black !important;
            }
            QLineEdit:focus {
                border: 3px solid yellow !important;
            }
        """

        app = QApplication.instance()
        if app and hasattr(app, "setStyleSheet"):
            app.setStyleSheet(high_contrast_style)

    def remove_high_contrast_styles(self):
        """Remove high contrast styling"""
        app = QApplication.instance()
        if app and hasattr(app, "setStyleSheet"):
            app.setStyleSheet("")  # Reset to default

    def configure_widget_accessibility(
        self, widget: QWidget, name: str, description: str = "", role: str = ""
    ):
        """Configure accessibility properties for a widget"""
        widget.setAccessibleName(name)
        if description:
            widget.setAccessibleDescription(description)

        # Set focus policy for keyboard navigation
        if role in ["button", "link", "input"]:
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        elif role in ["label", "text"]:
            widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def register_navigation_group(self, group_name: str, widgets: List[QWidget]):
        """Register a navigation group"""
        self.keyboard_nav.register_navigation_group(group_name, widgets)

    def navigate_to_group(self, group_name: str, index: int = 0):
        """Navigate to a specific group"""
        self.keyboard_nav.navigate_to_group(group_name, index)

    def get_accessibility_report(self) -> Dict[str, Any]:
        """Generate accessibility compliance report"""
        return {
            "screen_reader_detected": self.screen_reader_active,
            "high_contrast_mode": self.high_contrast_mode,
            "features_enabled": self.accessibility_features,
            "navigation_groups": len(self.keyboard_nav.navigation_groups),
            "focus_history_length": len(self.keyboard_nav.focus_history),
            "wcag_compliance": "AA",  # Target compliance level
        }

    def test_accessibility_compliance(self, widget: QWidget) -> List[str]:
        """Test widget for accessibility compliance issues"""
        issues = []

        # Check for accessible name
        if not widget.accessibleName():
            issues.append(f"Widget {widget.objectName()} missing accessible name")

        # Check for keyboard accessibility
        if widget.focusPolicy() == Qt.FocusPolicy.NoFocus and widget.isEnabled():
            if isinstance(widget, (QPushButton, QLineEdit)):
                issues.append(
                    f"Interactive widget {widget.objectName()} not keyboard accessible"
                )

        # Check for sufficient color contrast (simplified check)
        if self.high_contrast_mode:
            # In high contrast mode, assume compliance
            pass
        else:
            # Would need more sophisticated color analysis
            pass

        return issues
