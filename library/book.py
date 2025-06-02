from dataclasses import dataclass, field
from library.random_number_utils import RandomNumberUtils

@dataclass (frozen=True, order=True, slots=True)
class Book:
    name: str
    genre: str
    year: int
    available: bool = True
    id: str = field(default_factory=RandomNumberUtils.generate_random_id)

    # class variable to track used IDs
    _used_ids = set()

    def __post_init__(self):
        # Use object.__setattr__ because the class is frozen
        unique_id = self._generate_unique_id()
        object.__setattr__(self, 'id', unique_id)

    @classmethod
    def _generate_unique_id(cls):
        while True:
            new_id = RandomNumberUtils.generate_random_id()
            if new_id not in cls._used_ids:
                cls._used_ids.add(new_id)
                return new_id

    @property
    def search_string(self):
        return f"{self.name}{self.genre}"