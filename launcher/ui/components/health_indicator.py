# Health Indicator - Advanced System Health Display
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QFrame,
    QToolTip,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter
from typing import Dict, Any
import psutil


class SystemMetricsWidget(QFrame):
    """Detailed system metrics display"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Create metrics display"""
        self.setObjectName("systemMetrics")
        self.setStyleSheet(
            """
            QFrame#systemMetrics {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                padding: 12px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # CPU Usage
        self.cpu_label = QLabel("CPU: --")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximum(100)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(6)

        # Memory Usage
        self.memory_label = QLabel("Memory: --")
        self.memory_bar = QProgressBar()
        self.memory_bar.setMaximum(100)
        self.memory_bar.setTextVisible(False)
        self.memory_bar.setFixedHeight(6)

        # Running Processes
        self.processes_label = QLabel("Processes: --")

        for widget in [
            self.cpu_label,
            self.cpu_bar,
            self.memory_label,
            self.memory_bar,
            self.processes_label,
        ]:
            layout.addWidget(widget)

        self.style_progress_bars()

    def style_progress_bars(self):
        """Apply custom styling to progress bars"""
        progress_style = """
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:0.7 #f39c12, stop:1 #e74c3c);
                border-radius: 3px;
            }
        """
        self.cpu_bar.setStyleSheet(progress_style)
        self.memory_bar.setStyleSheet(progress_style)

    def update_metrics(self, metrics: Dict[str, Any]):
        """Update displayed metrics"""
        if "cpu_percent" in metrics:
            cpu = metrics["cpu_percent"]
            self.cpu_label.setText(f"CPU: {cpu:.1f}%")
            self.cpu_bar.setValue(int(cpu))

        if "memory_percent" in metrics:
            memory = metrics["memory_percent"]
            memory_gb = metrics.get("memory_used_gb", 0)
            self.memory_label.setText(f"Memory: {memory:.1f}% ({memory_gb}GB)")
            self.memory_bar.setValue(int(memory))

        if "running_processes" in metrics:
            processes = metrics["running_processes"]
            self.processes_label.setText(f"Processes: {processes}")


class HealthIndicator(QWidget):
    """
    Advanced system health indicator with detailed metrics

    Features:
    - Real-time system health status
    - CPU and memory usage monitoring
    - Process count tracking
    - Expandable detailed view
    - Accessibility announcements
    - Color-coded status indicators
    """

    health_clicked = pyqtSignal()
    metrics_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_healthy = True
        self.current_metrics = {}
        self.expanded = False
        self.setup_ui()
        self.setup_accessibility()

    def setup_ui(self):
        """Create the health indicator interface"""
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        # Main health button
        self.health_button = QPushButton()
        self.health_button.setFixedSize(120, 32)
        self.health_button.clicked.connect(self.toggle_details)
        self.health_button.setAccessibleName("System health indicator")
        self.health_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(39, 174, 96, 0.2);
                border: 1px solid rgba(39, 174, 96, 0.4);
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: rgba(39, 174, 96, 0.3);
                border-color: rgba(39, 174, 96, 0.6);
            }
            QPushButton:pressed {
                background: rgba(39, 174, 96, 0.4);
            }
        """
        )
        layout.addWidget(self.health_button)

        # Expandable metrics panel
        self.metrics_widget = SystemMetricsWidget()
        self.metrics_widget.hide()
        layout.addWidget(self.metrics_widget)

        # Update initial state
        self.update_health_display(True, {})

    def setup_accessibility(self):
        """Configure accessibility features"""
        self.setAccessibleName("System Health Monitor")
        self.setAccessibleDescription(
            "Shows current system health status. Click to view detailed metrics."
        )

    def update_health_display(self, is_healthy: bool, metrics: Dict[str, Any]):
        """Update health status and metrics"""
        # Safety check to prevent crashes if widget is deleted
        if not self.health_button or not hasattr(self.health_button, "setText"):
            return

        self.is_healthy = is_healthy
        self.current_metrics = metrics

        # Update button appearance and text
        if is_healthy:
            status_text = "🟢 Healthy"
            button_style = """
                QPushButton {
                    background: rgba(39, 174, 96, 0.2);
                    border: 1px solid rgba(39, 174, 96, 0.4);
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background: rgba(39, 174, 96, 0.3);
                    border-color: rgba(39, 174, 96, 0.6);
                }
            """
            accessible_desc = "System is healthy. All components functioning normally."
        else:
            status_text = "🔴 Issues"
            button_style = """
                QPushButton {
                    background: rgba(231, 76, 60, 0.2);
                    border: 1px solid rgba(231, 76, 60, 0.4);
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background: rgba(231, 76, 60, 0.3);
                    border-color: rgba(231, 76, 60, 0.6);
                }
            """
            accessible_desc = "System issues detected. Click for details."

        try:
            self.health_button.setText(status_text)
            self.health_button.setStyleSheet(button_style)
            self.health_button.setAccessibleDescription(accessible_desc)
        except RuntimeError:
            # Widget has been deleted, ignore the update
            return

        # Update metrics if expanded
        if self.expanded:
            self.metrics_widget.update_metrics(metrics)

        # Create detailed tooltip
        self.update_tooltip(metrics)

    def update_tooltip(self, metrics: Dict[str, Any]):
        """Create rich tooltip with system information"""
        tooltip_parts = []

        if self.is_healthy:
            tooltip_parts.append("✅ System Status: Healthy")
        else:
            tooltip_parts.append("❌ System Status: Issues Detected")

        if "cpu_percent" in metrics:
            cpu = metrics["cpu_percent"]
            tooltip_parts.append(f"🖥️ CPU Usage: {cpu:.1f}%")

        if "memory_percent" in metrics:
            memory = metrics["memory_percent"]
            memory_gb = metrics.get("memory_used_gb", 0)
            tooltip_parts.append(f"💾 Memory: {memory:.1f}% ({memory_gb}GB)")

        if "running_processes" in metrics:
            processes = metrics["running_processes"]
            tooltip_parts.append(f"⚙️ Processes: {processes}")

        if "error" in metrics:
            tooltip_parts.append(f"❗ Error: {metrics['error']}")

        tooltip_parts.append("\n💡 Click to toggle detailed view")

        self.health_button.setToolTip("\n".join(tooltip_parts))

    def toggle_details(self):
        """Toggle detailed metrics view"""
        self.expanded = not self.expanded

        if self.expanded:
            self.metrics_widget.show()
            self.metrics_widget.update_metrics(self.current_metrics)
            self.health_button.setText("🟢 Hide" if self.is_healthy else "🔴 Hide")

            # Announce expansion to screen readers
            self.setAccessibleDescription(
                "Detailed system metrics now visible. "
                f"CPU: {self.current_metrics.get('cpu_percent', 0):.1f}%, "
                f"Memory: {self.current_metrics.get('memory_percent', 0):.1f}%"
            )
        else:
            self.metrics_widget.hide()
            self.health_button.setText("🟢 Healthy" if self.is_healthy else "🔴 Issues")

            # Announce collapse to screen readers
            self.setAccessibleDescription("Detailed metrics hidden. Click to expand.")

        self.health_clicked.emit()

    def get_current_status(self) -> str:
        """Get current status for screen reader announcements"""
        if self.is_healthy:
            status = "System healthy"
        else:
            status = "System issues detected"

        if self.current_metrics:
            cpu = self.current_metrics.get("cpu_percent", 0)
            memory = self.current_metrics.get("memory_percent", 0)
            status += f". CPU {cpu:.1f}%, Memory {memory:.1f}%"

        return status

    def announce_status_change(self):
        """Announce status changes to screen readers"""
        status = self.get_current_status()
        self.setAccessibleDescription(status)

        # Force screen reader announcement
        self.health_button.setAccessibleDescription(status)
