from abc import ABC, abstractmethod
from enum import Enum
import random
import uuid


random.seed(int(uuid.uuid4()))

class Die(ABC):
    name: str

    @abstractmethod
    def roll(self) -> int:
        pass

class SixSidedDie(Die):
    def __init__(self):
        self.name = "d6"

    def roll(self) -> int:
        return random.randint(1,6)

class TenSidedDie(Die):
    def __init__(self):
        self.name = "d10"

    def roll(self) -> int:
        return random.randint(1,10)

class TwelveSidedDie(Die):
    def __init__(self):
        self.name = "d12"

    def roll(self) -> int:
        return random.randint(1,12)

class TwentySidedDie(Die):
    def __init__(self):
        self.name = "d20"

    def roll(self) -> int:
        return random.randint(1,20)