
from functools import cached_property
from random import choices


class ChanceCalculator:
    def __init__(self, chance: float):
        self._chance = max(0.0, min(1.0, chance))

    @property
    def chance(self):
        return self._chance

    @property
    def weights(self):
        return [self.chance, 1.0 - self.chance]

    @property
    def values(self):
        return [True, False]

    def roll(self):
        return choices(self.values, self.weights, k=1)[0]