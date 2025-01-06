from abc import ABC, abstractmethod
from typing import Self
import random
import uuid


random.seed(int(uuid.uuid4()))

class Die(ABC):
    name: str
    face_count: int
    rolled: int
    
    @abstractmethod
    def __init__(self, face_count: str):
        self.face_count = face_count
        self.name = f'd{face_count}'
        self.rolled = 0
        
    def roll(self) -> int:
        self.rolled = random.randint(1, self.face_count)
        return self.rolled
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'Die("{self.name}, face_count: {self.face_count}, rolled: {self.rolled}")'
    
    def __add__(self, other) -> int:
        if issubclass(type(other), self.__class__):
            return self.rolled + other.rolled
        elif isinstance(other, int):
            return self.rolled + other
        else:
            raise ValueError(f"unsupported (+) types: '{type(self)}' and '{type(other)}'")
        
    def __radd__(self, other):
        if (other == 0):
            return self
        else:
            return self.__add__(other)

class FourSidedDie(Die):
    def __init__(self):
        super().__init__(4)

class SixSidedDie(Die):
    def __init__(self):
        super().__init__(6)

class EightSidedDie(Die):
    def __init__(self):
        super().__init__(8)

class TenSidedDie(Die):
    def __init__(self):
        super().__init__(10)

class TwelveSidedDie(Die):
    def __init__(self):
        super().__init__(12)

class TwentySidedDie(Die):
    def __init__(self):
        super().__init__(20)
    
class OneHundredSidedDie(Die):
    def __init__(self):
        super().__init__(100)

class RollManager():
    """
    example:
        dice = [SixSidedDie() for _ in range(4)]

        RollManager(dice).roll()
        RollManager(dice).roll_with_advantage()
        RollManager(dice).roll_with_disadvantage()
    """
    dice: list[Die]

    def __init__(self, dice: list[Die]):
        self.dice = dice
        self.die_type = self.dice[0]

    def print_roll_results(self, message: str, results: list[int]) -> None:
        print(f"{message}:")
        print(",".join(str(num) for num in results))

    def add_die_to_roll(self) -> Self:
        print
        die_type = type(self.dice[0])
        self.dice.append(die_type())
        return self
    
    def roll_dice(self) -> Self:
        print(f"rolling {len(self.dice)}{self.dice[0].name}")
        self.print_roll_results("results", [d.roll() for d in self.dice])
        return self
    
    def get_roll_total(self) -> int:
        roll_total = sum([d.rolled for d in self.dice])
        print(f"total rolled: {roll_total}  ({" + ".join([str(d.rolled) for d in self.dice])})")
        return roll_total

    def remove_lowest_roll(self) -> Self:
        lowest = min(self.dice, key=lambda d: d.rolled)
        print(f"removing lowest roll: {lowest.rolled}")
        self.dice.remove(lowest)
        return self
    
    def remove_highest_roll(self) -> Self:
        highest = max(self.dice, key=lambda d: d.rolled)
        print(f"removing highest roll: {highest.rolled}")
        self.dice.remove(highest)
        return self
    
    def roll_with_advantage(self) -> int:
        print(f"Adding an additional {self.dice[0].name} to roll with advantage")
        self.add_die_to_roll()          \
            .roll_dice()                \
            .remove_lowest_roll()       \
            .get_roll_total()
        
    def roll_with_disadvantage(self) -> int:
        print(f"Adding an additional {self.dice[0].name} to roll with disadvantage")
        self.add_die_to_roll()          \
            .roll_dice()                \
            .remove_highest_roll()      \
            .get_roll_total()
        
    def roll(self) -> int:
        self.roll_dice().get_roll_total()
