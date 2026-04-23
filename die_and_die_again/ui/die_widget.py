from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPoint, Property, QSize
from PySide6.QtGui import QPainter, QColor, QPolygon, QPen
import math
import random as rnd


DEFAULT_BG = QColor(240, 240, 240)
DEFAULT_FG = QColor(48, 48, 48)
MINIMUM_SIZE = QSize(96, 96)


class DieWidget(QWidget):
    def __init__(
        self,
        sides=6,
        value=None,
        bg_color=DEFAULT_BG,
        fg_color=DEFAULT_FG,
        parent=None,
    ):
        super().__init__(parent)
        self.setMinimumSize(MINIMUM_SIZE)
        self._sides = sides
        if value is None:
            value = sides
        self._value = value
        self._is_rolling = False
        self._roll_timer = QTimer(self)
        self._roll_timer.timeout.connect(self._update_roll)
        self._animation_value = value

        self._bg_color = QColor(bg_color)
        self._fg_color = QColor(fg_color)
        self._update_palette()
        self._update_tooltip()

    def _update_palette(self):
        pal = self.palette()
        pal.setColor(self.backgroundRole(), self._bg_color)
        pal.setColor(self.foregroundRole(), self._fg_color)
        self.setPalette(pal)

    def _update_tooltip(self):
        self.setToolTip(f"D{self._sides}: {self._value}")

    @Property(QColor)
    def background_color(self):
        return self._bg_color

    @background_color.setter
    def background_color(self, color):
        self._bg_color = QColor(color)
        self._update_palette()
        self.update()

    @Property(QColor)
    def foreground_color(self):
        return self._fg_color

    @foreground_color.setter
    def foreground_color(self, color):
        self._fg_color = QColor(color)
        self._update_palette()
        self.update()

    @Property(int)
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, value):
        self._sides = value
        self._update_tooltip()
        self.update()

    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        if not self._is_rolling:
            self._animation_value = val
        self._update_tooltip()
        self.update()

    def start_roll(self):
        self._is_rolling = True
        self._roll_timer.start(50)

    def stop_roll(self, final_value=None):
        self._is_rolling = False
        self._roll_timer.stop()
        if final_value is not None:
            self.value = final_value
        self.update()

    def _update_roll(self):
        self._animation_value = rnd.choice(
            [i for i in range(1, self._sides + 1) if i != self._animation_value]
        )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(5, 5, -5, -5)
        side = min(rect.width(), rect.height())
        center = rect.center()

        # Calculate border color (darker version of background)
        border_color = self._bg_color.darker(150)

        painter.setBrush(self._bg_color)
        painter.setPen(QPen(border_color, 4))  # Thick border

        def create_poly(num_sides: int):
            poly = QPolygon()
            for i in range(num_sides):
                angle = -90 + i * 360 / num_sides
                px = center.x() + (side // 2) * math.cos(math.radians(angle))
                py = center.y() + (side // 2) * math.sin(math.radians(angle))
                poly.append(QPoint(px, py))
            return poly

        if self._sides in [3, 4, 6, 8, 10, 12, 20]:
            poly = create_poly(self._sides)
            painter.drawPolygon(poly)
        else:
            # Default Circle
            painter.drawEllipse(center, side // 2, side // 2)

        # Draw Value
        if self._is_rolling:
            rgb_avg = (
                sum(
                    [
                        self._fg_color.red(),
                        self._fg_color.green(),
                        self._fg_color.blue(),
                    ]
                )
                // 3
            )
            if rgb_avg < 64:
                text_color = self._fg_color.lighter(150)
            else:
                text_color = self._fg_color.darker(150)
        else:
            text_color = self._fg_color

        painter.setPen(text_color)
        font = painter.font()
        font.setBold(True)
        font.setPointSize(side // 3)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, str(self._animation_value))
