from enum import Enum, unique
from random import choice, random


from core.die import DieType, Die, DieWeightsWorker


@unique
class DieMaterial(Enum):
    Wood = ("Wood", "#F5B027")
    Stone = ("Stone", "#998C75")
    Resin = ("Resin", "#DA4B49")
    Metal = ("Metal", "#BFC9CA")
    GemStone = ("Gemstone", "#9DECD8")
    RareMetal = ("Rare Metal", "#D0F6F6")

    @staticmethod
    def random():
        return choice([dm for dm in DieMaterial])

    def __str__(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]


class GameDie(Die):
    def __init__(
        self,
        sides=6,
        weights=None,
        unique_id=None,
        material: DieMaterial | None = None,
    ):
        super().__init__(sides, weights, unique_id)
        self._material = material or DieMaterial.random()

    @property
    def material(self):
        return self._material

    def info_text(self):
        text = super().info_text()
        text.extend(
            [
                f"material={self.material}",
            ]
        )
        return text


class GameDieFactory:
    @classmethod
    def new_die(
        cls,
        sides: int,
        weights=None,
        unique_id=None,
        material=None,
        random_variations=True,
    ):
        die = GameDie(
            sides=sides, weights=weights, unique_id=unique_id, material=material
        )
        if random_variations:
            variation = max(0.1, random() * 5.0)
            DieWeightsWorker(die).random_weight_variation(variation)
        return die

    @classmethod
    def random_die(cls, die_type: DieType | None = None, random_variations=True):
        die_type = die_type if isinstance(die_type, DieType) else DieType.random()
        weights = None
        return GameDieFactory.new_die(
            sides=die_type.sides,
            weights=weights,
            unique_id=None,
            material=None,
            random_variations=random_variations,
        )
