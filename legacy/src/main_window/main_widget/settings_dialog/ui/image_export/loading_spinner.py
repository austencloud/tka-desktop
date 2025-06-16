import math
from PyQt6.QtCore import QRect, Qt, QTimer, QSize
from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPaintEvent,
    QShowEvent,
    QResizeEvent,
    QHideEvent,
    QCloseEvent,
)
from PyQt6.QtWidgets import QWidget


class WaitingSpinner(QWidget):
    """A highly configurable, custom loading spinner widget for PyQt6."""

    def __init__(
        self,
        parent: QWidget = None,
        center_on_parent: bool = True,
        disable_parent_when_spinning: bool = False,
        modality: Qt.WindowModality = Qt.WindowModality.NonModal,
        roundness: float = 100.0,
        fade: float = 80.0,
        lines: int = 20,
        line_length: int = 50,
        line_width: int = 2,
        radius: int = 50,
        speed: float = math.pi / 2,
        color: QColor = QColor(0, 0, 0),
    ) -> None:
        super().__init__(parent)

        self._center_on_parent = center_on_parent
        self._disable_parent_when_spinning = disable_parent_when_spinning

        self._color = color
        self._roundness = roundness
        self._minimum_trail_opacity = math.pi
        self._trail_fade_percentage = fade
        self._revolutions_per_second = speed
        self._number_of_lines = lines
        self._line_length = line_length
        self._line_width = line_width
        self._inner_radius = radius
        self._current_counter = 0
        self._is_spinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._update_size()
        self._update_timer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the spinner."""
        self._update_position()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        if self._current_counter >= self._number_of_lines:
            self._current_counter = 0

        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(self._number_of_lines):
            painter.save()
            painter.translate(
                self._inner_radius + self._line_length,
                self._inner_radius + self._line_length,
            )
            rotate_angle = 360 * i / self._number_of_lines
            painter.rotate(rotate_angle)
            painter.translate(self._inner_radius, 0)
            distance = self._line_count_distance_from_primary(
                i, self._current_counter, self._number_of_lines
            )
            color = self._current_line_color(
                distance,
                self._number_of_lines,
                self._trail_fade_percentage,
                self._minimum_trail_opacity,
                self._color,
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(
                    0,
                    -self._line_width // 2,
                    self._line_length,
                    self._line_width,
                ),
                self._roundness,
                self._roundness,
                Qt.SizeMode.RelativeSize,
            )
            painter.restore()

    def start(self) -> None:
        """Start the spinner."""
        self._update_position()
        self._is_spinning = True
        self.show()

        if self.parentWidget() and self._disable_parent_when_spinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._current_counter = 0

    def stop(self) -> None:
        """Stop the spinner."""
        self._is_spinning = False
        self.hide()

        if self.parentWidget() and self._disable_parent_when_spinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._current_counter = 0

    @property
    def color(self) -> QColor:
        """Get the spinner color."""
        return self._color

    @color.setter
    def color(self, color: QColor) -> None:
        """Set the spinner color."""
        self._color = color

    @property
    def roundness(self) -> float:
        """Get the roundness of the spinner lines."""
        return self._roundness

    @roundness.setter
    def roundness(self, roundness: float) -> None:
        """Set the roundness of the spinner lines."""
        self._roundness = max(0.0, min(100.0, roundness))

    @property
    def minimum_trail_opacity(self) -> float:
        """Get the minimum trail opacity."""
        return self._minimum_trail_opacity

    @minimum_trail_opacity.setter
    def minimum_trail_opacity(self, minimum_trail_opacity: float) -> None:
        """Set the minimum trail opacity."""
        self._minimum_trail_opacity = minimum_trail_opacity

    @property
    def trail_fade_percentage(self) -> float:
        """Get the trail fade percentage."""
        return self._trail_fade_percentage

    @trail_fade_percentage.setter
    def trail_fade_percentage(self, trail: float) -> None:
        """Set the trail fade percentage."""
        self._trail_fade_percentage = trail

    @property
    def revolutions_per_second(self) -> float:
        """Get the number of revolutions per second."""
        return self._revolutions_per_second

    @revolutions_per_second.setter
    def revolutions_per_second(self, revolutions_per_second: float) -> None:
        """Set the number of revolutions per second."""
        self._revolutions_per_second = revolutions_per_second
        self._update_timer()

    @property
    def number_of_lines(self) -> int:
        """Get the number of lines in the spinner."""
        return self._number_of_lines

    @number_of_lines.setter
    def number_of_lines(self, lines: int) -> None:
        """Set the number of lines in the spinner."""
        self._number_of_lines = lines
        self._current_counter = 0
        self._update_timer()

    @property
    def line_length(self) -> int:
        """Get the length of each line in the spinner."""
        return self._line_length

    @line_length.setter
    def line_length(self, length: int) -> None:
        """Set the length of each line in the spinner."""
        self._line_length = length
        self._update_size()

    @property
    def line_width(self) -> int:
        """Get the width of each line in the spinner."""
        return self._line_width

    @line_width.setter
    def line_width(self, width: int) -> None:
        """Set the width of each line in the spinner."""
        self._line_width = width
        self._update_size()

    @property
    def radius(self) -> int:
        """Get the radius of the spinner."""
        return self._inner_radius

    @radius.setter
    def radius(self, radius: int) -> None:
        """Set the radius of the spinner."""
        self._inner_radius = radius
        self._update_size()

    def _update_position(self) -> None:
        """Update the spinner position."""
        if self.parentWidget() and self._center_on_parent:
            self.move(
                self.parentWidget().width() // 2 - self.width() // 2,
                self.parentWidget().height() // 2 - self.height() // 2,
            )

    def _update_size(self) -> None:
        """Update the spinner size."""
        size = (self._inner_radius + self._line_length) * 2
        self.setFixedSize(QSize(size, size))

    def _update_timer(self) -> None:
        """Update the spinner timer."""
        self._timer.setInterval(
            int(1000 / (self._number_of_lines * self._revolutions_per_second))
        )

    def _rotate(self) -> None:
        """Rotate the spinner."""
        self._current_counter += 1
        if self._current_counter >= self._number_of_lines:
            self._current_counter = 0
        self.update()

    def _current_line_color(
        self,
        count: int,
        total_lines: int,
        fade: float,
        min_opacity: float,
        color: QColor,
    ) -> QColor:
        """Get the current line color."""
        color.setAlphaF(
            min_opacity + (1.0 - min_opacity) * ((count % total_lines) / total_lines)
        )
        return color

    def _line_count_distance_from_primary(
        self, current: int, primary: int, total_lines: int
    ) -> int:
        """Get the distance of the line count from the primary line."""
        distance = primary - current
        if distance < 0:
            distance += total_lines
        return distance

    def showEvent(self, event: QShowEvent) -> None:
        """Show the spinner."""
        self._update_position()
        super().showEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize the spinner."""
        self._update_position()
        super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Close the spinner."""
        self._timer.stop()
        super().closeEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        """Hide the spinner."""
        self._timer.stop()
        super().hideEvent(event)

    def show(self) -> None:

        super().show()
        self._update_position()
