from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PlayerWidget(QWidget):
    def __init__(self, player=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.name_label = QLabel("Name: -")
        self.cash_label = QLabel("Cash: -")
        self.dice_count_label = QLabel("Total Dice: -")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.cash_label)
        self.layout.addWidget(self.dice_count_label)

        if player:
            self.set_player(player)

    def set_player(self, player):
        self.name_label.setText(f"Name: {player.name}")
        self.cash_label.setText(f"Cash: ${player.cash}")
        self.dice_count_label.setText(f"Total Dice: {player.num_dice}")
