
import logging
from random import randint

from constants import __app_name__

from .die import DieType, Die, DieWeightsWorker
from .game_die import GameDie, GameDieFactory

from .dice_shaker import DiceShaker


logger = logging.getLogger(__app_name__)


class DieBoxFullException(RuntimeWarning):
    def __init__(self, *args):
        super().__init__(*args)


class DiceBox:

    @staticmethod
    def default_box():
        return DiceBox(20)

    def __init__(self, size: int = 28):
        self._size = size
        self._dice = []

    def __str__(self):
        just_size = len(str(self.size))
        return f"<{self.__class__.__name__} size={str(self.num_dice).ljust(just_size)}/{self.size}>"
    
    @property
    def size(self):
        return self._size
    
    @property
    def dice(self):
        return self._dice
    
    @property
    def num_dice(self):
        return len(self.dice)
    
    @property
    def has_space(self):
        return self.num_dice < self.size

    def take_die(self, remove_die: GameDie):
        if remove_die not in self.dice:
            logger.warning(f"Die {remove_die} not in box")
            return 
        self._dice.remove(remove_die)

    def empty(self):
        self._dice.clear()

    def take_all(self):
        all_dice = self.dice.copy()
        self.empty()
        return all_dice
    
    def add_die(self, new_die: GameDie):
        if not isinstance(new_die, GameDie):
            raise ValueError(f"new_die is not GameDie: {new_die}")
        
        if new_die in self._dice:
            logger.warning(f"{new_die} already in box")
            return
        
        if self.num_dice >= self.size:
            logger.warning(f"Max dice in box! size={self.size}")
            return
        
        self._dice.append(new_die)
        

class GamePlayer:

    @staticmethod
    def default_player():
        player = GamePlayer("Dwayne", 250)
        player.add_box(DiceBox.default_box())
        player.add_shaker(DiceShaker.default_shaker())

        # add Dice
        dice_types = [DieType.D6 for _ in range(4)] + [DieType.D4 for _ in range(3)]
        for dt in dice_types:
            new_die = GameDieFactory.random_die(die_type=dt)
            player.add_die(new_die)

        return player

    def __init__(self, name:str, cash: int):
        self._name = name
        self._cash = cash

        self._boxes = []
        self._shakers = []

    def __str__(self):
        return f"{self.name}, ${self.cash} #boxes={self.num_boxes}, #shakers={self.num_shakers}, #dice={self.total_num_dice()}"

    @property
    def name(self):
        return self._name
    
    @property
    def cash(self):
        return self._cash
    
    @property
    def boxes(self):
        return self._boxes

    @property
    def num_boxes(self):
        return len(self.boxes)
    
    @property
    def shakers(self):
        return self._shakers

    @property
    def num_shakers(self):
        return len(self.shakers)
    
    def total_num_dice(self):
        return sum([box.num_dice for box in self.boxes])
    
    def all_dice(self):
        dice = []
        for box in self.boxes:
            dice.extend(box.dice)
        return dice
    
    def add_box(self, dice_box: DiceBox):
        if not isinstance(dice_box, DiceBox):
            logger.warning(f"{dice_box} is not a dicebox")
            return
        elif self.boxes and dice_box in self.boxes:
            logger.warning(f"player already has box: {dice_box}")
            return
        
        self._boxes.append(dice_box)

    def add_shaker(self, dice_shaker: DiceShaker):
        if not isinstance(dice_shaker, DiceShaker):
            logger.warning(f"{dice_shaker} is not a DiceShaker")
            return
        elif self.shakers and dice_shaker in self.shakers:
            logger.warning(f"player already has shaker: {dice_shaker}")
            return
        
        self._shakers.append(dice_shaker)

    
    def get_box(self):
        if self.boxes:
            return self.boxes[0]
        return None
    
    def get_shaker(self):
        if self.shakers:
            return self.shakers[0]
        return None
    

    def add_die(self, die: GameDie):
        box = self.get_box()
        if isinstance(box, DiceBox):
            if box.has_space:
                box.add_die(die)
                return True
            else:
                logger.warning("Box is full")
        else:
            logger.warning("No boxes")
        return False
    

class Game:
    def __init__(
            self, 
            player: GamePlayer,
            game_seed: int = 0
        ):
        self._player = player
        self._game_seed = game_seed if game_seed != 0 else randint(0, 0xffffffff)

    def __str__(self):
        return f"<{self.__class__.__name__} player=({self.player}), game_seed={hex(self.game_seed)}>"
    
    @property
    def player(self):
        return self._player
    
    @property
    def game_seed(self):
        return self._game_seed