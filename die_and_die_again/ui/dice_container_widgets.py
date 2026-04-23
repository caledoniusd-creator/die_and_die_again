from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from ui.die_widget import DieWidget

class DiceContainerWidget(QWidget):
    """Base class for widgets holding multiple dice."""
    def __init__(self, title="Dice Container", parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.dice_layout = QGridLayout()
        self.layout.addLayout(self.dice_layout)
        self._dice_widgets = []

    def clear_dice(self):
        for widget in self._dice_widgets:
            self.dice_layout.removeWidget(widget)
            widget.deleteLater()
        self._dice_widgets = []

    def set_dice(self, dice_list):
        self.clear_dice()
        cols = 4
        for i, die in enumerate(dice_list):
            dw = DieWidget(sides=die.sides, value=getattr(die, 'last_roll', None))
            self._dice_widgets.append(dw)
            self.dice_layout.addWidget(dw, i // cols, i % cols)

class RollingDiceWidget(DiceContainerWidget):
    """Widget specifically for rolling a group of dice."""
    def __init__(self, title="Rolling Area", parent=None):
        super().__init__(title, parent)
        self.roll_button = QPushButton("Roll All")
        self.layout.addWidget(self.roll_button)
        self._current_dice = []

    def set_dice(self, dice_list):
        super().set_dice(dice_list)
        self._current_dice = dice_list

    def start_rolling(self):
        for dw in self._dice_widgets:
            dw.start_roll()

    def stop_rolling(self, values):
        for i, dw in enumerate(self._dice_widgets):
            if i < len(values):
                dw.stop_roll(values[i])
            else:
                dw.stop_roll()

class PlayerInventoryWidget(DiceContainerWidget):
    """Widget to show all dice a player has."""
    def __init__(self, title="Player Inventory", parent=None):
        super().__init__(title, parent)
