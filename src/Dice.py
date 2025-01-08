"""
This module defines classes for dice-based rolling mechanics, including a base Die class
and its specific subclasses (e.g., FourSidedDie, SixSidedDie, etc.), as well as a Dice
container class that manages multiple dice and maintains their roll history.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Self, List, Type
import random
import copy


@dataclass(order=True, frozen=True)
class Die(ABC):
    """
    Represents a generic die, enforcing a minimum interface for dice logic.

    Attributes:
        face_count (int): The number of faces on the die (e.g., 6 for a six-sided die).
        name (str): A computed name, set automatically to 'd<face_count>'.
        rolled (int): The most recent roll result.
    """
    face_count: int = field(compare=False)
    name: str = field(compare=False, init=False)
    rolled: int = field(default=0, compare=True)

    def __post_init__(self):
        """
        Automatically sets the `name` attribute based on the `face_count`.
        For instance, a die with 6 faces will have `name = 'd6'`.
        """
        object.__setattr__(self, "name", f'd{self.face_count}')

    def __str__(self):
        """
        Returns the name of the die (e.g., 'd6') as a string representation.
        """
        return self.name

    def __add__(self, other) -> int:
        """
        Adds this die's rolled value to another die's rolled value or an integer.

        If other is 0, returns this die's rolled value.
        If other is also a Die, returns sum of rolled values.
        If other is int, returns sum of this die's rolled value and the integer.
        Raises ValueError if `other` is none of the above.
        """
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
        """
        Called when using reversed operands with the + operator (e.g., 5 + die).
        Delegates to the regular __add__ method.
        """
        return self.__add__(other)

    def __sub__(self, other) -> int:
        """
        Subtracts another die's rolled value or an integer from this die's rolled value.

        If other is 0, returns this die's rolled value.
        If other is also a Die, returns difference of rolled values.
        If other is int, returns the difference of this die's rolled value and the integer.
        Raises ValueError if `other` is none of the above.
        """
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
        """
        Handles subtraction when the die is on the right side of the - operator (e.g., 5 - die).
        Delegates to the logic in __sub__, but swaps operands appropriately.
        """
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
        """
        Multiplies this die's rolled value with another die's rolled value or an integer.

        Returns 0 if other is 0.
        Returns product of rolled values if other is a Die.
        Returns product of die's rolled value with an integer if other is int.
        Raises ValueError if `other` is none of the above.
        """
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
        """
        Called when using reversed operands with the * operator (e.g., 5 * die).
        Delegates to the regular __mul__ method.
        """
        return self.__mul__(other)

    def __truediv__(self, other) -> int:
        """
        Divides this die's rolled value by another die's rolled value or an integer.

        Uses floor division by default. Raises ZeroDivisionError if dividing by zero.
        Raises ValueError if `other` is neither a Die nor an int.
        """
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
        """
        Handles division when the die is on the right side of the / operator (e.g., 5 / die).

        Uses floor division by default. Raises ZeroDivisionError if dividing by zero.
        Raises ValueError if `other` is neither a Die nor an int.
        """
        if self.rolled == 0:
            raise ZeroDivisionError("Cannot divided by 0")
        elif isinstance(other, self.__class__):
            return other.rolled // self.rolled
        elif isinstance(other, int):
            return other // self.rolled
        else:
            raise ValueError(
                f"unsupported (/) types: '{type(self)}' and '{type(other)}'")

    def roll(self) -> int:
        """
        Rolls the die to obtain a random integer between 1 and `face_count`,
        and updates the `rolled` attribute with that value.

        Returns:
            int: The result of the roll.
        """
        object.__setattr__(self, "rolled", random.randint(1, self.face_count))
        return self.rolled


@dataclass(order=True, frozen=True)
class FourSidedDie(Die):
    """
    A four-sided die with face_count set to 4 by default.
    """
    face_count: int = 4


@dataclass(order=True, frozen=True)
class SixSidedDie(Die):
    """
    A six-sided die with face_count set to 6 by default.
    """
    face_count: int = 6


@dataclass(order=True, frozen=True)
class EightSidedDie(Die):
    """
    An eight-sided die with face_count set to 8 by default.
    """
    face_count: int = 8


@dataclass(order=True, frozen=True)
class TenSidedDie(Die):
    """
    A ten-sided die with face_count set to 10 by default.
    """
    face_count: int = 10


@dataclass(order=True, frozen=True)
class TwelveSidedDie(Die):
    """
    A twelve-sided die with face_count set to 12 by default.
    """
    face_count: int = 12


@dataclass(order=True, frozen=True)
class TwentySidedDie(Die):
    """
    A twenty-sided die with face_count set to 20 by default.
    """
    face_count: int = 20


@dataclass(order=True, frozen=True)
class OneHundredSidedDie(Die):
    """
    A one-hundred-sided die with face_count set to 100 by default.
    """
    face_count: int = 100


@dataclass
class Dice:
    """
    A container for handling multiple dice of the same type, along with a roll history.

    Attributes:
        die_type (Type[Die]): The class of the die (e.g., SixSidedDie).
        count (int): The number of dice to instantiate.
        dice (List[Die]): The currently active dice.
        roll_history (List[List[Die]]): A history of all past rolls. Each element is
            a snapshot (list) of dice objects from a single roll.
    """
    die_type: Type[Die]
    count: int
    dice: List[Die] = field(init=False)
    roll_history: List[List[Die]] = field(init=False, repr=False)

    def __str__(self) -> str:
        """
        Returns a string representation of the dice collection by printing the
        latest roll results in a concise format.
        """
        return self.pprint_str(self.current_roll)

    def __post_init__(self) -> None:
        """
        Initializes the collection of dice using the provided die_type, then records
        the initial roll state in roll_history.
        """
        self.dice = [self.die_type() for _ in range(self.count)]
        self.roll_history = [copy.deepcopy(self.dice)]

    def __len__(self) -> int:
        """
        Returns the number of dice in this Dice instance.
        """
        return len(self.dice)

    def __iter__(self):
        """
        Allows iteration directly over the internal list of dice.
        Example usage: [d.rolled for d in Dice(...)]
        """
        return iter(self.dice)

    @staticmethod
    def pprint_str(dice: List[Die]) -> str:
        """
        Produces a formatted string displaying the dice name and each die's rolled value.

        Args:
            dice (List[Die]): A list of Die objects.

        Returns:
            str: A formatted string showing die name and each die's rolled value.
        """
        return f"{len(dice)}{dice[0].name}, [{', '.join(str(d.rolled) for d in dice)}]"

    @staticmethod
    def pprint_dice(dice: List[Die]) -> None:
        """
        Prints a formatted representation of the given dice list. Uses pprint_str
        internally to build the output string.

        Args:
            dice (List[Die]): A list of Die objects.
        """
        print(Dice.pprint_str(dice))

    def pprint_roll_history(self) -> None:
        """
        Prints each roll in the roll history, where every roll is a snapshot of
        the dice list at a given time.
        """
        for roll in self.roll_history:
            self.pprint_dice(roll)

    @property
    def current_roll(self) -> List[Die]:
        """
        Returns the most recent (current) roll from the roll history.
        """
        return self.roll_history[-1]

    @property
    def previous_roll(self) -> List[Die]:
        """
        Returns the previous roll from the roll history, if it exists.

        Raises:
            IndexError: If there is not enough roll history.
        """
        if len(self.roll_history) > 1:
            return self.roll_history[-2]
        else:
            raise IndexError(
                "Not enough roll history to obtain a previous roll. Roll the dice, then try previous_roll() again"
            )

    @property
    def current_total(self) -> int:
        """
        Returns:
            int: The sum of the most recently rolled dice values.
        """
        return sum(self.current_roll)

    @property
    def previous_total(self) -> int:
        """
        Returns:
            int: The sum of the second-to-last roll from roll history.
        """
        return sum(self.previous_roll)

    def roll(self) -> List[int]:
        """
        Rolls all dice in this Dice instance, then updates the roll history with
        the new results.

        Returns:
            List[int]: A list of the new rolled values.
        """
        for die in self.dice:
            die.roll()
        self.roll_history.append(copy.deepcopy(self.dice))
        return self.current_roll


"""
fix rollmanager class
"""
# class RollManager():
#     """
#     example:
#         dice = [SixSidedDie() for _ in range(4)]

