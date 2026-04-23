from PySide6.QtWidgets import QMainWindow, QMdiArea, QMdiSubWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from ui.die_widget import DieWidget
from ui.dice_container_widgets import RollingDiceWidget, PlayerInventoryWidget
from ui.player_widget import PlayerWidget
from core.game import GamePlayer
from core.game_die import GameDieFactory
from core.die import DieType

class SandboxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Die Sandbox - MDI")
        self.setMinimumSize(800, 600)
        
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        
        self.setup_widgets()
        
    def setup_widgets(self):
        # 1. Individual Die Test
        die_test_widget = QWidget()
        die_layout = QVBoxLayout(die_test_widget)
        
        controls_layout = QHBoxLayout()
        self.side_selector = QComboBox()
        self.side_selector.addItems(["3", "4", "6", "8", "10", "12", "20"])
        self.side_selector.setCurrentText("6")
        self.side_selector.currentTextChanged.connect(self.change_die_sides)
        controls_layout.addWidget(self.side_selector)
        
        roll_btn = QPushButton("Roll Single")
        roll_btn.clicked.connect(self.roll_single)
        controls_layout.addWidget(roll_btn)
        
        die_layout.addLayout(controls_layout)
        
        self.single_die = DieWidget(sides=6, bg_color=QColor("gold"), fg_color=QColor("darkblue"))
        die_layout.addWidget(self.single_die, alignment=Qt.AlignCenter)
        
        sw1 = QMdiSubWindow()
        sw1.setWidget(die_test_widget)
        sw1.setWindowTitle("Single Die Test")
        self.mdi.addSubWindow(sw1)
        
        # 2. Player Info Test
        self.player = GamePlayer.default_player()
        player_info = PlayerWidget(self.player)
        sw2 = QMdiSubWindow()
        sw2.setWidget(player_info)
        sw2.setWindowTitle("Player Info")
        self.mdi.addSubWindow(sw2)
        
        # 3. Player Inventory Test
        inventory = PlayerInventoryWidget("Player Inventory")
        inventory.set_dice(self.player.all_dice())
        sw3 = QMdiSubWindow()
        sw3.setWidget(inventory)
        sw3.setWindowTitle("Inventory")
        self.mdi.addSubWindow(sw3)
        
        # 4. Rolling Area Test
        self.rolling_area = RollingDiceWidget("Rolling Area")
        dice_to_roll = [GameDieFactory.random_die(dt) for dt in DieType]
        self.rolling_area.set_dice(dice_to_roll)
        self.rolling_area.roll_button.clicked.connect(self.perform_multi_roll)
        
        sw4 = QMdiSubWindow()
        sw4.setWidget(self.rolling_area)
        sw4.setWindowTitle("Multi-Roll Test")
        self.mdi.addSubWindow(sw4)
        
        self.mdi.tileSubWindows()

    def change_die_sides(self, text):
        self.single_die.sides = int(text)
        self.single_die.value = 1

    def roll_single(self):
        self.single_die.start_roll()
        QTimer.singleShot(1000, lambda: self.single_die.stop_roll(rnd_val := GameDieFactory.random_die(DieType.from_sides(self.single_die.sides)).roll()))

    def perform_multi_roll(self):
        self.rolling_area.start_rolling()
        def stop():
            results = [d.roll() for d in self.rolling_area._current_dice]
            self.rolling_area.stop_rolling(results)
        QTimer.singleShot(1000, stop)
