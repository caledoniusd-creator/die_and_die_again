import logging
from random import randint, shuffle

from constants import __app_name__

from .die import DieType
from .game_die import GameDie, GameDieFactory


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


class PlayerBase:
    def __init__(self, name: str, cash: int = 0, dice: list = None):
        self._name = name
        self._cash = cash
        self._dice = dice if dice is not None else []

    def __str__(self):
        return f"{self.name}, ${self.cash} #dice={self.num_dice}"

    @property
    def name(self):
        return self._name

    @property
    def cash(self):
        return self._cash

    @property
    def dice(self):
        return self._dice

    @property
    def num_dice(self):
        return len(self.dice)

    def add_die(self, new_die: GameDie):
        if isinstance(new_die, GameDie) and new_die not in self._dice:
            self._dice.append(new_die)

    def remove_die(self, remove_die: GameDie):
        if isinstance(remove_die, GameDie) and remove_die in self._dice:
            self._dice.remove(remove_die)

    def add_dice(self, dice: list):
        for d in dice:
            self.add_die(d)

    def add_cash(self, amount: int):
        self._cash += amount

    def remove_cash(self, amount: int):
        if amount < 0:
            raise ValueError(f"amount must be >= 0, got {amount}")

        actual_remove = min(amount, self._cash)
        self._cash -= actual_remove
        return actual_remove

    def get_all_dice(self, die_type: DieType | None = None):
        if die_type is None:
            return list(self.dice)
        return [d for d in self.dice if d.sides == die_type.sides]

    def get_dice_group(self, group: list):
        dice = []
        missing_dice = []
        total_count = 0
        for g in group:
            total_count += g[1]
            sided_dice = self.get_all_dice(g[0])
            shuffle(sided_dice)
            sided_count = len(sided_dice)
            if sided_count < g[1]:
                missing_dice.append((g, g[1] - sided_count))
                dice.extend(sided_dice[:sided_count])
            else:
                dice.extend(sided_dice[: g[1]])
        actual_count = len(dice)
        if actual_count < total_count:
            logger.warning(
                f"Not enough dice for group {group} (actual={actual_count}, total={total_count})"
            )

        return dice, missing_dice


class GamePlayer(PlayerBase):
    @staticmethod
    def default_player():
        player = GamePlayer("Dwayne", 250)

        # add Dice
        starting_dice = [
            (DieType.D3, 1),
            (DieType.D4, 2),
            (DieType.D6, 5),
            (DieType.D8, 1),
            (DieType.D20, 1),
        ]

        for dt in starting_dice:
            for _ in range(dt[1]):
                player.add_die(GameDieFactory.random_die(die_type=dt[0]))
        return player

    def __init__(self, name: str, cash: int):
        super().__init__(name, cash)

    def __str__(self):
        return super().__str__()


class Game:
    def __init__(self, player: GamePlayer, game_seed: int = 0):
        self._player = player
        self._game_seed = game_seed if game_seed != 0 else randint(0, 0xFFFFFFFF)

    def __str__(self):
        return f"<{self.__class__.__name__} player=({self.player}), game_seed={hex(self.game_seed)}>"

    @property
    def player(self):
        return self._player

    @property
    def game_seed(self):
        return self._game_seed
