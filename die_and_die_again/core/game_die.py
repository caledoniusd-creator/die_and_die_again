from enum import Enum, unique
from random import choice


from core.die import Die


@unique
class DieMaterial(Enum):
    Wood = ("Wood",)
    Stone = ("Stone",)
    Resin = ("Resin",)
    Metal = ("Metal",)
    GemStone = ("Gemstone",)
    RareMetal = ("Rare Metal",)

    @staticmethod
    def random():
        return choice([dm for dm in DieMaterial])

    def __str__(self):
        return self.value[0]


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
    def new_die(cls, sides: int, weights=None, unique_id=None, material=None):
        return GameDie(sides=sides, weights=weights, unique_id=unique_id, material=material)