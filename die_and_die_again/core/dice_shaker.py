
from uuid import uuid4, UUID


class DiceShaker:

    @staticmethod
    def default_shaker():
        return DiceShaker("Leather Shaker")

    def __init__(self, name, unique_id: UUID|None=None):
        self._name = name
        self._unique_id = unique_id if isinstance(unique_id, UUID) else uuid4()

    def __str__(self):
        return f"{self.name}: {self.unique_id}"
    
    @property
    def name(self):
        return self._name
    
    @property
    def unique_id(self):
        return self._unique_id
    