#         RollManager(dice).roll()
#         RollManager(dice).roll_with_advantage()
#         RollManager(dice).roll_with_disadvantage()
#     """
#     dice: Type[Dice]

#     def __init__(self, dice: (Dice | Die)) -> None:
#         if isinstance(dice, Die):
#             self.dice = [dice]
#         elif isinstance(dice, Dice):
#             self.dice = dice
#         else:
#             raise TypeError(
#                 "RollManager's constructor requires input be of type 'Die' or 'Dice'")

#         self.die_type = self.dice[0]

#     def print_roll_results(self, message: str, results: List[int]) -> None:
#         print(f"{message}:")
#         print(",".join(str(num) for num in results))

#     def add_die_to_roll(self) -> Self:
#         print
#         die_type = type(self.dice[0])
#         self.dice.append(die_type())
#         return self

#     def roll_dice(self) -> Self:
#         print(f"rolling {len(self.dice)}{self.dice[0].name}")
#         self.print_roll_results("results", [d.roll() for d in self.dice])
#         return self

#     def get_roll_total(self) -> int:
#         roll_total = sum([d.rolled for d in self.dice])
#         print(f"total rolled: {roll_total}  ({
#               " + ".join([str(d.rolled) for d in self.dice])})")
#         return roll_total

#     def remove_lowest_roll(self) -> Self:
#         lowest = min(self.dice, key=lambda d: d.rolled)
#         print(f"removing lowest roll: {lowest.rolled}")
#         self.dice.remove(lowest)
#         return self

#     def remove_highest_roll(self) -> Self:
#         highest = max(self.dice, key=lambda d: d.rolled)
#         print(f"removing highest roll: {highest.rolled}")
#         self.dice.remove(highest)
#         return self

#     def roll_with_advantage(self) -> int:
#         print(f"Adding an additional {
#               self.dice[0].name} to roll with advantage")
#         self.add_die_to_roll()          \
#             .roll_dice()                \
#             .remove_lowest_roll()       \
#             .get_roll_total()

#     def roll_with_disadvantage(self) -> int:
#         print(f"Adding an additional {
#               self.dice[0].name} to roll with disadvantage")
#         self.add_die_to_roll()          \
#             .roll_dice()                \
#             .remove_highest_roll()      \
#             .get_roll_total()

#     def roll(self) -> int:
#         self.roll_dice().get_roll_total()
