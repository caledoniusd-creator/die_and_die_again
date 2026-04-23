from enum import Enum, unique
from random import choices, random


from core.die import DieType, Die, DieWeightsWorker


@unique
class DieMaterial(Enum):
    Wood = ("Wood", "#F5B027", 1024)
    Stone = ("Stone", "#998C75", 512)
    Resin = ("Resin", "#DA4B49", 256)
    Metal = ("Metal", "#BFC9CA", 128)
    GemStone = ("Gemstone", "#9DECD8", 64)
    RareMetal = ("Rare Metal", "#D0F6F6", 32)

    @staticmethod
    def weights():
        return [dm.value[2] for dm in DieMaterial]

    @staticmethod
    def random():
        return choices([dm for dm in DieMaterial], DieMaterial.weights(), k=1)[0]

    def __str__(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]


class GameDie(Die):
    @staticmethod
    def dice_list_string(dice: list):
        return "[" + "|".join([str(d) for d in dice]) + "]"

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

    @classmethod
    def dice_group(cls, dice_types):
        dice = []
        for d in dice_types:
            dt, count = d[0], d[1]
            dice.extend([GameDieFactory.random_die(dt) for _ in range(count)])
        return dice
