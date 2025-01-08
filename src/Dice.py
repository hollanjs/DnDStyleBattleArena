from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, List, Dict, Any
import random
import uuid
import copy
import logging


random.seed(int(uuid.uuid4()))


@dataclass(order=True, frozen=True)
class Die(ABC):
    name: str = field(compare=False, init=False)
    face_count: int = field(compare=False)
    rolled: int = field(default=0, compare=True)

    def __post_init__(self):
        object.__setattr__(self, "name", f'd{self.face_count}')

    def __str__(self):
        return self.name

    def __add__(self, other) -> int:
        if other == 0:
            return self.rolled
        elif isinstance(other, self.__class__):
            return self.rolled + other.rolled
        elif isinstance(other, int):
            return self.rolled + other
        else:
            raise ValueError(
                f"unsupported (+) types: '{type(self)}' and '{type(other)}'")

    def __radd__(self, other) -> int:
        return self.__add__(other)

    def __sub__(self, other) -> int:
        if other == 0:
            return self.rolled
        elif isinstance(other, self.__class__):
            return self.rolled - other.rolled
        elif isinstance(other, int):
            return self.rolled - other
        else:
            raise ValueError(
                f"unsupported (-) types: '{type(self)}' and '{type(other)}'")

    def __rsub__(self, other) -> int:
        if (other == 0):
            return self.rolled
        elif isinstance(other, self.__class__):
            return other.rolled - self.rolled
        elif isinstance(other, int):
            return other - self.rolled
        else:
            raise ValueError(
                f"unsupported (-) types: '{type(self)}' and '{type(other)}'")

    def __mul__(self, other) -> int:
        if other == 0:
            return 0
        elif isinstance(other, self.__class__):
            return self.rolled * other.rolled
        elif isinstance(other, int):
            return self.rolled * other
        else:
            raise ValueError(
                f"unsupported (*) types: '{type(self)}' and '{type(other)}'")

    def __rmul__(self, other) -> int:
        return self.__mul__(other)

    def __truediv__(self, other) -> int:
        if other == 0:
            raise ZeroDivisionError(f"{self.rolled} cannot divided by 0")
        elif isinstance(other, self.__class__):
            return self.rolled // other.rolled
        elif isinstance(other, int):
            return self.rolled // other
        else:
            raise ValueError(
                f"unsupported (/) types: '{type(self)}' and '{type(other)}'")

    def __rtruediv__(self, other) -> int:
        if self.rolled == 0:
            raise ZeroDivisionError(f"Cannot divided by 0")
        elif isinstance(other, self.__class__):
            return other.rolled // self.rolled
        elif isinstance(other, int):
            return other // self.rolled
        else:
            raise ValueError(
                f"unsupported (/) types: '{type(self)}' and '{type(other)}'")

    def roll(self) -> int:
        object.__setattr__(self, "rolled", random.randint(1, self.face_count))
        return self.rolled


@dataclass(order=True, frozen=True)
class FourSidedDie(Die):
    face_count: int = 4


@dataclass(order=True, frozen=True)
class SixSidedDie(Die):
    face_count: int = 6


@dataclass(order=True, frozen=True)
class EightSidedDie(Die):
    face_count: int = 8


@dataclass(order=True, frozen=True)
class TenSidedDie(Die):
    face_count: int = 10


@dataclass(order=True, frozen=True)
class TwelveSidedDie(Die):
    face_count: int = 12


@dataclass(order=True, frozen=True)
class TwentySidedDie(Die):
    face_count: int = 20


@dataclass(order=True, frozen=True)
class OneHundredSidedDie(Die):
    face_count: int = 100


@dataclass
class Dice():
    die_type: Die
    count: int
    dice: List[Die] = field(init=False)
    roll_history: List[List[Die]] = field(init=False, repr=False)

    def __str__(self) -> str:
        return self.pprint_str(self.current_roll)

    def __post_init__(self) -> None:
        self.dice = [self.die_type() for _ in range(self.count)]
        self.roll_history = [copy.deepcopy(self.dice)]

    def __len__(self) -> int:
        return len(self.dice)

    def __iter__(self):
        return iter(self.dice)

    @classmethod
    def pprint_str(self, dice: List[Die]) -> str:
        return f"{len(dice)}{dice[0].name}, [{", ".join([str(d.rolled) for d in dice])}]"

    @classmethod
    def pprint_dice(self, dice: List[Die]) -> None:
        print(self.pprint_str(dice))

    def pprint_roll_history(self) -> None:
        for roll in self.roll_history:
            self.pprint_dice(roll)

    @property
    def current_roll(self) -> List[Die]:
        return self.roll_history[-1]

    @property
    def previous_roll(self) -> List[Die]:
        if len(self.roll_history) > 1:
            return self.roll_history[-2]
        else:
            raise IndexError(
                "Not enough roll history to obtain a previous roll. Roll the dice, then try previous_roll() again")

    @property
    def current_total(self) -> int:
        return sum(self.current_roll)

    @property
    def previous_total(self) -> int:
        return sum(self.previous_roll)

    def roll(self) -> List[int]:
        for die in self.dice:
            die.roll()
        self.roll_history.append(copy.deepcopy(self.dice))
        return self.current_roll


class RollManager():
    """
    example:
        dice = [SixSidedDie() for _ in range(4)]

        RollManager(dice).roll()
        RollManager(dice).roll_with_advantage()
        RollManager(dice).roll_with_disadvantage()
    """
    dice: List[Die]

    def __init__(self, dice: (Dice | Die)) -> None:
        if isinstance(dice, Die):
            self.dice = [dice]
        elif isinstance(dice, Dice):
            self.dice = dice
        else:
            raise TypeError(
                "RollManager's constructor requires input be of type 'Die' or 'Dice'")

        self.die_type = self.dice[0]

    def print_roll_results(self, message: str, results: List[int]) -> None:
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
        print(f"total rolled: {roll_total}  ({
              " + ".join([str(d.rolled) for d in self.dice])})")
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
        print(f"Adding an additional {
              self.dice[0].name} to roll with advantage")
        self.add_die_to_roll()          \
            .roll_dice()                \
            .remove_lowest_roll()       \
            .get_roll_total()

    def roll_with_disadvantage(self) -> int:
        print(f"Adding an additional {
              self.dice[0].name} to roll with disadvantage")
        self.add_die_to_roll()          \
            .roll_dice()                \
            .remove_highest_roll()      \
            .get_roll_total()

    def roll(self) -> int:
        self.roll_dice().get_roll_total()
