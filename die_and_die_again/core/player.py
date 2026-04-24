
from random import shuffle

from .die import DieType
from .game_die import GameDie


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