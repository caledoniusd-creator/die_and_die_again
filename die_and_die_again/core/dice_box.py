import logging

from constants import __app_name__
from .game_die import GameDie

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