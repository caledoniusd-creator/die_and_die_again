from enum import Enum, unique
import logging
from random import choices, choice, random
from uuid import uuid4, UUID


from constants import __app_name__

logger = logging.getLogger(__app_name__)


class InvalidSides(ValueError):
    pass


@unique
class DieType(Enum):
    D3 = ("D3", 3)
    D4 = ("D4", 4)
    D6 = ("D6", 6)
    D8 = ("D8", 8)
    D10 = ("D10", 10)
    D12 = ("D12", 12)
    D20 = ("D20", 20)

    @staticmethod
    def from_sides(sides: int):
        if sides < 3:
            raise DieType.InvalidSides(
                f"DieType: Too few sides({sides}) given expected minimum of 3"
            )

        for dt in DieType:
            if dt.sides == sides:
                return dt
        raise DieType.InvalidSides(
            f"DieType: invalid #sides({sides}), expected 3, 4, 6, 8, 10, 12 or 20"
        )

    @staticmethod
    def random():
        return choice([dt for dt in DieType])

    def __str__(self):
        return self.value[0]

    @property
    def sides(self):
        return self.value[1]


DieType.InvalidSides = InvalidSides


class Die:
    def __init__(
        self,
        sides: int = 6,
        weights: list | None = None,
        unique_id: UUID | None = None,
        roll_count: int | None = 0,
    ):
        if sides < 2:
            raise ValueError(f"Min sides is 2, got {sides}")

        if weights and len(weights) != sides:
            raise ValueError(
                f"Weight count mismatch. expected {sides} got {len(weights)}"
            )

        self._unique_id = unique_id if isinstance(unique_id, UUID) else uuid4()
        self._sides = sides
        self._values = [v for v in range(1, sides + 1)]
        self._weights = weights or [1.0 / sides for _ in range(sides)]

        self._rolled_values = {v: 0 for v in self._values}

    def __repr__(self):
        return f"<{self.__class__.__name__} unique_id={self.unique_id}, sides={self.sides}, values={self.weighting_str()}>"

    def __str__(self):
        return f"D{self.sides}"

    def info_text(self):
        return [
            f"<{self.__class__.__name__}>",
            f"unique_id={self.unique_id}",
            f"sides={self.sides}",
            f"values={self.weighting_str()}",
            f"roll_count={self.roll_count}",
        ]

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def sides(self):
        return self._sides

    @property
    def values(self):
        return self._values

    @property
    def weights(self):
        return self._weights

    @property
    def roll_count(self):
        return sum(self.rolled_values.values())

    @property
    def rolled_values(self):
        return self._rolled_values

    def reset_weights(self):
        self._weights = [1.0 / self.sides for _ in range(self.sides)]

    def value_weight(self, value: int):
        if value not in self.values:
            raise ValueError(f"Value must be in {self.values}, got {value}")
        return self.weights[self.values.index(value)]

    def change_weighting(self, value: int, percentage: float):
        if value not in self.values:
            raise ValueError(f"Value must be in {self.values}, got {value}")
        ix = self.values.index(value)
        self._weights[ix] = self._weights[ix] + (
            self._weights[ix] * (percentage / 100.0)
        )

    def normalize_weights(self):
        total = sum(self.weights)
        self._weights = [w / total for w in self.weights]

    def weighting_str(self):
        return (
            "["
            + ",".join([f"{v:2d}:{w:.2f}" for v, w in zip(self.values, self.weights)])
            + "]"
        )

    def roll(self):
        rolled_value = choices(self.values, weights=self.weights, k=1)[0]
        self._rolled_values[rolled_value] += 1
        return rolled_value

    def multiple_roll(self, n: int):
        if n < 1:
            raise ValueError(f"Min rolls is 1, got {n}")
        return [self.roll() for _ in range(n)]

    def reset_all(self):
        self._rolled_values = {v: 0 for v in self._values}
        self.reset_weights()


class DieWeightsWorker:
    def __init__(self, die: Die):
        self._die = die

    @property
    def die(self):
        return self._die

    def random_weight_variation(self, range_value: float):

        def new_variation_pc():
            return -range_value + (2 * range_value * random())

        # logger.info(f"Applying random weights variations: \u00b1 {range_value:3.3f}")
        for v in self.die.values:
            self.die.change_weighting(v, new_variation_pc())
